
import pygame
import random
import math
import copy
from engine.base import Scene
from battle.battle_scene import SlashEffect, DivineSlashEffect, CelestialFlameEffect
from engine.colors import *
from ui.components import (
    DialogueBox, TransitionScreen, FloatingText, NarratorBox, PartyHUD
)


                                                               
           
                                                               

DEMON_KING_DATA = {
    "name":    "Demon King",
    "hp":      9999,
    "max_hp":  9999,
    "atk":     80,
    "def":     40,
}

                                            
PARTY_MAX_HP = {
    "Arga":   500,
    "Elena":  380,
    "Reno":   350,
    "Lyra":   320,
    "Darius": 450,
}

                                                               
            
                                                               

ARGA_BOSS_SKILLS = {
    "Attack": {
        "dmg_base": 800, "mp": 0,
        "type": "physical",
        "desc": "Serangan pedang biasa",
        "color": GOLD_LIGHT,
        "anim": "attack",
    },
    "Divine Slash": {
        "dmg_base": 1200, "mp": 0,
        "type": "physical",
        "desc": "Tebasan pedang suci",
        "color": HOLY_WHITE,
        "anim": "attack",
    },
    "Celestial Flame": {
        "dmg_base": 1400, "mp": 0,
        "type": "magic",
        "desc": "Api surgawi yang membakar",
        "color": MAGIC_BLUE,
        "anim": "attack",
    },
}

                                                               
                                 
                                                               

BOSS_SKILLS_P1 = [
    {
        "name":    "Dark Claw",
        "dmg":     (60, 100),                                           
        "target":  "single_random",                          
        "msg":     "Dark Claw! Cakar kegelapan menghantam party!",
        "color":   DAMAGE_RED,
        "anim":    "attack",
    },
    {
        "name":    "Shadow Wave",
        "dmg":     (40, 70),
        "target":  "all_party",                           
        "msg":     "Shadow Wave! Gelombang kegelapan menyapu party!",
        "color":   (160, 60, 200),
        "anim":    "attack",
    },
]

                                                               
                                 
                                                               

BOSS_SKILLS_P2 = [
    {
        "name":    "Dark Claw",
        "dmg":     (80, 130),
        "target":  "single_random",
        "msg":     "Dark Claw! Serangan lebih ganas di Phase 2!",
        "color":   DAMAGE_RED,
        "anim":    "attack",
    },
    {
        "name":    "Shadow Wave",
        "dmg":     (60, 90),
        "target":  "all_party",
        "msg":     "Shadow Wave! Gelombang semakin kuat!",
        "color":   (160, 60, 200),
        "anim":    "attack",
    },
    {
        "name":    "Void Burst",
        "dmg":     (90, 140),
        "target":  "two_random",                             
        "msg":     "Void Burst! Ledakan kehampaan melukai dua anggota!",
        "color":   (200, 80, 255),
        "anim":    "attack",
    },
    {
        "name":    "Soul Drain",
        "dmg":     (70, 110),
        "target":  "arga_focused",                        
        "msg":     "Soul Drain! Demon King memfokuskan serangan ke Arga!",
        "color":   (255, 60, 100),
        "anim":    "attack",
    },
]

                                                               
                                       
                                                               

BOSS_ULTIMATE = {
    "name":  "Apocalypse",
    "msg":   "APOCALYPSE! Kekuatan Demon King meledak!",
    "color": (255, 100, 20),
    "anim":  "ultimate",
                                                         
}

                                                               
        
                                                               

PHASE2_ENTRY_MSG = [
    "⚠ Kekuatan Demon King berlipat ganda!",
    "PHASE 2 — ENRAGE MODE!",
]

CRISIS_DIALOGS = [
    ("Demon King", "Hahaha..."),
    ("SYSTEM",     "Ledakan dahsyat menyapu seluruh ruangan!"),
    ("SYSTEM",     "Seluruh party pahlawan hampir tewas... HP semua tersisa 5%!"),
    ("Arga",       "Gh... Sialan!..."),
    ("SYSTEM",     "PILIHAN KRITIS — Apa yang kamu lakukan?"),
]

TRUE_END_DIALOGS = [
    ("SYSTEM",  "Sebuah cahaya emas memancar dari Holy Sword Arga!"),
    ("Elena",   "Ar... Arga...! Ini... kekuatan apa ini?!"),
    ("Arga",    "Aku tidak akan membiarkan kalian mati di sini. TIDAK AKAN!"),
    ("SYSTEM",  "Aura Shield! Holy Sword bereaksi dan melindungi seluruh party!"),
    ("Lyra",    "Hah,  luka kita... sudah hilang?! Ini mustahil!"),
    ("Reno",    "Arga, kau luar biasa gila! TAPI AKU SUKA! SERANG!!"),
    ("Darius",  "Ini kesempatan kita!"),
    ("Arga",    "Terimalah ini!!!!!!!! CELESTIAL OVERDRIVE!!!"),
]

BAD_END_DIALOGS = [
    ("Arga",       "Hadapi aku...sialn...aku tidak akan membiarkanmu lolos begitu saja!"),
    ("Reno",       "Arga, kau gila?! Kita tidak bisa—"),
    ("SYSTEM",     "Arga memaksakan menyerang... tapi kekuatannya tidak berarti apa-apa di hadapan Demon King."),
    ("Demon King", "Hahaha... lihatlah manusia lemah nan sombong ini"),
]

VICTORY_DIALOGS = [
    ("SYSTEM",     "Serangan terakhir menghantam Demon King!"),
    ("Demon King", "Mustahil... kekuatan manusia... tidak seharusnya...bisa..keugh.."),
    ("SYSTEM",     "Demon King hancur menjadi debu cahaya!"),
    ("Arga",       "...Berakhir sudah."),
    ("Elena",      "Kita berhasil... kita benar-benar berhasil!"),
    ("SYSTEM",     "VICTORY — Demon King Berhasil Dikalahkan!"),
]


                                                               
                   
                                                               


                                                               
                     
                                                               

class BossClawEffect:
    def __init__(self, boss_x, boss_y, target_x, target_y):
        self.t = 0.0
        self.lifetime = 0.5
        self.alive = True
                                        
        spreads = [(-22, -15), (0, 0), (22, 15)]
        self.claws = []
        for sx, sy in spreads:
            self.claws.append({
                "sx": boss_x + sx,
                "sy": boss_y + sy,
                "tx": target_x + sx,
                "ty": target_y + sy,
            })

    def update(self, dt):
        self.t += dt
        if self.t >= self.lifetime:
            self.alive = False

    def draw(self, surface):
        if not self.alive:
            return
        prog = self.t / self.lifetime
        alpha = int(255 * (1.0 - prog))
        surf = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
                                                             
        reveal = min(1.0, prog / 0.4)
        for c in self.claws:
                                  
            ex = int(c["sx"] + (c["tx"] - c["sx"]) * reveal)
            ey = int(c["sy"] + (c["ty"] - c["sy"]) * reveal)
            sx = int(c["sx"])
            sy = int(c["sy"])
                                           
            pygame.draw.line(surf, (200, 0, 50, alpha), (sx, sy), (ex, ey), 8)
                                
            pygame.draw.line(surf, (255, 100, 100, min(255, alpha + 60)),
                             (sx, sy), (ex, ey), 3)
        surface.blit(surf, (0, 0))


class BlackWaveEffect:
    def __init__(self, boss_x, boss_y, screen_w, screen_h):
        self.t = 0.0
        self.lifetime = 0.8
        self.alive = True
        self.bx = boss_x
        self.by = boss_y
        self.sw = screen_w
        self.sh = screen_h

    def update(self, dt):
        self.t += dt
        if self.t >= self.lifetime:
            self.alive = False

    def draw(self, surface):
        if not self.alive:
            return
        prog = self.t / self.lifetime
        surf = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)

                                             
        max_r = int(math.hypot(self.sw, self.sh) * 1.1)
        waves = 3
        for i in range(waves):
            phase = (prog + i / waves) % 1.0
            r = int(max_r * phase)
            alpha = int(200 * (1.0 - phase))
            thick = max(2, int(30 * (1.0 - phase)))
                                        
            rb = int(80 * (1.0 - phase))
            gb = 0
            bb = int(120 * (1.0 - phase))
            pygame.draw.circle(surf, (rb, gb, bb, alpha),
                               (int(self.bx), int(self.by)), max(1, r), thick)

                                   
        if prog < 0.3:
            dark_alpha = int(160 * (1.0 - prog / 0.3))
            pygame.draw.rect(surf, (0, 0, 0, dark_alpha), (0, 0, self.sw, self.sh))

                                           
        if 0.2 < prog < 0.7:
            burst_prog = (prog - 0.2) / 0.5
            for i in range(8):
                angle = i * math.pi / 4 + prog * 5
                dist = int(200 * burst_prog)
                px = int(self.bx - dist * math.cos(angle))
                py = int(self.by - dist * math.sin(angle) * 0.4)
                r_spark = max(1, int(18 * (1.0 - burst_prog)))
                a_spark = int(180 * (1.0 - burst_prog))
                pygame.draw.circle(surf, (60, 0, 100, a_spark), (px, py), r_spark)

        surface.blit(surf, (0, 0))

class BossBattleScene(Scene):

                             
    _ARGA_X_RATIO    = 0.20
    _BOSS_X_RATIO    = 0.72
                                                                                           
    _CHAR_Y_RATIO    = 0.72
    _PARTY_FORMATION = [
        (-90,  -20),                                    
        ( 60,  -15),                                  
        (-160, -10),                                      
        ( 120,   15),                                       
    ]

                                                     
    _CHAR_SCALE         = 1.6
    _PARTY_DEPTH_SCALES = [0.82 * 1.6, 1.0 * 1.6, 0.82 * 1.6, 1.0 * 1.6]
    _BOSS_SPRITE_SCALE  = 2.2                                         
    _PARTY_ASSET_MAP = {
        "elena":  {"idle": "elena_idle_frames",  "label": "Elena"},
        "lyra":   {"idle": "lyra_idle_frames",   "label": "Lyra"},
        "darius": {"idle": "darius_idle_frames", "label": "Darius"},
        "reno":   {"idle": "reno_idle_frames",   "label": "Reno"},
    }
    _PARTY_ORDER = ["elena", "reno", "lyra", "darius"]

    def __init__(self, game):
        super().__init__(game)

                                           
        self._boss = copy.deepcopy(DEMON_KING_DATA)

                                  
        self._party_hp: dict[str, int] = {
            name: hp for name, hp in PARTY_MAX_HP.items()
        }
        self._party_dead: dict[str, bool] = {name: False for name in PARTY_MAX_HP}
        self._party_shield: dict[str, bool] = {name: False for name in PARTY_MAX_HP}

                           
                                                                    
                                             
                                                                           
                                       
        self._phase     = "intro"
        self._t         = 0.0
        self._anim_t    = 0.0
        self._shake_t   = 0.0
        self._shake_x   = 0
        self._flash_alpha = 0
        self._flash_color = GOLD_LIGHT

                                       
                                                       
                                                             
                                              
                                           
        self._boss_sprite_state  = "idle"
        self._boss_anim_t        = 0.0                                                            
        self._boss_anim_fps_idle = 6.0                             
        self._boss_anim_fps_act  = 8.0                                   
        self._boss_anim_done     = False                                            
        self._boss_hidden        = False                                                
                                                              
        self._boss_next_state    = ""                                                    
                                                                                    
        self._boss_delay_t       = 0.0                                      
        self._boss_delay_next    = ""                                               
                                                                             
        self._party_post_hurt_delay: dict = {}                                                 

                          
        self._boss_phase     = 1             
        self._crisis_done    = False
        self._arena_destroyed = False                                                     
        self._ending_route   = ""                     

                            
        self._dlg_step   = 0
        self._dlg_list   = []                              

                                             
        self._bad_arga_attacked = False

                                                                
        self._true_end_fighting = False
                                                                             
        self._fade_exit_started = False
        self._scene_exited = False
                                                                                                        
        self._pending_ultimate  = False
                                                           
        self._boss_ultimate_anim_done = False

                                               
                                                                 
                                                                                
                                                                                     
                                                              
                                                      
                                                                  
        self._party_anim: dict = {
            name: {"state": "idle", "t": 0.0, "done": False} for name in PARTY_MAX_HP
        }

                  
        self._dialogue   = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator   = NarratorBox(game.W, game.H)
        self._party_hud  = PartyHUD()
        self._floats: list[FloatingText] = []
        self._particles: list[dict] = []
        self._boss_effects: list = []                             
        self._skill_effects: list = []                             

                          
        self._skill_choices = list(ARGA_BOSS_SKILLS.keys())
        self._chosen_skill  = ""
        self._current_boss_skill: dict = {}

                      
        W, H = game.W, game.H
        gy          = int(H * self._CHAR_Y_RATIO)
        self._ground_y = gy
        self._arga_x   = int(W * self._ARGA_X_RATIO)
        self._boss_x   = int(W * self._BOSS_X_RATIO)

                      
        self._party_positions: list[dict] = []
        for slot_idx, name in enumerate(self._PARTY_ORDER):
            dx, dy = self._PARTY_FORMATION[slot_idx]
            self._party_positions.append({
                "name":  name,
                "label": self._PARTY_ASSET_MAP[name]["label"],
                "idle_attr": self._PARTY_ASSET_MAP[name]["idle"],
                "x": self._arga_x + dx,
                "y": gy + dy,
                "anim_offset": slot_idx * 0.4,
            })

                    
        try:
            self._font_name  = pygame.font.SysFont("Georgia",  18, bold=True)
            self._font_hp    = pygame.font.SysFont("Consolas", 14)
            self._font_hint  = pygame.font.SysFont("Consolas", 13)
            self._font_big   = pygame.font.SysFont("Georgia",  34, bold=True)
            self._font_phase = pygame.font.SysFont("Georgia",  16, bold=True)
        except Exception:
            self._font_name  = pygame.font.Font(None, 22)
            self._font_hp    = pygame.font.Font(None, 18)
            self._font_hint  = pygame.font.Font(None, 16)
            self._font_big   = pygame.font.Font(None, 40)
            self._font_phase = pygame.font.Font(None, 20)

                                                               
               
                                                               

    def on_enter(self) -> None:
        self._transition.fade_in(color=(0, 0, 0), speed=180)
        self._narrator.show(["⚔  FINAL BOSS", "DEMON KING"], 3.0)
        self._phase = "intro"
        self._t = 0.0
        try:
            self._game.assets.play_bgm("boss_theme", loop=-1, volume=0.85)
        except Exception:
            pass

    def on_exit(self) -> None:
        pass

                                                               
           
                                                               

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        key = event.key

        if key in (pygame.K_UP, pygame.K_w):
            if self._dialogue.showing_choices:
                self._dialogue.navigate_choice(-1)
                try: self._game.assets.play("cursor")
                except Exception: pass

        elif key in (pygame.K_DOWN, pygame.K_s):
            if self._dialogue.showing_choices:
                self._dialogue.navigate_choice(1)
                try: self._game.assets.play("cursor")
                except Exception: pass

        elif key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
            self._on_confirm()

    def _on_confirm(self):
        try: self._game.assets.play_sfx_file("space_enter_sfx")
        except Exception: pass

                                            
        if self._phase == "intro":
            if self._t >= 1.0 and not self._narrator.visible:
                self._show_skill_menu()
            return

                           
        if self._phase == "player_turn":
            if self._dialogue.showing_choices:
                idx = self._dialogue.confirm_choice()
                self._chosen_skill = self._skill_choices[idx]
                self._dialogue.hide()
                self._execute_player_skill()
            return

                                                             
        if self._phase in ("player_anim", "boss_anim", "boss_ultimate_anim",
                          "bad_end_arga_anim", "bad_end_boss_ulti2"):
            return                          

                                      
        if self._phase == "crisis_cutscene":
            self._advance_dialog()
            return

                                    
        if self._phase == "choice":
            if self._dialogue.showing_choices:
                idx = self._dialogue.confirm_choice()
                self._dialogue.hide()
                if idx == 0:
                    self._go_true_end()
                else:
                    self._go_bad_end()
            return

                                 
        if self._phase == "true_end_cutscene":
            self._advance_dialog()
            return

                                                    
        if self._phase == "true_victory_turn":
            if self._dialogue.showing_choices:
                self._dialogue.confirm_choice()
                self._chosen_skill = "Celestial Flame"                                         
                self._dialogue.hide()
                self._execute_true_final_attack()
            return

                                
        if self._phase == "victory_cutscene":
            self._advance_dialog()
            return

                                
        if self._phase == "bad_end_cutscene":
            self._advance_dialog()
            return

                                                              
        if self._phase == "bad_end_attack":
            if self._dialogue.showing_choices:
                idx = self._dialogue.confirm_choice()
                self._chosen_skill = self._skill_choices[idx]
                self._dialogue.hide()
                self._execute_bad_arga_attack()
            return

                             
        if self._phase == "victory":
            if self._t >= 2.0:
                self._exit_true_end()
            return

                                                               
                       
                                                               

    def _show_skill_menu(self):
        self._phase = "player_turn"
        hp_pct = int(self._boss["hp"] / self._boss["max_hp"] * 100)
        self._dialogue.show(
            f"Demon King  HP {self._boss['hp']}/{self._boss['max_hp']}  [{hp_pct}%]",
            "Arga",
            choices=self._skill_choices,
        )

    def _execute_player_skill(self):
        self._phase   = "player_anim"
        self._anim_t  = 0.0
        skill = ARGA_BOSS_SKILLS[self._chosen_skill]

                       
        base_dmg = skill["dmg_base"]
        variance = random.randint(-100, 150)
        dmg = max(50, base_dmg + variance)

                         
        self._boss["hp"] = max(0, self._boss["hp"] - dmg)

                       
        self._flash_color = skill["color"]
        self._flash_alpha = 180
        self._shake_t     = 0.3

                         
        self._floats.append(FloatingText(
            f"-{dmg}",
            self._boss_x, self._ground_y - 130,
            color=skill["color"], speed=60, lifetime=1.8,
        ))
        self._floats.append(FloatingText(
            self._chosen_skill,
            self._boss_x, self._ground_y - 90,
            color=GOLD_LIGHT, speed=35, lifetime=1.4,
        ))

                  
        self._spawn_particles(self._boss_x, self._ground_y - 120, skill["color"])

                                           
        ax = self._arga_x
        ay = self._ground_y - 60
        bx = self._boss_x
        by = self._ground_y - 90
        if self._chosen_skill == "Attack":
            self._skill_effects.append(SlashEffect(bx, by))
        elif self._chosen_skill == "Celestial Flame":
            self._skill_effects.append(CelestialFlameEffect(ax, ay, bx, by))
        else:                                      
            self._skill_effects.append(DivineSlashEffect(ax, ay, bx, by))

                                             
        try:
            if self._chosen_skill == "Attack":
                self._game.assets.play_sfx_file("attack_sfx")
            elif self._chosen_skill == "Celestial Flame":
                self._game.assets.play_sfx_file("celestial_flame_sfx")
            elif self._chosen_skill == "Divine Slash":
                self._game.assets.play_sfx_file("divine_slash_sfx")
            else:
                self._game.assets.play_sfx_file("divine_slash_sfx")
        except Exception:
            pass

                                                                                      
        self._boss_sprite_state = "hurt"
        self._boss_anim_t       = 0.0
        self._boss_anim_done    = False
        self._boss_next_state   = "attack"                                             

                                                                                                      
        self._execute_boss_skill()

                     
        hp_ratio = self._boss["hp"] / self._boss["max_hp"]
        if hp_ratio <= 0.5 and self._boss_phase == 1:
            self._boss_phase = 2
            self._narrator.show(PHASE2_ENTRY_MSG, 2.5)
            try: self._game.assets.play("damage")
            except Exception: pass

                                                               
                       
                                                               

    def _execute_boss_skill(self):
        hp_ratio = self._boss["hp"] / self._boss["max_hp"]

                                                                
        if hp_ratio <= 0.10 and not self._crisis_done:
                                                                                               
            self._pending_ultimate = True
            return

                                                                       
        pool = BOSS_SKILLS_P2 if self._boss_phase == 2 else BOSS_SKILLS_P1
        skill = random.choice(pool)
        self._current_boss_skill = skill
        self._pending_ultimate   = False

    def _apply_boss_skill_damage(self):
        skill = self._current_boss_skill
        if not skill:
            return

        dmg_min, dmg_max = skill["dmg"]
        targets = self._get_skill_targets(skill["target"])

        for tname in targets:
            if self._party_dead.get(tname, False):
                continue
            dmg = random.randint(dmg_min, dmg_max)
            self._party_hp[tname] = max(0, self._party_hp[tname] - dmg)

                               
            px, py = self._get_party_screen_pos(tname)
            self._floats.append(FloatingText(
                f"-{dmg}", px, py - 50,
                color=skill["color"], speed=50, lifetime=1.6,
            ))

                                                 
            if self._party_hp[tname] <= 0:
                self._party_hp[tname]   = 0
                self._party_dead[tname] = True
                self._party_anim[tname] = {"state": "dead_anim", "t": 0.0, "done": False}
                px2, py2 = self._get_party_screen_pos(tname)
                self._floats.append(FloatingText(
                    "DOWN!", px2, py2 - 80,
                    color=DAMAGE_RED, speed=40, lifetime=2.0,
                ))
            else:
                                                       
                if self._party_anim[tname]["state"] not in ("dead_anim", "hurt_hold"):
                    self._party_anim[tname] = {"state": "hurt_loop", "t": 0.0, "done": False}

                                           
        self._narrator.show([f"⚡ {skill['name']}!", skill["msg"]], 2.0)
        self._flash_color = skill["color"]
        self._flash_alpha = 120
        self._shake_t     = 0.4
        self._spawn_particles(self._arga_x, self._ground_y - 80, skill["color"], count=12)
                         
        self._boss_effects.append(BossClawEffect(
            self._boss_x, self._ground_y - 80,
            self._arga_x, self._ground_y - 60,
        ))

        try: self._game.assets.play("damage")
        except Exception: pass

                                                                                              
        try: self._game.assets.play_sfx_file("attack_boss")
        except Exception: pass

                                            
        try: self._game.assets.play_sfx_file("get_hit_sfx")
        except Exception: pass

    def _execute_boss_skill_anim_only(self):
        if getattr(self, "_pending_ultimate", False):
            self._pending_ultimate = False
            self._execute_boss_ultimate()
            return
                                                           
        self._apply_boss_skill_damage()

    def _execute_boss_ultimate(self):
        self._phase  = "boss_ultimate_anim"
        self._anim_t = 0.0
        self._crisis_done = True
        self._arena_destroyed = True                                  

                                                                             
                                                                      
        self._boss["hp"] = self._boss["max_hp"]

        ult = BOSS_ULTIMATE

                                            
        for name in self._party_hp:
            if not self._party_dead[name]:
                five_pct = max(1, int(PARTY_MAX_HP[name] * 0.05))
                self._party_hp[name] = five_pct
                px, py = self._get_party_screen_pos(name)
                self._floats.append(FloatingText(
                    "CRITICAL!", px, py - 60,
                    color=(255, 60, 60), speed=45, lifetime=2.2,
                ))

                                                                                       
        self._boss_sprite_state       = "ultimate"
        self._boss_anim_t             = 0.0
        self._boss_anim_done          = False
        self._boss_next_state         = "idle"
        self._boss_ultimate_anim_done = False

                             
        self._flash_color = ult["color"]
        self._flash_alpha = 230
        self._shake_t     = 0.8

                        
        self._spawn_big_particles(ult["color"])

                                       
        self._boss_effects.append(BlackWaveEffect(
            self._boss_x, self._ground_y - 120,
            self._game.W, self._game.H,
        ))

        self._narrator.show(
            [f"💀 {ult['name']}!", ult["msg"], "Seluruh party nyaris tewas!"],
            2.5,
        )

                                                                           
        self._trigger_party_hurt_hold()

        try: self._game.assets.play("damage")
        except Exception: pass
                                                                
        try: self._game.assets.play_sfx_file("ultimate", volume=1.0)
        except Exception: pass

    def _get_skill_targets(self, target_type: str) -> list[str]:
        alive = [n for n in PARTY_MAX_HP if not self._party_dead.get(n, False)]

        if target_type == "single_random":
            return [random.choice(alive)] if alive else []

        elif target_type == "all_party":
            return alive

        elif target_type == "two_random":
            if len(alive) >= 2:
                return random.sample(alive, 2)
            return alive

        elif target_type == "arga_focused":
            return ["Arga"]

        return alive

                                                               
                   
                                                               

    def _go_true_end(self):
        self._ending_route   = "true"
        self._phase          = "true_end_cutscene"
        self._dlg_step       = 0
        self._dlg_list       = TRUE_END_DIALOGS

                                                                
        for name in self._party_hp:
            self._party_shield[name] = True
            self._party_hp[name]     = PARTY_MAX_HP[name]
            self._party_dead[name]   = False
            self._party_anim[name]   = {"state": "idle", "t": 0.0, "done": False}

                          
        self._flash_color = HOLY_WHITE
        self._flash_alpha = 220
        self._spawn_big_particles(HOLY_WHITE)

                                                              
        self._boss["hp"] = max(1, self._boss["max_hp"])

        self._dialogue.show(TRUE_END_DIALOGS[0][1], TRUE_END_DIALOGS[0][0])

        try: self._game.assets.play("magic")
        except Exception: pass

    def _execute_true_final_attack(self):
        self._phase  = "player_anim"
        self._anim_t = 0.0

                                                                              
        self._boss["hp"] = 0
        self._boss_sprite_state = "dead"
        self._boss_anim_t       = 0.0
        self._boss_anim_done    = False
        self._boss_next_state   = ""
        self._flash_color = HOLY_WHITE
        self._flash_alpha = 255
        self._shake_t     = 0.5

        self._floats.append(FloatingText(
            "CELESTIAL OVERDRIVE!!!", self._boss_x, self._ground_y - 180,
            color=HOLY_WHITE, speed=70, lifetime=2.5,
        ))
        self._floats.append(FloatingText(
            "FATAL!", self._boss_x, self._ground_y - 130,
            color=GOLD_LIGHT, speed=50, lifetime=2.0,
        ))
        self._spawn_big_particles(HOLY_WHITE)
                                          
        self._skill_effects.append(DivineSlashEffect(
            self._arga_x, self._ground_y - 60,
            self._boss_x, self._ground_y - 90,
        ))

        try:
            self._game.assets.play("slash")
            self._game.assets.play("fanfare")
        except Exception:
            pass
                                                                  
        try:
            self._game.assets.play_sfx_file("celestial_flame_sfx", volume=1.0)
        except Exception:
            pass

                                                   
        self._pending_after_anim = "victory_cutscene"

                                                               
                  
                                                               

    def _go_bad_end(self):
        self._ending_route = "bad"
        self._phase        = "bad_end_cutscene"
        self._dlg_step     = 0
        self._dlg_list     = BAD_END_DIALOGS

                                                     
        self._party_anim["Arga"] = {"state": "idle", "t": 0.0, "done": False}
                                      

        self._dialogue.show(BAD_END_DIALOGS[0][1], BAD_END_DIALOGS[0][0])

        try: self._game.assets.play("damage")
        except Exception: pass

    def _execute_bad_arga_attack(self):
                                              
        self._phase  = "bad_end_arga_anim"
        self._anim_t = 0.0
        skill = ARGA_BOSS_SKILLS.get(self._chosen_skill, ARGA_BOSS_SKILLS["Attack"])

                                               
        self._floats.append(FloatingText(
            "NO EFFECT...", self._boss_x, self._ground_y - 130,
            color=(140, 140, 140), speed=40, lifetime=1.8,
        ))
        self._flash_color = skill["color"]
        self._flash_alpha = 80
        self._shake_t     = 0.15

        try: self._game.assets.play("slash")
        except Exception: pass

    def _execute_bad_final(self):
                                    
        self._party_hp["Arga"] = 1
        for name in self._party_hp:
            if name != "Arga":
                self._party_hp[name]   = 0
                self._party_dead[name] = True

        self._flash_color = DAMAGE_RED
        self._flash_alpha = 240
        self._shake_t     = 1.0
        self._spawn_big_particles(DAMAGE_RED)

        for name in self._PARTY_ORDER:
            px, py = self._get_party_screen_pos(name)
            self._floats.append(FloatingText(
                "DEAD", px, py - 60,
                color=DAMAGE_RED, speed=40, lifetime=2.5,
            ))

        try: self._game.assets.play("damage")
        except Exception: pass

    def _trigger_party_hurt_loop(self, names: list = None):
        targets = names if names else list(PARTY_MAX_HP.keys())
        for name in targets:
            if not self._party_dead.get(name, False):
                self._party_anim[name] = {"state": "hurt_loop", "t": 0.0, "done": False}

    def _trigger_party_hurt_hold(self, exclude: list = None):
        for name in PARTY_MAX_HP:
            if exclude and name in exclude:
                continue
            if not self._party_dead.get(name, False):
                self._party_anim[name] = {"state": "hurt_hold", "t": 0.0, "done": False}

    def _trigger_party_dead_anim(self, names: list):
        for name in names:
            self._party_anim[name] = {"state": "dead_anim", "t": 0.0, "done": False}

                                                               
                    
                                                               

    def _advance_dialog(self):
        if not self._dialogue.is_finished:
            self._dialogue.skip()
            return

        self._dlg_step += 1

        if self._dlg_step < len(self._dlg_list):
            spk, txt = self._dlg_list[self._dlg_step]
            self._dialogue.show(txt, spk)
        else:
                                             
            self._on_dialog_list_done()

    def _on_dialog_list_done(self):
        if self._phase == "crisis_cutscene":
                                       
            self._phase = "choice"
            self._dialogue.show(
                "Elena menerima luka fatal! Semua orang dalam bahaya!",
                "SYSTEM",
                choices=[
                    "Lindungi semuanya!",
                    "Tetap serang!",
                ],
            )

        elif self._phase == "true_end_cutscene":
                                                                             
            self._phase = "true_victory_turn"
            self._dialogue.show(
                "CELESTIAL OVERDRIVE — Serang sekarang!",
                "Arga",
                choices=["Celestial Overdrive!!!"],
            )

        elif self._phase == "victory_cutscene":
                                 
            self._phase = "victory"
            self._t     = 0.0
            self._fade_exit_started = True
            self._narrator.show(["TRUE END", "Dunia diselamatkan..."], 3.5)
            self._transition.fade_out(color=(255, 240, 180), speed=80)
            try: self._game.assets.play("fanfare")
            except Exception: pass

        elif self._phase == "bad_end_cutscene":
                                                                           
                                                               
            self._phase = "bad_end_attack"
            self._dialogue.show(
                "Sialan!",
                "Arga",
                choices=list(ARGA_BOSS_SKILLS.keys()),
            )

                                                               
          
                                                               

    def _exit_true_end(self):
        if getattr(self, "_scene_exited", False):
            return
        self._scene_exited = True
        from scenes.true_end_scene import TrueEndScene
        self._game.replace_scene(TrueEndScene(self._game))

    def _exit_bad_end(self):
        if getattr(self, "_scene_exited", False):
            return
        self._scene_exited = True
        from scenes.bad_end_scene import BadEndScene
        self._game.replace_scene(BadEndScene(self._game))

                                                               
            
                                                               

    def update(self, dt: float) -> None:
        self._t      += dt
        self._anim_t += dt
        self._transition.update(dt)
        self._narrator.update(dt)
        self._dialogue.update(dt)

               
        if self._shake_t > 0:
            self._shake_t -= dt
            self._shake_x = random.randint(-8, 8) if self._shake_t > 0 else 0
        else:
            self._shake_x = 0

                    
        if self._flash_alpha > 0:
            self._flash_alpha = max(0, self._flash_alpha - int(320 * dt))

                                  
                                               
                                                                                                   
        self._boss_anim_t += dt

                                                                                               
        if self._boss_delay_t > 0:
            self._boss_delay_t -= dt
            if self._boss_delay_t <= 0:
                self._boss_delay_t = 0.0
                next_st = self._boss_delay_next
                self._boss_delay_next = ""
                self._boss_sprite_state = next_st if next_st else "idle"
                self._boss_anim_t = 0.0
                self._boss_anim_done = False
                self._boss_next_state = "idle"                                  
                if next_st == "attack":
                    self._execute_boss_skill_anim_only()

        if self._boss_sprite_state != "idle" and not self._boss_anim_done and self._boss_delay_t <= 0:
            assets = self._game.assets
            state  = self._boss_sprite_state
            if state == "hurt":
                frames = getattr(assets, "demon_king_hurt_frames", None)
            elif state == "attack":
                frames = getattr(assets, "demon_king_attack_frames", None)
            elif state == "ultimate":
                frames = getattr(assets, "demon_king_ultimate_frames", None)
            elif state == "dead":
                frames = getattr(assets, "demon_king_dead_frames", None)
            else:
                frames = None
            if frames:
                n = len(frames)
                fps = self._boss_anim_fps_act
                one_cycle = n / fps
                if state == "dead":
                                                                       
                    if self._boss_anim_t >= one_cycle:
                        self._boss_anim_done = True                                              
                else:
                    if self._boss_anim_t >= one_cycle:
                        self._boss_anim_done = True
                        next_st = self._boss_next_state
                        self._boss_next_state = ""
                        if next_st == "attack":
                                                                            
                            self._boss_sprite_state = "idle"
                            self._boss_anim_t       = 0.0
                            self._boss_anim_done    = False
                            self._boss_delay_t      = 0.5
                            self._boss_delay_next   = "attack"
                        elif next_st == "ultimate":
                                                                                           
                            self._boss_sprite_state       = "ultimate"
                            self._boss_anim_t             = 0.0
                            self._boss_anim_done          = False
                            self._boss_next_state         = "idle"
                            self._boss_ultimate_anim_done = False
                        else:
                                                                                    
                            if self._boss_sprite_state == "ultimate":
                                self._boss_ultimate_anim_done = True
                            self._boss_sprite_state = next_st if next_st else "idle"
                            self._boss_anim_t       = 0.0
                            self._boss_anim_done    = False
                                                                                                    

                                       
        HURT_FPS      = 8.0                      
        HURT_DELAY    = 0.5                                                                    
        DEAD_FPS      = 8.0                      
        for name, pa in self._party_anim.items():
            pa["t"] += dt
            state = pa["state"]

            if state == "hurt_loop":
                                                                  
                _hurt_attr = {
                    "Elena": "elena_hurt_frames", "Lyra": "lyra_hurt_frames",
                    "Darius": "darius_hurt_frames", "Reno": "reno_hurt_frames",
                }
                _frs = getattr(self._game.assets, _hurt_attr.get(name, ""), None)
                if _frs and hasattr(_frs, "__len__") and len(_frs) > 1:
                    _one_cycle = len(_frs) / HURT_FPS
                else:
                    _one_cycle = 0.4                               
                if pa["t"] >= _one_cycle:
                                                                     
                    pa["state"] = "hurt_done_delay"
                    pa["t"]     = 0.0
                    pa["done"]  = False

            elif state == "hurt_done_delay":
                if pa["t"] >= HURT_DELAY:
                    pa["state"] = "idle"
                    pa["t"]     = 0.0
                    pa["done"]  = False

            elif state == "hurt_hold":
                pass                                      

            elif state == "dead_anim" and not pa["done"]:
                                               
                attr_map = {
                    "Elena": "elena_dead_frames", "Lyra": "lyra_dead_frames",
                    "Darius": "darius_dead_frames", "Reno": "reno_dead_frames",
                }
                attr = attr_map.get(name)
                assets_obj = self._game.assets
                frs = getattr(assets_obj, attr, None) if attr else None
                if frs:
                    one_cycle = len(frs) / DEAD_FPS
                    if pa["t"] >= one_cycle:
                        pa["done"] = True                              

                            
        for f in self._floats:
            f.update(dt)
        self._floats = [f for f in self._floats if f.alive]

        for p in self._particles:
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["vy"] += 130 * dt
            p["life"] -= dt
        self._particles = [p for p in self._particles if p["life"] > 0]

                                                
        for e in self._boss_effects:
            e.update(dt)
        self._boss_effects = [e for e in self._boss_effects if e.alive]
        for e in self._skill_effects:
            e.update(dt)
        self._skill_effects = [e for e in self._skill_effects if e.alive]

                             

        if self._phase == "intro":
            if self._t >= 2.0 and not self._narrator.visible:
                self._show_skill_menu()

        elif self._phase == "player_anim":
                                                                                                   
            attack_frames = getattr(self._game.assets, "arga_attack1_frames", [])
            n_arga = len(attack_frames) if attack_frames else 1
            fps_arga = 10.0
            arga_one_cycle = n_arga / fps_arga
            if self._anim_t >= arga_one_cycle:
                pending = getattr(self, "_pending_after_anim", "")
                if pending:
                    self._pending_after_anim = ""
                    if pending == "victory_cutscene":
                                                                                      
                        self._phase  = "boss_dead_anim"
                        self._anim_t = 0.0
                        return

                                                                             
                if self._boss["hp"] <= 0 and self._ending_route == "true":
                    return

                                                                                                  
                                                                                                    
                self._phase  = "boss_anim"
                self._anim_t = 0.0

        elif self._phase == "boss_anim":
                                                                 
                                                                                
                                                                                        
                                                                                               
            attack_frames = getattr(self._game.assets, "demon_king_attack_frames", None)
            n_atk = len(attack_frames) if attack_frames else 1
            atk_cycle = n_atk / self._boss_anim_fps_act
                                                                      
            hurt_frames = getattr(self._game.assets, "demon_king_hurt_frames", None)
            n_hurt = len(hurt_frames) if hurt_frames else 1
            hurt_cycle = n_hurt / self._boss_anim_fps_act
            min_wait = hurt_cycle + 0.5 + atk_cycle + 0.2
            if (self._boss_sprite_state == "idle"
                    and self._boss_delay_t <= 0
                    and self._anim_t >= min_wait):
                                                                         
                self._show_skill_menu()

        elif self._phase == "boss_ultimate_anim":
                                                                                     
            if self._boss_ultimate_anim_done:
                self._boss_ultimate_anim_done = False                                    
                                                        
                self._phase    = "crisis_cutscene"
                self._dlg_step = 0
                self._dlg_list = CRISIS_DIALOGS
                self._dialogue.show(CRISIS_DIALOGS[0][1], CRISIS_DIALOGS[0][0])

        elif self._phase == "bad_end_arga_anim":
                                                             
            attack_frames = getattr(self._game.assets, "arga_attack1_frames", [])
            n_arga = len(attack_frames) if attack_frames else 1
            arga_one_cycle = n_arga / 10.0
            if self._anim_t >= arga_one_cycle:
                                                                
                self._phase  = "bad_end_boss_ulti2"
                self._anim_t = 0.0
                                                 
                self._boss_sprite_state = "hurt"
                self._boss_anim_t       = 0.0
                self._boss_anim_done    = False
                self._boss_next_state   = "ultimate"
                                                         
                self._execute_bad_final()
                                                       
                try: self._game.assets.play_sfx_file("ultimate", volume=1.0)
                except Exception: pass
                                                                                        
                                                             
                self._trigger_party_dead_anim(["Elena", "Reno", "Lyra", "Darius"])
                                                                                        
                self._party_anim["Arga"] = {"state": "hurt_hold", "t": 0.0, "done": False}

        elif self._phase == "bad_end_boss_ulti2":
                                                                               
            if self._boss_ultimate_anim_done:
                self._boss_ultimate_anim_done = False
                self._phase = "bad_end_exit"
                self._t     = 0.0
                self._narrator.show(["💀 BAD END", "Kegelapan menang..."], 3.0)
                self._transition.fade_out(color=(0, 0, 0), speed=100)
                self._fade_exit_started = True

        elif self._phase == "boss_dead_anim":
                                                                                      
            if self._boss_anim_done:
                                                               
                self._boss_hidden = True
                self._phase    = "victory_cutscene"
                self._dlg_step = 0
                self._dlg_list = VICTORY_DIALOGS
                self._dialogue.show(VICTORY_DIALOGS[0][1], VICTORY_DIALOGS[0][0])

        elif self._phase == "victory":
                                                                                      
                                                                        
            if self._fade_exit_started and self._transition.done and self._t >= 2.0:
                self._exit_true_end()

        elif self._phase == "bad_end_exit":
            if self._fade_exit_started and self._transition.done and self._t >= 2.0:
                self._exit_bad_end()

                                                               
          
                                                               

    def draw(self, surface: pygame.Surface) -> None:
        ox = self._shake_x

                                                                           
        if self._arena_destroyed:
            bg = getattr(self._game.assets, "bg_ruang_boss_rusak", None)
        else:
            bg = getattr(self._game.assets, "bg_ruang_boss", None)
            if bg is None:
                bg = getattr(self._game.assets, "bg_castle_int", None)
        if bg:
            surface.blit(bg, (ox, 0))
        else:
            surface.fill((15, 5, 25))
            pygame.draw.rect(surface, (30, 15, 50),
                             (ox, self._ground_y + 5, self._game.W, 5))

        pygame.draw.line(surface, (50, 35, 80),
                         (ox, self._ground_y + 8),
                         (self._game.W + ox, self._ground_y + 8), 2)

                             
        self._draw_particles(surface)

                                                    
        depth_scales = self._PARTY_DEPTH_SCALES
        for i, member in enumerate(reversed(self._party_positions)):
            orig_idx = len(self._party_positions) - 1 - i
            ds = depth_scales[orig_idx] if orig_idx < len(depth_scales) else 0.85
            self._draw_party_member(surface, member, ox, depth_scale=ds)

              
        self._draw_arga(surface, ox)

              
        self._draw_boss(surface, ox)

                                   
        for e in self._skill_effects:
            e.draw(surface)

                    
        if self._flash_alpha > 0:
            fs = pygame.Surface((self._game.W, self._game.H), pygame.SRCALPHA)
            r, g, b = self._flash_color[:3]
            fs.fill((r, g, b, self._flash_alpha))
            surface.blit(fs, (0, 0))

                                                 
        for e in self._boss_effects:
            e.draw(surface)

                                       
        if self._ending_route == "true" and any(self._party_shield.values()):
            self._draw_aura_shield(surface)

                     
        self._draw_boss_hp_bar(surface)

                             
        members = [
            ("Arga",   self._party_hp["Arga"],   PARTY_MAX_HP["Arga"]),
            ("Elena",  self._party_hp["Elena"],  PARTY_MAX_HP["Elena"]),
            ("Reno",   self._party_hp["Reno"],   PARTY_MAX_HP["Reno"]),
            ("Lyra",   self._party_hp["Lyra"],   PARTY_MAX_HP["Lyra"]),
            ("Darius", self._party_hp["Darius"], PARTY_MAX_HP["Darius"]),
        ]
        self._party_hud.draw(surface, members)

                        
        for f in self._floats:
            f.draw(surface)

                     
        self._draw_phase_label(surface)

                      
        if self._phase == "player_turn" and self._dialogue.showing_choices:
            hint = self._font_hint.render(
                "↑↓ Pilih   SPACE/ENTER Konfirmasi", True, UI_DIMTEXT)
            surface.blit(hint, (self._game.W // 2 - hint.get_width() // 2,
                                self._game.H - 215))

                              
        self._dialogue.draw(surface)
        self._narrator.draw(surface)
        self._transition.draw(surface)

                                                               
                  
                                                               

    def _draw_boss(self, surface: pygame.Surface, ox: int) -> None:
        if self._boss_hidden:
            return
        bx = self._boss_x + ox
        by = self._ground_y
        assets = self._game.assets
        state = self._boss_sprite_state
        boss_dead = self._boss["hp"] <= 0

                                              
        if boss_dead or state == "dead":
            frames = getattr(assets, "demon_king_dead_frames", None)
            cur_state = "dead"
        elif state == "hurt":
            frames = getattr(assets, "demon_king_hurt_frames", None)
            cur_state = "hurt"
        elif state == "ultimate":
            frames = getattr(assets, "demon_king_ultimate_frames", None)
            cur_state = "ultimate"
        elif state == "attack":
            frames = getattr(assets, "demon_king_attack_frames", None)
            cur_state = "attack"
        else:
                                                                                     
            frames = getattr(assets, "demon_king_idle_side_frames", None)
            cur_state = "idle"

                                                                                        
        if not frames:
            frames = getattr(assets, "demon_king_idle_side_frames", None)
        if not frames:
            frames = getattr(assets, "demon_king_idle_frames", None)

        sprite = None
        if frames:
            n = len(frames)
            if cur_state == "idle":
                                            
                frame_idx = int(self._boss_anim_t * self._boss_anim_fps_idle) % n
            elif cur_state == "dead":
                                                            
                fps = self._boss_anim_fps_act
                frame_idx = int(self._boss_anim_t * fps)
                frame_idx = min(frame_idx, n - 1)
            else:
                                                                                
                fps = self._boss_anim_fps_act
                frame_idx = int(self._boss_anim_t * fps)
                frame_idx = min(frame_idx, n - 1)
            sprite = frames[frame_idx]

        if sprite:
                                                                                      
            w0, h0 = sprite.get_size()
            sc = self._BOSS_SPRITE_SCALE
            nw = max(1, int(w0 * sc))
            nh = max(1, int(h0 * sc))
            sprite = pygame.transform.scale(sprite, (nw, nh))

                                                                   
            if boss_dead and (state == "dead" or cur_state == "dead"):
                dead_frames = getattr(assets, "demon_king_dead_frames", None)
                n_dead = len(dead_frames) if dead_frames else 1
                one_cycle = n_dead / self._boss_anim_fps_act
                prog = min(1.0, self._boss_anim_t / max(0.001, one_cycle))
                                                                  
                if prog < 0.5:
                    alpha_val = 255
                else:
                    alpha_val = int(255 * (1.0 - (prog - 0.5) / 0.5))
                sprite.set_alpha(max(0, alpha_val))

            surface.blit(sprite, (bx - nw // 2, by - nh))
        else:
                               
            col = (180, 40, 60) if not boss_dead else (60, 60, 60)
            alpha_val = 255 if not boss_dead else 80
            s = pygame.Surface((70, 110), pygame.SRCALPHA)
            s.set_alpha(alpha_val)
            pygame.draw.rect(s, col, (5, 40, 60, 60))
            pygame.draw.circle(s, col, (35, 25), 22)
            pygame.draw.polygon(s, (200, 60, 80), [(20, 10), (10, -10), (25, 5)])
            pygame.draw.polygon(s, (200, 60, 80), [(50, 10), (60, -10), (45, 5)])
            surface.blit(s, (bx - 35, by - 110))

                   
        nm = self._font_name.render("Demon King", True, DAMAGE_RED)
        surface.blit(nm, (bx - nm.get_width() // 2, by + 6))

                                        
        if self._boss_phase == 2 and self._boss["hp"] > 0:
            ph = self._font_phase.render("⚠ PHASE 2", True, (255, 120, 60))
                   
            alpha = int(180 + 75 * math.sin(self._t * 4))
            ph.set_alpha(alpha)
            surface.blit(ph, (bx - ph.get_width() // 2, by - (140 if sprite else 120)))

                                                
        if self._phase == "boss_ultimate_anim" and self._anim_t < 1.2:
            ring_progress = self._anim_t / 1.2
            ring_radius   = int(60 + ring_progress * 200)
            ring_alpha    = int(255 * (1 - ring_progress))
            ring_surf = pygame.Surface((ring_radius * 2 + 4, ring_radius * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(ring_surf, (255, 100, 20, ring_alpha),
                               (ring_radius + 2, ring_radius + 2), ring_radius, 4)
            surface.blit(ring_surf, (bx - ring_radius - 2, by - 60 - ring_radius - 2))

    def _draw_boss_hp_bar(self, surface: pygame.Surface) -> None:
        boss = self._boss
        ratio = boss["hp"] / max(1, boss["max_hp"])
        bar_w = 400
        bar_h = 22
        bx = self._game.W // 2 - bar_w // 2
        by = 30

                        
        pygame.draw.rect(surface, (40, 10, 15), (bx - 2, by - 2, bar_w + 4, bar_h + 4),
                         border_radius=5)
        pygame.draw.rect(surface, (70, 20, 30), (bx, by, bar_w, bar_h), border_radius=4)

                                           
        if ratio > 0.5:
            bar_col = (200, 60, 80)
        elif ratio > 0.1:
            bar_col = (230, 120, 30)
        else:
            bar_col = (255, 40, 40)

        fill_w = max(0, int(bar_w * ratio))
        if fill_w > 0:
            pygame.draw.rect(surface, bar_col,
                             (bx, by, fill_w, bar_h), border_radius=4)

                
        pygame.draw.rect(surface, (180, 60, 80), (bx - 2, by - 2, bar_w + 4, bar_h + 4),
                         2, border_radius=5)

                 
        hp_txt = self._font_hp.render(
            f"DEMON KING   {boss['hp']:,} / {boss['max_hp']:,}",
            True, (255, 200, 200))
        surface.blit(hp_txt, (self._game.W // 2 - hp_txt.get_width() // 2, by + 2))

    def _draw_party_member(self, surface, member: dict, ox: int, depth_scale: float = 1.0) -> None:
        assets    = self._game.assets
        name_key  = member["name"]
        label     = member["label"]
        full_name = label                        

        px = member["x"] + ox
        py = member["y"]
        t  = self._t + member["anim_offset"]

        is_dead    = self._party_dead.get(full_name, False)
        has_shield = self._party_shield.get(full_name, False)
        panim      = self._party_anim.get(full_name, {"state": "idle", "t": 0.0})
        panim_state = panim["state"]

                                                         
        sprite = None

                                                    
                                                      
                                                           
                                                            
                                                                           
                                                                           
                                                                   

        def _get_hurt_sprite(nm, t_local):
            if nm == "Elena":
                frs = getattr(assets, "elena_hurt_frames", None)
                return frs[int(t_local * 8) % len(frs)] if frs else getattr(assets, "char_elena_hurt", None)
            elif nm == "Lyra":
                frs = getattr(assets, "lyra_hurt_frames", None)
                return frs[int(t_local * 8) % len(frs)] if frs else getattr(assets, "char_lyra_hurt", None)
            elif nm == "Darius":
                frs = getattr(assets, "darius_hurt_frames", None)
                return frs[int(t_local * 8) % len(frs)] if frs else getattr(assets, "char_darius_hurt", None)
            elif nm == "Reno":
                frs = getattr(assets, "reno_hurt_frames", None)
                return frs[int(t_local * 8) % len(frs)] if frs else getattr(assets, "char_reno_hurt", None)
            return None

        def _get_hurt_critical_sprite(nm):
            if nm == "Elena":
                frs = getattr(assets, "elena_hurt_frames", None)
                return frs[-1] if frs else getattr(assets, "char_elena_hurt", None)
            elif nm == "Lyra":
                frs = getattr(assets, "lyra_hurt_frames", None)
                return frs[-1] if frs else getattr(assets, "char_lyra_hurt", None)
            elif nm == "Darius":
                frs = getattr(assets, "darius_hurt_frames", None)
                return frs[-1] if frs else getattr(assets, "char_darius_hurt", None)
            elif nm == "Reno":
                frs = getattr(assets, "reno_hurt_frames", None)
                return frs[-1] if frs else getattr(assets, "char_reno_hurt", None)
            return None

        def _get_dead_frame(nm, anim_t_local):
            attr_map = {
                "Elena": "elena_dead_frames", "Lyra": "lyra_dead_frames",
                "Darius": "darius_dead_frames", "Reno": "reno_dead_frames",
            }
            attr = attr_map.get(nm)
            frs = getattr(assets, attr, None) if attr else None
            if frs:
                fps = 8.0
                idx = int(anim_t_local * fps)
                return frs[min(idx, len(frs) - 1)]
            return None

        pa_t = panim["t"]

        if panim_state == "hurt_loop":
            sprite = _get_hurt_sprite(full_name, pa_t)
        elif panim_state == "hurt_hold":
            sprite = _get_hurt_critical_sprite(full_name)
        elif panim_state == "dead_anim":
            sprite = _get_dead_frame(full_name, pa_t)

                         
        if sprite is None and panim_state not in ("dead_anim",) and not is_dead:
            frames = getattr(assets, member["idle_attr"], None)
            if frames:
                sprite = frames[int(t * 6) % len(frames)]
        if sprite is None and not is_dead:
            sprite = getattr(assets, f"char_{name_key}_idle", None)

                           
        is_visually_dead = (panim_state == "dead_anim" and panim["done"]) or (is_dead and panim_state not in ("hurt_loop", "hurt_hold", "dead_anim"))

        if sprite:
            w0, h0 = sprite.get_size()
            nw = max(1, int(w0 * depth_scale))
            nh = max(1, int(h0 * depth_scale))
            scaled = pygame.transform.scale(sprite, (nw, nh))
            if is_visually_dead:
                scaled = pygame.transform.rotate(scaled, -80)
                scaled.set_alpha(60)
            elif panim_state == "dead_anim" and not panim["done"]:
                pass                                               
            w, h = scaled.get_size()
            surface.blit(scaled, (px - w // 2, py - h))
        else:
            _col = {"elena": (180, 100, 200), "lyra": (100, 180, 220),
                    "darius": (200, 130, 80), "reno": (150, 200, 100)}.get(name_key, (120, 120, 180))
            sz = int(50 * depth_scale)
            alpha_val = 60 if is_visually_dead else 255
            s = pygame.Surface((sz // 2 + 4, sz + 4), pygame.SRCALPHA)
            s.set_alpha(alpha_val)
            pygame.draw.rect(s, _col, (2, 2, sz // 2, sz))
            surface.blit(s, (px - sz // 4, py - sz))

                             
        status = " [DEAD]" if is_dead else ""
        nm_col = (160, 60, 60) if is_dead else (200, 200, 220)
        nm_surf = self._font_hp.render(label + status, True, nm_col)
        nm_surf.set_alpha(180 if is_dead else 220)
        surface.blit(nm_surf, (px - nm_surf.get_width() // 2, py + 4))

                     
        if has_shield and not is_dead:
            shield_alpha = int(60 + 40 * math.sin(self._t * 3))
            ss = pygame.Surface((70, 100), pygame.SRCALPHA)
            pygame.draw.ellipse(ss, (100, 200, 255, shield_alpha), (5, 5, 60, 90))
            surface.blit(ss, (px - 35, py - 95))

    def _draw_arga(self, surface: pygame.Surface, ox: int) -> None:
        ax = self._arga_x + ox
        ay = self._ground_y
        assets = self._game.assets

        is_dead = self._party_hp.get("Arga", 1) <= 0 and self._party_dead.get("Arga", False)

        sprite = None
                                                                     
        if self._phase in ("player_anim", "true_victory_turn", "bad_end_arga_anim"):
            attack_frames = getattr(assets, "arga_attack1_frames", [])
            if attack_frames:
                n = len(attack_frames)
                fps = 10.0                          
                one_cycle = n / fps
                if self._anim_t < one_cycle:
                    frame_idx = int(self._anim_t * fps)
                    frame_idx = min(frame_idx, n - 1)
                    sprite = attack_frames[frame_idx]

                                                                                         
        pa_arga  = self._party_anim.get("Arga", {"state": "idle", "t": 0.0, "done": False})
        pa_state = pa_arga["state"]
        pa_t     = pa_arga["t"]

        if sprite is None:
            hurt_frames = getattr(assets, "arga_hurt_frames", [])
            dead_frames = getattr(assets, "arga_dead_frames", []) or hurt_frames            

            if pa_state in ("hurt_loop", "hurt_done_delay", "hurt_hold"):
                if hurt_frames:
                    fps_h = 8.0
                    fidx  = int(pa_t * fps_h) if pa_state == "hurt_loop" else len(hurt_frames) - 1
                    sprite = hurt_frames[min(fidx, len(hurt_frames) - 1)]

            elif pa_state == "dead_anim":
                if dead_frames:
                    fps_d = 8.0
                    fidx  = int(pa_t * fps_d)
                    sprite = dead_frames[min(fidx, len(dead_frames) - 1)]

                                                  
        if sprite is None:
            frames = getattr(assets, "arga_idle_after_frames", [])
            if frames:
                sprite = frames[int(self._t * 6) % len(frames)]
        if sprite is None:
            sprite = getattr(assets, "arga_idle_after_side", None)
        if sprite is None:
            sprite = getattr(assets, "arga_idle_before_side", None)

        if sprite:
                                                               
            sc = self._CHAR_SCALE
            w0, h0 = sprite.get_size()
            nw = max(1, int(w0 * sc))
            nh = max(1, int(h0 * sc))
            scaled = pygame.transform.scale(sprite, (nw, nh))
            if is_dead:
                scaled = pygame.transform.rotate(scaled, -80)
                scaled.set_alpha(80)
            w, h = scaled.get_size()
            surface.blit(scaled, (ax - w // 2, ay - h))
        else:
                      
            sc = self._CHAR_SCALE
            col = (70, 100, 180) if not is_dead else (60, 60, 60)
            pygame.draw.rect(surface, col, (ax - int(14*sc), ay - int(88*sc), int(28*sc), int(56*sc)))
            pygame.draw.circle(surface, col, (ax, ay - int(96*sc)), int(14*sc))

              
        nm = self._font_name.render("Arga", True, UI_ACCENT)
        surface.blit(nm, (ax - nm.get_width() // 2, ay + 6))

                          
        if self._party_shield.get("Arga", False) and not is_dead:
            shield_alpha = int(60 + 40 * math.sin(self._t * 3))
            ss = pygame.Surface((80, 110), pygame.SRCALPHA)
            pygame.draw.ellipse(ss, (100, 200, 255, shield_alpha), (5, 5, 70, 100))
            surface.blit(ss, (ax - 40, ay - 105))

    def _draw_aura_shield(self, surface: pygame.Surface) -> None:
        glow_alpha = int(30 + 20 * math.sin(self._t * 2.5))
        glow = pygame.Surface((self._game.W, self._game.H), pygame.SRCALPHA)
        glow.fill((180, 220, 255, glow_alpha))
        surface.blit(glow, (0, 0))

    def _draw_phase_label(self, surface: pygame.Surface) -> None:
        phase_labels = {
            "intro":               "Final Boss — Demon King",
            "player_turn":         f"Battle — Phase {self._boss_phase}",
            "player_anim":         "Arga menyerang!",
            "boss_anim":           "Demon King menyerang!",
            "boss_ultimate_anim":  "APOCALYPSE!",
            "crisis_cutscene":     "CRISIS — Party hampir tewas!",
            "choice":              "PILIHAN KRITIS",
            "true_end_cutscene":   "✨ TRUE END ROUTE",
            "true_victory_turn":   "✨ Serangan Terakhir!",
            "boss_dead_anim":      "💀 Raja Iblis Tumbang!",
            "victory_cutscene":    "🌟 VICTORY!",
            "victory":             "🌟 TRUE END",
            "bad_end_cutscene":    "💀 BAD END ROUTE",
            "bad_end_attack":      "💀 Serangan Terakhir Arga...",
            "bad_end_arga_anim":   "💀 Arga Menyerang...",
            "bad_end_boss_ulti2":  "💀 APOCALYPSE ke-2!",
            "bad_end_exit":        "💀 BAD END",
        }
        lbl = phase_labels.get(self._phase, "")
        if lbl:
            t = self._font_hint.render(lbl, True, UI_ACCENT)
            surface.blit(t, (self._game.W // 2 - t.get_width() // 2, 8))

    def _draw_particles(self, surface: pygame.Surface) -> None:
        for p in self._particles:
            alpha = int(255 * p["life"] / p["max_life"])
            sz = max(1, p["size"])
            s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p["col"], alpha), (sz, sz), sz)
            surface.blit(s, (int(p["x"]) - sz, int(p["y"]) - sz))

                                                               
                      
                                                               

    def _spawn_particles(self, cx, cy, color, count=16):
        for _ in range(count):
            self._particles.append({
                "x": cx, "y": cy,
                "vx": random.uniform(-160, 160),
                "vy": random.uniform(-200, 50),
                "life": random.uniform(0.4, 1.2),
                "max_life": 1.2,
                "size": random.randint(3, 7),
                "col": color[:3] if len(color) >= 3 else (255, 220, 80),
            })

    def _spawn_big_particles(self, color):
        for _ in range(50):
            self._particles.append({
                "x": random.randint(0, self._game.W),
                "y": random.randint(0, self._game.H),
                "vx": random.uniform(-100, 100),
                "vy": random.uniform(-280, -40),
                "life": random.uniform(0.8, 2.0),
                "max_life": 2.0,
                "size": random.randint(4, 12),
                "col": color[:3] if len(color) >= 3 else (255, 240, 120),
            })

                                                               
                     
                                                               

    def _get_party_screen_pos(self, name: str) -> tuple[int, int]:
        if name == "Arga":
            return self._arga_x, self._ground_y - 50

        name_lower = name.lower()
        for member in self._party_positions:
            if member["name"] == name_lower:
                return member["x"], member["y"] - 20

        return self._arga_x, self._ground_y - 50


                                                               
                                                     
                                                               

def start_boss_battle(game):
    scene = BossBattleScene(game)
    game.replace_scene(scene)
