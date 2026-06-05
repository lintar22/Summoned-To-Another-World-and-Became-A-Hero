
import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox


                                                                                 
                                                             
                                                                                 

                                                              
BGM_GLOAT  = "game_over_theme"

                                                    
BGM_REGRET = "regret_theme"

                                                     
BGM_RUIN   = "ruin_theme"

                                      
BGM_GLOAT_VOLUME  = 0.75
BGM_REGRET_VOLUME = 0.70
BGM_RUIN_VOLUME   = 0.65


                                                                                 
                  
                                                                                 

                                                    
GLOAT_DLGS = [
    ("Demon King", "...Hahaha."),
    ("Demon King", "Ini dia. Sang 'pahlawan' dari dunia lain yang begitu diagung-agungkan."),
    ("Demon King", "Tergeletak di hadapanku. Seperti sampah."),
    ("Arga",       "Ugh..."),
    ("Demon King", "Huh?...sih hidup toh baguss baguss. Aku ingin kau dengar ini dengan jelas."),
    ("Demon King", "Setiap doa yang manusia panjatkan untukmu, itu semua sia-sia."),
    ("Demon King", "Setiap harapan yang mereka titipkan padamu, sudah kupatahkan dengan mudah begitu saja."),
    ("Demon King", "Haha, kau tahu hal apa yang paling lucu?"),
    ("Demon King", "Itu semua terjadi karena kebodohanmu AHAHAHAHAHA!"),
    ("Demon King", "HANYA KARNA KEEGOISANMU. Dan semuanya....RUNTUH BEGITU AJA AHAHAHA."),
    ("Elena",      "Ar... ga..."),
    ("Demon King", "Lihat gadis itu.Dia memanggil namamu bahkan di saat-saat terakhirnya."),
    ("Demon King", "hah, itulah manusia. Makhluk yang tetap lemah sampai akhir."),
    ("Demon King", "Sungguh menyedihkan."),
    ("Arga",       "Keughh..."),
    ("Demon King", "Duniamu memanggil seorang pahlawan. Tapi yang datang... hanyalah kamu."),
    ("Demon King", "Tapi yang datang..hanyalah seorang manusia lemah yang hanya bisa bergantung dengan pedangnya tanpa tau potensi sebenarnnya pedan itu"),
    ("Demon King", "Selamat tinggal, Arga. Nikmatilah keputusasaanmu."),
    ("SYSTEM",     "Raja Iblis meninggalkan singgasananya, dan dibalik itu..."),
    ("SYSTEM",     "Tanpa tau apa yang terjadi dengan pahlawannya yang diagung-aungkan,kehancuran telah menunggu di depan mereka.."),
    
]

                             
REGRET_DLGS = [
    ("SYSTEM",  "...Hening. Hanya suara nafas terengah-engah yang tersisa."),
    ("Reno",    "...Keughhh...aku... harusnya lebih cepat."),
    ("Lyra",    "............................."),
    ("Darius",  "...Maaf. Aku gagal menjadi perisai kalian."),
    ("Elena",   "Arga... maafkan aku."),
    ("Arga",    "........................."),
    ("Elena",   "Arga.... Jawab aku."),
    ("Arga",    "...Bukan salah kalian."),
    ("Arga",    "Itu salahku. Sepenuhnya."),
    ("Arga",    "Aku pikir... satu serangan bisa mengakhiri segalanya."),
    ("Arga",    "Ternyata justru itu yang mengakhiri kita."),
    ("SYSTEM",  "Tidak ada yang menjawab."),
    ("SYSTEM",  "Keheningan itu terasa lebih menghancurkan dari semua serangan Raja Iblis."),
    ("SYSTEM",  "Dan di luar sana — dunia mulai terbakar."),
]

                                                                      
                                               
RUIN_NARRATIONS = [
                    
    "Tiga hari.",
    "Hanya tiga hari yang Raja Iblis butuhkan.",
    "",
                       
    "Pasukan kegelapan mengalir dari kastil seperti air bah yang tak bisa dibendung.",
    "Kota-kota yang pernah bercahaya padam satu per satu...seperti lilin ditiup angin.",
    "Ladang-ladang terbakar. Sungai mengering. Langit berubah merah.",
    "",
                       
    "Balairung Kerajaan Astravia yang megah roboh sebelum fajar hari kedua.",
    "Raja Aldric tidak melarikan diri. Ia memilih berdiri di takhta terakhirnya.",
    "Tidak ada yang tahu apa yang terjadi padanya setelah malam itu.",
    "Tidak ada yang berani mencari tahu.",
    "",
                     
    "Para warga yang tersisa berlari ke hutan — tanpa arah, tanpa harapan.",
    "Anak-anak yang pernah bermain di alun-alun kota kini bersembunyi dalam kegelapan.",
    "Nama-nama yang dulu dipanggil penuh kasih...kini hilang tanpa jejak.",
    "",
                    
    "Reno.",
    "Lyra.",
    "Darius.",
    "Elena.",
    "Nama-nama yang seharusnya dikenang sebagai pahlawan —",
    "— ditelan kegelapan bersama dunia yang mereka gagal selamatkan.",
    "",
                   
    "Dan Arga.",
    "Sang pahlawan yang dipanggil melintasi dunia.",
    "Yang datang dengan pedang, harapan, dan satu tekad yang terlalu besar untuk tubuhnya.",
    "Ia menghilang.",
    "Bukan sebagai pahlawan.",
    "Bukan sebagai pemenang.",
    "Hanya sebagai seorang anak muda yang membuat satu keputusan yang salah.",
    "",
                            
    "Manusia selalu berkata bahwa setiap kehidupan memiliki makna.",
    "Tapi tidak ada yang pernah menjelaskan...",
    "bagaimana rasanya menjadi seseorang",
    "yang bahkan tak diberi kesempatan",
    "untuk menemukannya.",
    "Berjuang.",
    "Gagal.",
    "Bangkit.",
    "Terjatuh lagi.",
    "Berulang.",
    "Dan berulang.",
    "Hingga suatu hari kau menyadari...",
    "tak ada seorang pun yang benar-benar melihat.",
    "Semua pujian akan lenyap.",
    "Semua kebencian akan lenyap.",
    "Semua cinta akan lenyap.",
    "Bahkan ingatan tentang dirimu",
    "akan perlahan terkikis oleh waktu.",
    "Karena waktu tidak mengenal belas kasihan.",
    "Ia mengubur raja.",
    "Ia mengubur pahlawan.",
    "Ia mengubur segalanya.",
    "Dan suatu hari...",
    "ia akan mengubur namamu juga.",
    "Dalam kegelapan yang sempurna,",
    "yang paling menakutkan bukanlah kesendirian.",
    "Melainkan kesadaran...",
    "bahwa mungkin dengan adanya keberadaan kita...",
    "tidak pernah mengubah apa pun.",
]


class BadEndScene(Scene):

    def __init__(self, game):
        super().__init__(game)
        self._t          = 0.0
        self._dlg_step   = 0
                                                             
        self._phase      = "demon_gloat"

        self._dialogue   = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator   = NarratorBox(game.W, game.H)

                     
        self._narr_index = 0
        self._narr_timer = 0.0
        self._narr_alpha = 0
        self._narr_phase = "fade_in"                                     

               
        self._final_timer = 0.0
        self._final_alpha = 0

                  
        self._ashes:  list[dict] = []
        self._embers: list[dict] = []
        self._blood_drops: list[dict] = []                                
        self._build_particles()

                                                              
        from entities.characters import Player, PartyNPC, BossNPC
        W, H = game.W, game.H
        self._ground_y = int(H * 0.82)
        gy = self._ground_y

                                                  
        self._CHAR_SCALE         = 1.6
        self._BOSS_SPRITE_SCALE  = 2.2
                                                                         
        self._PARTY_DEPTH_SCALES = [0.82 * 1.6, 1.0 * 1.6, 0.82 * 1.6, 1.0 * 1.6]
        _PARTY_FORMATION = [
            (-90,  -20),                   
            ( 60,  -15),                  
            (-160, -10),                  
            ( 120,   15),                   
        ]
        arga_x = int(W * 0.20)
        boss_x = int(W * 0.72)
        self._arga_x = arga_x
        self._boss_x = boss_x

                                                                  
        self._boss = BossNPC(boss_x, gy)

              
        self._player = Player(arga_x, gy)
        self._player.before_isekai = False
        self._player._anim_state = "hurt"
        self._player._frame_idx  = 2
        self._player._anim_once  = True
        self._player._anim_done  = True

                                                              
        self._elena  = PartyNPC("Elena",  arga_x + _PARTY_FORMATION[0][0], gy + _PARTY_FORMATION[0][1])
        self._reno   = PartyNPC("Reno",   arga_x + _PARTY_FORMATION[1][0], gy + _PARTY_FORMATION[1][1])
        self._lyra   = PartyNPC("Lyra",   arga_x + _PARTY_FORMATION[2][0], gy + _PARTY_FORMATION[2][1])
        self._darius = PartyNPC("Darius", arga_x + _PARTY_FORMATION[3][0], gy + _PARTY_FORMATION[3][1])

                                                    
        self._party_list = [
            (self._elena,  self._PARTY_DEPTH_SCALES[0]),
            (self._reno,   self._PARTY_DEPTH_SCALES[1]),
            (self._lyra,   self._PARTY_DEPTH_SCALES[2]),
            (self._darius, self._PARTY_DEPTH_SCALES[3]),
        ]

                                           
        for ch in (self._elena, self._reno, self._lyra, self._darius):
            ch._knocked_out = True

                                                                          

                        
        self._shake_timer = 0.0
        self._shake_x     = 0

                       
        self._pending_phase = ""
        self._waiting_fade  = False

                     
        self._ruin_debris = self._gen_ruin_debris(W, H)
        self._crack_lines = self._gen_crack_lines(W, H)

                                                              
        self._dark_orbs:   list[dict] = []                                
        self._void_sparks: list[dict] = []                              
        self._shadow_tendrils: list[dict] = []                                  

                                           
                                                      
        self._ruin_slides = ["bg_kota_hancur", "bg_dalam_belairung_hancur"]
        self._ruin_slide_idx   = 0                           
        self._ruin_slide_timer = 0.0                      
        self._ruin_slide_fade  = 0                                                           
        self._ruin_slide_state = "show"                                 
                                                                          
        _RUIN_SLIDE_DURATIONS = [22.0, 999.0]                                            
        self._ruin_slide_durations = _RUIN_SLIDE_DURATIONS

                   
        self._bgm_current = ""

        try:
            self._font_big    = pygame.font.SysFont("Georgia", 38, bold=True)
            self._font_sub    = pygame.font.SysFont("Georgia", 22, italic=True)
            self._font_narr   = pygame.font.SysFont("Georgia", 30, italic=True)
            self._font_narr_s = pygame.font.SysFont("Georgia", 24, italic=True)
            self._font_end    = pygame.font.SysFont("Georgia", 56, bold=True)
            self._font_hint   = pygame.font.SysFont("Consolas", 13)
            self._font_ui     = pygame.font.SysFont("Consolas", 13)
        except Exception:
            self._font_big    = pygame.font.Font(None, 42)
            self._font_sub    = pygame.font.Font(None, 26)
            self._font_narr   = pygame.font.Font(None, 34)
            self._font_narr_s = pygame.font.Font(None, 28)
            self._font_end    = pygame.font.Font(None, 60)
            self._font_hint   = pygame.font.Font(None, 17)
            self._font_ui     = pygame.font.Font(None, 16)

                                                                               

    def _play_bgm(self, key: str, volume: float, loops: int = -1):
        if self._bgm_current == key:
            return
        try:
            self._game.assets.play_bgm(key, loop=loops, volume=volume)
            self._bgm_current = key
        except Exception:
            pass

    def _stop_bgm(self, fadeout_ms: int = 1500):
        try:
            pygame.mixer.music.fadeout(fadeout_ms)
        except Exception:
            pass
        self._bgm_current = ""

                                                                               

    def _build_particles(self):
        W, H = self._game.W, self._game.H
        for _ in range(80):
            self._ashes.append({
                'x':     float(random.randint(0, W)),
                'y':     float(random.randint(-60, H)),
                'vx':    random.uniform(-30, 30),
                'vy':    random.uniform(15, 50),
                'size':  random.randint(2, 7),
                'alpha': random.randint(80, 180),
            })
        for _ in range(35):
            self._embers.append({
                'x':    float(random.randint(0, W)),
                'y':    float(H),
                'vx':   random.uniform(-18, 18),
                'vy':   random.uniform(-100, -30),
                'life': random.uniform(0.6, 2.5),
                'max':  2.5,
                'col':  random.choice([(210, 60, 10), (255, 120, 15), (255, 40, 5)]),
            })
                                                            
        for _ in range(20):
            self._blood_drops.append({
                'x': float(random.randint(40, self._game.W - 40)),
                'y': float(random.randint(int(self._game.H * 0.6), self._game.H - 20)),
                'r': random.randint(3, 10),
                'col': random.choice([(80, 0, 10), (60, 0, 8), (100, 10, 15)]),
            })

    def _gen_ruin_debris(self, W: int, H: int) -> list:
        debris = []
        gy = int(H * 0.82)
        for _ in range(15):
            x = random.randint(15, W - 15)
            y = random.randint(gy - 70, gy + 25)
            w = random.randint(25, 90)
            h = random.randint(12, 45)
            col = (random.randint(45, 85), random.randint(40, 75), random.randint(45, 80))
            angle = random.uniform(-40, 40)
            debris.append({'x': x, 'y': y, 'w': w, 'h': h, 'col': col, 'angle': angle})
        for i in range(6):
            x = i * (W // 6) + random.randint(-15, 15)
            debris.append({
                'x': x, 'y': gy - random.randint(50, 200),
                'w': 18, 'h': random.randint(50, 200),
                'col': (55, 50, 62), 'angle': random.uniform(-12, 12),
            })
        return debris

    def _gen_crack_lines(self, W: int, H: int) -> list:
        lines = []
        for _ in range(18):
            sx = random.randint(0, W)
            sy = random.randint(int(H * 0.4), H)
            length = random.randint(40, 130)
            angle  = random.uniform(0, math.pi * 2)
            segs   = random.randint(3, 7)
            pts    = [(sx, sy)]
            cx, cy = float(sx), float(sy)
            seg_len = length / segs
            for _ in range(segs):
                angle += random.uniform(-0.6, 0.6)
                cx += math.cos(angle) * seg_len
                cy += math.sin(angle) * seg_len
                pts.append((int(cx), int(cy)))
            lines.append({'pts': pts, 'alpha': random.randint(60, 130),
                          'width': random.choice([1, 1, 2])})
        return lines

                                                                               

    def _go_to_phase(self, new_phase: str, speed: int = 210,
                     color: tuple = (0, 0, 0)):
        self._pending_phase = new_phase
        self._waiting_fade  = True
        self._transition.fade_out(color=color, speed=speed)

                                                                               

    def on_enter(self) -> None:
        self._transition.fade_in(color=(0, 0, 0), speed=130)
        self._narrator.show(["BAD ENDING", "The Heroes Have Fallen"], 3.0)
        self._dialogue.show(GLOAT_DLGS[0][1], GLOAT_DLGS[0][0])
                              
        self._play_bgm(BGM_GLOAT, BGM_GLOAT_VOLUME)
        try:
            self._game.assets.play("damage")
        except Exception:
            pass

                                                                               

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                if self._waiting_fade:
                    return
                if self._phase == "final":
                    self._stop_bgm(800)
                    from scenes.opening_scene import OpeningScene
                    self._game.replace_scene(OpeningScene(self._game))
                    return
                if self._phase == "ruin_narration":
                                                                 
                    self._narr_timer = 999.0
                    return
                if not self._dialogue.is_finished:
                    self._dialogue.skip()
                else:
                    self._advance()

                                                                               

    def _advance(self):
        try:
            self._game.assets.play("cursor")
        except Exception:
            pass
        try: self._game.assets.play_sfx_file("space_enter_sfx")
        except Exception: pass

        if self._phase == "demon_gloat":
            self._dlg_step += 1
            if self._dlg_step < len(GLOAT_DLGS):
                spk, txt = GLOAT_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                                                              
                if self._dlg_step in (6, 14, 16):
                    self._shake_timer = 0.45
                if self._dlg_step == 16:
                    try:
                        self._game.assets.play("damage")
                    except Exception:
                        pass
            else:
                self._dlg_step = 0
                self._go_to_phase("regret", speed=180)

        elif self._phase == "regret":
            self._dlg_step += 1
            if self._dlg_step < len(REGRET_DLGS):
                spk, txt = REGRET_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
            else:
                self._dlg_step = 0
                self._go_to_phase("ruin_narration", speed=150)

                                                                               

    def update(self, dt: float) -> None:
        self._t += dt
        self._transition.update(dt)
        self._dialogue.update(dt)
        self._narrator.update(dt)

                                         
        if self._waiting_fade and self._transition.done:
            self._waiting_fade  = False
            self._phase         = self._pending_phase
            self._pending_phase = ""
            self._dlg_step      = 0
            self._on_phase_enter()

                                                 
        self._player.update(dt)
        self._player._anim_state = "hurt"
        self._player._frame_idx  = 2
        self._player._anim_done  = True
        self._elena.update(dt)
        self._reno.update(dt)
        self._lyra.update(dt)
        self._darius.update(dt)
        self._boss.update(dt)

               
        if self._shake_timer > 0:
            self._shake_timer -= dt
            self._shake_x = random.randint(-6, 6) if self._shake_timer > 0 else 0
        else:
            self._shake_x = 0

             
        for a in self._ashes:
            a['x'] += a['vx'] * dt
            a['y'] += a['vy'] * dt
            if a['y'] > self._game.H + 20:
                a['y'] = -12.0
                a['x'] = float(random.randint(0, self._game.W))

              
        for e in self._embers:
            e['x']  += e['vx'] * dt
            e['y']  += e['vy'] * dt
            e['vy'] += 50 * dt
            e['life'] -= dt
        self._embers = [e for e in self._embers if e['life'] > 0]
                                           
        if self._phase == "ruin_narration":
            while len(self._embers) < 55:
                W, H = self._game.W, self._game.H
                self._embers.append({
                    'x':   float(random.randint(0, W)),
                    'y':   float(H + 5),
                    'vx':  random.uniform(-22, 22),
                    'vy':  random.uniform(-110, -40),
                    'life': random.uniform(1.0, 3.0),
                    'max': 3.0,
                    'col': random.choice([(210, 55, 5), (255, 110, 10),
                                          (255, 30, 0), (180, 40, 0)]),
                })

                                                                                                
        if self._phase == "ruin_narration":
            W, H = self._game.W, self._game.H
                                                                    
            for orb in self._dark_orbs:
                orb['x'] += orb['vx'] * dt
                orb['y'] += math.sin(self._t * orb['freq'] + orb['phase']) * orb['amp'] * dt
                orb['y'] -= orb['rise'] * dt
                orb['life'] -= dt
                if orb['life'] <= 0 or orb['y'] < -40:
                    orb['x']    = float(random.randint(0, W))
                    orb['y']    = float(random.randint(int(H * 0.5), H))
                    orb['life'] = random.uniform(3.0, 7.0)
            while len(self._dark_orbs) < 18:
                self._dark_orbs.append({
                    'x':     float(random.randint(0, W)),
                    'y':     float(random.randint(int(H * 0.3), H)),
                    'vx':    random.uniform(-18, 18),
                    'rise':  random.uniform(8, 30),
                    'freq':  random.uniform(0.8, 2.5),
                    'amp':   random.uniform(15, 45),
                    'phase': random.uniform(0, math.pi * 2),
                    'r':     random.randint(6, 18),
                    'col':   random.choice([
                        (20, 0, 40), (40, 0, 60), (10, 0, 30),
                        (50, 0, 80), (30, 0, 50),
                    ]),
                    'life':  random.uniform(3.0, 7.0),
                })
                                                                 
            for sp in self._void_sparks:
                sp['x']   += sp['vx'] * dt
                sp['y']   += sp['vy'] * dt
                sp['vy']  -= 15 * dt                             
                sp['life'] -= dt
            self._void_sparks = [s for s in self._void_sparks if s['life'] > 0]
            while len(self._void_sparks) < 40:
                self._void_sparks.append({
                    'x':   float(random.randint(0, W)),
                    'y':   float(H + 5),
                    'vx':  random.uniform(-35, 35),
                    'vy':  random.uniform(-90, -25),
                    'life': random.uniform(0.4, 1.8),
                    'max': 1.8,
                    'col': random.choice([
                        (80, 0, 120), (100, 0, 160), (60, 0, 100),
                        (120, 0, 200), (40, 0, 80), (160, 20, 255),
                    ]),
                    'r':   random.randint(2, 5),
                })
                                                                           
            for td in self._shadow_tendrils:
                td['progress'] += td['speed'] * dt
                td['wobble']   += dt
                td['life']     -= dt
            self._shadow_tendrils = [
                t for t in self._shadow_tendrils if t['life'] > 0 and t['progress'] < 1.5
            ]
            if random.random() < dt * 3.5:
                bx = float(random.randint(30, W - 30))
                self._shadow_tendrils.append({
                    'bx':      bx,
                    'by':      float(H),
                    'height':  random.randint(int(H * 0.25), int(H * 0.65)),
                    'wobble':  random.uniform(0, math.pi * 2),
                    'wfreq':   random.uniform(1.5, 4.0),
                    'wamp':    random.randint(10, 30),
                    'progress': 0.0,
                    'speed':   random.uniform(0.25, 0.55),
                    'col':     random.choice([
                        (25, 0, 45, 160), (40, 0, 70, 140),
                        (15, 0, 35, 180), (60, 0, 100, 120),
                    ]),
                    'width':   random.randint(2, 5),
                    'life':    random.uniform(1.5, 3.5),
                })

                     
        if self._phase == "ruin_narration":
            self._update_ruin_narration(dt)
            self._update_ruin_slideshow(dt)

                       
        if self._phase == "final":
            self._final_timer += dt
            self._final_alpha  = min(255, int(255 * self._final_timer / 2.8))

    def _update_ruin_narration(self, dt: float):
        self._narr_timer += dt

        if self._narr_phase == "fade_in":
            self._narr_alpha = min(255, int(255 * self._narr_timer / 1.1))
            if self._narr_timer >= 1.1:
                self._narr_phase = "hold"
                self._narr_timer = 0.0

        elif self._narr_phase == "hold":
            self._narr_alpha = 255
            txt = RUIN_NARRATIONS[self._narr_index] if self._narr_index < len(RUIN_NARRATIONS) else ""
                                                                        
            hold = 0.6 if txt == "" else 3.2
                                            
            if self._narr_index >= len(RUIN_NARRATIONS) - 3:
                hold = 4.0
            if self._narr_timer >= hold:
                self._narr_phase = "fade_out"
                self._narr_timer = 0.0

        elif self._narr_phase == "fade_out":
            self._narr_alpha = max(0, 255 - int(255 * self._narr_timer / 0.85))
            if self._narr_timer >= 0.85:
                self._narr_index += 1
                if self._narr_index >= len(RUIN_NARRATIONS):
                                                  
                    self._phase       = "final"
                    self._final_timer = 0.0
                else:
                    self._narr_phase = "fade_in"
                    self._narr_timer = 0.0

    def _on_phase_enter(self):
        if self._phase == "regret":
            self._transition.fade_in(speed=150)
            self._narrator.show(["Di Dalam Kegelapan yang Tersisa..."], 2.0)
            self._dialogue.show(REGRET_DLGS[0][1], REGRET_DLGS[0][0])
                                                                  
            self._stop_bgm(fadeout_ms=1500)
            self._play_bgm(BGM_REGRET, BGM_REGRET_VOLUME)
                                                                 
            W = self._game.W
            cx = W // 2
            self._player._x  = cx
            self._elena._x   = cx - 100
            self._reno._x    = cx + 110
            self._lyra._x    = cx - 190
            self._darius._x  = cx + 200

        elif self._phase == "ruin_narration":
            self._transition.fade_in(color=(0, 0, 0), speed=100)
            self._narr_index = 0
            self._narr_timer = 0.0
            self._narr_alpha = 0
            self._narr_phase = "fade_in"
                                
            self._ruin_slide_idx   = 0
            self._ruin_slide_timer = 0.0
            self._ruin_slide_fade  = 0
            self._ruin_slide_state = "show"
                                                          
            self._stop_bgm(fadeout_ms=2000)
            self._play_bgm(BGM_RUIN, BGM_RUIN_VOLUME)

        elif self._phase == "final":
            pass                     

                                                                               

    def draw(self, surface: pygame.Surface) -> None:
        W, H = self._game.W, self._game.H
        sx   = self._shake_x

                                                                               
        if self._phase == "demon_gloat":
            surface.blit(self._game.assets.bg_ruang_boss_rusak, (sx, 0))
                                                        
            dark = pygame.Surface((W, H), pygame.SRCALPHA)
            dark.fill((40, 0, 0, 90))
            surface.blit(dark, (0, 0))
                                             
            self._draw_blood_drops(surface)
                             
            self._draw_crack_lines(surface)
                                                           
            for ch, ds in reversed(self._party_list):
                self.draw_char_scaled(surface, ch, ds)
            self.draw_char_scaled(surface, self._player, self._CHAR_SCALE)
                                                     
            self.draw_char_scaled(surface, self._boss, self._BOSS_SPRITE_SCALE)
            self._draw_ko_labels(surface)
                          
            self._draw_ashes(surface)

                                                                               
        elif self._phase == "regret":
            surface.blit(self._game.assets.bg_ruang_boss_rusak, (sx, 0))
                                                            
            dark = pygame.Surface((W, H), pygame.SRCALPHA)
            dark.fill((0, 0, 0, 140))
            surface.blit(dark, (0, 0))
            self._draw_crack_lines(surface)
            for ch, ds in reversed(self._party_list):
                self.draw_char_scaled(surface, ch, ds)
            self.draw_char_scaled(surface, self._player, self._CHAR_SCALE)
            self._draw_ashes(surface)
                                                                              
            self._draw_guilt_aura(surface)

                                                                               
        elif self._phase == "ruin_narration":
                                                               
            self._draw_ruin_slideshow(surface)
                                                                                       
            self._draw_darkness_particles(surface)
                                         
            self._draw_embers(surface)
                                          
            self._draw_vignette(surface)
                    
            self._draw_narration_text(surface)

                                                                               
        elif self._phase == "final":
            self._draw_ruin_background(surface)
            self._draw_fire_backdrop(surface)
            self._draw_ashes(surface)
            self._draw_vignette(surface)
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, min(200, self._final_alpha)))
            surface.blit(ov, (0, 0))
            if self._final_alpha > 70:
                a2 = min(255, (self._final_alpha - 70) * 3)
                self._draw_final_text(surface, a2)

                 
        self._narrator.draw(surface)
                                                                                               
        if self._phase != "ruin_narration":
            self._dialogue.draw(surface)
        self._transition.draw(surface)

                      
        lbl_map = {
            "Final Chapter": "Singgasana Kegelapan — Setelah Kekalahan",
            "Final Chapter":  "Singgasana Kegelapan — Dalam Keheningan",
        }
        lbl = lbl_map.get(self._phase, "")
        if lbl:
            try:
                t = self._font_ui.render(lbl, True, (160, 80, 80))
                surface.blit(t, (W // 2 - t.get_width() // 2, 8))
            except Exception:
                pass

                                                                               

    def _draw_ko_labels(self, surface: pygame.Surface):
        chars = [
            (self._player, "Arga"),
            (self._elena,  "Elena"),
            (self._reno,   "Reno"),
            (self._lyra,   "Lyra"),
            (self._darius, "Darius"),
        ]
        try:
            f = pygame.font.SysFont("Georgia", 13, bold=True)
            for ch, name in chars:
                t = f.render("✕  KO", True, (200, 40, 40))
                                                                                    
                surface.blit(t, (int(ch._x) - t.get_width() // 2,
                                 int(ch._y) - 160))
        except Exception:
            pass

    def _draw_blood_drops(self, surface: pygame.Surface):
        for d in self._blood_drops:
            s = pygame.Surface((d['r'] * 2, d['r'] * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (*d['col'], 160),
                                (0, 0, d['r'] * 2, d['r'] // 2 * 2 + d['r']))
            surface.blit(s, (int(d['x']) - d['r'], int(d['y']) - d['r'] // 2))

    def _draw_crack_lines(self, surface: pygame.Surface):
        for ln in self._crack_lines:
            if len(ln['pts']) < 2:
                continue
            try:
                s = pygame.Surface((self._game.W, self._game.H), pygame.SRCALPHA)
                pygame.draw.lines(s, (20, 15, 20, ln['alpha']),
                                  False, ln['pts'], ln['width'])
                surface.blit(s, (0, 0))
            except Exception:
                pass

    def _draw_guilt_aura(self, surface: pygame.Surface):
        px, py = int(self._player._x), int(self._player._y)
        pulse  = math.sin(self._t * 2.2) * 0.5 + 0.5
        for r in range(50, 10, -8):
            alpha = int(30 * pulse * (1 - r / 55))
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (120, 0, 0, alpha), (r, r), r)
            surface.blit(s, (px - r, py - 20 - r))

    def _draw_ashes(self, surface: pygame.Surface):
        for a in self._ashes:
            s = pygame.Surface((a['size'], a['size']), pygame.SRCALPHA)
            pygame.draw.rect(s, (130, 120, 115, a['alpha']),
                             (0, 0, a['size'], a['size']))
            surface.blit(s, (int(a['x']), int(a['y'])))

    def _draw_embers(self, surface: pygame.Surface):
        for e in self._embers:
            alpha = int(255 * max(0, e['life'] / e['max']))
            sz = 3
            s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*e['col'], alpha), (sz, sz), sz)
            surface.blit(s, (int(e['x']) - sz, int(e['y']) - sz))

    def _draw_fire_backdrop(self, surface: pygame.Surface):
        W, H = self._game.W, self._game.H
        for i in range(14):
            fx = int(i * (W // 14) + math.sin(self._t * 2.8 + i * 0.9) * 22)
            fh = int(80 + math.sin(self._t * 4.0 + i * 0.7) * 45)
                                     
            col_a = int(120 + 70 * abs(math.sin(self._t * 3.5 + i)))
            s = pygame.Surface((40, fh), pygame.SRCALPHA)
            pygame.draw.polygon(s, (170, 40, 5, col_a),
                                [(0, fh), (20, 0), (40, fh)])
                                      
            ih = int(fh * 0.6)
            pygame.draw.polygon(s, (255, 120, 10, col_a // 2),
                                [(10, fh), (20, fh - ih), (30, fh)])
            surface.blit(s, (fx, H - fh - 40))

    def _draw_ruin_background(self, surface: pygame.Surface):
        W, H = self._game.W, self._game.H
        for y in range(H):
            t = y / H
                                                           
            r = int(5  + 50  * t)
            g = int(0  + 4   * t)
            b = int(0  + 4   * t)
            pygame.draw.line(surface, (r, g, b), (0, y), (W, y))

    def _draw_ruin_debris_visual(self, surface: pygame.Surface):
        try:
            for d in self._ruin_debris:
                tmp = pygame.Surface((d['w'], d['h']), pygame.SRCALPHA)
                pygame.draw.rect(tmp, (*d['col'], 210),
                                 (0, 0, d['w'], d['h']), border_radius=2)
                                 
                pygame.draw.line(tmp, (25, 20, 25),
                                 (2, 3), (d['w'] - 3, d['h'] - 4), 1)
                rot = pygame.transform.rotate(tmp, d['angle'])
                surface.blit(rot, (d['x'] - rot.get_width() // 2,
                                   d['y'] - rot.get_height() // 2))
        except Exception:
            pass

                              
        W, H = self._game.W, self._game.H
        gy   = self._ground_y
        towers = [
            (60,      gy - 160, 28, 160),
            (220,     gy - 90,  22, 90),
            (W - 70,  gy - 180, 32, 180),
            (W - 230, gy - 70,  20, 70),
            (W // 2 - 80, gy - 120, 18, 120),
        ]
        for tx, ty, tw, th in towers:
            pygame.draw.rect(surface, (22, 18, 25),
                             pygame.Rect(tx - tw // 2, ty, tw, th))
                                               
            pts = [
                (tx - tw // 2, ty),
                (tx - tw // 3 + random.randint(-4, 4), ty - 25),
                (tx,           ty - random.randint(18, 38)),
                (tx + tw // 3 + random.randint(-4, 4), ty - 12),
                (tx + tw // 2, ty),
            ]
            pygame.draw.polygon(surface, (18, 14, 20), pts)

                     
        crack_col = (30, 20, 22)
        for i in range(8):
            x1 = random.randint(0, W)
            y1 = gy + random.randint(-10, 20)
            x2 = x1 + random.randint(-80, 80)
            y2 = y1 + random.randint(5, 30)
            pygame.draw.line(surface, crack_col, (x1, y1), (x2, y2), 2)

    def _update_ruin_slideshow(self, dt: float):
        if self._ruin_slide_idx >= len(self._ruin_slides):
            return

        if self._ruin_slide_state == "show":
            self._ruin_slide_timer += dt
            max_dur = (self._ruin_slide_durations[self._ruin_slide_idx]
                       if self._ruin_slide_idx < len(self._ruin_slide_durations)
                       else 999.0)
            if self._ruin_slide_timer >= max_dur:
                if self._ruin_slide_idx + 1 < len(self._ruin_slides):
                    self._ruin_slide_state = "fadeout"
                    self._ruin_slide_timer = 0.0

        elif self._ruin_slide_state == "fadeout":
            self._ruin_slide_timer += dt
            self._ruin_slide_fade = min(255, int(255 * self._ruin_slide_timer / 1.2))
            if self._ruin_slide_timer >= 1.2:
                self._ruin_slide_idx  += 1
                self._ruin_slide_timer = 0.0
                self._ruin_slide_state = "fadein"
                self._ruin_slide_fade  = 255

        elif self._ruin_slide_state == "fadein":
            self._ruin_slide_timer += dt
            self._ruin_slide_fade = max(0, 255 - int(255 * self._ruin_slide_timer / 1.2))
            if self._ruin_slide_timer >= 1.2:
                self._ruin_slide_state = "show"
                self._ruin_slide_timer = 0.0
                self._ruin_slide_fade  = 0

    def _draw_ruin_slideshow(self, surface: pygame.Surface):
        W, H = self._game.W, self._game.H

                               
        idx = min(self._ruin_slide_idx, len(self._ruin_slides) - 1)
        attr = self._ruin_slides[idx]
        bg = getattr(self._game.assets, attr, None)
        if bg:
            surface.blit(bg, (0, 0))
        else:
                                          
            for y in range(H):
                t = y / H
                r = int(5 + 50 * t)
                pygame.draw.line(surface, (r, 0, 0), (0, y), (W, y))

                                                        
        dark = pygame.Surface((W, H), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 80))
        surface.blit(dark, (0, 0))

                                      
        if self._ruin_slide_fade > 0:
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, self._ruin_slide_fade))
            surface.blit(ov, (0, 0))

    def _draw_darkness_particles(self, surface: pygame.Surface):
        W, H = self._game.W, self._game.H

                                                                
        for td in self._shadow_tendrils:
            pts = []
            steps = 12
            for i in range(steps + 1):
                frac = (i / steps) * td['progress']
                if frac > 1.0:
                    break
                ty = td['by'] - frac * td['height']
                tx = td['bx'] + math.sin(td['wobble'] + frac * td['wfreq'] * math.pi) * td['wamp']
                pts.append((int(tx), int(ty)))
            if len(pts) >= 2:
                life_r = max(0.0, td['life'] / 3.5)
                alpha  = int(td['col'][3] * min(1.0, life_r * 2))
                try:
                    ts = pygame.Surface((W, H), pygame.SRCALPHA)
                    pygame.draw.lines(ts, (*td['col'][:3], alpha), False, pts, td['width'])
                    surface.blit(ts, (0, 0))
                except Exception:
                    pass

                                                  
        for orb in self._dark_orbs:
            r = orb['r']
            col = orb['col']
            try:
                os_ = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
                            
                pygame.draw.circle(os_, (*col, 200), (r * 2, r * 2), r)
                                 
                pygame.draw.circle(os_, (*col, 60), (r * 2, r * 2), r + r // 2)
                surface.blit(os_, (int(orb['x']) - r * 2, int(orb['y']) - r * 2))
            except Exception:
                pass

                                           
        for sp in self._void_sparks:
            life_r = sp['life'] / sp['max']
            alpha  = int(200 * min(life_r * 3, 1.0))
            r = sp['r']
            try:
                ss = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
                pygame.draw.circle(ss, (*sp['col'], alpha), (r + 1, r + 1), r)
                surface.blit(ss, (int(sp['x']) - r, int(sp['y']) - r))
            except Exception:
                pass

    def _draw_vignette(self, surface: pygame.Surface):
        W, H = self._game.W, self._game.H
        vgn  = pygame.Surface((W, H), pygame.SRCALPHA)
                    
        strength = 180
        for i in range(80):
            t = i / 80
            a = int(strength * (1 - t) ** 2)
            pygame.draw.rect(vgn, (0, 0, 0, a),
                             pygame.Rect(i, i, W - i * 2, H - i * 2), 1)
        surface.blit(vgn, (0, 0))

    def _draw_narration_text(self, surface: pygame.Surface):
        W, H = self._game.W, self._game.H
        if self._narr_index >= len(RUIN_NARRATIONS):
            return
        txt = RUIN_NARRATIONS[self._narr_index]
        if txt == "":
            return                                                        

        try:
            is_header = (txt.endswith(".") and len(txt) < 20 and
                         not txt.startswith("Dan") and not txt.startswith("Hanya"))
            is_closing = self._narr_index >= len(RUIN_NARRATIONS) - 5

            if is_closing:
                                                              
                col  = (160, 60, 60)
                font = self._font_narr_s
            elif is_header:
                                                                            
                col  = (210, 195, 185)
                font = self._font_narr
            else:
                col  = (180, 165, 155)
                font = self._font_narr_s

            surf = font.render(txt, True, col)
            surf.set_alpha(self._narr_alpha)

                                             
            tx = W // 2 - surf.get_width() // 2
            ty = H // 2 - surf.get_height() // 2

                                  
            if self._narr_alpha > 30:
                line_w = min(surf.get_width() + 60, W - 80)
                line_a = self._narr_alpha // 3
                ls = pygame.Surface((line_w, 1), pygame.SRCALPHA)
                ls.fill((120, 50, 50, line_a))
                surface.blit(ls, (W // 2 - line_w // 2, ty - 14))
                surface.blit(ls, (W // 2 - line_w // 2, ty + surf.get_height() + 10))

            surface.blit(surf, (tx, ty))

        except Exception:
            pass

                                                                 
        if self._narr_alpha > 220:
            try:
                h = self._font_hint.render("[ SPACE untuk lanjut ]",
                                           True, (90, 70, 70))
                surface.blit(h, (W // 2 - h.get_width() // 2, H - 36))
            except Exception:
                pass

    def _draw_final_text(self, surface: pygame.Surface, alpha: int):
        W, H = self._game.W, self._game.H
        lines = [
            (self._font_end,  "BAD END",                            (200, 40, 40),  H // 2 - 80),
            (self._font_sub,  "The Heroes Failed to Save the World.", (160, 110, 110), H // 2),
            (self._font_hint, "[ SPACE / ENTER untuk coba lagi ]",  (100, 85, 85), H // 2 + 110),
        ]
        for font, text, col, y in lines:
            surf = font.render(text, True, col)
            surf.set_alpha(alpha)
            surface.blit(surf, (W // 2 - surf.get_width() // 2, y))