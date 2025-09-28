
import os, json, time, math
import requests

def _choose_webhook(region: str) -> str | None:
    env = os.environ
    if region == "eu" and env.get("DISCORD_WEBHOOK_EU"):
        return env.get("DISCORD_WEBHOOK_EU")
    if region == "jp" and env.get("DISCORD_WEBHOOK_JP"):
        return env.get("DISCORD_WEBHOOK_JP")
    return env.get("DISCORD_WEBHOOK_DEFAULT")

def post_embed(item_title: str, item_url: str, item_image: str | None, brand: str, provider: str, price, currency, region: str) -> bool:
    webhook = _choose_webhook(region)
    if not webhook:
        print("[discord] no webhook configured; skipping post")
        return False
    embed = {
        "title": item_title[:256],
        "url": item_url,
        "description": f"{brand} • {provider}",
        "fields": [
            {"name": "Brand", "value": brand, "inline": True},
            {"name": "Provider", "value": provider, "inline": True},
            {"name": "Price", "value": str(price) if price is not None else "?", "inline": True},
            {"name": "Currency", "value": currency or "?", "inline": True},
        ]
    }
    if item_image:
        embed["image"] = {"url": item_image}

    payload = {"embeds": [embed]}

    for attempt in range(2):
        r = requests.post(webhook, json=payload, timeout=12)
        if r.status_code == 204:
            return True
        if r.status_code == 429:
            try:
                retry_after = r.json().get("retry_after", 1.0)
            except Exception:
                retry_after = 1.0
            time.sleep(float(retry_after) + 0.1)
            continue
        if 200 <= r.status_code < 300:
            return True
        # else fall through
    print(f"[discord] failed to post: {r.status_code} {r.text[:200]}")
    return False
