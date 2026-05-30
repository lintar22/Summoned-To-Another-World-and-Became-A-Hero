"""
scenes/true_end_scene.py
========================
TRUE ENDING — Festival Kerajaan, Pernikahan Arga & Elena.
[INHERITANCE] Scene(ABC).
"""

import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox


class TrueEndScene(Scene):

    DLGS = [
        ("Citizen",    "Hidup sang pahlawan! Hidup Astravia!"),
        ("Child",      "Kak Arga keren banget! Kak Elena cantik!"),
        ("Reno",       "Hahahaha!! Kita menang!! Aku tahu kita bisa!"),
        ("Lyra",       "...Selamat. Kau layak mendapatkannya."),
        ("Darius",     "Dunia aman kini. Tugas kita selesai."),
        ("King Aldric","Dengan ini, aku meresmikan pernikahan Arga dan Elena."),
        ("Elena",      "Hehe... akhirnya ya."),
        ("Arga",       "Iya."),
        ("Elena",      "Menyesal dipanggil ke dunia ini?"),
        ("Arga",       "...Sama sekali nggak."),
        ("SYSTEM",     "✨ Mereka berciuman di bawah langit kembang api..."),
        ("SYSTEM",     "🌅 Matahari terbit di Astravia yang damai."),
    ]

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
        self._dlg_step = 0
        self._phase = "festival"  # festival → wedding → final
        self._dialogue = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator = NarratorBox(game.W, game.H)
        self._fireworks: list[dict] = []
        self._fw_timer = 0.0
        self._confetti: list[dict] = []
        self._final_alpha = 0
        self._final_timer = 0.0

        from entities.characters import Player, PartyNPC, TownNPC
        ground_y = int(game.H * 0.62)
        self._player = Player(game.W//2 - 40, ground_y - 55)
        self._elena  = PartyNPC("Elena", game.W//2 + 40, ground_y - 55)
        self._elena.emotion = "happy"
        self._player.emotion = "happy"
        self._reno   = PartyNPC("Reno",  game.W//2 - 140, ground_y - 55)
        self._lyra   = PartyNPC("Lyra",  game.W//2 + 140, ground_y - 55)
        self._darius = PartyNPC("Darius",game.W//2 - 220, ground_y - 55)
        self._king   = TownNPC("King Aldric", game.W//2, game.H*0.25, (200,160,60))

        # Konfeti
        for _ in range(60):
            self._confetti.append({
                'x': float(random.randint(0,960)),
                'y': float(random.randint(-50,540)),
                'vx': random.uniform(-30,30),
                'vy': random.uniform(40,100),
                'col': random.choice([(255,80,80),(80,200,80),(80,80,255),(255,220,80),(255,80,200)]),
                'size': random.randint(5,12),
                'rot': random.uniform(0,360),
                'rot_speed': random.uniform(-120,120),
            })

        try:
            self._font_big   = pygame.font.SysFont("Georgia", 48, bold=True)
            self._font_sub   = pygame.font.SysFont("Georgia", 24, italic=True)
            self._font_quote = pygame.font.SysFont("Georgia", 20, italic=True)
            self._font_ui    = pygame.font.SysFont("Consolas", 14)
        except Exception:
            self._font_big   = pygame.font.Font(None, 52)
            self._font_sub   = pygame.font.Font(None, 28)
            self._font_quote = pygame.font.Font(None, 22)
            self._font_ui    = pygame.font.Font(None, 16)

    def on_enter(self) -> None:
        self._transition.fade_in(color=(255,255,255), speed=200)
        self._narrator.show(["TRUE ENDING", "Savior of the World"], 3.0)
        self._dialogue.show(self.DLGS[0][1], self.DLGS[0][0])
        self._game.assets.play("fanfare")

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                if not self._dialogue.is_finished:
                    self._dialogue.skip()
                else:
                    self._advance()

    def _advance(self):
        self._game.assets.play("cursor")
        self._dlg_step += 1
        if self._dlg_step < len(self.DLGS):
            spk, txt = self.DLGS[self._dlg_step]
            self._dialogue.show(txt, spk)
            if self._dlg_step == 5:
                self._phase = "wedding"
                self._game.assets.play("fanfare")
            elif self._dlg_step == 10:
                self._game.assets.play("magic")
        else:
            self._phase = "final"
            self._final_timer = 0.0

    def update(self, dt: float) -> None:
        self._t += dt
        self._transition.update(dt)
        self._dialogue.update(dt)
        self._narrator.update(dt)
        self._player.update(dt)
        self._elena.update(dt)
        self._reno.update(dt)
        self._lyra.update(dt)
        self._darius.update(dt)
        self._king.update(dt)

        # Konfeti
        for c in self._confetti:
            c['x'] += c['vx'] * dt
            c['y'] += c['vy'] * dt
            c['rot'] += c['rot_speed'] * dt
            if c['y'] > 560:
                c['y'] = -10
                c['x'] = random.randint(0, 960)

        # Kembang api
        self._fw_timer += dt
        if self._fw_timer > 0.6:
            self._fw_timer = 0.0
            self._spawn_firework()
        for fw in self._fireworks:
            fw['age'] += dt
            for p in fw['particles']:
                p[0] += p[2] * dt
                p[1] += p[3] * dt
                p[3] += 100 * dt
        self._fireworks = [fw for fw in self._fireworks if fw['age'] < 1.2]

        if self._phase == "final":
            self._final_timer += dt
            self._final_alpha = min(255, int(255 * self._final_timer / 1.5))

    def _spawn_firework(self):
        cx = random.randint(100, 860)
        cy = random.randint(40, 220)
        col = random.choice([
            (255,220,80),(255,100,100),(100,200,255),(200,255,100),(255,100,200)
        ])
        particles = []
        for _ in range(20):
            angle = random.uniform(0, math.pi*2)
            spd   = random.uniform(60, 180)
            particles.append([float(cx), float(cy),
                               math.cos(angle)*spd, math.sin(angle)*spd])
        self._fireworks.append({'cx':cx,'cy':cy,'col':col,'particles':particles,'age':0.0})

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._game.assets.bg_ending, (0,0))

        # Kembang api
        for fw in self._fireworks:
            alpha = int(255 * (1 - fw['age']/1.2))
            for p in fw['particles']:
                s = pygame.Surface((8,8), pygame.SRCALPHA)
                pygame.draw.circle(s, (*fw['col'], alpha), (4,4), 4)
                surface.blit(s, (int(p[0])-4, int(p[1])-4))

        # Konfeti
        for c in self._confetti:
            s = pygame.Surface((c['size'],c['size']),pygame.SRCALPHA)
            pygame.draw.rect(s, (*c['col'],200),(0,0,c['size'],c['size']))
            surface.blit(s,(int(c['x']),int(c['y'])))

        # Karakter
        if self._phase in ("festival","wedding"):
            self._reno.draw(surface)
            self._lyra.draw(surface)
            self._darius.draw(surface)
        if self._phase == "wedding":
            self._king.draw(surface)
        self._player.draw(surface)
        self._elena.draw(surface)

        # Efek hati di wedding
        if self._phase == "wedding":
            for i in range(5):
                hx = self._game.W//2 + int(math.sin(self._t*2+i)*40)
                hy = 120 + int(math.cos(self._t*2+i)*20) - i*15
                s = pygame.Surface((20,20),pygame.SRCALPHA)
                alpha = int(180+75*math.sin(self._t*3+i))
                pygame.draw.circle(s,(255,100,120,alpha),(10,10),8)
                surface.blit(s,(hx,hy))

        self._narrator.draw(surface)
        self._dialogue.draw(surface)

        # Final screen
        if self._phase == "final":
            s = pygame.Surface((self._game.W, self._game.H), pygame.SRCALPHA)
            s.fill((0,0,0,min(180,self._final_alpha)))
            surface.blit(s,(0,0))
            if self._final_alpha > 100:
                alpha2 = min(255, (self._final_alpha-100)*3)
                try:
                    t1 = self._font_big.render("The Summoned Hero", True, GOLD_LIGHT)
                    t2 = self._font_big.render("Saved the World.", True, GOLD_LIGHT)
                    t3 = self._font_sub.render("— TRUE ENDING —", True, UI_ACCENT)
                    t4 = self._font_quote.render("[ Press any key to return to title ]", True, UI_DIMTEXT)
                    for t,y in [(t1,160),(t2,220),(t3,300),(t4,420)]:
                        t.set_alpha(alpha2)
                        surface.blit(t,(self._game.W//2-t.get_width()//2,y))
                except Exception:
                    pass
                if self._final_alpha >= 255:
                    if pygame.key.get_pressed()[pygame.K_SPACE] or \
                       pygame.key.get_pressed()[pygame.K_RETURN]:
                        from scenes.opening_scene import OpeningScene
                        self._game.replace_scene(OpeningScene(self._game))

        self._transition.draw(surface)
