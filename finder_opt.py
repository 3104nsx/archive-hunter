
import argparse, json, os, random, time, sys
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

from aliases import CANONICAL_BRANDS, match_brand
from provider_registry import run as run_provider

from tools.discord_send import post_embed

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_seen(path: Path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}

def save_seen(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def jitter(seconds: int) -> float:
    j = seconds * 0.1
    return max(1.0, seconds + random.uniform(-j, j))

def run_once(cfg_path, dry_run=False, provider_only=None, brand_only=None):
    cfg = load_yaml(cfg_path)
    seen_path = Path("data/seen.json")
    seen = load_seen(seen_path)
    now_iso = datetime.now(timezone.utc).isoformat()

    providers = cfg.get("providers", {})
    region = cfg.get("region", "eu")

    summary_counts = []

    for name, pcfg in providers.items():
        if provider_only and name != provider_only:
            continue
        if not pcfg.get("enabled", True):
            continue
        opts = pcfg.get("options", {})
        opts.setdefault("user_agent", USER_AGENT)
        items = []
        try:
            items = run_provider(name, {"brands": CANONICAL_BRANDS, "region": region}, opts) or []
        except Exception as e:
            print(f"[engine] provider {name} crashed: {e}", file=sys.stderr)
            items = []

        fetched = len(items)
        matched = 0
        posted = 0

        for it in items:
            # Brand match on title (and optionally seller name)
            brand = None
            txt = f"{it.get('title','')}"
            if txt:
                brand = match_brand(txt)
            if not brand and it.get("seller_name"):
                brand = match_brand(it["seller_name"])
            if brand_only and brand and brand != brand_only:
                continue
            if not brand:
                continue
            matched += 1

            key = f"{name}:{it.get('id','')}"
            if not it.get("id"):
                continue
            if key in seen:
                continue
            seen[key] = now_iso

            if dry_run:
                print(f"[dry-run] {brand} | {name} | {it.get('title')} | {it.get('price')} {it.get('currency')} | {it.get('url')}")
            else:
                ok = post_embed(
                    item_title=it.get("title",""),
                    item_url=it.get("url",""),
                    item_image=it.get("image"),
                    brand=brand,
                    provider=name,
                    price=it.get("price"),
                    currency=it.get("currency"),
                    region=region
                )
                if ok:
                    posted += 1
                else:
                    # roll back dedupe on failed post to avoid losing it
                    seen.pop(key, None)

        summary_counts.append((name, fetched, matched, posted))
        print(f"[engine] {name}: fetched={fetched} matched={matched} posted={posted}")

    save_seen(seen_path, seen)
    return summary_counts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.eu.yaml")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--provider", help="force single provider")
    ap.add_argument("--brand", help="limit to brand name")
    args = ap.parse_args()

    cfg = load_yaml(args.config)
    cadence = cfg.get("cadence_seconds", 180)
    circuit = { }  # provider -> consecutive_errors

    if args.once:
        run_once(args.config, dry_run=args.dry_run, provider_only=args.provider, brand_only=args.brand)
        return

    providers = cfg.get("providers", {})
    next_run = {name: 0.0 for name in providers.keys()}

    while True:
        t0 = time.time()
        for name, pcfg in providers.items():
            if args.provider and name != args.provider:
                continue
            if not pcfg.get("enabled", True):
                continue

            cadence_p = int(pcfg.get("options", {}).get("cadence_seconds", cadence))
            if t0 < next_run.get(name, 0.0):
                continue

            errors = circuit.get(name, 0)
            if errors >= 3:
                # skip one cadence
                next_run[name] = t0 + jitter(cadence_p)
                circuit[name] = 0
                print(f"[engine] circuit skip for {name}")
                continue

            try:
                run_once(args.config, dry_run=args.dry_run, provider_only=name, brand_only=args.brand)
                circuit[name] = 0
            except Exception as e:
                circuit[name] = errors + 1
                print(f"[engine] error in {name}: {e}", file=sys.stderr)

            next_run[name] = t0 + jitter(cadence_p)

        time.sleep(2)

if __name__ == "__main__":
    main()
