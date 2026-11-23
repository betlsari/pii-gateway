import re

from pii_gateway.models import Category, Finding

ADAY_DESENI = re.compile(r"(?<!\d)\d{11}(?!\d)")


def tckn_adaylari_bul(metin: str) -> list[Finding]:
    bulgular = []
    for m in ADAY_DESENI.finditer(metin):
        bulgular.append(
            Finding(Category.TCKN, m.start(), m.end(), m.group(), 0.5)
        )
    return bulgular