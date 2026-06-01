"""
ui/components.py
================
Komponen UI: DialogueBox, HUD, TransitionScreen, StatusWindow, BattleUI.
"""

import pygame
import math
from engine.colors import *


class DialogueBox:
    """
    Kotak dialog gaya visual novel dengan typewriter effect.
    Mendukung nama karakter, pilihan, dan portrait indicator.
    """

    def __init__(self, W: int, H: int):
        self.W = W
        self.H = H
        self.box_h = 165
        self.box_y = H - self.box_h - 12
        self.padding = 22

        self._text = ""
        self._displayed = ""
        self._display_index = 0
        self._type_timer = 0.0
        self._type_speed = 0.025
        self._finished = False
        self._speaker = ""
        self._choices: list[str] = []
        self._choice_index = 0
        self._show_choices = False
        self.visible = False
        self._blink = 0.0

        try:
            self.font_text   = pygame.font.SysFont("Georgia", 20)
            self.font_name   = pygame.font.SysFont("Georgia", 18, bold=True)
            self.font_choice = pygame.font.SysFont("Georgia", 18)
            self.font_hint   = pygame.font.SysFont("Consolas", 13)
        except Exception:
            self.font_text   = pygame.font.Font(None, 22)
            self.font_name   = pygame.font.Font(None, 22)
            self.font_choice = pygame.font.Font(None, 22)
            self.font_hint   = pygame.font.Font(None, 18)

    def show(self, text: str, speaker: str = "", choices: list[str] = None):
        self._text = text
        self._speaker = speaker
        self._displayed = ""
        self._display_index = 0
        self._type_timer = 0.0
        self._finished = False
        self._choices = choices or []
        self._choice_index = 0
        self._show_choices = False
        self.visible = True

    def hide(self):
        self.visible = False
        self._choices = []
        self._show_choices = False

    def skip(self):
        if not self._finished:
            self._displayed = self._text
            self._display_index = len(self._text)
            self._finished = True
        elif self._choices:
            self._show_choices = True

    @property
    def is_finished(self) -> bool:
        return self._finished

    @property
    def selected_choice(self) -> int:
        return self._choice_index

    @property
    def showing_choices(self) -> bool:
        return self._show_choices

    def navigate_choice(self, direction: int):
        if self._show_choices and self._choices:
            self._choice_index = (self._choice_index + direction) % len(self._choices)

    def confirm_choice(self) -> int:
        return self._choice_index

    def update(self, dt: float):
        self._blink += dt
        if not self._finished and self._display_index < len(self._text):
            self._type_timer += dt
            while self._type_timer >= self._type_speed and self._display_index < len(self._text):
                self._type_timer -= self._type_speed
                self._displayed += self._text[self._display_index]
                self._display_index += 1
            if self._display_index >= len(self._text):
                self._finished = True
                if self._choices:
                    self._show_choices = True

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return

        # Kotak utama
        box_surf = pygame.Surface((self.W - 40, self.box_h), pygame.SRCALPHA)
        pygame.draw.rect(box_surf, (10, 8, 22, 220), (0, 0, self.W-40, self.box_h), border_radius=8)
        pygame.draw.rect(box_surf, UI_BORDER, (0, 0, self.W-40, self.box_h), 2, border_radius=8)
        surface.blit(box_surf, (20, self.box_y))

        # Nama karakter
        if self._speaker:
            name_surf = self.font_name.render(self._speaker, True, UI_ACCENT)
            name_bg = pygame.Surface((name_surf.get_width()+20, 26), pygame.SRCALPHA)
            pygame.draw.rect(name_bg, (40, 20, 80, 200), (0,0,name_surf.get_width()+20,26), border_radius=4)
            pygame.draw.rect(name_bg, UI_BORDER, (0,0,name_surf.get_width()+20,26), 1, border_radius=4)
            surface.blit(name_bg, (30, self.box_y-22))
            surface.blit(name_surf, (40, self.box_y-19))

        # Teks dengan word wrap
        if not self._show_choices:
            self._draw_wrapped(surface, self._displayed, 40, self.box_y + 18, self.W - 80, UI_TEXT)
            # Indikator lanjut
            if self._finished and not self._choices:
                blink_alpha = int(128 + 127 * math.sin(self._blink * 4))
                try:
                    hint = self._render_alpha("▼ [SPACE/ENTER]", self.font_hint, UI_DIMTEXT, blink_alpha)
                    surface.blit(hint, (self.W - 160, self.box_y + self.box_h - 24))
                except Exception:
                    pass
        else:
            # Tampilkan pilihan
            y_offset = self.box_y + 15
            for i, choice in enumerate(self._choices):
                selected = (i == self._choice_index)
                col = UI_ACCENT if selected else UI_TEXT
                prefix = "► " if selected else "  "
                txt = self.font_choice.render(prefix + choice, True, col)
                if selected:
                    hl = pygame.Surface((txt.get_width()+10, 26), pygame.SRCALPHA)
                    pygame.draw.rect(hl, (100, 80, 200, 80), (0,0,txt.get_width()+10,26), border_radius=3)
                    surface.blit(hl, (35, y_offset-2))
                surface.blit(txt, (40, y_offset))
                y_offset += 32

    def _draw_wrapped(self, surface, text, x, y, max_w, color, line_height=26):
        words = text.split(' ')
        line = ""
        cur_y = y
        for word in words:
            test = (line + " " + word).strip()
            if self.font_text.size(test)[0] > max_w:
                if line:
                    surface.blit(self.font_text.render(line, True, color), (x, cur_y))
                    cur_y += line_height
                    if cur_y > self.box_y + self.box_h - 30:
                        return
                line = word
            else:
                line = test
        if line:
            surface.blit(self.font_text.render(line, True, color), (x, cur_y))

    def _render_alpha(self, text, font, color, alpha):
        s = font.render(text, True, color)
        s.set_alpha(alpha)
        return s


class StatusWindow:
    """Window stat permanen Arga setelah menerima Holy Sword.
    Data paten — tidak berubah mengikuti kondisi battle.
    Dibuka/tutup dengan TAB, hanya aktif di Chapter 1 setelah sword_taken.
    """

    ARGA_STATS = {
        "title":  "The Chosen One",
        "age":    17,
        "level":  99,
        "hp":     9999,
        "max_hp": 9999,
        "mp":     100,
        "max_mp": 100,
        "str":    999,
        "mag":    999,
        "def_":   999,
        "spd":    999,
        "weapon": "Holy Sword",
    }

    def __init__(self, W: int, H: int):
        self.W = W
        self.H = H
        self.visible = False
        self._anim = 0.0
        try:
            self.font_title = pygame.font.SysFont("Georgia", 20, bold=True)
            self.font_label = pygame.font.SysFont("Georgia", 15)
            self.font_value = pygame.font.SysFont("Consolas", 15, bold=True)
            self.font_hint  = pygame.font.SysFont("Consolas", 12)
        except Exception:
            self.font_title = pygame.font.Font(None, 22)
            self.font_label = pygame.font.Font(None, 18)
            self.font_value = pygame.font.Font(None, 18)
            self.font_hint  = pygame.font.Font(None, 16)

    def update(self, dt: float):
        self._anim += dt

    def draw(self, surface: pygame.Surface, player=None):
        # parameter 'player' diabaikan — pakai data paten
        if not self.visible:
            return

        s = self.ARGA_STATS
        pw, ph = 300, 370
        px = (self.W - pw) // 2
        py = (self.H - ph) // 2

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(panel, (8, 6, 20, 235), (0, 0, pw, ph), border_radius=10)
        pygame.draw.rect(panel, (124, 92, 191), (0, 0, pw, ph), 2, border_radius=10)

        # Header
        pygame.draw.rect(panel, (50, 20, 100, 100), (0, 0, pw, 40), border_radius=10)
        title = self.font_title.render("【 STATUS 】", True, (200, 160, 255))
        panel.blit(title, (pw // 2 - title.get_width() // 2, 10))

        # Nama & title
        y = 52
        name_surf = self.font_label.render(f"Arga  —  {s['title']}", True, (232, 216, 255))
        panel.blit(name_surf, (20, y))
        y += 20

        # Badge Holy Sword
        badge = self.font_hint.render("+ Holy Sword equipped", True, (200, 160, 255))
        badge_w = badge.get_width() + 12
        badge_bg = pygame.Surface((badge_w, 18), pygame.SRCALPHA)
        pygame.draw.rect(badge_bg, (80, 40, 160, 100), (0, 0, badge_w, 18), border_radius=4)
        pygame.draw.rect(badge_bg, (90, 58, 154), (0, 0, badge_w, 18), 1, border_radius=4)
        panel.blit(badge_bg, (20, y))
        panel.blit(badge, (26, y + 1))
        y += 26

        # HP & MP bar
        self._draw_bar(panel, "HP", s["hp"], s["max_hp"], 20, y, 260, (220, 80, 80))
        y += 36
        self._draw_bar(panel, "MP", s["mp"], s["max_mp"], 20, y, 260, (64, 128, 224))
        y += 38

        pygame.draw.line(panel, (42, 24, 80), (20, y), (pw - 20, y), 1)
        y += 10

        # Stat rows
        rows = [
            ("Level",           str(s["level"]),  (255, 208, 96)),
            ("Umur (Age)",      str(s["age"]),    (224, 208, 255)),
            ("STR  ",           str(s["str"]),    (255, 208, 96)),
            ("MAG  ",           str(s["mag"]),    (96, 176, 255)),
            ("DEF  ",           str(s["def_"]),   (96, 224, 160)),
            ("SPD  ",           str(s["spd"]),    (224, 208, 255)),
        ]
        for label, value, color in rows:
            lbl = self.font_label.render(label, True, (136, 120, 170))
            val = self.font_value.render(value, True, color)
            panel.blit(lbl, (20, y))
            panel.blit(val, (pw - 20 - val.get_width(), y))
            y += 22

        pygame.draw.line(panel, (42, 24, 80), (20, y), (pw - 20, y), 1)
        y += 10

        # Weapon
        lbl = self.font_label.render("Weapon", True, (136, 120, 170))
        val = self.font_value.render(s["weapon"], True, (255, 208, 96))
        panel.blit(lbl, (20, y))
        panel.blit(val, (pw - 20 - val.get_width(), y))

        # Hint
        pygame.draw.line(panel, (42, 24, 80), (20, ph - 30), (pw - 20, ph - 30), 1)
        hint = self.font_hint.render("[ TAB ]  buka / tutup", True, (74, 56, 112))
        panel.blit(hint, (pw // 2 - hint.get_width() // 2, ph - 22))

        surface.blit(panel, (px, py))

    def _draw_bar(self, surf, label, val, maxv, x, y, w, col):
        lbl = self.font_label.render(f"{label}  {val} / {maxv}", True, (136, 120, 170))
        surf.blit(lbl, (x, y))
        pygame.draw.rect(surf, (26, 16, 48), (x, y + 18, w, 10), border_radius=4)
        pygame.draw.rect(surf, col,           (x, y + 18, w, 10), border_radius=4)

class BattleUI:
    """UI untuk scene pertarungan."""

    def __init__(self, W, H):
        self.W = W
        self.H = H
        self._anim = 0.0
        try:
            self.font_skill = pygame.font.SysFont("Georgia", 17)
            self.font_info  = pygame.font.SysFont("Consolas", 15)
            self.font_large = pygame.font.SysFont("Georgia", 28, bold=True)
        except Exception:
            self.font_skill = pygame.font.Font(None, 20)
            self.font_info  = pygame.font.Font(None, 18)
            self.font_large = pygame.font.Font(None, 32)

    def update(self, dt):
        self._anim += dt

    def draw_enemy_bar(self, surface, enemy):
        ratio = enemy.hp / max(1, enemy.max_hp)
        bar_w = 300
        bx, by = self.W//2 - bar_w//2, 20
        # Background
        panel = pygame.Surface((bar_w+20, 50), pygame.SRCALPHA)
        pygame.draw.rect(panel,(8,6,20,180),(0,0,bar_w+20,50), border_radius=6)
        surface.blit(panel,(bx-10, by-5))
        # Nama
        name_txt = self.font_info.render(enemy.name, True, UI_ACCENT)
        surface.blit(name_txt,(bx, by))
        # HP bar
        pygame.draw.rect(surface,(40,0,0),(bx, by+18, bar_w, 14), border_radius=3)
        bar_col = HP_BAR if ratio > 0.4 else HP_BAR_LOW
        pygame.draw.rect(surface, bar_col,(bx, by+18, int(bar_w*ratio), 14), border_radius=3)
        hp_txt = self.font_info.render(f"{enemy.hp}/{enemy.max_hp}", True, UI_TEXT)
        surface.blit(hp_txt,(bx+bar_w+5, by+16))

    def draw_player_hud(self, surface, player):
        # HUD kiri bawah
        hx, hy = 20, self.H - 80
        panel = pygame.Surface((260,70),pygame.SRCALPHA)
        pygame.draw.rect(panel,(8,6,20,200),(0,0,260,70), border_radius=6)
        pygame.draw.rect(panel, UI_BORDER,(0,0,260,70),2, border_radius=6)
        surface.blit(panel,(hx-4,hy-4))
        # HP
        hp_ratio = player.hp/max(1,player.max_hp)
        pygame.draw.rect(surface,(40,0,0),(hx,hy,200,12),border_radius=3)
        pygame.draw.rect(surface,HP_BAR,(hx,hy,int(200*hp_ratio),12),border_radius=3)
        hp_lbl = self.font_info.render(f"HP {player.hp}/{player.max_hp}",True,UI_TEXT)
        surface.blit(hp_lbl,(hx+205,hy))
        # MP
        mp_ratio = player.mp/max(1,player.max_mp)
        pygame.draw.rect(surface,(0,0,40),(hx,hy+18,200,12),border_radius=3)
        pygame.draw.rect(surface,MP_BAR,(hx,hy+18,int(200*mp_ratio),12),border_radius=3)
        mp_lbl = self.font_info.render(f"MP {player.mp}/{player.max_mp}",True,UI_TEXT)
        surface.blit(mp_lbl,(hx+205,hy+18))

    def draw_big_text(self, surface, text, color, alpha=255):
        txt = self.font_large.render(text, True, color)
        s = txt.copy()
        s.set_alpha(alpha)
        surface.blit(s,(self.W//2-s.get_width()//2, self.H//2-60))


class TransitionScreen:
    """Efek transisi fade in/out dan flash."""

    def __init__(self, W, H):
        self.W = W
        self.H = H
        self._alpha = 0
        self._target = 0
        self._speed = 300
        self._color = (0,0,0)
        self._surf = pygame.Surface((W,H))

    def fade_out(self, color=(0,0,0), speed=300):
        self._color = color
        self._alpha = 0
        self._target = 255
        self._speed = speed

    def fade_in(self, color=(0,0,0), speed=300):
        self._color = color
        self._alpha = 255
        self._target = 0
        self._speed = speed

    def flash(self, color=(255,255,255)):
        self._color = color
        self._alpha = 255
        self._target = 0
        self._speed = 600

    @property
    def done(self) -> bool:
        return self._alpha == self._target

    @property
    def alpha(self) -> int:
        return self._alpha

    def update(self, dt):
        if self._alpha < self._target:
            self._alpha = min(self._target, self._alpha + int(self._speed*dt))
        elif self._alpha > self._target:
            self._alpha = max(self._target, self._alpha - int(self._speed*dt))

    def draw(self, surface):
        if self._alpha <= 0:
            return
        self._surf.fill(self._color)
        self._surf.set_alpha(self._alpha)
        surface.blit(self._surf, (0,0))


class FloatingText:
    """Teks mengambang untuk damage/heal indicator."""

    def __init__(self, text, x, y, color=DAMAGE_RED, speed=60, lifetime=1.5):
        self._text = text
        self._x = float(x)
        self._y = float(y)
        self._color = color
        self._speed = speed
        self._lifetime = lifetime
        self._timer = 0.0
        self._alive = True
        try:
            self._font = pygame.font.SysFont("Georgia", 22, bold=True)
        except Exception:
            self._font = pygame.font.Font(None, 26)

    @property
    def alive(self):
        return self._alive

    def update(self, dt):
        self._timer += dt
        self._y -= self._speed * dt
        if self._timer >= self._lifetime:
            self._alive = False

    def draw(self, surface):
        alpha = int(255 * (1 - self._timer/self._lifetime))
        txt = self._font.render(self._text, True, self._color)
        txt.set_alpha(alpha)
        surface.blit(txt,(int(self._x)-txt.get_width()//2, int(self._y)))


class NarratorBox:
    """Kotak narasi di tengah layar."""

    def __init__(self, W, H):
        self.W = W
        self.H = H
        self._lines: list[str] = []
        self._timer = 0.0
        self._duration = 3.0
        self.visible = False
        try:
            self._font = pygame.font.SysFont("Georgia", 20, italic=True)
        except Exception:
            self._font = pygame.font.Font(None, 22)

    def show(self, lines: list[str], duration: float = 3.0):
        self._lines = lines
        self._timer = 0.0
        self._duration = duration
        self.visible = True

    def update(self, dt):
        if not self.visible:
            return
        self._timer += dt
        if self._timer >= self._duration:
            self.visible = False

    def draw(self, surface):
        if not self.visible:
            return
        alpha = 255
        if self._timer < 0.5:
            alpha = int(255 * self._timer / 0.5)
        elif self._timer > self._duration - 0.5:
            alpha = int(255 * (self._duration - self._timer) / 0.5)
        total_h = len(self._lines) * 30 + 20
        panel = pygame.Surface((self.W - 200, total_h), pygame.SRCALPHA)
        pygame.draw.rect(panel,(0,0,0,120),(0,0,self.W-200,total_h), border_radius=6)
        surface.blit(panel,(100, self.H//2 - total_h//2))
        for i, line in enumerate(self._lines):
            txt = self._font.render(line, True, (230, 220, 200))
            txt.set_alpha(alpha)
            surface.blit(txt,(self.W//2-txt.get_width()//2, self.H//2-total_h//2+10+i*30))

class PartyHUD:
    """HUD party pojok kiri atas — nama putih + HP bar hijau."""

    def __init__(self):
        try:
            self._font = pygame.font.SysFont("Georgia", 13)
        except Exception:
            self._font = pygame.font.Font(None, 15)

    def draw(self, surface, members):
        """
        members = list of tuple: [("Arga", hp, max_hp), ("Elena", hp, max_hp), ...]
        """
        for i, (name, hp, max_hp) in enumerate(members):
            px, py = 10, 10 + i * 44
            panel = pygame.Surface((165, 38), pygame.SRCALPHA)
            pygame.draw.rect(panel, (8, 6, 20, 180), (0, 0, 165, 38), border_radius=5)
            pygame.draw.rect(panel, UI_BORDER, (0, 0, 165, 38), 1, border_radius=5)
            surface.blit(panel, (px, py))
            nm = self._font.render(name, True, (255, 255, 255))
            surface.blit(nm, (px + 6, py + 4))
            pygame.draw.rect(surface, (30, 20, 30), (px + 6, py + 22, 135, 9), border_radius=3)
            ratio = max(0, hp / max(1, max_hp))
            pygame.draw.rect(surface, (60, 200, 80),
                             (px + 6, py + 22, int(135 * ratio), 9), border_radius=3)