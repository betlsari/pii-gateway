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

def tckn_gecerli_mi(metin: str) -> bool:
    # 1. Ön kontroller: uygun değilse hemen False
    if len(metin) != 11:
        return False
    if not (metin.isascii() and metin.isdigit()):
        return False
    if metin[0] == "0":
        return False

    # 2. Rakam listesi: "10000000146" -> [1,0,0,0,0,0,0,0,1,4,6]
    rakamlar = [int(c) for c in metin]

    # 3. d10 kontrolü
    tekler = sum(rakamlar[0:9:2])    # d1, d3, d5, d7, d9
    ciftler = sum(rakamlar[1:8:2])   # d2, d4, d6, d8
    d10 = (tekler * 7 - ciftler) % 10
    if d10 != rakamlar[9]:
        return False

    # 4. d11 kontrolü
    d11 = sum(rakamlar[0:10]) % 10   # ilk 10 hanenin toplamı
    if d11 != rakamlar[10]:
        return False

    return True
