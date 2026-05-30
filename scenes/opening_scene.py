"""
scenes/opening_scene.py
=======================
Opening Cutscene: Jalan kota, hujan, Arga dipanggil ke dunia lain.
[INHERITANCE] Mewarisi Scene (ABC).
"""

import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox
from entities.characters import Player


class OpeningScene(Scene):
    """Opening cinematic sebelum Chapter 1."""

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
        self._phase = "title"  # title → narration → walk → flash → throne
        self._phase_timer = 0.0
        self._dialogue = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator = NarratorBox(game.W, game.H)
        self._rain_drops = self._gen_rain()
        self._magic_circles = []
        self._dialogue_step = 0

        # ── Karakter Arga dengan animasi ──
        ground_y = int(game.H * 0.65)
        self._player = Player(200.0, float(ground_y))
        self._player.before_isekai = True           # masih di dunia asli, belum dapat Holy Sword
        self._player_target_x = 450.0
        self._player_walk_dir = True                # True = jalan ke kanan
        self._player_walk_speed = 60.0              # diperlambat agar terasa natural

        self._title_alpha = 0
        self._subtitle_alpha = 0
        self._stars = self._gen_stars()
        self._input_ready = False
        self._press_hint_timer = 0.0

        try:
            self._font_title  = pygame.font.SysFont("Georgia", 58, bold=True)
            self._font_sub    = pygame.font.SysFont("Georgia", 22, italic=True)
            self._font_hint   = pygame.font.SysFont("Consolas", 14)
            self._font_narr   = pygame.font.SysFont("Georgia", 20, italic=True)
        except Exception:
            self._font_title  = pygame.font.Font(None, 62)
            self._font_sub    = pygame.font.Font(None, 26)
            self._font_hint   = pygame.font.Font(None, 18)
            self._font_narr   = pygame.font.Font(None, 22)

        self._dialogue_data = [
           ("Arga", "Hahhh..."),
            ("Arga", "Hidup kok gini amat yah.."),
            ("Arga", "Bangun..nugas..kuliah..kerja..makan..terus tidur lagi.."),
            ("Arga", "Bosenin banget dah.."),
            ("Arga", "Aduh mana hujan, ga bawa payung lagi.."),
            ("Arga", "Tugas juga pada numpuk...mana besok udah masuk kuliah lagi..."),
            ("Arga", "Belum juga tagihan ukt yang harus dibayar.."),
            ("Arga", "hahh...Hidup capek juga yah..."),
            ("Arga", "Apa mending bundir aja kali yah..."),
            ("Arga", "Ughh jangan deh takut.."),
        ]
        self._post_flash_data = [
            ("Arga", "Hah...?"),
            ("Arga", "Tunggu— APA INI?!"),
        ]

    def _gen_rain(self):
        drops = []
        for _ in range(120):
            drops.append({
                'x': random.randint(0, 960),
                'y': random.randint(0, 540),
                'speed': random.uniform(300, 500),
                'length': random.randint(8, 18),
            })
        return drops

    def _gen_stars(self):
        random.seed(77)
        return [{'x':random.randint(0,960),'y':random.randint(0,340),
                 'size':random.choice([1,1,2]),'phase':random.uniform(0,6)} for _ in range(120)]

    def on_enter(self) -> None:
        self._transition.fade_in(speed=180)

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self._input_ready:
            return
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                self._advance()
            elif key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                if self._dialogue.showing_choices:
                    self._dialogue.navigate_choice(1 if key in (pygame.K_DOWN, pygame.K_s) else -1)

    def _advance(self):
        if self._phase == "title":
            self._phase = "narration"
            self._phase_timer = 0.0
            self._narrator.show([
                "Di dunia yang berbeda...",
                "seorang pahlawan sedang dipanggil."
            ], 3.5)
        elif self._phase == "narration":
            if not self._dialogue.is_finished:
                self._dialogue.skip()
            else:
                self._dialogue_step += 1
                if self._dialogue_step < len(self._dialogue_data):
                    spk, txt = self._dialogue_data[self._dialogue_step]
                    self._dialogue.show(txt, spk)
                    self._game.assets.play("cursor")
                else:
                    # Mulai efek magic circle
                    self._phase = "magic"
                    self._phase_timer = 0.0
                    self._dialogue.hide()
        elif self._phase == "magic":
            if not self._dialogue.is_finished:
                self._dialogue.skip()
            else:
                self._dialogue_step += 1
                if self._dialogue_step - len(self._dialogue_data) < len(self._post_flash_data):
                    idx = self._dialogue_step - len(self._dialogue_data)
                    spk, txt = self._post_flash_data[idx]
                    self._dialogue.show(txt, spk)
                else:
                    self._phase = "flash"
                    self._phase_timer = 0.0
                    self._transition.flash((255,255,255))
                    self._game.assets.play("flash")
        elif self._phase == "chapter1":
            self._go_to_chapter1()

    def _go_to_chapter1(self):
        from scenes.chapter1_scene import Chapter1Scene
        self._game.replace_scene(Chapter1Scene(self._game))

    def update(self, dt: float) -> None:
        self._t += dt
        self._phase_timer += dt
        self._transition.update(dt)
        self._narrator.update(dt)
        self._dialogue.update(dt)
        self._press_hint_timer += dt

        # Hujan
        for d in self._rain_drops:
            d['y'] += d['speed'] * dt
            d['x'] += d['speed'] * 0.2 * dt
            if d['y'] > 540:
                d['y'] = 0
                d['x'] = random.randint(0, 960)

        if self._phase == "title":
            self._title_alpha = min(255, self._title_alpha + 200*dt)
            self._subtitle_alpha = min(255, max(0, self._title_alpha - 100))
            if self._phase_timer > 1.0:
                self._input_ready = True
            self._player.set_walking(False)

        elif self._phase == "narration":
            self._input_ready = True
            if self._phase_timer < 0.1 and self._dialogue_step == 0:
                spk, txt = self._dialogue_data[0]
                self._dialogue.show(txt, spk)
            # Arga berjalan perlahan ke kanan (pakai speed yang sudah diperlambat)
            if self._player._x < self._player_target_x:
                self._player._x = min(self._player_target_x, self._player._x + self._player_walk_speed * dt)
                self._player.set_walking(True, True)    # jalan ke kanan
            else:
                self._player.set_walking(False)          # berhenti, hadap kanan

        elif self._phase == "magic":
            self._input_ready = True
            if self._phase_timer < 0.1 and not self._dialogue.visible:
                idx = self._dialogue_step - len(self._dialogue_data)
                if 0 <= idx < len(self._post_flash_data):
                    spk, txt = self._post_flash_data[idx]
                    self._dialogue.show(txt, spk)
            # Arga berhenti saat magic circle muncul
            self._player.set_walking(False)
            # Magic circle muncul
            if len(self._magic_circles) < 3 and self._phase_timer > 0.3:
                self._magic_circles.append({'r': 10, 'alpha': 200, 'angle': 0})

        elif self._phase == "flash":
            self._input_ready = False
            self._player.set_walking(False)
            if self._phase_timer > 1.2:
                self._phase = "chapter1"
                self._phase_timer = 0.0
                self._dialogue.show("Apa... tempat ini?", "Arga")
                self._input_ready = True

        elif self._phase == "chapter1":
            self._player.set_walking(False)

        # Update player animasi
        self._player.update(dt)

        # Update magic circles
        for mc in self._magic_circles:
            mc['r'] = min(100, mc['r'] + 40*dt)
            mc['angle'] += dt * 120

    def draw(self, surface: pygame.Surface) -> None:
        # Background kota malam
        surface.blit(self._game.assets.bg_night_city, (0, 0))

        if self._phase == "title":
            self._draw_title(surface)
        elif self._phase in ("narration", "magic", "flash", "chapter1"):
            self._draw_city_scene(surface)

        self._narrator.draw(surface)
        self._dialogue.draw(surface)
        self._transition.draw(surface)

        # Press hint
        if self._phase == "title" and self._input_ready:
            alpha = int(128 + 127 * math.sin(self._press_hint_timer * 3))
            try:
                hint = self._font_hint.render("[ Press any key to continue ]", True, UI_DIMTEXT)
                hint.set_alpha(alpha)
                surface.blit(hint, (self._game.W//2 - hint.get_width()//2, 480))
            except Exception:
                pass

    def _draw_title(self, surface):
        # Bintang
        for star in self._stars:
            tw = int(128+127*math.sin(self._t*star.get('speed', 1.0) if 'speed' in star else self._t+star['phase']))
            pygame.draw.circle(surface,(tw,tw,tw),(star['x'],star['y']),star['size'])

        # Judul game
        try:
            title_txt = self._font_title.render("Summoned To Another World", True, UI_ACCENT)
            title_txt.set_alpha(int(self._title_alpha))
            title2    = self._font_title.render("and Became A Hero", True, GOLD_LIGHT)
            title2.set_alpha(int(self._title_alpha))
            sub_txt   = self._font_sub.render("PROJEK AKHIR PBO", True, UI_DIMTEXT)
            sub_txt.set_alpha(int(self._subtitle_alpha))

            W, H = self._game.W, self._game.H
            surface.blit(title_txt, (W//2-title_txt.get_width()//2, H//2-90))
            surface.blit(title2,    (W//2-title2.get_width()//2, H//2-30))
            surface.blit(sub_txt,   (W//2-sub_txt.get_width()//2, H//2+50))

            if self._title_alpha > 200:
                pygame.draw.line(surface, UI_BORDER,
                                 (W//2-200, H//2+40),(W//2+200, H//2+40), 1)
        except Exception:
            pass

    def _draw_city_scene(self, surface):
        # Hujan
        for d in self._rain_drops:
            end_x = int(d['x'] + d['length']*0.3)
            end_y = int(d['y'] + d['length'])
            pygame.draw.line(surface, (150,180,220,100), (int(d['x']),int(d['y'])),(end_x,end_y),1)

        # Karakter Arga (animasi multi-frame)
        self._player.draw(surface)

        # Magic circles
        px = int(self._player._x)
        ground_y = int(self._game.H * 0.65)
        for mc in self._magic_circles:
            cx, cy = px, ground_y - 5
            s = pygame.Surface((int(mc['r'])*2+4, int(mc['r'])*2+4), pygame.SRCALPHA)
            pygame.draw.circle(s, (100,150,255,int(mc['alpha'])),
                               (int(mc['r'])+2,int(mc['r'])+2), int(mc['r']), 2)
            for i in range(6):
                angle = i*60*math.pi/180 + mc['angle']*math.pi/180
                x2 = int(mc['r']+2 + math.cos(angle)*mc['r'])
                y2 = int(mc['r']+2 + math.sin(angle)*mc['r']*0.5)
                pygame.draw.line(s,(80,120,255,80),(int(mc['r'])+2,int(mc['r'])+2),(x2,y2),1)
            surface.blit(s,(cx-int(mc['r'])-2, cy-int(mc['r'])-2))
