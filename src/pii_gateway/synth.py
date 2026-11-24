import json
import random
from pathlib import Path

from faker import Faker

from pii_gateway.detectors import iban_gecerli_mi, tckn_gecerli_mi


def tckn_uret(rng: random.Random) -> str:
    d = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(8)]
    d.append((sum(d[0:9:2]) * 7 - sum(d[1:8:2])) % 10)
    d.append(sum(d) % 10)
    return "".join(str(x) for x in d)


def sahte_tckn_uret(rng: random.Random) -> str:
    while True:
        sayi = str(rng.randint(1, 9)) + "".join(
            str(rng.randint(0, 9)) for _ in range(10)
        )
        if not tckn_gecerli_mi(sayi):
            return sayi


def iban_uret(rng: random.Random) -> str:
    bban = "".join(str(rng.randint(0, 9)) for _ in range(22))
    kontrol = 98 - int(bban + "292700") % 97
    return f"TR{kontrol:02d}{bban}"


def sahte_iban_uret(rng: random.Random) -> str:
    while True:
        bban = "".join(str(rng.randint(0, 9)) for _ in range(22))
        iban = f"TR{rng.randint(2, 98):02d}{bban}"
        if not iban_gecerli_mi(iban):
            return iban


def iban_bicimle(iban: str, rng: random.Random) -> str:
    if rng.random() < 0.5:
        return iban
    return " ".join(iban[i:i + 4] for i in range(0, 26, 4))


def telefon_uret(rng: random.Random) -> str:
    op = "5" + f"{rng.randint(0, 99):02d}"
    a = f"{rng.randint(0, 999):03d}"
    b = f"{rng.randint(0, 99):02d}"
    c = f"{rng.randint(0, 99):02d}"
    bicimler = [
        f"0{op}{a}{b}{c}",
        f"0{op} {a} {b} {c}",
        f"+90 {op} {a} {b} {c}",
        f"+90{op}{a}{b}{c}",
        f"0{op}-{a}-{b}-{c}",
        f"(0{op}) {a} {b} {c}",
    ]
    return rng.choice(bicimler)


def siparis_no_uret(rng: random.Random) -> str:
    return "".join(str(rng.randint(0, 9)) for _ in range(15))


SABLONLAR = {
    "tckn": [
        "{isim} için TCKN {} olarak kayıtlı.",
        "Kimlik numaram {}, lütfen kontrol edin.",
        "Müşteri {isim}, TC: {}",
    ],
    "iban": [
        "Ödemeyi {} hesabına yapın.",
        "{isim} adına IBAN: {}",
        "Hesap numarası {} olarak güncellendi.",
    ],
    "telefon": [
        "Beni {} numarasından arayın.",
        "{isim} ile iletişim: {}",
        "Acil durumda {} aranabilir.",
    ],
    "sahte_tckn": [
        "Sipariş kodu {} onaylandı.",
        "Takip numarası: {}",
    ],
    "sahte_iban": [
        "Hatalı IBAN girişi: {}",
    ],
    "siparis": [
        "Sipariş no: {}",
        "Fatura referansı {} işleme alındı.",
    ],
    "temiz": [
        "{isim} yarın toplantıya katılacak.",
        "Raporu cuma gününe kadar göndereceğim.",
    ],
}


def olustur(sablon: str, degerler: list[tuple[str | None, str]], isim: str) -> dict:
    sablon = sablon.replace("{isim}", isim)
    parcalar = sablon.split("{}")
    metin = ""
    etiketler = []
    for i, parca in enumerate(parcalar[:-1]):
        metin += parca
        kategori, deger = degerler[i]
        if kategori is not None:
            etiketler.append(
                {"kategori": kategori, "start": len(metin), "end": len(metin) + len(deger)}
            )
        metin += deger
    metin += parcalar[-1]
    return {"metin": metin, "etiketler": etiketler}


def uret(adet: int, seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    fake = Faker("tr_TR")
    Faker.seed(seed)
    turler = list(SABLONLAR)
    sonuc = []
    for _ in range(adet):
        tur = rng.choice(turler)
        sablon = rng.choice(SABLONLAR[tur])
        isim = fake.name()
        if tur == "tckn":
            degerler = [("TCKN", tckn_uret(rng))]
        elif tur == "iban":
            degerler = [("IBAN", iban_bicimle(iban_uret(rng), rng))]
        elif tur == "telefon":
            degerler = [("TELEFON", telefon_uret(rng))]
        elif tur == "sahte_tckn":
            degerler = [(None, sahte_tckn_uret(rng))]
        elif tur == "sahte_iban":
            degerler = [(None, iban_bicimle(sahte_iban_uret(rng), rng))]
        elif tur == "siparis":
            degerler = [(None, siparis_no_uret(rng))]
        else:
            degerler = []
        sonuc.append(olustur(sablon, degerler, isim))
    return sonuc


def main() -> None:
    veri = uret(300)
    yol = Path("data/sentetik.json")
    yol.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(veri)} örnek yazıldı: {yol}")


if __name__ == "__main__":
    main()