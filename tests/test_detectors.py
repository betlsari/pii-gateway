import pytest

from pii_gateway.detectors import tckn_adaylari_bul


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