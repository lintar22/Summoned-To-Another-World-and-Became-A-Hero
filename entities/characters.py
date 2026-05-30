"""
entities/characters.py
======================
Hierarki karakter — INHERITANCE, ENCAPSULATION, POLYMORPHISM.

Entity (ABC)
└── Character          ← kelas menengah
    ├── Player         ← dikontrol pemain (Arga)
    └── NPC            ← karakter non-player
        ├── TownNPC    ← warga biasa
        ├── PartyNPC   ← anggota party (Elena, Lyra, Darius)
        ├── BossNPC    ← musuh boss (Demon King)
        └── MonsterNPC ← musuh biasa (Slime, Mushroom, dll)

Nama karakter:
  Hero/Player : Arga
  Heroine     : Elena
  Party       : Lyra, Darius
  Boss        : Demon King
"""

import pygame
import math
import random
from engine.base import Entity, BattleEntity


# ── Helper internal ───────────────────────────────────────────

def _get_assets():
    """Ambil instance AssetManager dari GAME_INSTANCE global."""
    try:
        from engine.game import GAME_INSTANCE
        return GAME_INSTANCE.assets if GAME_INSTANCE else None
    except Exception:
        return None


def _blit_centered(surface: pygame.Surface, sprite: pygame.Surface, cx: int, cy: int):
    """Blit sprite dengan titik anchor di tengah-bawah (kaki karakter)."""
    w, h = sprite.get_size()
    surface.blit(sprite, (cx - w // 2, cy - h))


# ─────────────────────────────────────────────────────────────
# CHARACTER — Kelas Menengah
# ─────────────────────────────────────────────────────────────
class Character(Entity):
    """
    [INHERITANCE] Mewarisi Entity.
    [ENCAPSULATION] __emotion, __hp, __stats bersifat private.
    """

    EMOTIONS = ["normal", "happy", "sad", "surprised", "thinking", "angry", "excited"]

    def __init__(self, name: str, x: float, y: float, color: tuple):
        super().__init__(name, x, y)
        self.__emotion = "normal"
        self.__dialogue_lines: list[str] = []
        self._color = color
        self._anim_timer = 0.0
        self._bob_offset = 0.0
        self._facing_right = True
        self._highlight = False
        self._scale = 1.0

    @property
    def emotion(self) -> str:
        return self.__emotion

    @emotion.setter
    def emotion(self, value: str):
        if value in self.EMOTIONS:
            self.__emotion = value

    def set_dialogues(self, lines: list[str]):
        self.__dialogue_lines = lines

    def get_dialogue(self, index: int) -> str:
        if 0 <= index < len(self.__dialogue_lines):
            return self.__dialogue_lines[index]
        return ""

    def dialogue_count(self) -> int:
        return len(self.__dialogue_lines)

    def update(self, dt: float) -> None:
        self._anim_timer += dt
        self._bob_offset = math.sin(self._anim_timer * 2.5) * 3

    # ── Draw utama ────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        if assets:
            sprite = assets.get_character(self._name, self.__emotion, (96, 96))
            if sprite:
                _blit_centered(surface, sprite, x, y)
                self._draw_highlight(surface, x, y)
                return
        self._draw_body(surface, x, y)

    # ── Fallback: gambar primitif ──────────────────────────────

    def _draw_highlight(self, surface, x, y):
        if self._highlight:
            hs = pygame.Surface((50, 70), pygame.SRCALPHA)
            pygame.draw.rect(hs, (255, 240, 100, 40), (0, 0, 50, 70))
            surface.blit(hs, (x - 25, y - 68))
            try:
                font = pygame.font.SysFont("Consolas", 13, bold=True)
                ind = font.render("[E]", True, (100, 200, 255))
                surface.blit(ind, (x - ind.get_width() // 2, y - 85))
            except Exception:
                pass

    def _draw_body(self, surface, x, y, scale=1.0):
        """Fallback gambar primitif — hanya muncul jika asset belum ada."""
        s = scale
        sz = lambda v: int(v * s)
        sh = pygame.Surface((sz(40), sz(10)), pygame.SRCALPHA)
        pygame.draw.ellipse(sh, (0, 0, 0, 60), (0, 0, sz(40), sz(10)))
        surface.blit(sh, (x - sz(20), y + sz(48) - sz(96)))
        pygame.draw.rect(surface, self._color,
                         (x - sz(14), y - sz(91), sz(28), sz(26)))
        pygame.draw.circle(surface, self._color, (x, y - sz(80)), sz(14))
        if self._highlight:
            self._draw_highlight(surface, x, y)

    def interact(self) -> str:
        return ""


# ─────────────────────────────────────────────────────────────
# PLAYER — Arga  (dengan sistem animasi multi-frame)
# ─────────────────────────────────────────────────────────────
class Player(Character, BattleEntity):
    """
    [INHERITANCE] Mewarisi Character DAN BattleEntity.
    [ENCAPSULATION] __hp, __mp, __stats private.
    [POLYMORPHISM] use_skill() berbeda dari NPC/Boss.

    Hero utama: Arga
    Asset: assets/characters/heroes/arga/
    
    Sistem animasi:
    - before_isekai = True  → pakai set asset sebelum Holy Sword
    - before_isekai = False → pakai set asset setelah Holy Sword
    
    State animasi: "idle", "walk", "attack", "hurt", "dead", "defend"
    Arah: _facing_right (True = kanan, False = kiri, flip horizontal otomatis)
    """

    ANIM_SPEEDS = {
        "walk":   0.10,   # detik per frame (8 frame = ~0.8s per siklus)
        "idle":   0.50,   # idle lebih lambat, terasa natural
        "attack": 0.12,   # attack sedikit lebih lambat agar terlihat
        "hurt":   0.15,
        "dead":   0.20,
        "defend": 0.25,
    }

    SKILLS = {
        "Divine Slash":         {"dmg": 800,  "mp": 0,   "type": "physical", "desc": "Tebasan pedang suci"},
        "Celestial Flame":      {"dmg": 1200, "mp": 20,  "type": "magic",    "desc": "Api surgawi"},
        "Holy Barrier":         {"dmg": 0,    "mp": 30,  "type": "buff",     "desc": "Barrier suci"},
        "Time Acceleration":    {"dmg": 0,    "mp": 40,  "type": "buff",     "desc": "Percepat waktu"},
        "Absolute Regeneration":{"dmg": 0,    "mp": 50,  "type": "heal",     "desc": "Regenerasi total"},
        "LIMIT BREAK":          {"dmg": 9999, "mp": 100, "type": "ultimate", "desc": "CELESTIAL OVERDRIVE!!"},
    }

    def __init__(self, x: float, y: float):
        super().__init__("Arga", x, y, (70, 100, 180))
        self.__hp = 9999
        self.__max_hp = 9999
        self.__mp = 100
        self.__max_mp = 100
        self.__level = 99
        self.__stats = {"STR": 999, "MAG": 999, "DEF": 999, "SPD": 999}

        # === Sistem Animasi ===
        self.before_isekai = True      # True = sebelum Holy Sword, False = setelah
        self._anim_state  = "idle"    # state animasi saat ini
        self._frame_idx   = 0         # index frame saat ini
        self._frame_timer = 0.0       # timer untuk pergantian frame
        self._anim_timer  = 0.0       # timer global animasi
        self._bob_offset  = 0.0
        self._is_walking  = False     # True saat sedang bergerak
        self._anim_once   = False     # True jika animasi hanya sekali (attack/hurt)
        self._anim_done   = False     # sudah selesai untuk one-shot anim

    @property
    def hp(self): return self.__hp
    @property
    def max_hp(self): return self.__max_hp
    @property
    def mp(self): return self.__mp
    @property
    def max_mp(self): return self.__max_mp
    @property
    def level(self): return self.__level

    def get_stats(self) -> dict:
        return dict(self.__stats)

    # ── Kontrol animasi dari luar ──────────────────────────────

    def set_walking(self, moving: bool, direction_right: bool = None):
        """Panggil setiap frame jika karakter bergerak/berhenti."""
        self._is_walking = moving
        if direction_right is not None:
            if self._facing_right != direction_right:
                self._facing_right = direction_right
                # Reset frame saat ganti arah
                self._frame_idx = 0
                self._frame_timer = 0.0
        if moving:
            self._set_anim("walk")
        else:
            self._set_anim("idle")

    def play_attack(self):
        """Mulai animasi attack (sekali jalan)."""
        self._set_anim("attack", once=True)

    def play_hurt(self):
        """Mulai animasi hurt (sekali jalan)."""
        self._set_anim("hurt", once=True)

    def play_dead(self):
        """Mulai animasi dead."""
        self._set_anim("dead", once=True)

    def play_defend(self):
        """Mulai animasi defend."""
        self._set_anim("defend")

    def _set_anim(self, state: str, once: bool = False):
        """Ganti state animasi jika berbeda."""
        if self._anim_state == state and not once:
            return
        self._anim_state  = state
        self._frame_idx   = 0
        self._frame_timer = 0.0
        self._anim_once   = once
        self._anim_done   = False

    def _get_frames(self, assets) -> list:
        """Ambil list frame surface sesuai state & fase isekai."""
        if self.before_isekai:
            if self._anim_state == "walk":
                return assets.arga_walk_before_frames
            else:
                # Idle — gunakan frame side (tampak samping)
                return [assets.arga_idle_before_side]
        else:
            if self._anim_state == "walk":
                return assets.arga_walk_after_frames
            elif self._anim_state == "attack":
                return assets.arga_attack1_frames
            elif self._anim_state == "hurt":
                return assets.arga_hurt_frames
            elif self._anim_state == "dead":
                return assets.arga_dead_frames
            elif self._anim_state == "defend":
                return assets.arga_defend_frames
            else:
                # Idle after isekai — gunakan frame side (tampak samping)
                return [assets.arga_idle_after_side]

    def use_skill(self, skill_name: str, target) -> dict:
        """[POLYMORPHISM] Implementasi use_skill untuk Player (Arga)."""
        skill = self.SKILLS.get(skill_name, {})
        dmg = skill.get("dmg", 0)
        mp_cost = skill.get("mp", 0)
        if self.__mp < mp_cost:
            return {"success": False, "msg": "MP tidak cukup!"}
        self.__mp -= mp_cost
        actual = target.take_damage(dmg) if target and hasattr(target, "take_damage") else dmg
        return {"success": True, "damage": actual,
                "type": skill.get("type", "physical"), "msg": skill.get("desc", "")}

    def take_damage(self, amount: int) -> int:
        actual = max(1, amount // 100)
        self.__hp = max(0, self.__hp - actual)
        return actual

    def is_alive(self) -> bool:
        return self.__hp > 0

    def update(self, dt: float) -> None:
        """Update animasi frame-by-frame."""
        self._anim_timer += dt
        # Bob hanya saat idle
        if self._anim_state == "idle":
            self._bob_offset = math.sin(self._anim_timer * 2.5) * 3
        else:
            self._bob_offset = 0.0

        assets = _get_assets()
        if not assets:
            return

        frames = self._get_frames(assets)
        n = len(frames)
        if n == 0:
            return

        speed = self.ANIM_SPEEDS.get(self._anim_state, 0.12)
        self._frame_timer += dt
        if self._frame_timer >= speed:
            self._frame_timer -= speed
            if self._anim_once and self._frame_idx >= n - 1:
                # Animasi one-shot selesai
                self._anim_done = True
                # Kembali ke idle setelah selesai
                if self._anim_state in ("attack", "hurt"):
                    self._set_anim("idle")
            else:
                self._frame_idx = (self._frame_idx + 1) % n

    def draw(self, surface: pygame.Surface) -> None:
        """
        Gambar Arga dengan animasi multi-frame.
        - Flip horizontal jika _facing_right = False
        - Pakai set asset sesuai before_isekai
        - Aura biru tetap sebagai efek visual
        """
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        drawn = False

        if assets:
            frames = self._get_frames(assets)
            n = len(frames)
            if n > 0:
                idx = min(self._frame_idx, n - 1)
                sprite = frames[idx]

                # Flip jika menghadap kiri
                if not self._facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)

                _blit_centered(surface, sprite, x, y)
                drawn = True

        if not drawn:
            self._draw_body(surface, x, y)

        # Aura biru (efek visual, selalu tampil di atas sprite)
        aura = pygame.Surface((60, 80), pygame.SRCALPHA)
        alpha = int(abs(math.sin(self._anim_timer * 2)) * 30)
        pygame.draw.rect(aura, (100, 150, 255, alpha), (0, 0, 60, 80))
        surface.blit(aura, (x - 30, y - 78))

    def interact(self) -> str:
        return "player"


# ─────────────────────────────────────────────────────────────
# NPC
# ─────────────────────────────────────────────────────────────
class NPC(Character):
    """[INHERITANCE] NPC dasar dari Character."""

    def __init__(self, name: str, x: float, y: float, color: tuple):
        super().__init__(name, x, y, color)
        self._dialogue_index = 0

    def interact(self) -> str:
        """[POLYMORPHISM] Override berdasarkan jenis NPC."""
        if self.dialogue_count() == 0:
            return "..."
        line = self.get_dialogue(self._dialogue_index)
        self._dialogue_index = (self._dialogue_index + 1) % max(1, self.dialogue_count())
        return line


class TownNPC(NPC):
    """[INHERITANCE] NPC warga kota."""

    def __init__(self, name, x, y, color=None, role="citizen"):
        if color is None:
            color = random.choice([(180, 120, 80), (140, 100, 160),
                                   (100, 140, 100), (160, 130, 80)])
        super().__init__(name, x, y, color)
        self._role = role

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        drawn = False

        if assets:
            name_key = self._name.lower().replace(" ", "_")
            attr = f"char_npc_{name_key}"
            sprite = getattr(assets, attr, None)
            if sprite is None:
                sprite = assets.get_character(self._name, "normal", (80, 80))
            if sprite is not None:
                # Flip jika menghadap kiri
                if not self._facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                _blit_centered(surface, sprite, x, y)
                drawn = True

        if not drawn:
            self._draw_body(surface, x, y)

        self._draw_highlight(surface, x, y)

    def interact(self) -> str:
        return super().interact()


class PartyNPC(NPC, BattleEntity):
    """
    [INHERITANCE] Anggota party.
    [POLYMORPHISM] use_skill() unik per karakter.

    Karakter party: Elena (heroine), Lyra, Darius
    """

    PARTY_SKILLS = {
        "Elena":  {"skill": "Royal Heal",   "dmg": 0,   "heal": 500, "desc": "Sihir penyembuhan kerajaan"},
        "Lyra":   {"skill": "Arcane Burst", "dmg": 900, "heal": 0,   "desc": "Ledakan sihir murni"},
        "Darius": {"skill": "Iron Wall",    "dmg": 400, "heal": 0,   "desc": "Serangan dengan perisai baja"},
        "Luna":   {"skill": "Lunar Veil",   "dmg": 0,   "heal": 400, "desc": "Sihir bulan penyembuh"},
        "Kael":   {"skill": "Storm Blade",  "dmg": 0,   "heal": 0,   "desc": "Serangan petir (fake)"},
        "Aria":   {"skill": "Arcane Song",  "dmg": 0,   "heal": 0,   "desc": "Mantra penyemangat (fake)"},
        "Reno":   {"skill": "Wild Strike",  "dmg": 600, "heal": 0,   "desc": "Serangan liar penuh tenaga"},
    }

    COLORS = {
        "Elena":  (220, 180, 220),
        "Lyra":   (100, 140, 200),
        "Darius": (140, 130, 120),
        "Luna":   (180, 200, 240),
        "Kael":   (100, 160, 220),
        "Aria":   (220, 160, 200),
        "Reno":   (200, 120, 60),
    }

    def __init__(self, char_name: str, x: float, y: float):
        col = self.COLORS.get(char_name, (150, 150, 150))
        super().__init__(char_name, x, y, col)
        self.__hp = 5000
        self.__max_hp = 5000
        self._knocked_out = False

    @property
    def hp(self): return self.__hp
    @property
    def max_hp(self): return self.__max_hp
    @property
    def knocked_out(self): return self._knocked_out

    def use_skill(self, skill_name: str, target) -> dict:
        """[POLYMORPHISM] Party NPC hanya melakukan FAKE ATTACK."""
        data = self.PARTY_SKILLS.get(self._name, {})
        return {"damage": 0, "fake": True,
                "desc": data.get("desc", ""), "skill": data.get("skill", "")}

    def take_damage(self, amount: int) -> int:
        actual = min(self.__hp, amount)
        self.__hp -= actual
        if self.__hp <= 0:
            self._knocked_out = True
        return actual

    def is_alive(self) -> bool:
        return self.__hp > 0

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)

        if self._knocked_out:
            assets = _get_assets()
            drawn = False
            if assets:
                name_lower = self._name.lower()
                hurt = getattr(assets, f"char_{name_lower}_hurt", None)
                if hurt is None:
                    hurt = getattr(assets, f"char_{name_lower}_attack", None)
                if hurt:
                    rot = pygame.transform.rotate(hurt, 90)
                    rot = pygame.transform.scale(rot, (80, 40))
                    surface.blit(rot, (x - 40, y - 30))
                    drawn = True
            if not drawn:
                ko_s = pygame.Surface((70, 30), pygame.SRCALPHA)
                pygame.draw.ellipse(ko_s, self._color, (0, 0, 70, 30))
                surface.blit(ko_s, (x - 35, y - 20))
            try:
                font = pygame.font.SysFont("Georgia", 12)
                txt = font.render("KO", True, (255, 60, 60))
                surface.blit(txt, (x - txt.get_width() // 2, y - 40))
            except Exception:
                pass
            return

        assets = _get_assets()
        drawn = False
        if assets:
            name_lower = self._name.lower()
            sprite = getattr(assets, f"char_{name_lower}_idle", None)
            if sprite is None:
                sprite = assets.get_character(self._name, "idle", (96, 96))
            if sprite is not None:
                # Flip jika menghadap kiri
                if not self._facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                _blit_centered(surface, sprite, x, y)
                drawn = True

        if not drawn:
            self._draw_body(surface, x, y)

    def interact(self) -> str:
        return super().interact()


class BossNPC(NPC, BattleEntity):
    """
    [INHERITANCE] Boss karakter (Demon King).
    [POLYMORPHISM] use_skill() dan draw() berbeda dan jauh lebih kuat.
    """

    def __init__(self, x: float, y: float):
        super().__init__("Demon King", x, y, (60, 20, 80))
        self.__hp = 50000
        self.__max_hp = 50000
        self.__phase = 1
        self._anim_timer = 0.0

    @property
    def hp(self): return self.__hp
    @property
    def max_hp(self): return self.__max_hp
    @property
    def phase(self): return self.__phase

    def use_skill(self, skill_name: str, target) -> dict:
        """[POLYMORPHISM] Boss punya skill mematikan."""
        skills = {
            "Dark Slash":    {"dmg": 500,  "desc": "Tebasan kegelapan"},
            "Hellfire":      {"dmg": 800,  "desc": "Api neraka"},
            "Void Collapse": {"dmg": 2000, "desc": "Kehancuran mutlak"},
            "Death Embrace": {"dmg": 9999, "desc": "Pelukan kematian"},
        }
        data = skills.get(skill_name, {"dmg": 300, "desc": "Serangan gelap"})
        dmg = data["dmg"]
        if target and hasattr(target, "take_damage"):
            target.take_damage(dmg)
        return {"damage": dmg, "desc": data["desc"]}

    def take_damage(self, amount: int) -> int:
        actual = min(self.__hp, amount)
        self.__hp -= actual
        if self.__hp < self.__max_hp * 0.5:
            self.__phase = 2
        return actual

    def is_alive(self) -> bool:
        return self.__hp > 0

    def update(self, dt: float) -> None:
        self._anim_timer += dt
        self._bob_offset = math.sin(self._anim_timer * 1.5) * 5

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()

        for r in range(80, 20, -20):
            aura = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            alpha = int(40 * (1 - r / 80))
            pygame.draw.circle(aura, (80, 0, 120, alpha), (r, r), r)
            surface.blit(aura, (x - r, y - r + 20))

        drawn = False
        if assets and assets.char_demon_king_idle is not None:
            sprite = assets.char_demon_king_idle
            # Boss selalu menghadap kiri (ke arah player)
            if self._facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            _blit_centered(surface, sprite, x, y)
            drawn = True

        if not drawn:
            pygame.draw.polygon(surface, (30, 10, 40), [
                (x-40, y+80), (x+40, y+80), (x+55, y-10), (x, y-30), (x-55, y-10)
            ])
            pygame.draw.circle(surface, (50, 20, 60), (x, y - 30), 28)
            pygame.draw.polygon(surface, (80, 30, 30),
                                [(x-25, y-50), (x-15, y-80), (x-5, y-50)])
            pygame.draw.polygon(surface, (80, 30, 30),
                                [(x+5, y-50), (x+15, y-80), (x+25, y-50)])
            pygame.draw.circle(surface, (255, 30, 30), (x-10, y-32), 6)
            pygame.draw.circle(surface, (255, 30, 30), (x+10, y-32), 6)

        if self.__phase == 2:
            phase_aura = pygame.Surface((120, 120), pygame.SRCALPHA)
            t = abs(math.sin(self._anim_timer * 3))
            pygame.draw.circle(phase_aura, (200, 0, 50, int(40 * t)), (60, 60), 60)
            surface.blit(phase_aura, (x - 60, y - 60))

    def interact(self) -> str:
        return "Hahaha... coba saja!"


class MonsterNPC(NPC, BattleEntity):
    """
    [INHERITANCE] Monster biasa (Slime, Mushroom, dll).
    """

    _MONSTER_ASSET_MAP = {
        "slime":    "slime",
        "mushroom": "mushroom",
        "goblin":   "goblin",
    }

    def __init__(self, name: str, x: float, y: float, hp: int = 100):
        super().__init__(name, x, y, (80, 160, 80))
        self.__hp = hp
        self.__max_hp = hp

    @property
    def hp(self): return self.__hp
    @property
    def max_hp(self): return self.__max_hp

    def use_skill(self, skill_name: str, target) -> dict:
        dmg = 50
        if target and hasattr(target, "take_damage"):
            target.take_damage(dmg)
        return {"damage": dmg, "desc": "Serangan monster"}

    def take_damage(self, amount: int) -> int:
        actual = min(self.__hp, amount)
        self.__hp -= actual
        return actual

    def is_alive(self) -> bool:
        return self.__hp > 0

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        drawn = False

        if assets:
            name_lower = self._name.lower()
            monster_key = self._MONSTER_ASSET_MAP.get(name_lower, name_lower)
            sprite = getattr(assets, f"char_{monster_key}_idle", None)
            if sprite is not None:
                if not self._facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                _blit_centered(surface, sprite, x, y)
                drawn = True

        if not drawn:
            pygame.draw.ellipse(surface, (80, 200, 80),  (x-20, y-54, 40, 25))
            pygame.draw.ellipse(surface, (60, 180, 60),  (x-18, y-69, 36, 30))
            pygame.draw.circle(surface, (30, 120, 30), (x-7, y-61), 4)
            pygame.draw.circle(surface, (30, 120, 30), (x+7, y-61), 4)

        # HP bar
        hp_ratio = self.__hp / max(1, self.__max_hp)
        bar_w = 40
        bar_y = y - 80
        pygame.draw.rect(surface, (60, 0, 0),    (x - bar_w//2, bar_y, bar_w, 6))
        pygame.draw.rect(surface, (50, 200, 50), (x - bar_w//2, bar_y, int(bar_w * hp_ratio), 6))

    def interact(self) -> str:
        name_lower = self._name.lower()
        reactions = {
            "slime":    "*Slime bergerak mengancam*",
            "mushroom": "*Mushroom mengeluarkan spora berbahaya*",
            "goblin":   "*Goblin mengancam dengan tombaknya*",
        }
        return reactions.get(name_lower, f"*{self._name} bersiap menyerang*")
