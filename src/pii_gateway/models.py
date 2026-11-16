from dataclasses import dataclass
from enum import Enum


class Category(Enum):
    TCKN = "TCKN"
    IBAN = "IBAN"
    TELEFON = "TELEFON"


@dataclass
class Finding:
    category: Category
    start: int
    end: int
    text: str
    confidence: float