import pytest

from pii_gateway.detectors import (
    iban_bul,
    iban_gecerli_mi,
    tckn_adaylari_bul,
    tckn_bul,
    tckn_gecerli_mi,
)
from pii_gateway.models import Category, Finding

def test_tek_tckn_bulur():
    metin = "Ahmet Yılmaz'ın TCKN'si 10000000146 yazıyor."
    bulgular = tckn_adaylari_bul(metin)
    assert len(bulgular) == 1
    assert bulgular[0].start == 24
    assert bulgular[0].end == 35
    assert bulgular[0].text == "10000000146"


@pytest.mark.parametrize(
    "metin",
    [
        "Sipariş no: 123456789012345",   # 15 hane
        "Kod: 1234567890",               # 10 hane
        "Merhaba dünya",                 # hiç sayı yok
    ],
)
def test_tckn_olmayanlari_bulmaz(metin):
    assert tckn_adaylari_bul(metin) == []


@pytest.mark.parametrize(
    "tckn",
    ["10000000146", "12345678950"],
)
def test_gecerli_tckn(tckn):
    assert tckn_gecerli_mi(tckn) is True


@pytest.mark.parametrize(
    "tckn",
    [
        "10000000147",   # son hane yanlış
        "10000000156",   # d10 yanlış
        "01234567890",   # ilk hane 0
        "1234567890",    # 10 hane
        "123456789012",  # 12 hane
        "1000000014a",   # harf içeriyor
        "",              # boş
    ],
)
def test_gecersiz_tckn(tckn):
    assert tckn_gecerli_mi(tckn) is False





def test_gecerli_tckn_bulunur():
    metin = "Ahmet Yılmaz'ın TCKN'si 10000000146 yazıyor."
    bulgular = tckn_bul(metin)
    assert len(bulgular) == 1
    assert bulgular[0].confidence == 1.0
    assert bulgular[0].text == "10000000146"


def test_sahte_tckn_elenir():
    metin = "Sipariş no: 12345678901"
    assert tckn_bul(metin) == []


def test_iki_tckn_ikisi_de_bulunur():
    metin = "Birincisi 10000000146, ikincisi 12345678950."
    bulgular = tckn_bul(metin)
    assert len(bulgular) == 2
    assert bulgular[0].start < bulgular[1].start

@pytest.mark.parametrize(
    "iban",
    [
        "TR330006100519786457841326",
        "TR33 0006 1005 1978 6457 8413 26",
        "tr330006100519786457841326",
    ],
)
def test_gecerli_iban(iban):
    assert iban_gecerli_mi(iban) is True


@pytest.mark.parametrize(
    "iban",
    [
        "TR330006100519786457841327",    # son hane yanlış
        "TR340006100519786457841326",    # kontrol hanesi yanlış
        "TR33000610051978645784132",     # 25 karakter
        "DE89370400440532013000",        # Türk IBAN'ı değil
        "TR33000610051978645784132A",    # harf içeriyor
        "",
    ],
)
def test_gecersiz_iban(iban):
    assert iban_gecerli_mi(iban) is False


def test_iban_bulunur_boslukla():
    metin = "Hesap: TR33 0006 1005 1978 6457 8413 26 numarasına yatırın."
    bulgular = iban_bul(metin)
    assert len(bulgular) == 1
    assert bulgular[0].confidence == 1.0
    assert bulgular[0].text == "TR33 0006 1005 1978 6457 8413 26"


def test_iban_bulunur_bitisik():
    metin = "IBAN TR330006100519786457841326 yazıyor."
    bulgular = iban_bul(metin)
    assert len(bulgular) == 1
    assert bulgular[0].start == 5


def test_sahte_iban_elenir():
    metin = "IBAN TR330006100519786457841327 yazıyor."
    assert iban_bul(metin) == []