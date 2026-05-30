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
        """
        Coba load sprite dari AssetManager.
        Urutan prioritas:
          1. assets/characters/heroes/<name_lower>/<state>.png  (via get_character)
          2. Fallback sprite primitif (_draw_body)
        """
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
        # Bayangan
        sh = pygame.Surface((sz(40), sz(10)), pygame.SRCALPHA)
        pygame.draw.ellipse(sh, (0, 0, 0, 60), (0, 0, sz(40), sz(10)))
        surface.blit(sh, (x - sz(20), y + sz(48) - sz(96)))
        # Tubuh sederhana
        pygame.draw.rect(surface, self._color,
                         (x - sz(14), y - sz(91), sz(28), sz(26)))
        pygame.draw.circle(surface, self._color, (x, y - sz(80)), sz(14))
        if self._highlight:
            self._draw_highlight(surface, x, y)

    def interact(self) -> str:
        return ""


# ─────────────────────────────────────────────────────────────
# PLAYER — Arga
# ─────────────────────────────────────────────────────────────
class Player(Character, BattleEntity):
    """
    [INHERITANCE] Mewarisi Character DAN BattleEntity.
    [ENCAPSULATION] __hp, __mp, __stats private.
    [POLYMORPHISM] use_skill() berbeda dari NPC/Boss.

    Hero utama: Arga
    Asset: assets/characters/heroes/arga/
    """

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

    def draw(self, surface: pygame.Surface) -> None:
        """
        Gambar Arga (hero) menggunakan asset dari:
          assets/characters/heroes/arga/arga_idle.png
          (atau arga_idle.png, idle.png, dll — fallback berlapis)
        Aura biru tetap digambar di atas sprite sebagai efek visual.
        """
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        drawn = False

        if assets:
            # Prioritas 1: char_arga_idle
            sprite = assets.char_arga_idle
            # Prioritas 2: char_hero_idle (alias)
            if sprite is None:
                sprite = assets.char_hero_idle
            # Prioritas 3: char_player_idle (alias)
            if sprite is None:
                sprite = assets.char_player_idle

            if sprite is not None:
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
        """
        Gambar NPC kota.
        Coba load dari assets/characters/npc/<name_lower>.png
        atau assets/characters/npc/<name_lower>/ folder.
        """
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        drawn = False

        if assets:
            # Coba properti npc yang sudah diload (king, merchant, guard, village_elder)
            name_key = self._name.lower().replace(" ", "_")
            attr = f"char_npc_{name_key}"
            sprite = getattr(assets, attr, None)
            # Fallback: get_character generic
            if sprite is None:
                sprite = assets.get_character(self._name, "normal", (80, 80))
            if sprite is not None:
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
    Asset folder:
      Elena  → assets/characters/heroes/elena/
      Lyra   → assets/characters/heroes/lyra/
      Darius → assets/characters/heroes/darius/
    """

    PARTY_SKILLS = {
        # Party utama
        "Elena":  {"skill": "Royal Heal",   "dmg": 0,   "heal": 500, "desc": "Sihir penyembuhan kerajaan"},
        "Lyra":   {"skill": "Arcane Burst", "dmg": 900, "heal": 0,   "desc": "Ledakan sihir murni"},
        "Darius": {"skill": "Iron Wall",    "dmg": 400, "heal": 0,   "desc": "Serangan dengan perisai baja"},
        # Legacy (alias lama jika masih ada di dialog)
        "Luna":   {"skill": "Lunar Veil",   "dmg": 0,   "heal": 400, "desc": "Sihir bulan penyembuh"},
        "Kael":   {"skill": "Storm Blade",  "dmg": 0,   "heal": 0,   "desc": "Serangan petir (fake)"},
        "Aria":   {"skill": "Arcane Song",  "dmg": 0,   "heal": 0,   "desc": "Mantra penyemangat (fake)"},
        "Reno":   {"skill": "Wild Strike",  "dmg": 600, "heal": 0,   "desc": "Serangan liar penuh tenaga"},
    }

    COLORS = {
        "Elena":  (220, 180, 220),
        "Lyra":   (100, 140, 200),
        "Darius": (140, 130, 120),
        # Legacy
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
        """
        [POLYMORPHISM] Party NPC hanya melakukan FAKE ATTACK.
        Tidak ada real damage — hanya efek visual.
        """
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
        """
        Gambar companion/party member dari asset folder heroes/.
        Mapping:
          Elena  → assets/characters/heroes/elena/elena_idle.png
          Lyra   → assets/characters/heroes/lyra/lyra_idle.png
          Darius → assets/characters/heroes/darius/darius_idle.png
        Jika KO, tampilkan sprite hurt/dead jika tersedia.
        """
        x = int(self._x)
        y = int(self._y + self._bob_offset)

        if self._knocked_out:
            assets = _get_assets()
            drawn = False
            if assets:
                name_lower = self._name.lower()
                # Coba sprite hurt dari folder heroes
                hurt = getattr(assets, f"char_{name_lower}_hurt", None)
                if hurt is None:
                    hurt = getattr(assets, f"char_{name_lower}_attack", None)
                if hurt:
                    # Tampilkan miring sebagai KO
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
            # Coba atribut char_<name>_idle langsung
            sprite = getattr(assets, f"char_{name_lower}_idle", None)
            # Fallback: get_character generic (covers alias mapping)
            if sprite is None:
                sprite = assets.get_character(self._name, "idle", (96, 96))
            if sprite is not None:
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

    Asset: assets/characters/enemies/demon_king/
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
        """
        Gambar Demon King dari assets/characters/enemies/demon_king/.
        Overlay aura kegelapan & mata merah tetap digambar sebagai efek visual.
        Jika asset belum ada, fallback ke gambar primitif.
        """
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()

        # ── Aura kegelapan (efek, selalu tampil) ──────────────
        for r in range(80, 20, -20):
            aura = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            alpha = int(40 * (1 - r / 80))
            pygame.draw.circle(aura, (80, 0, 120, alpha), (r, r), r)
            surface.blit(aura, (x - r, y - r + 20))

        # ── Sprite boss ────────────────────────────────────────
        drawn = False
        if assets and assets.char_demon_king_idle is not None:
            sprite = assets.char_demon_king_idle
            _blit_centered(surface, sprite, x, y)
            drawn = True

        if not drawn:
            # Fallback primitif boss
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

        # Phase 2 aura merah
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
    Asset:
      Slime    → assets/characters/enemies/slime/
      Mushroom → assets/characters/enemies/mushroom/
    """

    # Mapping nama monster → nama atribut di assets
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
        """
        Gambar monster dari assets/characters/enemies/<name_lower>/.
        HP bar selalu digambar di atas sprite.
        """
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        drawn = False

        if assets:
            name_lower = self._name.lower()
            monster_key = self._MONSTER_ASSET_MAP.get(name_lower, name_lower)
            # Coba atribut char_<monster>_idle
            sprite = getattr(assets, f"char_{monster_key}_idle", None)
            if sprite is not None:
                _blit_centered(surface, sprite, x, y)
                drawn = True

        if not drawn:
            # Fallback monster primitif (slime-like)
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
