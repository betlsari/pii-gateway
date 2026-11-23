import pytest

from pii_gateway.metrics import olc


def test_olc_ornek():
    sonuc = olc(tp=8, fp=2, fn=2)
    assert sonuc["precision"] == pytest.approx(0.8)
    assert sonuc["recall"] == pytest.approx(0.8)
    assert sonuc["f1"] == pytest.approx(0.8)


def test_olc_sifira_bolme_yok():
    assert olc(0, 0, 0) == {"precision": 0.0, "recall": 0.0, "f1": 0.0}


def test_olc_hic_bulamadi():
    sonuc = olc(tp=0, fp=0, fn=5)
    assert sonuc["recall"] == 0.0