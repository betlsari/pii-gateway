from pii_gateway.evaluate import say


def test_say_dogru_bulma():
    ornekler = [
        {
            "metin": "Ahmet'in TCKN'si 10000000146 yazıyor.",
            "etiketler": [{"kategori": "TCKN", "start": 17, "end": 28}],
        },
        {"metin": "Sipariş no: 12345678901", "etiketler": []},
    ]
    sayac = say(ornekler)
    assert sayac["TCKN"] == {"tp": 1, "fp": 0, "fn": 0}


def test_say_yanlis_etiket_fp_ve_fn_uretir():
    ornekler = [
        {
            "metin": "Ahmet'in TCKN'si 10000000146 yazıyor.",
            "etiketler": [{"kategori": "TCKN", "start": 19, "end": 30}],
        }
    ]
    sayac = say(ornekler)
    assert sayac["TCKN"] == {"tp": 0, "fp": 1, "fn": 1}