from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    "User Class Repr"
    user_id: int = 0
    address: str = ""


@dataclass
class Order:
    "Bot Order Model"
    buyer: str = ""
    vendor: str = ""
    msg_id: int = 0
    item: str = ""
    address: str = ""
    active: bool = True
    status: str = "new"
    created_at: str = ""
