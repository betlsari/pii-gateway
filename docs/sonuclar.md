# Sonuçlar

> Tüm veri sentetiktir. Sonuçlar gerçek dünya performansını göstermez.

## Sentetik veri (300 örnek)
Tüm kategorilerde 1.00. Veri dedektör kurallarına göre üretildiği için bu beklenen bir sonuçtur, başarı kanıtı değildir.

## Zor örnekler (12 örnek): önce / sonra

| Kategori | Önce (P/R/F1) | Sonra (P/R/F1) |
|---|---|---|
| IBAN | 0.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 |
| TCKN | 0.67 / 0.67 / 0.67 | 0.67 / 0.67 / 0.67 |
| TELEFON | 0.67 / 0.40 / 0.50 | (yeni tabloyu yazın) |

## Bilinen sınırlar
- Sabit hatlar kapsam dışı
- Ayrık yazılmış TCKN (`1 0 0 0 ...`) kaçırılıyor
- `Sipariş: 05321234567` telefon sanılıyor (FP)
- Sağlamayı tesadüfen geçen sipariş numarası TCKN sanılıyor (FP)
- 12 örnek istatistiksel olarak küçük, yüzdeler yön gösterir, kesin değildir