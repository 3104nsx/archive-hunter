
# Stub provider for Vestiaire Collective (potentially cookie / API heavy)
from providers.common import Item
def search(cfg: dict, opts: dict):
    """Vestiaire Collective provider stub.
    TODO: Implement HTML/API fetching with polite rate limits, optional cookies in opts['storage_state'].
    Return [] for now.
    """
    return []
