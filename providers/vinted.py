
import requests, time
from providers.common import Item

API = "https://www.vinted.com/api/v2/catalog/items"

def search(cfg: dict, opts: dict):
    try:
        brands = cfg.get("brands", [])
        ua = opts.get("user_agent")
        out = []
        for b in brands:
            params = {
                "search_text": b,
                "order": "newest_first",
                "per_page": 20,
            }
            headers = {"User-Agent": ua, "Accept": "application/json"}
            try:
                r = requests.get(API, params=params, headers=headers, timeout=12)
                if r.status_code != 200:
                    continue
                data = r.json()
                for it in data.get("items", []):
                    iid = str(it.get("id"))
                    title = it.get("title") or ""
                    url = it.get("url") or (f"https://www.vinted.com/items/{iid}" if iid else "")
                    photos = it.get("photos") or []
                    image = photos[0].get("url") if photos else None
                    price = None
                    currency = None
                    try:
                        price = float(it.get("price_numeric"))
                        currency = it.get("currency") or "EUR"
                    except Exception:
                        pass
                    out.append(Item(id=iid, title=title, url=url, image=image, price=price, currency=currency,
                                    seller_id=str(it.get('user_id')) if it.get('user_id') else None,
                                    seller_name=None).to_dict())
                time.sleep(0.35)
            except Exception:
                continue
        return out[:300]
    except Exception:
        return []
