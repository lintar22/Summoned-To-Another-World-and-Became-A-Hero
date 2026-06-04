# Chronicle of the Summoned Hero

## Pixel Fantasy RPG — Multi Ending | Visual Novel

---

## Cara Menjalankan

```bash
pip install pygame
python main.py          # Game utama
python class_diagram.py # Class Diagram OOP (scrollable)
```

---

## Perbaikan v2.0

- ✅ **Walk-in karakter**: Setiap pergantian area/scene, karakter berjalan masuk dari sisi kiri layar secara bergantian — tidak lagi muncul tiba-tiba.
- ✅ **Summoning fall-in**: Di Chapter 1, Arga jatuh dari atas layar (efek disummon) bukan teleport.
- ✅ **Fix black screen**: Background selalu tampil saat fade-out/fade-in. Scene desa terbakar, lorong kastil, dan singgasana Raja Iblis kini muncul dengan benar.
- ✅ **Transisi antar area**: Fade-out → tunggu selesai → ganti background + fade-in. Tidak ada frame hitam tanpa background.
- ✅ **Cerita diperluas**: Dialog lebih kaya dan mengikuti naskah asli lebih detail (campfire scene, pre-battle dialog, dungeon walk).
- ✅ **Fire particles**: Desa terbakar kini ada efek partikel api animasi.
- ✅ **Input blocking**: Tidak bisa skip/advance saat animasi walk-in atau fade sedang berjalan.

---

## Kontrol

| Key | Aksi |
|-----|------|
| SPACE / ENTER / Z | Lanjut dialog / konfirmasi |
| ↑ ↓ / W S | Navigasi pilihan |
| ← → | Jalan (di kota) |
| E | Bicara NPC |
| TAB | Buka status |
| ESC | Quit |

---

## Alur Game

```
Opening (Kota Malam) → Chapter 1 (Summoning)
→ Town (Astravia) → Chapter 2:
    Forest (Reno) → Ruins (Lyra) → Village (Darius)
    → Campfire (Malam sebelum perang)
    → Montage (Satu tahun berlalu)
→ Chapter Final:
    Pre-battle → Lorong Kastil → Boss Intro
    → Final Battle → PILIHAN KRITIS
    ├── Lindungi Elena → TRUE END (Pernikahan)
    └── Serang Boss   → BAD END  (Dunia tenggelam)
```

---

## Konsep OOP

| Konsep | Implementasi |
|--------|-------------|
| **Abstraksi** | `Entity`, `Scene`, `BattleEntity` (ABC) |
| **Enkapsulasi** | `__hp`, `__emotion`, `__stats` (private) |
| **Inheritance** | `Entity→Character→Player/NPC→*` |
| **Polimorfisme** | `draw()`, `use_skill()`, `interact()` berbeda tiap class |

---

## File Diagram

- `class_diagram.py` — Visualisasi class diagram interaktif (scrollable, drag)
