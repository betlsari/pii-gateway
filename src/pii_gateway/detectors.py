import re

from pii_gateway.models import Category, Finding

ADAY_DESENI = re.compile(r"(?<!\d)\d{11}(?!\d)")
IBAN_ADAY_DESENI = re.compile(r"(?<![A-Za-z0-9])TR\d{2}(?:[ ]?\d{4}){5}[ ]?\d{2}(?![A-Za-z0-9])")
TELEFON_DESENI = re.compile(
    r"(?<![\w+])\(?(?:\+90|0)[ ]?5\d{2}\)?[ \-]?\d{3}[ \-]?\d{2}[ \-]?\d{2}(?!\d)"
)

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

def tckn_bul(metin: str) -> list[Finding]:
    sonuc = []
    for aday in tckn_adaylari_bul(metin):
        if tckn_gecerli_mi(aday.text):
            sonuc.append(
                Finding(Category.TCKN, aday.start, aday.end, aday.text, 1.0)
            )
    return sonuc

def iban_gecerli_mi(metin: str) -> bool:
    iban = metin.replace(" ", "").upper()

    if len(iban) != 26:
        return False
    if not iban.startswith("TR"):
        return False
    if not (iban.isascii() and iban[2:].isdigit()):
        return False

    yeniden_dizilmis = iban[4:] + iban[:4]

    sayi_metni = ""
    for karakter in yeniden_dizilmis:
        if karakter.isdigit():
            sayi_metni += karakter
        else:
            sayi_metni += str(ord(karakter) - ord("A") + 10)

    return int(sayi_metni) % 97 == 1


def iban_adaylari_bul(metin: str) -> list[Finding]:
    bulgular = []
    for m in IBAN_ADAY_DESENI.finditer(metin):
        bulgular.append(
            Finding(Category.IBAN, m.start(), m.end(), m.group(), 0.5)
        )
    return bulgular


def iban_bul(metin: str) -> list[Finding]:
    sonuc = []
    for aday in iban_adaylari_bul(metin):
        if iban_gecerli_mi(aday.text):
            sonuc.append(
                Finding(Category.IBAN, aday.start, aday.end, aday.text, 1.0)
            )
    return sonuc

def telefon_bul(metin: str) -> list[Finding]:
    bulgular = []
    for m in TELEFON_DESENI.finditer(metin):
        bulgular.append(
            Finding(Category.TELEFON, m.start(), m.end(), m.group(), 0.8)
        )
    return bulgular

def cakismalari_coz(bulgular: list[Finding]) -> list[Finding]:
    sirali = sorted(
        bulgular,
        key=lambda b: (b.confidence, b.end - b.start),
        reverse=True,
    )
    secilen = []
    for aday in sirali:
        cakisiyor = any(
            aday.start < s.end and s.start < aday.end for s in secilen
        )
        if not cakisiyor:
            secilen.append(aday)
    secilen.sort(key=lambda b: b.start)
    return secilen


def detect(metin: str) -> list[Finding]:
    bulgular = tckn_bul(metin) + iban_bul(metin) + telefon_bul(metin)
    return cakismalari_coz(bulgular)