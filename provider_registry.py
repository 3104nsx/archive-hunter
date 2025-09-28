
from providers import ebay, vinted, vestiaire, grailed, mercari_jp, buyee_yahoo

REGISTRY = {
    "ebay": ebay.search,
    "vinted": vinted.search,
    "vestiaire": vestiaire.search,
    "grailed": grailed.search,
    "mercari_jp": mercari_jp.search,
    "buyee_yahoo": buyee_yahoo.search,
}

def run(name: str, cfg: dict, opts: dict):
    fn = REGISTRY.get(name)
    if not fn:
        return []
    return fn(cfg, opts)
