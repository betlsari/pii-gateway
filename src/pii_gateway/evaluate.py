import json
from collections import defaultdict
from pathlib import Path

from pii_gateway.detectors import detect
from pii_gateway.metrics import olc


def say(ornekler: list[dict]) -> dict[str, dict[str, int]]:
    sayac = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    for ornek in ornekler:
        gercek = {
            (e["kategori"], e["start"], e["end"]) for e in ornek["etiketler"]
        }
        bulunan = {
            (b.category.value, b.start, b.end) for b in detect(ornek["metin"])
        }
        for kategori, _, _ in gercek & bulunan:
            sayac[kategori]["tp"] += 1
        for kategori, _, _ in bulunan - gercek:
            sayac[kategori]["fp"] += 1
        for kategori, _, _ in gercek - bulunan:
            sayac[kategori]["fn"] += 1
    return dict(sayac)


def rapor_yaz(sayac: dict[str, dict[str, int]]) -> None:
    print(f"{'kategori':<10}{'TP':>4}{'FP':>4}{'FN':>4}{'prec':>7}{'recall':>8}{'f1':>7}")
    for kategori in sorted(sayac):
        s = sayac[kategori]
        o = olc(s["tp"], s["fp"], s["fn"])
        print(
            f"{kategori:<10}{s['tp']:>4}{s['fp']:>4}{s['fn']:>4}"
            f"{o['precision']:>7.2f}{o['recall']:>8.2f}{o['f1']:>7.2f}"
        )


def main() -> None:
    yol = Path("data/ornekler.json")
    ornekler = json.loads(yol.read_text(encoding="utf-8"))
    rapor_yaz(say(ornekler))


if __name__ == "__main__":
    main()