<div align="center">

# ⚔️ Summoned To Another World and Became A Hero ⚔️

*"Tunggu, pahlawan? Maksudnya aku?"*


---

Riski Anugrah Firmansyah      		    (25051204040)

Lintar Handy Wibowo             		(25051204045)

Mochammad Arva Josi S.        		    (25051204145)

Mochammad Afrizal Santoso             	(25051204233)

---

## 📖 Deskripsi Project

Summoned To Another World and Became A Hero adalah game berbasis Python yang menggabungkan genre Visual Novel dan RPG Turn-Based. Game ini bercerita tentang Arga, seorang pelajar biasa yang tiba-tiba tersedot ke dunia fantasi bernama Astravia dan dipilih oleh Pedang Suci untuk menjadi pahlawan yang menyelamatkan dunia dari ancaman Demon King.

Pemain mengikuti perjalanan Arga bersama party-nya Elena, Lyra, Darius, dan Reno melewati kota Astravia, hutan berbahaya, reruntuhan kuno, hingga kastil Demon King. Setiap keputusan yang diambil pemain memengaruhi jalannya cerita dan menentukan ending yang didapat.

| Atribut | Detail |
|:--------|:-------|
| 🕹️ **Tipe** | Visual Novel / RPG Turn-Based |
| 🌟 **Genre** | Isekai Fantasy · Adventure · Story-Driven |
| 🐍 **Engine** | Python + Pygame |

---
<img width="1280" height="714" alt="Screenshot 2026-06-05 195029" src="https://github.com/user-attachments/assets/673bae3b-7c7c-4c0d-b083-4aecd701e89f" />
<img width="1281" height="716" alt="Screenshot 2026-06-05 201600" src="https://github.com/user-attachments/assets/29541e3e-a955-4a23-8a8e-0d3600edcb43" />

## ✨ Fitur Utama

### 📜 Narasi Visual Novel
Dialog bergaya visual novel dengan efek typewriter, narrator box sinematik, dan latar belakang yang berubah dinamis sesuai lokasi. Dilengkapi cutscene pembuka dengan efek hujan dan magic circle.

### 🗺️ Sistem Chapter & Eksplorasi
Game terbagi menjadi beberapa chapter dengan alur cerita yang berkesinambungan:

| Chapter | Lokasi | Keterangan |
|:-------:|:-------|:-----------|
| Opening | Dunia nyata — malam hujan | Kehidupan Arga sebelum isekai |
| Chapter 1 | Aula Kerajaan Astravia | Pemanggilan, Pedang Suci, pertemuan Raja Aldric |
| Chapter 2 | Kota Astravia | Eksplorasi bebas dan interaksi NPC |
| Chapter 3 | Hutan · Reruntuhan · Perkampungan | Perjalanan menuju kastil Demon King |
| Chapter Final | Dungeon kastil | Konfrontasi terakhir dengan Demon King |

### ⚔️ Battle Turn-Based
Sistem pertarungan berbasis giliran dengan dua mode: Normal (melawan monster biasa seperti Slime, Goblin, dan Minotaur) dan Boss (melawan Demon King). Pemain memilih skill di setiap giliran
### 🔀 Multiple Ending
Pilihan kritis di tengah cerita menentukan ending yang didapat:
- ✅ **True End** — Dunia Astravia diselamatkan
- ❌ **Bad End** — Dunia dikuasai oleh Demon King.

### 🎭 Animasi & Efek Visual
Animasi karakter multi-frame dengan state `idle`, `walk`, `attack`, `hurt`, `dead`, dan `defend`. Dilengkapi efek hujan dinamis, magic circle, floating text (damage/EXP), dan transition fade antar scene.

---

## ▶️ Cara Menjalankan Project

### Prasyarat
Pastikan **Python 3.x** sudah terinstal di sistem.

### Instalasi & Menjalankan

```bash
# 1. Clone repository
git clone https://github.com/username/summoned-to-another-world.git
cd summoned-to-another-world

# 2. Install dependency
pip install pygame

# 3. Jalankan game
python main.py
```

### Kontrol

| Tombol | Fungsi |
|:------:|:-------|
| `Space` / `Enter` | Lanjutkan dialog · Konfirmasi pilihan |
| `↑` `↓` | Navigasi pilihan menu |
| `E` | Interaksi dengan NPC |
| `A` / `D` | Gerak kiri / kanan saat eksplorasi |

---

## 🏗️ Implementasi Materi PBO 

Project ini dibangun di atas enam konsep PBO yang saling melengkapi.

<div align="center">
---

### 1. Abstraction

Dua kelas abstrak di `engine/base.py` menjadi fondasi seluruh sistem game. Kelas `Entity` dan `Scene` tidak bisa diinstansiasi langsung — mereka hanya mendefinisikan kontrak yang **wajib** diimplementasikan oleh setiap turunannya.

```python
from abc import ABC, abstractmethod

class Entity(ABC):
    @abstractmethod
    def update(self, dt: float) -> None: ...  # logika per-frame

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...  # rendering

    @abstractmethod
    def interact(self) -> str: ...  # respons saat berinteraksi

class Scene(ABC):
    @abstractmethod
    def on_enter(self) -> None: ...  # setup saat scene aktif

    @abstractmethod
    def handle_event(self, event) -> None: ...  # input pemain

    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def draw(self, surface) -> None: ...
```

---

### 2. Inheritance

Semua karakter dan scene mewarisi dari kelas abstrak di atas. Hierarki ini memungkinkan kode yang reusable tanpa duplikasi.

```
Entity (ABC)
└── Character
    ├── Player          ← Hero: Arga (dikontrol pemain)
    └── NPC
        ├── KingdomNPC  ← Warga kota biasa
        ├── PartyNPC    ← Elena, Lyra, Darius, Reno
        ├── BossNPC     ← Demon King
        └── MonsterNPC  ← Slime, Goblin, Minotaur, dll.

Scene (ABC)
├── OpeningScene
├── Chapter1Scene
├── Chapter2Scene  (TownScene)
├── Chapter3Scene
├── ChapterFinalScene
├── BattleScene
├── BossBattleScene
├── TrueEndScene
└── BadEndScene
```

---

### 3. Encapsulation

Atribut sensitif karakter dilindungi menggunakan `__private` dan hanya bisa diakses melalui `@property`, mencegah modifikasi langsung dari luar kelas.

```python
class Player(Character):
    def __init__(self, x: float, y: float):
        self.__hp     = 9999   # tidak bisa diakses langsung dari luar
        self.__max_hp = 9999
        self.__level  = 99

    @property
    def hp(self):
        return self.__hp       # akses hanya lewat property ini

class Character(Entity):
    @emotion.setter
    def emotion(self, value: str):
        if value in self.EMOTIONS:   # validasi sebelum nilai di-set
            self.__emotion = value
```

---

### 4. Polymorphism

Method yang sama menghasilkan perilaku berbeda tergantung kelas yang memanggilnya. Contohnya pada method `interact()` dan `draw()`:

```python
# interact() — setiap kelas mengembalikan respons berbeda
Player.interact()      # → "player"
KingdomNPC.interact()  # → baris dialog warga kota
BossNPC.interact()     # → "Hahaha... coba saja!"
MonsterNPC.interact()  # → "*Slime bergerak mengancam*"

# draw() — setiap entitas merender dirinya sendiri secara berbeda
Player.draw()          # → multi-frame animation + flip sprite otomatis
BossNPC.draw()         # → frame cycling animasi idle mengancam
MonsterNPC.draw()      # → sprite + HP bar melayang di atas kepala
```

---

### 5. Composition

Objek-objek kompleks dibangun dari komponen yang lebih kecil (*has-a relationship*), bukan hanya mengandalkan pewarisan.

```
Game
├── AssetManager          # mengelola loading sprite & audio
├── list[Scene]           # stack scene yang sedang aktif
└── dict flags            # menyimpan flag cerita global

Scene
├── DialogueBox           # menampilkan teks dengan typewriter effect
├── TransitionScreen      # efek fade in/out antar scene
├── NarratorBox           # kotak narasi sinematik
├── PartyHUD              # menampilkan HP seluruh anggota party
└── list[Entity]          # semua entitas yang ada di scene

PartyNPC
└── follow_target → Player    # menyimpan referensi ke objek Player
```

---

### 6. Singleton Pattern

`GAME_INSTANCE` di `engine/game.py` memastikan hanya ada satu instance `Game` yang aktif. Ini memungkinkan `AssetManager` diakses dari seluruh modul tanpa perlu passing referensi secara manual.

```python
GAME_INSTANCE = None  # satu-satunya instance global

class Game:
    def __init__(self, screen, clock):
        global GAME_INSTANCE
        GAME_INSTANCE = self   # di-set satu kali saat game diinisialisasi

# Di entities/characters.py — bisa akses asset tanpa import langsung
def _get_assets():
    from engine.game import GAME_INSTANCE
    return GAME_INSTANCE.assets if GAME_INSTANCE else None
```

---
