import random

from pii_gateway.detectors import iban_gecerli_mi, tckn_gecerli_mi
from pii_gateway.synth import iban_uret, tckn_uret, uret


def test_uretilen_tckn_gecerli():
    rng = random.Random(1)
    for _ in range(200):
        assert tckn_gecerli_mi(tckn_uret(rng))


def test_uretilen_iban_gecerli():
    rng = random.Random(1)
    for _ in range(200):
        assert iban_gecerli_mi(iban_uret(rng))


def test_etiket_konumlari_dogru_ve_tekrarlanabilir():
    veri = uret(100, seed=7)
    assert veri == uret(100, seed=7)
    for ornek in veri:
        for e in ornek["etiketler"]:
            parca = ornek["metin"][e["start"]:e["end"]]
            assert len(parca) > 0