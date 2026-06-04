import pygame
import os

# ── path setup 
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_HERE)       

_ASSET_ROOTS = [
    os.path.join(_PROJECT_ROOT, "assets"),
    os.path.join(os.path.dirname(_PROJECT_ROOT), "assets"),
]

def _find_asset_root() -> str:
    for root in _ASSET_ROOTS:
        if os.path.isdir(root):
            return root
    return _ASSET_ROOTS[0]

_ASSET_ROOT = _find_asset_root()


def _p(*parts: str) -> str:
    return os.path.join(_ASSET_ROOT, *parts)


def _load_img(path: str, size=None, alpha: bool = True) -> pygame.Surface:
    """Load image; placeholder merah jika gagal."""
    try:
        img = pygame.image.load(path).convert_alpha() if alpha else pygame.image.load(path).convert()
        return pygame.transform.scale(img, size) if size else img
    except Exception:
        w, h = size if size else (64, 64)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((180, 30, 30, 160))
        pygame.draw.rect(surf, (255, 60, 60), surf.get_rect(), 2)
        try:
            font = pygame.font.Font(None, max(12, min(16, w // 6)))
            lbl = font.render(os.path.basename(path), True, (255, 240, 200))
            surf.blit(lbl, (2, h // 2 - lbl.get_height() // 2))
        except Exception:
            pass
        return surf


def _first_frame(folder: str, size=None) -> pygame.Surface:
    """Ambil frame pertama (.png/.jpg) dari sebuah folder."""
    if os.path.isdir(folder):
        files = sorted(f for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg")))
        if files:
            return _load_img(os.path.join(folder, files[0]), size)
    return _load_img("__missing__", size)


def _load_anim_frames(folder: str, size=None) -> list:
    """Load semua frame animasi dari folder, return list surface."""
    frames = []
    if os.path.isdir(folder):
        files = sorted(f for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg")))
        for f in files:
            frames.append(_load_img(os.path.join(folder, f), size))
    if not frames:
        frames.append(_load_img("__missing__", size))
    return frames


def _load_char(base_dir: str, char_name: str, state: str, size) -> pygame.Surface:
    """
    Load karakter dengan fallback berlapis:
      1. base_dir/<char_name>/<char_name>_<state>.png
      2. base_dir/<char_name>/<state>.png
      3. base_dir/<char_name>/<state>/ (ambil frame pertama jika folder)
      4. base_dir/<char_name>_<state>.png  (flat)
      5. base_dir/<char_name>/ (frame pertama di folder karakter)
    """
    name_lower = char_name.lower()
    state_lower = state.lower()

    # 1. subfolder + nama_state
    p1 = os.path.join(base_dir, name_lower, f"{name_lower}_{state_lower}.png")
    if os.path.isfile(p1):
        return _load_img(p1, size)

    # 2. subfolder + state saja
    p2 = os.path.join(base_dir, name_lower, f"{state_lower}.png")
    if os.path.isfile(p2):
        return _load_img(p2, size)

    # 3. subfolder/state/ sebagai folder animasi
    p3 = os.path.join(base_dir, name_lower, state_lower)
    if os.path.isdir(p3):
        return _first_frame(p3, size)

    # 4. flat di base_dir: nama_state.png
    p4 = os.path.join(base_dir, f"{name_lower}_{state_lower}.png")
    if os.path.isfile(p4):
        return _load_img(p4, size)

    # 5. frame pertama di subfolder karakter
    p5 = os.path.join(base_dir, name_lower)
    if os.path.isdir(p5):
        return _first_frame(p5, size)

    # Gagal
    return _load_img(p1, size)  # placeholder merah dengan nama file


def _load_sfx(path: str):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


# ── AssetManager 

class AssetManager:

    def __init__(self, W: int, H: int):
        self.W = W
        self.H = H
        self._init_fonts()
        self._load_backgrounds()
        self._load_characters()
        self._load_ui()
        self._load_holy_sword()
        self._load_audio()

    # ── Fonts 

    def _init_fonts(self):
        font_dir = _p("ui", "fonts")
        custom = None
        if os.path.isdir(font_dir):
            for f in os.listdir(font_dir):
                if f.endswith((".ttf", ".otf")):
                    custom = os.path.join(font_dir, f)
                    break

        def mf(size: int, bold: bool = False) -> pygame.font.Font:
            if custom:
                try:
                    return pygame.font.Font(custom, size)
                except Exception:
                    pass
            try:
                return pygame.font.SysFont("Georgia", size, bold=bold)
            except Exception:
                return pygame.font.Font(None, size)

        self.font_title  = mf(56, bold=True)
        self.font_large  = mf(36)
        self.font_medium = mf(26)
        self.font_small  = mf(20)
        self.font_ui     = mf(22)
        self.font_name   = mf(24, bold=True)
        self.font_tiny   = mf(16)

    # ── Backgrounds 

    def _load_backgrounds(self):
        W, H = self.W, self.H

        # Daftar semua subfolder backgrounds yang akan di-scan secara rekursif
        _BG_SEARCH_DIRS = [
            _p("backgrounds"),
            _p("backgrounds", "opening"),
            _p("backgrounds", "chapter_1"),
            _p("backgrounds", "chapter_2"),
            _p("backgrounds", "battle"),
            _p("backgrounds", "endings"),
        ]

        def _bg(filename: str, fallback=(20, 18, 40)) -> pygame.Surface:
            """Cari file BG di semua subfolder backgrounds, tanpa perlu tahu folder-nya."""
            for search_dir in _BG_SEARCH_DIRS:
                p = os.path.join(search_dir, filename)
                if os.path.isfile(p):
                    return _load_img(p, (W, H), alpha=False)
            # Gradient fallback jika file tidak ditemukan
            surf = pygame.Surface((W, H))
            for y in range(H):
                t = y / H
                col = tuple(max(0, int(c * (1 - 0.4 * t))) for c in fallback)
                pygame.draw.line(surf, col, (0, y), (W, y))
            return surf

        # ── Opening ──────────────────────────────────────────────────────────
        self.bg_night_city  = _bg("bg_night_city.png",  (10, 12, 30))
        self.bg_prolog      = _bg("prolog.png",         (10, 12, 30))

        # ── Chapter 1 ────────────────────────────────────────────────────────
        self.bg_throne_room = _bg("bg_throne_room.png", (30, 20, 50))
        self.bg_belairung   = _bg("belairung_kerajan.png", (30, 20, 50))
        self.bg_town        = _bg("bg_town.png",        (40, 50, 80))

        # ── Chapter 2 ────────────────────────────────────────────────────────
        self.bg_forest      = _bg("bg_forest.png",      (15, 35, 15))
        self.bg_ruins       = _bg("bg_ruins.png",       (50, 40, 30))
        self.bg_village     = _bg("bg_village.png",     (60, 30, 20))
        self.bg_castle_ext  = _bg("bg_castle_ext.png",  (20, 15, 30))
        self.bg_campfire    = _bg("bg_campfire.png",    (10, 12, 30))
        # ── Battle ───────────────────────────────────────────────────────────
        self.bg_battle           = _bg("bg_battle.png",       (30, 10, 50))
        self.bg_castle_int       = _bg("bg_castle_int.png",   (15, 5, 25))
        self.bg_ruang_boss       = _bg("ruang_boss.png",      (15, 5, 25))
        self.bg_ruang_boss_rusak = _bg("ruang_boss_rusak.png",(20, 5, 5))
        self.bg_hari_pernikahan  = _bg("hari_pernikahan.png", (60, 50, 80))

        # ── Endings ──────────────────────────────────────────────────────────
        self.bg_ending                 = _bg("bg_ending.png",               (50, 40, 80))
        self.bg_kota_hancur            = _bg("kota_hancur.png",             (10, 5, 5))
        self.bg_dalam_belairung_hancur = _bg("dalam_belairung_hancur.png",  (10, 5, 5))

    # ── Characters 

    def _load_characters(self):
        CS = (96, 96)    # karakter biasa
        PS = (80, 80)    # portrait
        BS = (128, 128)  # boss

        heroes_dir  = _p("characters", "heroes")
        enemies_dir = _p("characters", "enemies")
        npc_dir     = _p("characters", "npc")

        # ── Arga (Hero / Player utama) — Multi-frame Animation System ──
        arga_dir = os.path.join(heroes_dir, "arga")

        # === BEFORE ISEKAI (sebelum dapat Holy Sword) ===
        # Idle frames — before
        idle_before_dir = os.path.join(arga_dir, "idle_before")
        self.arga_idle_before_front = _load_img(
            os.path.join(idle_before_dir, "idle_front.png"), CS)
        self.arga_idle_before_side  = _load_img(
            os.path.join(idle_before_dir, "idle_side.png"),  CS)
        # Idle animasi samping (loop) — before isekai
        self.arga_idle_before_frames = _load_anim_frames(idle_before_dir, CS)
        # Filter hanya idle_side_*.png
        import re as _re
        _side_files = sorted(
            f for f in __import__("os").listdir(idle_before_dir)
            if _re.match(r"idle_side_", f) and f.endswith(".png")
        )
        if _side_files:
            self.arga_idle_before_frames = [
                _load_img(__import__("os").path.join(idle_before_dir, f), CS)
                for f in _side_files
            ]
        else:
            self.arga_idle_before_frames = [self.arga_idle_before_side]
        # Walk frames — before (8 frame animasi)
        self.arga_walk_before_frames = _load_anim_frames(
            os.path.join(arga_dir, "walk_before"), CS)

        # === AFTER ISEKAI (setelah dapat Holy Sword) ===
        # Idle frames — after isekai
        # Mendukung dua struktur folder:
        #   Lama: idle_front.png + idle_side.png + idle_side_N.png
        #   Baru: arga-idle1.png ... arga-idleN.png (depan) + arga-idle_sampingN.png (samping)
        idle_after_dir = os.path.join(arga_dir, "idle_after")
        _all_after = sorted(f for f in os.listdir(idle_after_dir) if f.lower().endswith(".png")) if os.path.isdir(idle_after_dir) else []

        # Front: prefer arga-idle*.png (bukan samping), fallback idle_front.png
        _front_files = [f for f in _all_after if "samping" not in f.lower() and "side" not in f.lower()]
        if _front_files:
            self.arga_idle_after_front  = _load_img(os.path.join(idle_after_dir, _front_files[0]), CS)
            self.arga_idle_after_frames_front = [_load_img(os.path.join(idle_after_dir, f), CS) for f in _front_files]
        else:
            self.arga_idle_after_front  = _load_img(os.path.join(idle_after_dir, "idle_front.png"), CS)
            self.arga_idle_after_frames_front = [self.arga_idle_after_front]

        # Side: prefer arga-idle_samping*.png, fallback idle_side*.png
        _side_files = [f for f in _all_after if "samping" in f.lower() or "side" in f.lower()]
        if _side_files:
            self.arga_idle_after_side   = _load_img(os.path.join(idle_after_dir, _side_files[0]), CS)
            self.arga_idle_after_frames = [_load_img(os.path.join(idle_after_dir, f), CS) for f in _side_files]
        else:
            self.arga_idle_after_side   = _load_img(os.path.join(idle_after_dir, "idle_side.png"), CS)
            self.arga_idle_after_frames = [self.arga_idle_after_side]
        # Walk frames — after (8 frame animasi)
        self.arga_walk_after_frames = _load_anim_frames(
            os.path.join(arga_dir, "walk_after"), CS)
        # Attack frames — after
        self.arga_attack1_frames = _load_anim_frames(
            os.path.join(arga_dir, "attack_after"), CS)
        # Hurt frames — after
        self.arga_hurt_frames = _load_anim_frames(
            os.path.join(arga_dir, "hurt_after"), CS)
        # Dead frames — after
        self.arga_dead_frames = _load_anim_frames(
            os.path.join(arga_dir, "dead_after"), CS)
        # Defend frames — after
        self.arga_defend_frames = _load_anim_frames(
            os.path.join(arga_dir, "defend_after"), CS)

        # === Legacy single-image aliases (untuk kompatibilitas kode lama) ===
        # Sebelum isekai = default awal game
        self.char_arga_idle    = self.arga_idle_before_front
        self.char_arga_walk    = self.arga_walk_before_frames[0] if self.arga_walk_before_frames else self.arga_idle_before_front
        self.char_arga_attack  = self.arga_attack1_frames[0]  if self.arga_attack1_frames  else self.arga_idle_after_front
        self.char_arga_hurt    = self.arga_hurt_frames[0]     if self.arga_hurt_frames      else self.arga_idle_after_front
        self.char_arga_portrait= self.arga_idle_before_front

        self.char_hero_idle     = self.char_arga_idle
        self.char_hero_walk     = self.char_arga_walk
        self.char_hero_attack   = self.char_arga_attack
        self.char_hero_hurt     = self.char_arga_hurt
        self.char_hero_portrait = self.char_arga_portrait
        self.char_player_idle    = self.char_arga_idle
        self.char_player_walk    = self.char_arga_walk
        self.char_player_attack  = self.char_arga_attack
        self.char_player_hurt    = self.char_arga_hurt
        self.char_player_portrait = self.char_arga_portrait

        for expr in ("normal", "happy", "angry", "sad", "shocked"):
            setattr(self, f"char_player_expr_{expr}", self.arga_idle_before_front)
        self.char_player_skill = self.char_arga_attack
        self.char_player_dead  = self.arga_dead_frames[0] if self.arga_dead_frames else self.arga_idle_after_front

        # ── Elena (Heroine / Party)

        for state in ("idle", "attack", "hurt"):
            setattr(
                self,
                f"char_elena_{state}",
                _load_char(heroes_dir, "elena", state, CS)
            )

        self.char_elena_portrait = _load_char(
            heroes_dir,
            "elena",
            "portrait",
            PS
        )

        # WALK ANIMATION
        self.elena_walk_frames = _load_anim_frames(
            os.path.join(heroes_dir, "elena", "walk"),
            CS
        )
        self.elena_idle_frames = _load_anim_frames(
            os.path.join(heroes_dir, "elena", "idle"),
            CS
        )
        if not self.elena_idle_frames:
            self.elena_idle_frames = [self.char_elena_idle]

        self.elena_dead_frames = _load_anim_frames(
            os.path.join(heroes_dir, "elena", "dead"),
            CS
        )
        if not self.elena_dead_frames:
            self.elena_dead_frames = [getattr(self, "elena_dead5", self.char_elena_idle)]

        self.elena_hurt_frames = _load_anim_frames(
            os.path.join(heroes_dir, "elena", "hurt"),
            CS
        )
        if not self.elena_hurt_frames:
            self.elena_hurt_frames = [self.char_elena_hurt]

       # ── Lyra (Party)

        for state in ("idle", "attack", "hurt"):
            setattr(
                self,
                f"char_lyra_{state}",
                _load_char(heroes_dir, "lyra", state, CS)
            )

        self.char_lyra_portrait = _load_char(
            heroes_dir,
            "lyra",
            "portrait",
            PS
        )

        # WALK ANIMATION
        self.lyra_walk_frames = _load_anim_frames(
            os.path.join(heroes_dir, "lyra", "walk"),
            CS
        )
        self.lyra_idle_frames = _load_anim_frames(
            os.path.join(heroes_dir, "lyra", "idle"),
            CS
        )
        if not self.lyra_idle_frames:
            self.lyra_idle_frames = [self.char_lyra_idle]

        self.lyra_dead_frames = _load_anim_frames(
            os.path.join(heroes_dir, "lyra", "dead"),
            CS
        )
        if not self.lyra_dead_frames:
            self.lyra_dead_frames = [getattr(self, "lyra_dead6", self.char_lyra_idle)]

        self.lyra_hurt_frames = _load_anim_frames(
            os.path.join(heroes_dir, "lyra", "hurt"),
            CS
        )
        if not self.lyra_hurt_frames:
            self.lyra_hurt_frames = [self.char_lyra_hurt]

        # ── Darius (Party)

        for state in ("idle", "attack", "hurt"):
            setattr(
                self,
                f"char_darius_{state}",
                _load_char(heroes_dir, "darius", state, CS)
            )

        self.char_darius_portrait = _load_char(
            heroes_dir,
            "darius",
            "portrait",
            PS
        )
        # WALK / IDLE / ATTACK / DEAD ANIMATION — Darius
        self.darius_walk_frames   = _load_anim_frames(os.path.join(heroes_dir, "darius", "walk"),   CS)
        self.darius_idle_frames   = _load_anim_frames(os.path.join(heroes_dir, "darius", "idle"),   CS)
        self.darius_attack_frames = _load_anim_frames(os.path.join(heroes_dir, "darius", "attack"), CS)
        self.darius_dead_frames   = _load_anim_frames(os.path.join(heroes_dir, "darius", "dead"),   CS)
        self.darius_hurt_frames   = _load_anim_frames(os.path.join(heroes_dir, "darius", "hurt"),   CS)
        if not self.darius_idle_frames:
            self.darius_idle_frames = [self.char_darius_idle]
        if not self.darius_attack_frames:
            self.darius_attack_frames = [self.char_darius_attack]
        if not self.darius_dead_frames:
            self.darius_dead_frames = [self.darius_idle_frames[-1]]
        # Darius hurt4 — 1 frame static untuk pose terluka sebelum battle desa
        self.darius_hurt4 = _load_img(
            os.path.join(heroes_dir, "darius", "hurt", "hurt_4.png"), CS
        )
        
        # ── Reno (Party)
        for state in ("idle", "attack", "hurt"):
            setattr(
                self,
                f"char_reno_{state}",
                _load_char(heroes_dir, "reno", state, CS)
            )

        self.char_reno_portrait = _load_char(
            heroes_dir,
            "reno",
            "portrait",
            PS
        )
        # WALK / IDLE / ATTACK / DEAD ANIMATION — Reno
        self.reno_walk_frames   = _load_anim_frames(os.path.join(heroes_dir, "reno", "walk"),   CS)
        self.reno_attack_frames = _load_anim_frames(os.path.join(heroes_dir, "reno", "attack"), CS)
        self.reno_dead_frames   = _load_anim_frames(os.path.join(heroes_dir, "reno", "dead"),   CS)
        self.reno_hurt_frames   = _load_anim_frames(os.path.join(heroes_dir, "reno", "hurt"),   CS)
        _reno_idle_dir = os.path.join(heroes_dir, "reno", "idle")
        _reno_side = sorted(
            f for f in os.listdir(_reno_idle_dir)
            if f.startswith("idle_side_") and f.endswith(".png")
        )
        if _reno_side:
            self.reno_idle_frames = [
                _load_img(os.path.join(_reno_idle_dir, f), CS)
                for f in _reno_side
            ]
        else:
            self.reno_idle_frames = _load_anim_frames(_reno_idle_dir, CS)
        if not self.reno_idle_frames:
            self.reno_idle_frames = [self.char_reno_idle]
        if not self.reno_attack_frames:
            self.reno_attack_frames = [self.char_reno_attack]
        if not self.reno_dead_frames:
            self.reno_dead_frames = [self.reno_idle_frames[-1]]
        # Dead pose spesifik untuk bad ending
        self.reno_dead5   = _load_img(os.path.join(heroes_dir, "reno",   "dead", "reno-dead5.png"), CS)
        self.elena_dead5  = _load_img(os.path.join(heroes_dir, "elena",  "dead", "dead_5.png"),     CS)
        self.lyra_dead6   = _load_img(os.path.join(heroes_dir, "lyra",   "dead", "dead_6.png"),     CS)
        self.darius_dead7 = _load_img(os.path.join(heroes_dir, "darius", "dead", "darius-dead7.png"), CS)
        self.darius_hurt5 = _load_img(os.path.join(heroes_dir, "darius", "hurt", "darius-hurt5.png"), CS)
        self.arga_hurt3   = _load_img(os.path.join(heroes_dir, "arga",   "hurt_after", "hurt_3.png"), CS)
        # Reno hurt4 — 1 frame static untuk pose terluka sebelum battle hutan
        self.reno_hurt4 = _load_img(
            os.path.join(heroes_dir, "reno", "hurt", "reno-hurt4.png"), CS
        )

        # ── Wedding idle frames (untuk true ending scene pernikahan) ──
        arga_wedding_dir  = os.path.join(heroes_dir, "arga",  "wedding")
        elena_wedding_dir = os.path.join(heroes_dir, "elena", "wedding")
        self.arga_wedding_idle_frames  = _load_anim_frames(arga_wedding_dir,  None)
        self.elena_wedding_idle_frames = _load_anim_frames(elena_wedding_dir, None)
        # Fallback ke idle biasa jika folder tidak ada atau kosong
        if not self.arga_wedding_idle_frames or (
            len(self.arga_wedding_idle_frames) == 1 and
            self.arga_wedding_idle_frames[0].get_size() == (32, 32)
        ):
            self.arga_wedding_idle_frames = self.arga_idle_before_frames or [self.arga_idle_before_front]
        if not self.elena_wedding_idle_frames or (
            len(self.elena_wedding_idle_frames) == 1 and
            self.elena_wedding_idle_frames[0].get_size() == (32, 32)
        ):
            self.elena_wedding_idle_frames = self.elena_idle_frames or [self.char_elena_idle]

        # Silence alias references (no-op)
        self.char_elena_idle
        self.char_elena_attack
        self.char_elena_portrait

        self.char_darius_idle
        self.char_darius_attack
        self.char_darius_portrait

        self.char_lyra_idle
        self.char_lyra_attack
        self.char_lyra_portrait

        self.char_reno_idle
        self.char_reno_attack
        self.char_reno_portrait

        # ── Enemies 
        # Enemies — full animation frames (scaling dilakukan di draw, bukan di sini)
        MS = None

        # Slime
        slime_dir = os.path.join(enemies_dir, "slime")
        self.slime_idle_frames  = _load_anim_frames(os.path.join(slime_dir, "idle"), MS)
        self.slime_walk_frames  = _load_anim_frames(os.path.join(slime_dir, "walk"), MS)
        _slime_dead_dir = os.path.join(slime_dir, "dead")
        self.slime_dead_frames  = (_load_anim_frames(_slime_dead_dir, MS)
                                   if os.path.isdir(_slime_dead_dir) and os.listdir(_slime_dead_dir)
                                   else [self.slime_idle_frames[-1]])
        self.char_slime_idle    = self.slime_idle_frames[0]
        self.char_slime_attack  = self.slime_idle_frames[0]
        self.char_slime_hurt    = self.slime_idle_frames[0]
        self.char_slime_dead    = self.slime_dead_frames[-1]

        # Goblin
        goblin_dir = os.path.join(enemies_dir, "goblin")
        self.goblin_idle_frames = _load_anim_frames(os.path.join(goblin_dir, "idle"), MS)
        self.goblin_walk_frames = _load_anim_frames(os.path.join(goblin_dir, "walk"), MS)
        self.goblin_dead_frames = _load_anim_frames(os.path.join(goblin_dir, "dead"), MS)
        self.char_goblin_idle   = self.goblin_idle_frames[0]

        # Minotaur — menggantikan Stone Golem, Dark Knight, Orc
        mino_dir = os.path.join(enemies_dir, "minotaur")
        self.minotaur_idle_frames = _load_anim_frames(os.path.join(mino_dir, "idle"), MS)
        self.minotaur_walk_frames = _load_anim_frames(os.path.join(mino_dir, "walk"), MS)
        self.minotaur_dead_frames = _load_anim_frames(os.path.join(mino_dir, "dead"), MS)
        self.char_minotaur_idle   = self.minotaur_idle_frames[0]

        # Mushroom dihapus — alias fallback aman
        self.char_mushroom_idle = self.char_goblin_idle

        # ── Demon King — load semua frame animasi ──
        demon_king_dir = os.path.join(enemies_dir, "demon_king")

        # Idle frames — pisahkan idle_side dari idle_front
        dk_idle_dir = os.path.join(demon_king_dir, "idle")
        # Idle side: file yang namanya mengandung "side" (demon-idle_side1..5)
        _dk_side_files = sorted(
            f for f in os.listdir(dk_idle_dir)
            if f.lower().endswith((".png", ".jpg")) and "side" in f.lower()
        ) if os.path.isdir(dk_idle_dir) else []
        self.demon_king_idle_side_frames = (
            [_load_img(os.path.join(dk_idle_dir, f), BS) for f in _dk_side_files]
            if _dk_side_files else []
        )
        # Idle front: file yang namanya TIDAK mengandung "side"
        _dk_front_files = sorted(
            f for f in os.listdir(dk_idle_dir)
            if f.lower().endswith((".png", ".jpg")) and "side" not in f.lower()
        ) if os.path.isdir(dk_idle_dir) else []
        self.demon_king_idle_frames = (
            [_load_img(os.path.join(dk_idle_dir, f), BS) for f in _dk_front_files]
            if _dk_front_files else []
        )
        if not self.demon_king_idle_frames:
            self.demon_king_idle_frames = [_load_char(enemies_dir, "demon_king", "idle", BS)]
        # Jika idle_side tidak tersedia, fallback ke idle_front
        if not self.demon_king_idle_side_frames:
            self.demon_king_idle_side_frames = self.demon_king_idle_frames
        self.char_demon_king_idle = self.demon_king_idle_side_frames[0]

        # Attack frames (demon-att-1..5)
        dk_attack_dir = os.path.join(demon_king_dir, "attack")
        self.demon_king_attack_frames = _load_anim_frames(dk_attack_dir, BS)
        if not self.demon_king_attack_frames:
            self.demon_king_attack_frames = self.demon_king_idle_frames
        self.char_demon_king_attack = self.demon_king_attack_frames[0]

        # Ultimate frames (demon-ulti1..8)
        dk_ult_dir = os.path.join(demon_king_dir, "ultimate")
        self.demon_king_ultimate_frames = _load_anim_frames(dk_ult_dir, BS)
        if not self.demon_king_ultimate_frames:
            self.demon_king_ultimate_frames = self.demon_king_idle_frames
        self.char_demon_king_ultimate = self.demon_king_ultimate_frames[0]

        # Hurt frames (demon-hurt1..4)
        dk_hurt_dir = os.path.join(demon_king_dir, "hurt")
        self.demon_king_hurt_frames = _load_anim_frames(dk_hurt_dir, BS)
        if not self.demon_king_hurt_frames:
            self.demon_king_hurt_frames = self.demon_king_idle_frames

        # Dead frames (demon-dead1..5)
        dk_dead_dir = os.path.join(demon_king_dir, "dead")
        self.demon_king_dead_frames = _load_anim_frames(dk_dead_dir, BS)
        if not self.demon_king_dead_frames:
            self.demon_king_dead_frames = self.demon_king_idle_frames

        # ── NPC 
        for npc in ("king", "village_elder", "merchant", "guard"):
            d = os.path.join(npc_dir, npc)
            if os.path.isdir(d):
                surf = _first_frame(d, PS)
            else:
                surf = _load_img(os.path.join(npc_dir, f"{npc}.png"), PS)
            setattr(self, f"char_npc_{npc}", surf)

        # ── NPC Opening: Mahasiswa & Pekerja Kantoran ──
        self.npc_college_frames = _load_anim_frames(os.path.join(npc_dir, "college"), None)
        self.npc_worker_frames  = _load_anim_frames(os.path.join(npc_dir, "worker"),  None)
        if not self.npc_college_frames:
            self.npc_college_frames = [_load_img("__missing__", None)]
        if not self.npc_worker_frames:
            self.npc_worker_frames  = [_load_img("__missing__", None)]

        # ── NPC Chapter 1: King Aldric, Mage, Knight ──
        self.king_aldric_idle_frames = _load_anim_frames(os.path.join(npc_dir, "king_aldric"), None)
        self.mage_idle_frames        = _load_anim_frames(os.path.join(npc_dir, "mage"),        None)
        self.knight_idle_frames      = _load_anim_frames(os.path.join(npc_dir, "knight"),      None)
        if not self.king_aldric_idle_frames:
            self.king_aldric_idle_frames = [_load_img("__missing__", None)]
        if not self.mage_idle_frames:
            self.mage_idle_frames = [_load_img("__missing__", None)]
        if not self.knight_idle_frames:
            self.knight_idle_frames = [_load_img("__missing__", None)]
        # Alias single-frame untuk kompatibilitas KingdomNPC/char_npc_ lookup
        self.char_npc_king_aldric = self.king_aldric_idle_frames[0]
        self.char_npc_mage        = self.mage_idle_frames[0]
        self.char_npc_knight      = self.knight_idle_frames[0]

        # ── NPC Chapter 2 (Town): Citizen Child, Citizen Man, Old Man, Soldier ──
        self.citizen_child_idle_frames = _load_anim_frames(os.path.join(npc_dir, "citizen-child"), None)
        self.citizen_man_idle_frames   = _load_anim_frames(os.path.join(npc_dir, "citizen-man"),   None)
        self.oldman_idle_frames        = _load_anim_frames(os.path.join(npc_dir, "oldman"),        None)
        self.soldier_idle_frames       = _load_anim_frames(os.path.join(npc_dir, "soldier"),       None)
        if not self.citizen_child_idle_frames:
            self.citizen_child_idle_frames = [_load_img("__missing__", None)]
        if not self.citizen_man_idle_frames:
            self.citizen_man_idle_frames = [_load_img("__missing__", None)]
        if not self.oldman_idle_frames:
            self.oldman_idle_frames = [_load_img("__missing__", None)]
        if not self.soldier_idle_frames:
            self.soldier_idle_frames = [_load_img("__missing__", None)]

    # ── UI 

    def _load_ui(self):
        uid = _p("ui")

        def _ui(fname: str, size=None) -> pygame.Surface:
            return _load_img(os.path.join(uid, fname), size)

        self.ui_dialog_box    = _ui("dialog_box.png",    (self.W - 40, 165))
        self.ui_choice_button = _ui("choice_button.png", (300, 42))
        self.ui_nameplate     = _ui("nameplate.png",     (220, 34))

        cursor_dir = os.path.join(uid, "cursor")
        self.ui_cursor = _first_frame(cursor_dir, (24, 24)) if os.path.isdir(cursor_dir) else None

    # ── Holy Sword ────────────────────────────────────────────

    def _load_holy_sword(self):
        d = _p("holy_sword")
        # Load full-res sword sprite (scaling dilakukan saat draw)
        sword_path = os.path.join(d, "holy_sword.png")
        self.holy_sword = _load_img(sword_path) if os.path.isfile(sword_path) else None
        # Glow sprite tidak lagi digunakan — efek partikel dirender secara prosedural
        self.holy_sword_glow = None

    # ── Audio ─────────────────────────────────────────────────

    def _load_audio(self):
        bgm_dir = _p("audio", "bgm")
        sfx_dir = _p("audio", "sfx")

        self._bgm_paths: dict[str, str | None] = {}
        for key, fname in [("kingdom_theme", "kingdom_theme.mp3"),
                            ("battle_theme",  "battle_theme.mp3"),
                            ("sad_theme",     "sad_theme.mp3")]:
            p = os.path.join(bgm_dir, fname)
            self._bgm_paths[key] = p if os.path.isfile(p) else None

        for sub in ("opening", "village", "battle", "boss", "ending"):
            sd = os.path.join(bgm_dir, sub)
            if os.path.isdir(sd):
                for f in sorted(os.listdir(sd)):
                    if f.lower().endswith((".mp3", ".ogg", ".wav")):
                        k = f"{sub}_{os.path.splitext(f)[0]}"
                        self._bgm_paths[k] = os.path.join(sd, f)
                        self._bgm_paths.setdefault(sub, os.path.join(sd, f))

        self._current_bgm = ""

        self._sfx: dict = {}
        for key, path in [
            ("sword_hit",   os.path.join(sfx_dir, "sword_hit.wav")),
            ("menu_click",  os.path.join(sfx_dir, "menu_click.wav")),
            ("magic_flash", os.path.join(sfx_dir, "magic_flash.wav")),
        ]:
            sfx = _load_sfx(path)
            self._sfx[key] = sfx
            aliases = {
                "sword_hit":   ["slash", "damage"],
                "menu_click":  ["cursor", "select"],
                "magic_flash": ["magic", "flash", "fanfare"],
            }
            for alias in aliases.get(key, []):
                self._sfx.setdefault(alias, sfx)

        for sub in ("ui", "battle", "footsteps", "ambient"):
            sd = os.path.join(sfx_dir, sub)
            if os.path.isdir(sd):
                for f in sorted(os.listdir(sd)):
                    if f.lower().endswith((".wav", ".ogg", ".mp3")):
                        k = f"{sub}_{os.path.splitext(f)[0]}"
                        self._sfx[k] = _load_sfx(os.path.join(sd, f))

    # ── Public API 

    def play_bgm(self, key: str, loop: int = -1, volume: float = 0.7) -> None:
        if key == self._current_bgm:
            return
        path = self._bgm_paths.get(key)
        if path and os.path.isfile(path):
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loop)
                self._current_bgm = key
            except Exception:
                pass

    def stop_bgm(self) -> None:
        try:
            pygame.mixer.music.stop()
            self._current_bgm = ""
        except Exception:
            pass

    def play(self, key: str, volume: float = 0.8) -> None:
        sfx = self._sfx.get(key)
        if sfx:
            try:
                sfx.set_volume(volume)
                sfx.play()
            except Exception:
                pass

    # ── Compatibility helpers 

    def load_image(self, category: str, filename: str, size=None) -> pygame.Surface:
        return _load_img(_p(category, filename), size)

    def get_background(self, name: str) -> pygame.Surface:
        attr = f"bg_{name}"
        if hasattr(self, attr):
            return getattr(self, attr)
        return _load_img(_p("backgrounds", f"{name}.png"), (self.W, self.H), alpha=False)

    def get_character(self, name: str, state: str = "idle", size=(96, 96)) -> pygame.Surface:
        name_lower = name.lower()
        state_lower = state.lower()

        char_map = {
            "arga":   "arga",
            "hero":   "arga",
            "player": "arga",
            "elena":  "elena",
            "lyra":   "lyra",
            "darius": "darius",
        }
        mapped = char_map.get(name_lower, name_lower)

        attr = f"char_{mapped}_{state_lower}"
        if hasattr(self, attr):
            surf = getattr(self, attr)
            if surf and surf.get_size() != size:
                return pygame.transform.scale(surf, size)
            return surf

        heroes_dir  = _p("characters", "heroes")
        enemies_dir = _p("characters", "enemies")
        npc_dir     = _p("characters", "npc")

        for base in (heroes_dir, enemies_dir, npc_dir):
            p = os.path.join(base, mapped, f"{mapped}_{state_lower}.png")
            if os.path.isfile(p):
                return _load_img(p, size)
            p2 = os.path.join(base, mapped, f"{state_lower}.png")
            if os.path.isfile(p2):
                return _load_img(p2, size)

        return _load_img(f"__missing_{name}_{state}__", size)

    def get_ui(self, name: str, size=None) -> pygame.Surface:
        attr = f"ui_{name.replace('-','_').replace('.png','')}"
        if hasattr(self, attr) and getattr(self, attr) is not None:
            surf = getattr(self, attr)
            if size and surf.get_size() != size:
                return pygame.transform.scale(surf, size)
            return surf
        return _load_img(_p("ui", name), size)
