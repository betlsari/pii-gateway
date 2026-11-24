import json
from pathlib import Path

from pii_gateway.synth import olustur

# (şablon, [(kategori veya None, değer)])
# None = bu değer kişisel veri DEĞİL, hiçbir şey bulunmamalı
ZOR_ORNEKLER = [
    # --- Kaçırmasını beklediklerimiz (FN) ---
    ("Beni {} arayın.", [("TELEFON", "5321234567")]),            # başında 0/+90 yok
    ("Sabit hat: {}", [("TELEFON", "0212 123 45 67")]),          # sabit hat
    ("Ara: {}", [("TELEFON", "0 (532) 123 45 67")]),             # alışılmadık biçim
    ("IBAN: {}", [("IBAN", "TR33-0006-1005-1978-6457-8413-26")]),# tireli
    ("IBAN: {}", [("IBAN", "tr330006100519786457841326")]),      # küçük harf
    ("TC kimlik: {}", [("TCKN", "1 0 0 0 0 0 0 0 1 4 6")]),      # ayrık yazım
    # --- Bulmasını beklediklerimiz (kontrol) ---
    ("TCKN:{}", [("TCKN", "10000000146")]),
    ("tel:{}", [("TELEFON", "05321234567")]),
    ("{} ve {}", [("TCKN", "10000000146"), ("TELEFON", "0532 123 45 67")]),
    # --- Yanlış alarm beklediklerimiz (FP) ---
    ("Sipariş: {}", [(None, "05321234567")]),    # telefon gibi görünen sipariş no
    ("Sipariş no: {}", [(None, "12345678950")]), # sağlamayı tesadüfen geçen sayı
]


def uret() -> list[dict]:
    return [olustur(sablon, degerler, "") for sablon, degerler in ZOR_ORNEKLER]


def main() -> None:
    veri = uret()
    yol = Path("data/zor.json")
    yol.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(veri)} zor örnek yazıldı: {yol}")


if __name__ == "__main__":
    main()