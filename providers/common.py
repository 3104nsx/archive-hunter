
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Item:
    id: str
    title: str
    url: str
    image: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    seller_id: Optional[str] = None
    seller_name: Optional[str] = None

    def to_dict(self):
        return asdict(self)
