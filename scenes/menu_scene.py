
import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import TransitionScreen


class MenuScene(Scene):

    MENU_ITEMS = ["New Game", "Quit"]

    def __init__(self, game):
        super().__init__(game)
        self._t             = 0.0
        self._selected      = 0
        self._input_ready   = False
        self._exiting       = False

                                                             
        self._phase         = "title"
        self._phase_timer   = 0.0

        self._transition    = TransitionScreen(game.W, game.H)
        self._hint_timer    = 0.0

                                                                            
        self._title1_alpha  = 0.0                                
        self._title2_alpha  = 0.0                        
        self._sub_alpha     = 0.0                       
        self._line_alpha    = 0.0                    
        self._press_alpha   = 0.0                                
        self._press_visible = False

                                    
        self._menu_alpha    = 0.0                               
        self._menu_visible  = False

                                                                    
        random.seed(77)
        self._stars = [
            {
                "x":     random.randint(0, game.W),
                "y":     random.randint(0, int(game.H * 0.85)),
                "size":  random.choice([1, 1, 2]),
                "phase": random.uniform(0, 6.28),
                "speed": random.uniform(0.8, 2.2),
            }
            for _ in range(140)
        ]

                                                  
        random.seed(42)
        self._particles = [
            {
                "x":        random.uniform(0, game.W),
                "y":        random.uniform(0, game.H),
                "vy":       random.uniform(-18, -8),
                "vx":       random.uniform(-6, 6),
                "alpha":    random.randint(60, 160),
                "size":     random.choice([1, 2, 2]),
                "life":     random.uniform(0, 4),
                "max_life": random.uniform(3, 6),
            }
            for _ in range(60)
        ]

                    
        try:
            self._font_title    = pygame.font.SysFont("Georgia", 58, bold=True)
            self._font_title2   = pygame.font.SysFont("Georgia", 58, bold=True)
            self._font_sub      = pygame.font.SysFont("Georgia", 22, italic=True)
            self._font_item     = pygame.font.SysFont("Georgia", 32)
            self._font_item_sel = pygame.font.SysFont("Georgia", 36, bold=True)
            self._font_hint     = pygame.font.SysFont("Consolas", 14)
            self._font_version  = pygame.font.SysFont("Consolas", 12)
        except Exception:
            self._font_title    = pygame.font.Font(None, 62)
            self._font_title2   = pygame.font.Font(None, 62)
            self._font_sub      = pygame.font.Font(None, 26)
            self._font_item     = pygame.font.Font(None, 36)
            self._font_item_sel = pygame.font.Font(None, 42)
            self._font_hint     = pygame.font.Font(None, 18)
            self._font_version  = pygame.font.Font(None, 15)

                                                                 

    def on_enter(self) -> None:
        self._transition.fade_in(speed=120)
        self._game.assets.play_bgm("menu_theme", loop=-1, volume=0.75)

    def on_exit(self) -> None:
        pass

                                                                 

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._exiting:
            return
        if event.type != pygame.KEYDOWN:
            return

        key = event.key

        if self._phase == "title" and self._input_ready:
                                                 
            try: self._game.assets.play_sfx_file("space_enter_sfx")
            except Exception: pass
            self._phase = "menu"
            self._phase_timer = 0.0
            self._menu_visible = True
            return

        if self._phase == "menu":
            if key in (pygame.K_UP, pygame.K_w):
                self._selected = (self._selected - 1) % len(self.MENU_ITEMS)
                try: self._game.assets.play("cursor")
                except Exception: pass

            elif key in (pygame.K_DOWN, pygame.K_s):
                self._selected = (self._selected + 1) % len(self.MENU_ITEMS)
                try: self._game.assets.play("cursor")
                except Exception: pass

            elif key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                if self._menu_alpha > 150:
                    self._confirm()

    def _confirm(self):
        try: self._game.assets.play_sfx_file("space_enter_sfx")
        except Exception: pass

        choice = self.MENU_ITEMS[self._selected]

        if choice == "New Game":
            self._exiting = True
            self._transition.fade_out(color=(0, 0, 0), speed=160)

        elif choice == "Quit":
            self._exiting = True
            self._transition.fade_out(color=(0, 0, 0), speed=180)

                                                                 

    def update(self, dt: float) -> None:
        self._t          += dt
        self._hint_timer += dt
        self._phase_timer += dt
        self._transition.update(dt)

                                                                             
        if self._phase in ("title", "menu"):
                                        
            if self._t > 0.4:
                self._title1_alpha = min(255.0, self._title1_alpha + 160 * dt)
                                                         
            if self._title1_alpha > 80:
                self._title2_alpha = min(255.0, self._title2_alpha + 140 * dt)
                                              
            if self._title2_alpha > 120:
                self._sub_alpha  = min(255.0, self._sub_alpha  + 120 * dt)
                self._line_alpha = min(255.0, self._line_alpha + 130 * dt)
                                                               
            if self._sub_alpha > 160 and self._phase == "title":
                self._press_visible = True
                self._input_ready = True

                                                 
        if self._menu_visible:
            self._menu_alpha = min(255.0, self._menu_alpha + 220 * dt)

                                      
        for p in self._particles:
            p["life"] += dt
            p["x"]    += p["vx"] * dt
            p["y"]    += p["vy"] * dt
            if p["life"] >= p["max_life"] or p["y"] < -10 or p["x"] < -10 or p["x"] > self._game.W + 10:
                p["x"]       = random.uniform(0, self._game.W)
                p["y"]       = self._game.H + 10
                p["vy"]      = random.uniform(-18, -8)
                p["vx"]      = random.uniform(-6, 6)
                p["alpha"]   = random.randint(60, 160)
                p["size"]    = random.choice([1, 2, 2])
                p["life"]    = 0.0
                p["max_life"]= random.uniform(3, 6)

                                                 
        if self._exiting and self._transition.done:
            choice = self.MENU_ITEMS[self._selected]
            if choice == "New Game":
                from scenes.opening_scene import OpeningScene
                self._game.replace_scene(OpeningScene(self._game))
            elif choice == "Quit":
                self._game.running = False

                                                                 

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._game.assets.bg_night_city, (0, 0))

        self._draw_stars(surface)
        self._draw_particles(surface)

                             
        overlay = pygame.Surface((self._game.W, self._game.H), pygame.SRCALPHA)
        overlay.fill((0, 0, 10, 80))
        surface.blit(overlay, (0, 0))

        self._draw_title(surface)

        if self._phase == "title" and self._press_visible:
            self._draw_press_hint(surface)

        if self._menu_visible:
            self._draw_menu(surface, int(self._menu_alpha))
            self._draw_hint(surface, int(self._menu_alpha))

        self._draw_footer(surface)
        self._transition.draw(surface)

    def _draw_stars(self, surface):
        for s in self._stars:
            bright = int(100 + 80 * math.sin(self._t * s["speed"] + s["phase"]))
            bright = max(60, min(220, bright))
            pygame.draw.circle(surface, (bright, bright, min(bright + 30, 255)),
                               (s["x"], s["y"]), s["size"])

    def _draw_particles(self, surface):
        for p in self._particles:
            life_ratio = p["life"] / p["max_life"]
            fade = min(life_ratio * 4, (1 - life_ratio) * 4, 1.0)
            a = int(p["alpha"] * fade)
            if a < 5:
                continue
            ps = pygame.Surface((p["size"] * 2 + 2, p["size"] * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (160, 190, 255, a),
                               (p["size"] + 1, p["size"] + 1), p["size"])
            surface.blit(ps, (int(p["x"]) - p["size"], int(p["y"]) - p["size"]))

    def _draw_title(self, surface):
        W, H = self._game.W, self._game.H

        try:
                                                    
            t1_y = H // 2 - 190
            t1_x_center = W // 2
            t1_text = "Summoned To Another World"

                                                                                
            for ox, oy, col, sha in [
                (3, 4, (0, 0, 0), 180),
                (2, 3, (10, 5, 30), 140),
                (1, 2, (20, 10, 60), 100),
            ]:
                sh1 = self._font_title.render(t1_text, True, col)
                sh1.set_alpha(int(self._title1_alpha * sha / 255))
                surface.blit(sh1, (t1_x_center - sh1.get_width() // 2 + ox, t1_y + oy))

            t1 = self._font_title.render(t1_text, True, UI_ACCENT)
            t1.set_alpha(int(self._title1_alpha))
            surface.blit(t1, (t1_x_center - t1.get_width() // 2, t1_y))

                                                    
            t2_y = H // 2 - 125
            t2_text = "and Became A Hero"

            for ox, oy, col, sha in [
                (3, 4, (0, 0, 0), 180),
                (2, 3, (20, 15, 0), 140),
                (1, 2, (40, 30, 0), 100),
            ]:
                sh2 = self._font_title2.render(t2_text, True, col)
                sh2.set_alpha(int(self._title2_alpha * sha / 255))
                surface.blit(sh2, (t1_x_center - sh2.get_width() // 2 + ox, t2_y + oy))

            t2 = self._font_title2.render(t2_text, True, GOLD_LIGHT)
            t2.set_alpha(int(self._title2_alpha))
            surface.blit(t2, (t1_x_center - t2.get_width() // 2, t2_y))

                                   
            if self._line_alpha > 10:
                line_w = 380
                line_surf = pygame.Surface((line_w, 2), pygame.SRCALPHA)
                                                 
                for lx in range(line_w):
                    ratio = 1.0 - abs(lx / line_w - 0.5) * 2
                    la = int(self._line_alpha * ratio * 0.75)
                    pygame.draw.line(line_surf, (*UI_BORDER, la), (lx, 0), (lx, 1))
                surface.blit(line_surf, (W // 2 - line_w // 2, H // 2 - 72))

                                                       
                if self._line_alpha > 80:
                    dia_a = int(min(self._line_alpha, 200))
                    dia_size = 5
                    dia_surf = pygame.Surface((dia_size * 2, dia_size * 2), pygame.SRCALPHA)
                    pygame.draw.polygon(dia_surf, (*GOLD_LIGHT, dia_a),
                                        [(dia_size, 0), (dia_size*2, dia_size),
                                         (dia_size, dia_size*2), (0, dia_size)])
                    surface.blit(dia_surf, (W // 2 - dia_size, H // 2 - 72 - dia_size + 1))

                            
            sub = self._font_sub.render("PROJEK AKHIR PBO", True, UI_DIMTEXT)
            sub.set_alpha(int(min(self._sub_alpha, 200)))
            surface.blit(sub, (W // 2 - sub.get_width() // 2, H // 2 - 55))

        except Exception:
            pass

    def _draw_press_hint(self, surface):
        W, H = self._game.W, self._game.H
        alpha = int(128 + 127 * math.sin(self._hint_timer * 3.0))
        try:
            hint = self._font_hint.render("[ Press any key to continue ]", True, UI_DIMTEXT)
            hint.set_alpha(alpha)
            surface.blit(hint, (W // 2 - hint.get_width() // 2, H // 2 + 60))
        except Exception:
            pass

    def _draw_menu(self, surface, alpha: int):
        W, H = self._game.W, self._game.H
                                                                   
        base_y = H // 2 + 115
        spacing = 62

        for i, item in enumerate(self.MENU_ITEMS):
            is_sel = (i == self._selected)

            if is_sel:
                color   = UI_ACCENT
                font    = self._font_item_sel
                arrow_a = int(180 + 75 * math.sin(self._t * 4.0))
                arrow_a = max(100, min(255, arrow_a))
            else:
                color   = UI_DIMTEXT
                font    = self._font_item
                arrow_a = 0

            y = base_y + i * spacing

            try:
                txt = font.render(item, True, color)
                txt.set_alpha(alpha)
                tx = W // 2 - txt.get_width() // 2
                surface.blit(txt, (tx, y))

                if is_sel and alpha > 60:
                                         
                    box_w = txt.get_width() + 70
                    box_h = txt.get_height() + 16
                    box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
                    box_bg_a = min(alpha // 3, 65)
                    box_bd_a = min(alpha, 130)
                    pygame.draw.rect(box, (*UI_BORDER, box_bg_a),
                                     (0, 0, box_w, box_h), border_radius=10)
                    pygame.draw.rect(box, (*UI_BORDER, box_bd_a),
                                     (0, 0, box_w, box_h), 1, border_radius=10)
                                                  
                    for gx, ga in [(0, 40), (box_w - 3, 40)]:
                        gg = pygame.Surface((3, box_h), pygame.SRCALPHA)
                        gg.fill((*UI_ACCENT, min(alpha // 4, ga)))
                        box.blit(gg, (gx, 0))
                    surface.blit(box, (W // 2 - box_w // 2, y - 8))

                                             
                    txt2 = font.render(item, True, color)
                    txt2.set_alpha(alpha)
                    surface.blit(txt2, (tx, y))

                                                      
                    arrow = self._font_item_sel.render("▶", True, GOLD_LIGHT)
                    arrow.set_alpha(arrow_a)
                    ax = tx - arrow.get_width() - 16
                    ay = y + txt.get_height() // 2 - arrow.get_height() // 2
                    surface.blit(arrow, (ax, ay))

                                               
                    arrow_r = self._font_item_sel.render("◀", True, GOLD_LIGHT)
                    arrow_r.set_alpha(arrow_a)
                    surface.blit(arrow_r, (tx + txt.get_width() + 16, ay))

            except Exception:
                pass

    def _draw_hint(self, surface, alpha: int):
        if alpha < 80:
            return
        W, H = self._game.W, self._game.H
        pulse = int(90 + 70 * math.sin(self._hint_timer * 2.5))
        try:
            hint = self._font_hint.render("↑ ↓  Navigasi      Space / Enter  Pilih", True, UI_DIMTEXT)
            hint.set_alpha(min(alpha, pulse))
            surface.blit(hint, (W // 2 - hint.get_width() // 2, H - 58))
        except Exception:
            pass

    def _draw_footer(self, surface):
        try:
            ver = self._font_version.render(
                "v1.0  |  Summoned To Another World and Became A Hero", True, UI_DIMTEXT)
            a = int(min(self._sub_alpha, 90))
            ver.set_alpha(a)
            surface.blit(ver, (self._game.W // 2 - ver.get_width() // 2,
                               self._game.H - 26))
        except Exception:
            pass
