from pii_gateway.zor import uret


def test_zor_etiket_konumlari_dogru():
    for ornek in uret():
        for e in ornek["etiketler"]:
            assert len(ornek["metin"][e["start"]:e["end"]]) > 0