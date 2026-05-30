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

        def _bg(filename: str, subfolder: str = "", fallback=(20, 18, 40)) -> pygame.Surface:
            # 1. Coba langsung di backgrounds/
            p = _p("backgrounds", filename)
            if os.path.isfile(p):
                return _load_img(p, (W, H), alpha=False)
            # 2. Coba di subfolder
            if subfolder:
                p2 = _p("backgrounds", subfolder, filename)
                if os.path.isfile(p2):
                    return _load_img(p2, (W, H), alpha=False)
                # 3. File pertama di subfolder
                subdir = _p("backgrounds", subfolder)
                if os.path.isdir(subdir):
                    for f in sorted(os.listdir(subdir)):
                        if f.lower().endswith((".png", ".jpg", ".jpeg")):
                            return _load_img(os.path.join(subdir, f), (W, H), alpha=False)
            # 4. Gradient fallback
            surf = pygame.Surface((W, H))
            for y in range(H):
                t = y / H
                col = tuple(max(0, int(c * (1 - 0.4 * t))) for c in fallback)
                pygame.draw.line(surf, col, (0, y), (W, y))
            return surf

        self.bg_night_city  = _bg("bg_night_city.png",  "opening",   (10, 12, 30))
        self.bg_throne_room = _bg("bg_throne_room.png", "chapter_1", (30, 20, 50))
        self.bg_town        = _bg("bg_town.png",        "chapter_1", (40, 50, 80))
        self.bg_forest      = _bg("bg_forest.png",      "chapter_2", (15, 35, 15))
        self.bg_ruins       = _bg("bg_ruins.png",       "chapter_2", (50, 40, 30))
        self.bg_village     = _bg("bg_village.png",     "chapter_2", (60, 30, 20))
        self.bg_battle      = _bg("bg_battle.png",      "battle",    (30, 10, 50))
        self.bg_castle_ext  = _bg("bg_castle_ext.png",  "chapter_2", (20, 15, 30))
        self.bg_castle_int  = _bg("bg_castle_int.png",  "battle",    (15, 5, 25))
        self.bg_ending      = _bg("bg_ending.png",      "endings",   (50, 40, 80))

    # ── Characters 

    def _load_characters(self):
        CS = (96, 96)    # karakter biasa
        PS = (80, 80)    # portrait
        BS = (128, 128)  # boss

        heroes_dir  = _p("characters", "heroes")
        enemies_dir = _p("characters", "enemies")
        npc_dir     = _p("characters", "npc")

        # ── Arga (Hero / Player utama) 
        # Folder: assets/characters/heroes/arga/
        for state in ("idle", "walk", "attack", "hurt"):
            attr = f"char_arga_{state}"
            setattr(self, attr, _load_char(heroes_dir, "arga", state, CS))
        self.char_arga_portrait = _load_char(heroes_dir, "arga", "portrait", PS)

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
        # Expression aliases (semua pakai portrait arga)
        for expr in ("normal", "happy", "angry", "sad", "shocked"):
            expr_attr = f"char_player_expr_{expr}"
            # Coba cari ekspresi spesifik dulu, fallback ke portrait
            expr_surf = _load_char(heroes_dir, "arga", expr, PS)
            setattr(self, expr_attr, expr_surf)
        # Skill/dead
        self.char_player_skill = _load_char(heroes_dir, "arga", "skill", CS)
        self.char_player_dead  = _load_char(heroes_dir, "arga", "dead", CS)

        # ── Elena (Heroine / Party) 
        # Folder: assets/characters/heroes/elena/
        for state in ("idle", "attack", "hurt"):
            setattr(self, f"char_elena_{state}",
                    _load_char(heroes_dir, "elena", state, CS))
        self.char_elena_portrait = _load_char(heroes_dir, "elena", "portrait", PS)

        # ── Lyra (Party) 
        # Folder: assets/characters/heroes/lyra/
        for state in ("idle", "attack", "hurt"):
            setattr(self, f"char_lyra_{state}",
                    _load_char(heroes_dir, "lyra", state, CS))
        self.char_lyra_portrait = _load_char(heroes_dir, "lyra", "portrait", PS)

        # ── Darius (Party) 
        # Folder: assets/characters/heroes/darius/
        for state in ("idle", "attack", "hurt"):
            setattr(self, f"char_darius_{state}",
                    _load_char(heroes_dir, "darius", state, CS))
        self.char_darius_portrait = _load_char(heroes_dir, "darius", "portrait", PS)

        # Alias lama: luna/kael/aria → elena/lyra/darius (jika masih ada referensi lama)
        self.char_elena_idle
        self.char_elena_attack
        self.char_elena_portrait
        self.char_darius_idle
        self.char_darius_attack
        self.char_darius_portrait
        self.char_lyra_idle
        self.char_lyra_attack
        self.char_lyra_portrait

        # ── Enemies 
        # Slime — folder: assets/characters/enemies/slime/idle/, attack/, dll
        slime_dir = os.path.join(enemies_dir, "slime")
        self.char_slime_idle   = _first_frame(os.path.join(slime_dir, "idle"),   (64, 64)) \
                                  if os.path.isdir(os.path.join(slime_dir, "idle")) \
                                  else _load_char(enemies_dir, "slime", "idle", (64, 64))
        self.char_slime_attack = _first_frame(os.path.join(slime_dir, "attack"), (64, 64)) \
                                  if os.path.isdir(os.path.join(slime_dir, "attack")) \
                                  else _load_char(enemies_dir, "slime", "attack", (64, 64))
        self.char_slime_hurt   = _first_frame(os.path.join(slime_dir, "hurt"),   (64, 64)) \
                                  if os.path.isdir(os.path.join(slime_dir, "hurt")) \
                                  else _load_char(enemies_dir, "slime", "hurt", (64, 64))
        self.char_slime_dead   = _first_frame(os.path.join(slime_dir, "dead"),   (64, 64)) \
                                  if os.path.isdir(os.path.join(slime_dir, "dead")) \
                                  else _load_char(enemies_dir, "slime", "dead", (64, 64))

        # Mushroom 
        self.char_mushroom_idle = _load_char(enemies_dir, "mushroom", "idle", (64, 64))

        # Goblin 
        self.char_goblin_idle = _load_char(enemies_dir, "goblin", "idle", (64, 64))

        # ── Boss: Demon King 
        # Folder: assets/characters/enemies/demon_king/
        demon_king_dir = os.path.join(enemies_dir, "demon_king")
        if os.path.isdir(demon_king_dir):
            self.char_demon_king_idle = _first_frame(demon_king_dir, BS)
        else:
            self.char_demon_king_idle = _load_char(enemies_dir, "demon_king", "idle", BS)

        # ── NPC 
        for npc in ("king", "village_elder", "merchant", "guard"):
            d = os.path.join(npc_dir, npc)
            if os.path.isdir(d):
                surf = _first_frame(d, PS)
            else:
                surf = _load_img(os.path.join(npc_dir, f"{npc}.png"), PS)
            setattr(self, f"char_npc_{npc}", surf)

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
        self.holy_sword      = _load_img(os.path.join(d, "holy_sword.png"),      (40, 100))
        self.holy_sword_glow = _load_img(os.path.join(d, "holy_sword_glow.png"), (100, 100))

    # ── Audio ─────────────────────────────────────────────────

    def _load_audio(self):
        bgm_dir = _p("audio", "bgm")
        sfx_dir = _p("audio", "sfx")

        # BGM — simpan sebagai path string
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

        # SFX
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

        # Scan subfolder SFX
        for sub in ("ui", "battle", "footsteps", "ambient"):
            sd = os.path.join(sfx_dir, sub)
            if os.path.isdir(sd):
                for f in sorted(os.listdir(sd)):
                    if f.lower().endswith((".wav", ".ogg", ".mp3")):
                        k = f"{sub}_{os.path.splitext(f)[0]}"
                        self._sfx[k] = _load_sfx(os.path.join(sd, f))

    # ── Public API 

    def play_bgm(self, key: str, loop: int = -1, volume: float = 0.7) -> None:
        """Putar BGM. Tidak restart jika sudah main BGM yang sama."""
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
        """Putar SFX sekali."""
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

        # Mapping nama → atribut (termasuk alias)
        char_map = {
            "arga":       "arga",
            "hero":       "arga",
            "player":     "arga",
            "elena":      "elena",
            "lyra":       "lyra",
            "darius":     "darius",
        }
        mapped = char_map.get(name_lower, name_lower)

        # Coba atribut yang sudah dimuat
        attr = f"char_{mapped}_{state_lower}"
        if hasattr(self, attr):
            surf = getattr(self, attr)
            if surf and surf.get_size() != size:
                return pygame.transform.scale(surf, size)
            return surf

        # Fallback: coba load langsung
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

        # Placeholder
        return _load_img(f"__missing_{name}_{state}__", size)

    def get_ui(self, name: str, size=None) -> pygame.Surface:
        attr = f"ui_{name.replace('-','_').replace('.png','')}"
        if hasattr(self, attr) and getattr(self, attr) is not None:
            surf = getattr(self, attr)
            if size and surf.get_size() != size:
                return pygame.transform.scale(surf, size)
            return surf
        return _load_img(_p("ui", name), size)
