
import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, StatusWindow, NarratorBox, FloatingText, PartyHUD
from entities.characters import Player, PartyNPC, BossNPC, KingdomNPC


class Chapter1Scene(Scene):

    DIALOGUES = [
    ("Knight A",    "Dia muncul! Akhirnya Ritualnya berhasil!"),
    ("Mage",        "Cahaya dari lingkaran sihir itu... luar biasa sekali. Ramalan benar-benar menjadi nyata."),
    ("Arga",        "...Hah? Apa... apa ini?"),
    ("Arga",        "Barusan aku di perasaan lagi di jalan mau pulang, tapi kok sekarang—"),
    ("Arga",        "Ini mimpi, kan? Ini pasti mimpi."),
    ("King Aldric", "Selamat datang, anak muda. Ah tidak.."),
    ("King Aldric", "Wahai Pahlawan, Maafkan kami karena memanggil tanpa izin."),
    ("Arga",        "Memanggil? Maksudnya apaan... kalian yang bikin aku ada di sini?!"),
    ("King Aldric", "Benar. Dan aku mohon kau dengarkan dulu sebelum menghakimi kami."),
    ("King Aldric", "Namaku Aldric. Raja Kerajaan Astravia. Dan dunia ini sedang benar-benar diambang kehancuran."),
    ("Arga",        "...Dunia ini?"),
    ("King Aldric", "Raja Iblis — makhluk yang lahir dari kebencian yang ada di dunia ini — mulai bergerak."),
    ("King Aldric", "Satu per satu kerajaan jatuh. Desa-desa dibakar. Ribuan nyawa hilang."),
    ("King Aldric", "Ramalan kuno berkata: hanya pahlawan dari dunia lain yang bisa menghentikannya."),
    ("Arga",        "Tunggu— pahlawan? Maksudnya aku?"),
    ("Arga",        "Aku itu cuma pelajar biasa. Aku bahkan gak bisa masak nasi dengan benar."),
    ("King Aldric", "Kami tahu ini terdengar mustahil. Tapi lihat... pedang itu merespons kehadiranmu."),
    ("SYSTEM",      "Pedang Suci melayang perlahan dari altar menuju ke arah Arga..."),
    ("Knight A",    "Lihat itu! Itu Pedang Suci...! Ia benar-benar merespon sang pahlawan!"),
    ("Knight B",    "Dalam catatan sejarah, ini belum pernah terjadi selama 500 tahun!"),
    ("Mage",        "Mana yang terpancar dari tubuhnya... ini bukan mana manusia biasa."),
    ("Arga",        "Apa ini... kenapa pedang ini mendekat sendiri ke tanganku?"),
]

                                                                            
    SWORD_APPEAR_STEP = 16

    SWORD_CHOICE = ["Ambil Pedang (YES)", "Tolak (NO)"]

    AFTER_SWORD = [
    ("SYSTEM",      "Cahaya emas memenuhi ruangan, dinding batu bergetar!"),
    ("Arga",        "Apa— apa yang terjadi pada tanganku?!"),
    ("Arga",        "Rasanya seperti... seperti ada sesuatu yang masuk ke dalam diriku."),
    ("Mage",        "Pedang Suci telah memilih tuannya. Kekuatan ramalan tersegel dalam dirinya."),
    ("Knight B",    "Ini... luar biasa. Aku hidup untuk menyaksikan momen ini."),
    ("King Aldric", "Kau tidak harus menerimanya sepenuhnya sekarang."),
    ("King Aldric", "Tapi nasib dunia ini sudah ada di genggaman tanganmu, anak muda."),
    ("Arga",        "...Aku tidak punya pilihan lain, kan."),
    ("King Aldric", "Selalu ada pilihan. Tapi kadang satu pilihan membawa bobot yang berbeda."),
]

    ELENA_DIALOGUES = [
    ("Elena",       "Ayah... jadi... dia orangnya?"),
    ("King Aldric", "Benar. Dia yang dipilih pedang itu."),
    ("Elena",       "..."),
    ("Elena",       "Maaf, aku tidak bermaksud menatap terlalu lama. Ini hanya... di luar dugaan."),
    ("Arga",        "Aku juga di luar dugaan soal semuanya."),
    ("Elena",       "Namaku Elena. Putri kerajaan Astravia."),
    ("Arga",        "Arga. Dari... yah, tampaknya dari dunia yang berbeda."),
    ("Elena",       "Arga... boleh aku bertanya sesuatu?"),
    ("Arga",        "Silakan."),
    ("Elena",       "Apakah kau benar-benar bersedia mengemban ini semua? Karena aku tidak ingin kau merasa dipaksa."),
    ("Arga",        "Jujur saja... aku masih belum tahu. Ini terlalu tiba-tiba."),
    ("Elena",       "Kalau begitu, setidaknya jangan lakukan sendiri."),
    ("Elena",       "Bolehkah aku ikut bersamamu? Aku mungkin tidak sekuat pedangmu, tapi aku tahu dunia ini lebih baik darimu."),
    ("Arga",        "Kau... minta izin padaku?"),
    ("Elena",       "Bukankah itu hal yang wajar? Kita belum saling kenal."),
    ("Arga",        "...Baiklah. Aku tidak keberatan punya pemandu yang tahu jalan."),
    ("Elena",       "Hm. Jawaban yang cukup jujur. Aku suka itu."),
    ("SYSTEM",      "Elena memutuskan untuk menemani perjalanan Arga."),
]

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
        self._phase = "arrival"
        self._dialogue = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._status_win = StatusWindow(game.W, game.H)
        self._narrator = NarratorBox(game.W, game.H)
        self._floats: list[FloatingText] = []
        self._party_hud = PartyHUD()

                                         
        self._player = Player(game.W//2, -80)
        self._player.emotion = "surprised"
        self._player.before_isekai = True                                    

                                                                   
        self._elena = PartyNPC("Elena", game.W + 80, int(game.H*0.82)-55)

                                                                
        _ground_y = int(game.H*0.82) - 55
        _king_target_x = float(game.W // 2) + 160
        self._king = KingdomNPC("King Aldric", _king_target_x, float(_ground_y), (180,150,80))
        self._king.emotion = "normal"
        self._king._facing_right = False                                            

                                                                               
        self._mage   = KingdomNPC("Mage",   int(game.W * 0.28),  float(_ground_y))
        self._knight = KingdomNPC("Knight", int(game.W * 0.38), float(_ground_y))
        self._mage._facing_right   = True
        self._knight._facing_right = True
                                                                         
        self._npc_anim_timer  = 0.0
        self._npc_anim_speed  = 0.18                    
        self._npc_king_frame  = 0
        self._npc_mage_frame  = 0
        self._npc_knight_frame= 0

        self._dlg_step = 0
        self._phase_timer = 0.0

                                                                   
        self._sword_visible = False
        self._sword_y = 200.0
        self._sword_glow = 0.0

        self._show_status = False
        self._particles: list[dict] = []
        self._choice_made = False

                                                                    
        self._king_walkin_done = True
        self._king_target_x = float(game.W // 2) + 160

                                              
        self._elena_walkin_done = False
        self._elena_target_x = float(game.W * 0.65)                                
        self._elena_walkin_active = False

        try:
            self._font_chapter = pygame.font.SysFont("Georgia", 36, bold=True)
            self._font_system  = pygame.font.SysFont("Consolas", 16)
        except Exception:
            self._font_chapter = pygame.font.Font(None, 40)
            self._font_system  = pygame.font.Font(None, 18)

    def on_enter(self) -> None:
        self._transition.fade_in(color=(255, 255, 255), speed=220)
        self._narrator.show(["Aula Kerajaan Astravia"], 3.0)
        self._game.assets.play_bgm("summoning_theme", loop=-1, volume=0.7)
                                                                  
        self._arga_fall_y = -80.0
        self._arga_falling = True
                                                            
        self._landing_dialogue_queued = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            key = event.key
                                               
            if getattr(self, '_arga_falling', False):
                return
            if key in (pygame.K_UP, pygame.K_w):
                if self._dialogue.showing_choices:
                    self._dialogue.navigate_choice(-1)
            elif key in (pygame.K_DOWN, pygame.K_s):
                if self._dialogue.showing_choices:
                    self._dialogue.navigate_choice(1)
            elif key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                self._advance()
            elif key == pygame.K_TAB:
                if self._phase in ("sword_taken", "status_show", "elena", "goto_town"):
                    self._show_status = not self._show_status
                    self._status_win.visible = self._show_status

    def _advance(self):
        self._game.assets.play("cursor")
        try: self._game.assets.play_sfx_file("space_enter_sfx")
        except Exception: pass
        if self._phase == "arrival":
            if self._dialogue.showing_choices:
                choice = self._dialogue.confirm_choice()
                if choice == 0:
                                                                   
                    self._phase = "sword_taken"
                    self._sword_visible = False                                        
                    self._player.before_isekai = False                                  
                                                                             
                    self._dialogue.hide()
                    self._game.assets.play("flash")
                    self._spawn_particles(self._game.W//2, 200)
                    self._game.assets.play("fanfare")
                                                         
                    try: self._game.assets.play_sfx_file("blessing_sfx", volume=0.85)
                    except Exception: pass
                    pygame.time.delay(100)
                    self._dialogue.show(self.AFTER_SWORD[0][1], self.AFTER_SWORD[0][0])
                    self._dlg_step = 0
                else:
                                          
                    self._dialogue.show(
                        "Kau tidak bisa menolak takdir.",
                        "SYSTEM"
                    )
                    self._choice_made = True
                return

            if not self._dialogue.is_finished:
                self._dialogue.skip()
                return

            self._dlg_step += 1
            if self._dlg_step < len(self.DIALOGUES):
                spk, txt = self.DIALOGUES[self._dlg_step]
                                                                
                if self._dlg_step >= self.SWORD_APPEAR_STEP:
                    self._sword_visible = True
                if self._dlg_step == len(self.DIALOGUES)-1:
                                        
                    self._dialogue.show(
                        "Pedang Suci melayang ke hadapanmu.\nAmbil Pedang Suci?",
                        "SYSTEM",
                        choices=self.SWORD_CHOICE
                    )
                else:
                    self._dialogue.show(txt, spk)
            else:
                self._sword_visible = True
                self._dialogue.show(
                    "Pedang Suci melayang ke hadapanmu.\nAmbil Pedang Suci?",
                    "SYSTEM",
                    choices=self.SWORD_CHOICE
                )

        elif self._phase == "sword_taken":
            if not self._dialogue.is_finished:
                self._dialogue.skip()
                return
            self._dlg_step += 1
            if self._dlg_step < len(self.AFTER_SWORD):
                spk, txt = self.AFTER_SWORD[self._dlg_step]
                self._dialogue.show(txt, spk)
                self._game.assets.play("fanfare")
            else:
                                                                            
                self._phase = "status_show"
                self._show_status = True
                self._status_win.visible = True
                self._dialogue.show(
                    "Kekuatan pedang suci telah tersegel dalam dirimu.",
                    "SYSTEM"
                )

        elif self._phase == "status_show":
            if not self._dialogue.is_finished:
                self._dialogue.skip()
                return
            self._show_status = False
            self._phase = "elena"
            self._dlg_step = 0
                                           
            self._elena._x = -80.0
            self._elena_walkin_active = True
            self._elena_walkin_done = False
                                            
            self._elena_arrived_dialogue_queued = True

        elif self._phase == "elena":
                                                              
            if self._elena_walkin_active:
                return
            if not self._dialogue.is_finished:
                self._dialogue.skip()
                return
            self._dlg_step += 1
            if self._dlg_step < len(self.ELENA_DIALOGUES):
                spk, txt = self.ELENA_DIALOGUES[self._dlg_step]
                self._dialogue.show(txt, spk)
                if "Elena" in spk:
                    self._elena.emotion = "happy" if self._dlg_step > 2 else "normal"
            else:
                                      
                self._game.party.append("Elena")
                self._phase = "goto_town"
                self._transition.fade_out(speed=200)
                self._narrator.show(["Jelajahi Kota Astravia"], 2.0)

    def _spawn_particles(self, cx, cy):
        for _ in range(30):
            angle = random.uniform(0, math.pi*2)
            speed = random.uniform(80, 200)
            self._particles.append({
                'x': float(cx), 'y': float(cy),
                'vx': math.cos(angle)*speed, 'vy': math.sin(angle)*speed,
                'life': random.uniform(0.5, 1.5),
                'max_life': 1.5,
                'col': random.choice([GOLD_LIGHT, HOLY_WHITE, (255,230,150)]),
                'size': random.randint(3, 7),
            })

    def update(self, dt: float) -> None:
        self._t += dt
        self._phase_timer += dt

                                                                   
        if getattr(self, '_arga_falling', False):
            target_y = int(self._game.H * 0.82) - 55
            self._arga_fall_y = min(target_y, self._arga_fall_y + 420 * dt)
            self._player._y = self._arga_fall_y
            if self._arga_fall_y >= target_y:
                self._arga_falling = False
                self._player._y = target_y
                                              
                try: self._game.assets.play_sfx_file("fall_sfx", volume=0.85)
                except Exception: pass
                                                                                  
                if not getattr(self, '_landing_dialogue_queued', False):
                    self._landing_dialogue_queued = True
                    self._dialogue.show(self.DIALOGUES[0][1], self.DIALOGUES[0][0])

                                                                            

                                                                   
        if self._elena_walkin_active:
            tx = self._elena_target_x
            if self._elena._x < tx - 2:
                self._elena._x = min(tx, self._elena._x + 260 * dt)
                self._elena._facing_right = True                         
                                             
                if hasattr(self._elena, 'set_walking'):
                    self._elena.set_walking(True, True)
            else:
                self._elena._x = tx
                self._elena_walkin_active = False
                self._elena_walkin_done   = True
                self._elena.follow(self._player)
                self._elena.follow_distance = -80
                self._elena_walkin_done = True
                self._elena._facing_right = False                                          
                                             
                if hasattr(self._elena, 'set_walking'):
                    self._elena.set_walking(False)
                                                 
                if getattr(self, '_elena_arrived_dialogue_queued', False):
                    self._elena_arrived_dialogue_queued = False
                    spk, txt = self.ELENA_DIALOGUES[0]
                    self._dialogue.show(txt, spk)
                    self._elena.emotion = "thinking"

        self._transition.update(dt)
        self._dialogue.update(dt)
        self._narrator.update(dt)
        self._status_win.update(dt)

                                                        
        self._player.update(dt)
        self._elena.update(dt)
        self._king.update(dt)

                                                           
        self._npc_anim_timer += dt
        if self._npc_anim_timer >= self._npc_anim_speed:
            self._npc_anim_timer = 0.0
            assets = self._game.assets
            king_f = getattr(assets, "king_aldric_idle_frames", [])
            mage_f = getattr(assets, "mage_idle_frames", [])
            kngt_f = getattr(assets, "knight_idle_frames", [])
            if king_f:  self._npc_king_frame   = (self._npc_king_frame   + 1) % len(king_f)
            if mage_f:  self._npc_mage_frame   = (self._npc_mage_frame   + 1) % len(mage_f)
            if kngt_f:  self._npc_knight_frame = (self._npc_knight_frame + 1) % len(kngt_f)

                                                                                          
        self._sword_y = 180 + math.sin(self._t * 2) * 15
        self._sword_glow = abs(math.sin(self._t * 3))

                  
        for p in self._particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['vy'] += 150*dt
            p['life'] -= dt
        self._particles = [p for p in self._particles if p['life'] > 0]

                     
        for ft in self._floats:
            ft.update(dt)
        self._floats = [ft for ft in self._floats if ft.alive]

                                                                    
        if self._phase == "goto_town" and self._transition.done:
            from scenes.town_scene import Chapter2Scene
            self._game.replace_scene(Chapter2Scene(self._game))

                                    
    CHAR_SCALE = 1.6


    def _draw_npc_frame(self, surface, frames_attr, frame_idx, x, y,
                        scale=1.6, facing_right=True):
        SPRITE_BASE_H = 96
        frames = getattr(self._game.assets, frames_attr, [])
        if not frames:
            return
        img = frames[frame_idx % len(frames)]
        orig_w, orig_h = img.get_size()
        if orig_h <= 0:
            return
        norm_w = int(orig_w * SPRITE_BASE_H / orig_h)
        normalized = pygame.transform.scale(img, (norm_w, SPRITE_BASE_H))
        new_w = int(norm_w * scale)
        new_h = int(SPRITE_BASE_H * scale)
        scaled = pygame.transform.scale(normalized, (new_w, new_h))
        if not facing_right:
            scaled = pygame.transform.flip(scaled, True, False)
        surface.blit(scaled, (x - new_w // 2, y - new_h))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._game.assets.bg_belairung, (0,0))

                                                                            
        self._draw_npc_frame(surface, "mage_idle_frames",        self._npc_mage_frame,
                             int(self._mage._x),   int(self._mage._y))
        self._draw_npc_frame(surface, "knight_idle_frames",      self._npc_knight_frame,
                             int(self._knight._x), int(self._knight._y))
                                      
        self._draw_npc_frame(surface, "king_aldric_idle_frames", self._npc_king_frame,
                             int(self._king._x),   int(self._king._y),
                             facing_right=self._king._facing_right)
        self.draw_char_scaled(surface, self._player, self.CHAR_SCALE)
        if self._phase in ("elena","goto_town","status_show"):
            self.draw_char_scaled(surface, self._elena, self.CHAR_SCALE)

                                                               
        if self._sword_visible:
            self._draw_sword(surface)

                  
        for p in self._particles:
            alpha = int(255 * p['life'] / p['max_life'])
            s = pygame.Surface((p['size']*2,p['size']*2),pygame.SRCALPHA)
            pygame.draw.circle(s, (*p['col'],alpha),(p['size'],p['size']),p['size'])
            surface.blit(s,(int(p['x'])-p['size'],int(p['y'])-p['size']))

        self._narrator.draw(surface)
        self._dialogue.draw(surface)
        members = [("Arga", self._player.hp, self._player.max_hp)]
        if self._game.flags.get("elena_joined"):
            members.append(("Elena", self._elena.hp, self._elena.max_hp))
        self._party_hud.draw(surface, members)
        self._transition.draw(surface)

        for ft in self._floats:
            ft.draw(surface)

                                                     

                       
        if self._show_status:
            self._status_win.draw(surface, self._player)

    def _draw_sword(self, surface):
        sx = self._game.W // 2
        sy = int(self._sword_y)
        assets = self._game.assets
        t = self._t

                                                                     
                                       
        for radius, color, base_alpha in [
            (70, (80, 140, 255), 35),              
            (45, (120, 180, 255), 55),               
            (25, (200, 220, 255), 70),                     
            (15, (255, 240, 160), 90),             
        ]:
            pulse = abs(math.sin(t * 2.5 + radius * 0.05))
            alpha = int(base_alpha + pulse * 30)
            gs = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(gs, (*color, alpha), (radius, radius), radius)
            surface.blit(gs, (sx - radius, sy - radius - 30))

                                                                      
        random.seed(int(t * 12) + 42)
        for i in range(18):
            seed_val = int(t * 8 + i * 137.5)
            random.seed(seed_val)
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(15, 65)
            px = sx + math.cos(angle + t * 0.7) * dist
            py = (sy - 30) + math.sin(angle * 1.3 + t * 0.5) * dist * 0.6
                                                               
            if i % 3 == 0:
                col = (255, int(200 + random.uniform(0, 55)), int(80 + random.uniform(0, 60)))         
            elif i % 3 == 1:
                col = (int(80 + random.uniform(0, 80)), int(150 + random.uniform(0, 80)), 255)         
            else:
                col = (int(150 + random.uniform(0, 80)), int(200 + random.uniform(0, 55)), 255)              
            size = random.randint(2, 5)
            alpha_p = int(120 + random.uniform(0, 100) * abs(math.sin(t * 3 + i)))
            ps = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*col, alpha_p), (size, size), size)
            surface.blit(ps, (int(px) - size, int(py) - size))

                                                                      
        beam_alpha = int(30 + abs(math.sin(t * 2)) * 40)
        beam_h = 200
        beam_surf = pygame.Surface((12, beam_h), pygame.SRCALPHA)
        for by in range(beam_h):
            t_fade = by / beam_h
            a = int(beam_alpha * (1.0 - t_fade) * (1.0 - t_fade))
            pygame.draw.line(beam_surf, (220, 200, 100, a), (6, by), (6, by))
        surface.blit(beam_surf, (sx - 6, sy - beam_h - 10))

                                                                    
        sword_drawn = False
        try:
            sword_sprite = assets.holy_sword
            if sword_sprite:
                                                          
                target_h = 160
                sw_orig, sh_orig = sword_sprite.get_size()
                if sh_orig > 0:
                    scale = target_h / sh_orig
                    sw = int(sw_orig * scale)
                    sh = target_h
                    scaled_sword = pygame.transform.scale(sword_sprite, (sw, sh))
                    surface.blit(scaled_sword, (sx - sw // 2, sy - sh + 30))
                    sword_drawn = True
        except Exception:
            pass

        if not sword_drawn:
                                              
            pygame.draw.polygon(surface, (220, 220, 240),
                                [(sx, sy-80), (sx-8, sy+40), (sx+8, sy+40)])
            pygame.draw.rect(surface, (200, 170, 50), (sx-22, sy+35, 44, 10))
            pygame.draw.rect(surface, (140, 110, 40), (sx-7, sy+44, 14, 24))

                                                                      
        random.seed(int(t * 6) + 99)
        for i in range(8):
            seed_val = int(t * 4 + i * 89.3)
            random.seed(seed_val)
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(30, 80)
            spx = sx + math.cos(angle + t * 1.2) * dist
            spy = (sy - 20) + math.sin(angle * 0.9 + t * 0.8) * dist * 0.5
            spark_alpha = int(150 + 80 * abs(math.sin(t * 4 + i)))
            star_col = (255, 240, 180, spark_alpha) if i % 2 == 0 else (160, 210, 255, spark_alpha)
            ss = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(ss, star_col, (3, 3), 3)
            surface.blit(ss, (int(spx) - 3, int(spy) - 3))
