
import requests, time
from lxml import html
from providers.common import Item

def _req(url, ua, timeout=12):
    headers = {"User-Agent": ua, "Accept-Language": "en-US,en;q=0.9"}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.text

def _parse_items(doc):
    items = []
    for li in doc.cssselect("li.s-item"):
        try:
            iid = li.get("data-view", "") or li.get("data-id", "")
            if not iid:
                # fallback: extract from link href
                a = li.cssselect("a.s-item__link")
                if a:
                    href = a[0].get("href", "")
                    if "itm/" in href:
                        iid = href.split("itm/")[-1].split("?")[0]
            title_el = li.cssselect("span.s-item__title")
            title = title_el[0].text_content().strip() if title_el else ""
            a = li.cssselect("a.s-item__link")
            url = a[0].get("href") if a else ""
            img_el = li.cssselect("img.s-item__image-img")
            image = img_el[0].get("src") if img_el else None
            price_el = li.cssselect("span.s-item__price")
            price_raw = price_el[0].text_content().strip() if price_el else ""
            price = None
            currency = None
            if price_raw:
                # crude parse: assume like "$123.45" or "EUR 123,45"
                pr = price_raw.replace(",", "").replace("EUR", "€").replace("USD", "$")
                digits = "".join(ch if ch.isdigit() or ch == "." else " " for ch in pr).split()
                if digits:
                    try:
                        price = float(digits[0])
                    except:
                        price = None
                if "€" in price_raw:
                    currency = "EUR"
                elif "$" in price_raw:
                    currency = "USD"
            if iid and title and url:
                items.append(Item(id=iid, title=title, url=url, image=image, price=price, currency=currency).to_dict())
        except Exception:
            continue
    return items

def search(cfg: dict, opts: dict):
    try:
        brands = cfg.get("brands", [])
        ua = opts.get("user_agent")
        per_brand = []
        for b in brands:
            q = b.replace(" ", "+")
            url = f"https://www.ebay.com/sch/i.html?_nkw={q}&_sop=10"
            try:
                html_text = _req(url, ua)
                doc = html.fromstring(html_text)
                per_brand.extend(_parse_items(doc))
                time.sleep(0.4)
            except Exception:
                continue
        return per_brand[:200]
    except Exception:
        return []
