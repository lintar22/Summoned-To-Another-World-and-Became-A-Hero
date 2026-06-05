
import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox
from entities.characters import Player


class OpeningScene(Scene):

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
        self._phase = "narration"                                                                        
        self._phase_timer = 0.0
        self._dialogue = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator = NarratorBox(game.W, game.H)
        self._rain_drops = self._gen_rain(game.W, game.H)
        self._magic_circles = []
        self._dialogue_step = 0

                                            
        ground_y = game.H - 177 - 15
        self._player = Player(200.0, float(ground_y))
        self._player.before_isekai = True
        self._player._draw_scale = 1.0
        self._player_target_x = 450.0
        self._player_walk_dir = True
        self._player_walk_speed = 60.0

                                                 
                                                                  
                                                                
        self._npc_ground_y = float(ground_y)
        self._npc_college_x = 680.0                              
        self._npc_worker_x  = 900.0                                      
        self._npc_anim_timer = 0.0
        self._npc_frame_duration = 0.18                                
        self._npc_college_frame = 0
        self._npc_worker_frame  = 0

                                                                               
        self._npc_bubble_timer   = 2.5                                                 
        self._npc_bubble_interval= 4.5                           
        self._npc_bubble_active  = False
        self._npc_bubble_duration= 3.2                          
        self._npc_bubble_elapsed = 0.0
        self._npc_bubble_which   = 0                                  
        self._npc_bubble_texts = [
                              
            ("Mahasiswa",       "Aduh, tugas deadline bentar lagi..."),
            ("Pekerja Kantoran","Lembur lagi... capek juga ya hidup ini."),
            ("Mahasiswa",       "Eh, udah malem gini masih belum kelar juga."),
            ("Pekerja Kantoran","Besok meeting pagi, istirahatnya kapan dong..."),
            ("Mahasiswa",       "Mana ukt belum dibayar... pusing."),
            ("Pekerja Kantoran","Macet, hujan, cape... mantap dah."),
        ]
        self._npc_bubble_idx = 0
        self._npc_bubble_text = ""
        self._npc_bubble_name = ""
                               
        try:
            self._font_bubble = pygame.font.SysFont("Georgia", 16, italic=True)
            self._font_bubble_name = pygame.font.SysFont("Georgia", 14, bold=True)
        except Exception:
            self._font_bubble = pygame.font.Font(None, 18)
            self._font_bubble_name = pygame.font.Font(None, 16)

        self._input_ready = False
        self._press_hint_timer = 0.0

        try:
            self._font_narr   = pygame.font.SysFont("Georgia", 20, italic=True)
        except Exception:
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

    def _gen_rain(self, W=1280, H=720):
        drops = []
        for _ in range(120):
            drops.append({
                'x': random.randint(0, W),
                'y': random.randint(0, H),
                'speed': random.uniform(300, 500),
                'length': random.randint(8, 18),
            })
        return drops

    def on_enter(self) -> None:
        self._transition.fade_in(speed=180)
        self._game.assets.play_bgm("prolog_theme", loop=-1, volume=0.7)
                                                                          
        try:
            self._game.assets.play_bgm2("opening_theme", loop=-1, volume=0.5)
        except Exception:
            pass
                                                          
        self._input_ready = True
        self._narrator.show([
            "Di dunia yang berbeda...",
            "seorang pahlawan sedang dipanggil."
        ], 3.5)

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
        try: self._game.assets.play_sfx_file("space_enter_sfx")
        except Exception: pass
        if self._phase == "narration":
            if not self._dialogue.is_finished:
                self._dialogue.skip()
            else:
                self._dialogue_step += 1
                if self._dialogue_step < len(self._dialogue_data):
                    spk, txt = self._dialogue_data[self._dialogue_step]
                    self._dialogue.show(txt, spk)
                    self._game.assets.play("cursor")
                else:
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
                    self._game.assets.stop_bgm()
                    try: self._game.assets.stop_bgm2()
                    except Exception: pass
                    self._game.assets.play_sfx_file("teleport_sfx", volume=0.9)
        elif self._phase == "chapter1":
            self._go_to_chapter1()

    def _go_to_chapter1(self):
        from scenes.chapter1_scene import Chapter1Scene
        self._game.replace_scene(Chapter1Scene(self._game))

    def _update_npc_bubbles(self, dt):
        if self._npc_bubble_active:
            self._npc_bubble_elapsed += dt
            if self._npc_bubble_elapsed >= self._npc_bubble_duration:
                self._npc_bubble_active = False
                self._npc_bubble_timer  = self._npc_bubble_interval
                self._npc_bubble_idx = (self._npc_bubble_idx + 1) % len(self._npc_bubble_texts)
        else:
            self._npc_bubble_timer -= dt
            if self._npc_bubble_timer <= 0:
                name, text = self._npc_bubble_texts[self._npc_bubble_idx]
                self._npc_bubble_name = name
                self._npc_bubble_text = text
                self._npc_bubble_which = 0 if name == "Mahasiswa" else 1
                self._npc_bubble_active  = True
                self._npc_bubble_elapsed = 0.0

    def update(self, dt: float) -> None:
        self._t += dt
        self._phase_timer += dt
        self._transition.update(dt)
        self._narrator.update(dt)
        self._dialogue.update(dt)
        self._press_hint_timer += dt

               
        for d in self._rain_drops:
            d['y'] += d['speed'] * dt
            d['x'] += d['speed'] * 0.2 * dt
            if d['y'] > self._game.H:
                d['y'] = 0
                d['x'] = random.randint(0, self._game.W)

        if self._phase == "narration":
            self._input_ready = True
            if self._phase_timer < 0.1 and self._dialogue_step == 0:
                spk, txt = self._dialogue_data[0]
                self._dialogue.show(txt, spk)
            if self._player._x < self._player_target_x:
                self._player._x = min(self._player_target_x, self._player._x + self._player_walk_speed * dt)
                self._player.set_walking(True, True)
            else:
                self._player.set_walking(False)
                               
            self._update_npc_bubbles(dt)

        elif self._phase == "magic":
            self._input_ready = True
            if self._phase_timer < 0.1 and not self._dialogue.visible:
                idx = self._dialogue_step - len(self._dialogue_data)
                if 0 <= idx < len(self._post_flash_data):
                    spk, txt = self._post_flash_data[idx]
                    self._dialogue.show(txt, spk)
            self._player.set_walking(False)
            if len(self._magic_circles) < 3 and self._phase_timer > 0.3:
                self._magic_circles.append({'r': 10, 'alpha': 200, 'angle': 0})
            self._update_npc_bubbles(dt)

        elif self._phase == "flash":
            self._input_ready = False
            self._player.set_walking(False)
            if self._phase_timer > 1.2:
                self._phase = "chapter1"
                self._phase_timer = 0.0
                self._input_ready = True

        elif self._phase == "chapter1":
            self._player.set_walking(False)

                               
        self._player.update(dt)

                                               
        self._npc_anim_timer += dt
        if self._npc_anim_timer >= self._npc_frame_duration:
            self._npc_anim_timer = 0.0
            frames_c = getattr(self._game.assets, 'npc_college_frames', [])
            frames_w = getattr(self._game.assets, 'npc_worker_frames',  [])
            if frames_c:
                self._npc_college_frame = (self._npc_college_frame + 1) % len(frames_c)
            if frames_w:
                self._npc_worker_frame  = (self._npc_worker_frame  + 1) % len(frames_w)

                              
        for mc in self._magic_circles:
            mc['r'] = min(100, mc['r'] + 40*dt)
            mc['angle'] += dt * 120

    def _draw_char_scaled(self, surface, char, scale=2.2):
        SPRITE_BASE_H = 96                                            
        tmp = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        char.draw(tmp)
        region = tmp.get_bounding_rect()
        if region.width < 2 or region.height < 2:
            char.draw(surface)
            return
        char_surf = tmp.subsurface(region).copy()
        orig_w, orig_h = char_surf.get_size()
                                                                             
        if orig_h > 0:
            norm_w = int(orig_w * SPRITE_BASE_H / orig_h)
            norm_h = SPRITE_BASE_H
        else:
            norm_w, norm_h = orig_w, orig_h
        normalized = pygame.transform.scale(char_surf, (norm_w, norm_h))
        new_w = int(norm_w * scale)
        new_h = int(norm_h * scale)
        scaled = pygame.transform.scale(normalized, (new_w, new_h))
        foot_x = region.centerx
        foot_y = region.bottom
        surface.blit(scaled, (foot_x - new_w // 2, foot_y - new_h))

    def _draw_npc(self, surface, frames, frame_idx, x, y, scale=2.2):
        if not frames:
            return
        SPRITE_BASE_H = 96                                                             
        frame_idx = frame_idx % len(frames)
        img = frames[frame_idx]
                                                              
        orig_w, orig_h = img.get_size()
        if orig_h > 0:
            norm_w = int(orig_w * SPRITE_BASE_H / orig_h)
            norm_h = SPRITE_BASE_H
        else:
            norm_w, norm_h = orig_w, orig_h
        normalized = pygame.transform.scale(img, (norm_w, norm_h))
                                                        
        new_w = int(norm_w * scale)
        new_h = int(norm_h * scale)
        scaled = pygame.transform.scale(normalized, (new_w, new_h))
        surface.blit(scaled, (int(x) - new_w // 2, int(y) - new_h))

    def _draw_npc_bubble(self, surface, text, name, x, y, align_right=False):
        pad_x, pad_y = 10, 7
        max_w = 240
                             
        words = text.split()
        lines = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            if self._font_bubble.size(test)[0] <= max_w - pad_x * 2:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)

        line_h = self._font_bubble.get_height() + 2
        name_h = self._font_bubble_name.get_height() + 4
        box_h  = pad_y * 2 + name_h + len(lines) * line_h
        box_w  = max_w

                                     
        bx = int(x) - box_w // 2
        by = int(y) - box_h - 12

                                       
        bx = max(4, min(bx, surface.get_width() - box_w - 4))
        by = max(4, by)

                                   
        box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        pygame.draw.rect(box, (20, 20, 40, 210), (0, 0, box_w, box_h), border_radius=8)
        pygame.draw.rect(box, (120, 140, 200, 180), (0, 0, box_w, box_h), 1, border_radius=8)

                  
        name_surf = self._font_bubble_name.render(name, True, (180, 210, 255))
        box.blit(name_surf, (pad_x, pad_y))

                     
        for i, line in enumerate(lines):
            t_surf = self._font_bubble.render(line, True, (220, 220, 220))
            box.blit(t_surf, (pad_x, pad_y + name_h + i * line_h))

        surface.blit(box, (bx, by))

                                                  
        tip_x = int(x)
        tip_x = max(bx + 10, min(tip_x, bx + box_w - 10))
        tip_y = by + box_h
        pygame.draw.polygon(surface, (20, 20, 40, 210),
                            [(tip_x - 7, tip_y), (tip_x + 7, tip_y), (tip_x, tip_y + 8)])

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._game.assets.bg_prolog, (0, 0))
        self._draw_city_scene(surface)

        self._narrator.draw(surface)
        self._dialogue.draw(surface)
        self._transition.draw(surface)

    def _draw_city_scene(self, surface):
               
        for d in self._rain_drops:
            end_x = int(d['x'] + d['length']*0.3)
            end_y = int(d['y'] + d['length'])
            pygame.draw.line(surface, (150,180,220,100), (int(d['x']),int(d['y'])),(end_x,end_y),1)

                                                         
        frames_c = getattr(self._game.assets, 'npc_college_frames', [])
        frames_w = getattr(self._game.assets, 'npc_worker_frames',  [])

        self._draw_npc(surface, frames_c, self._npc_college_frame,
                       self._npc_college_x, self._npc_ground_y)
        self._draw_npc(surface, frames_w, self._npc_worker_frame,
                       self._npc_worker_x,  self._npc_ground_y)

                                                              
        if self._phase in ("narration", "magic") and self._npc_bubble_active:
                                                                 
            alpha_ratio = 1.0
            fade_dur = 0.4
            if self._npc_bubble_elapsed < fade_dur:
                alpha_ratio = self._npc_bubble_elapsed / fade_dur
            elif self._npc_bubble_elapsed > self._npc_bubble_duration - fade_dur:
                alpha_ratio = (self._npc_bubble_duration - self._npc_bubble_elapsed) / fade_dur
            alpha_ratio = max(0.0, min(1.0, alpha_ratio))

            if alpha_ratio > 0.05:
                CHAR_H = int(96 * 2.2)                                               
                if self._npc_bubble_which == 0:
                    bx = self._npc_college_x
                    by = self._npc_ground_y - CHAR_H
                else:
                    bx = self._npc_worker_x
                    by = self._npc_ground_y - CHAR_H
                self._draw_npc_bubble(surface, self._npc_bubble_text,
                                      self._npc_bubble_name, bx, by)

                                            
        self._draw_char_scaled(surface, self._player, 2.0)

                       
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
