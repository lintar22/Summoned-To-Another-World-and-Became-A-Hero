"""
scenes/bad_end_scene.py
=======================
BAD ENDING — Dunia tenggelam dalam kegelapan.
[INHERITANCE] Scene(ABC).
"""

import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox


class BadEndScene(Scene):

    TEXTS = [
        "Kerajaan Astravia jatuh dalam 3 hari.",
        "Manusia kehilangan perang.",
        "Dunia tenggelam dalam kegelapan.",
        "",
        "The Hero Failed to Save the World.",
    ]

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
        self._text_index = 0
        self._text_timer = 0.0
        self._text_alpha = 0
        self._phase = "text"
        self._final = False
        self._ashes: list[dict] = []
        self._transition = TransitionScreen(game.W, game.H)

        for _ in range(80):
            self._ashes.append({
                'x': float(random.randint(0,960)),
                'y': float(random.randint(-60,540)),
                'vx': random.uniform(-20,20),
                'vy': random.uniform(20,60),
                'size': random.randint(3,8),
                'alpha': random.randint(100,200),
            })

        try:
            self._font_big  = pygame.font.SysFont("Georgia", 36, bold=True)
            self._font_sub  = pygame.font.SysFont("Georgia", 22, italic=True)
            self._font_end  = pygame.font.SysFont("Georgia", 44, bold=True)
            self._font_hint = pygame.font.SysFont("Consolas", 14)
        except Exception:
            self._font_big  = pygame.font.Font(None, 40)
            self._font_sub  = pygame.font.Font(None, 26)
            self._font_end  = pygame.font.Font(None, 48)
            self._font_hint = pygame.font.Font(None, 18)

    def on_enter(self) -> None:
        self._transition.fade_in(color=(0,0,0), speed=150)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                if self._final:
                    from scenes.opening_scene import OpeningScene
                    self._game.replace_scene(OpeningScene(self._game))
                else:
                    self._text_timer = 10.0  # skip to next

    def update(self, dt: float) -> None:
        self._t += dt
        self._transition.update(dt)
        self._text_timer += dt

        if self._phase == "text":
            if self._text_timer < 0.8:
                self._text_alpha = int(255 * self._text_timer / 0.8)
            elif self._text_timer < 2.5:
                self._text_alpha = 255
            elif self._text_timer < 3.2:
                self._text_alpha = int(255 * (3.2 - self._text_timer) / 0.7)
            else:
                self._text_timer = 0.0
                self._text_index += 1
                if self._text_index >= len(self.TEXTS):
                    self._phase = "final_screen"
                    self._final = True

        # Debu/abu
        for a in self._ashes:
            a['x'] += a['vx'] * dt
            a['y'] += a['vy'] * dt
            if a['y'] > 550:
                a['y'] = -10
                a['x'] = random.randint(0, 960)

    def draw(self, surface: pygame.Surface) -> None:
        # Latar merah gelap
        for y in range(self._game.H):
            t = y / self._game.H
            col = (int(20+30*t), int(3+5*t), int(3+5*t))
            pygame.draw.line(surface, col, (0,y),(self._game.W,y))

        # Api di latar belakang
        for i in range(8):
            fx = int(i * 130 + math.sin(self._t*2+i)*20)
            fh = int(60 + math.sin(self._t*3+i*0.7)*30)
            s = pygame.Surface((30, fh), pygame.SRCALPHA)
            pygame.draw.polygon(s,(200,60,10,150),[(0,fh),(15,0),(30,fh)])
            surface.blit(s,(fx, self._game.H-fh-80))

        # Abu
        for a in self._ashes:
            s = pygame.Surface((a['size'],a['size']),pygame.SRCALPHA)
            pygame.draw.rect(s,(150,140,130,a['alpha']),(0,0,a['size'],a['size']))
            surface.blit(s,(int(a['x']),int(a['y'])))

        if self._phase == "text":
            if self._text_index < len(self.TEXTS):
                txt = self.TEXTS[self._text_index]
                if txt:
                    if self._text_index == len(self.TEXTS)-1:
                        t = self._font_end.render(txt, True, (220,60,60))
                    else:
                        t = self._font_sub.render(txt, True, (220,200,180))
                    t.set_alpha(self._text_alpha)
                    surface.blit(t,(self._game.W//2-t.get_width()//2, self._game.H//2-20))

        elif self._phase == "final_screen":
            # Dark overlay
            s = pygame.Surface((self._game.W,self._game.H),pygame.SRCALPHA)
            s.fill((0,0,0,160))
            surface.blit(s,(0,0))
            try:
                alpha = min(255, int(255*(self._t-0.5)))
                t1 = self._font_end.render("BAD END", True, (220,60,60))
                t2 = self._font_sub.render("The Hero Failed to Save the World.", True,(200,170,160))
                t3 = self._font_hint.render("[ Press SPACE to try again ]", True,(150,140,140))
                for t,y in [(t1,180),(t2,260),(t3,380)]:
                    t.set_alpha(min(255,alpha))
                    surface.blit(t,(self._game.W//2-t.get_width()//2,y))
            except Exception:
                pass

        self._transition.draw(surface)
