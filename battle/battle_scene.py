
import pygame
import random
import math
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, FloatingText, NarratorBox


                                                               
                                                
                                                               

ENCOUNTER_TOWN_SLIMES = [
    {"name": "Slime",  "hp": 80,  "max_hp": 80,  "atk": 10, "def": 3,  "exp": 20, "gold": 5},
    {"name": "Slime",  "hp": 80,  "max_hp": 80,  "atk": 10, "def": 3,  "exp": 20, "gold": 5},
    {"name": "Slime",  "hp": 80,  "max_hp": 80,  "atk": 10, "def": 3,  "exp": 20, "gold": 5},
]

ENCOUNTER_FOREST_MONSTERS = [
    {"name": "Goblin",   "hp": 100, "max_hp": 100, "atk": 13, "def": 4, "exp": 30, "gold": 8},
    {"name": "Goblin",   "hp": 100, "max_hp": 100, "atk": 13, "def": 4, "exp": 30, "gold": 8},
]

ENCOUNTER_RUINS_TRAP = [
    {"name": "Minotaur", "hp": 200, "max_hp": 200, "atk": 20, "def": 12, "exp": 60, "gold": 15},
    {"name": "Minotaur", "hp": 200, "max_hp": 200, "atk": 20, "def": 12, "exp": 60, "gold": 15},
    {"name": "Minotaur", "hp": 200, "max_hp": 200, "atk": 20, "def": 12, "exp": 60, "gold": 15},
]

ENCOUNTER_VILLAGE_MONSTERS = [
    {"name": "Goblin",   "hp": 90,  "max_hp": 90,  "atk": 14, "def": 4,  "exp": 30, "gold": 7},
    {"name": "Goblin",   "hp": 90,  "max_hp": 90,  "atk": 14, "def": 4,  "exp": 30, "gold": 7},
    {"name": "Goblin",   "hp": 90,  "max_hp": 90,  "atk": 14, "def": 4,  "exp": 30, "gold": 7},
    {"name": "Minotaur", "hp": 220, "max_hp": 220, "atk": 24, "def": 11, "exp": 80, "gold": 20},
]

ENCOUNTER_CASTLE_DUNGEON = [
    {"name": "Minotaur", "hp": 260, "max_hp": 260, "atk": 28, "def": 14, "exp": 100, "gold": 30},
    {"name": "Minotaur", "hp": 260, "max_hp": 260, "atk": 28, "def": 14, "exp": 100, "gold": 30},
]

ENCOUNTER_DEMON_KING = [
    {
        "name":    "Demon King",
        "hp":      9999,
        "max_hp":  9999,
        "atk":     80,
        "def":     40,
        "exp":     9999,
        "gold":    0,
        "is_boss": True,
        "phases":  2,
    },
]

                                                               
                                                                  
                                                               

ARGA_SKILLS = {
    "Attack":            {"dmg": 9999, "mp": 0,   "type": "physical", "desc": "Serangan biasa",        "color": GOLD_LIGHT},
    "Divine Slash":      {"dmg": 9999, "mp": 0,   "type": "physical", "desc": "Tebasan pedang suci",   "color": HOLY_WHITE},
    "Celestial Flame":   {"dmg": 9999, "mp": 0,   "type": "magic",    "desc": "Api surgawi",            "color": MAGIC_BLUE},
}

                                                               
                                  
                                                               

                                                              
                                                                   
def _get_monster_frames(assets, name: str):
    key = name.lower()
    if "slime" in key:
        return (getattr(assets, "slime_idle_frames", None),
                getattr(assets, "slime_walk_frames", None),
                getattr(assets, "slime_dead_frames", None))
    if "goblin" in key:
        return (getattr(assets, "goblin_idle_frames", None),
                getattr(assets, "goblin_walk_frames", None),
                getattr(assets, "goblin_dead_frames", None))
    if any(k in key for k in ("minotaur", "orc", "stone golem", "dark knight", "mushroom")):
        return (getattr(assets, "minotaur_idle_frames", None),
                getattr(assets, "minotaur_walk_frames", None),
                getattr(assets, "minotaur_dead_frames", None))
                      
    idle = getattr(assets, "goblin_idle_frames", None)
    return (idle, getattr(assets, "goblin_walk_frames", None),
            getattr(assets, "goblin_dead_frames", None))

def _get_monster_sprite(assets, name: str, size=None):
    idle_frames, _, _ = _get_monster_frames(assets, name)
    if idle_frames:
        return idle_frames[0]
    return None


                                                               
              
                                                               


                                                               
                      
                                                               

class SlashEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.t = 0.0
        self.lifetime = 0.45
        self.alive = True
                                   
        self.slashes = [
            (-30, -40, 30, 20, (255, 240, 100), 7),
            (-20, -60, 40, 10, (255, 200, 60),  5),
            (-40, -20, 20, 40, (255, 255, 180), 4),
        ]

    def update(self, dt):
        self.t += dt
        if self.t >= self.lifetime:
            self.alive = False

    def draw(self, surface):
        if not self.alive:
            return
        prog = self.t / self.lifetime
        alpha = int(255 * (1.0 - prog))
        scale = 1.0 + prog * 0.5
        surf = pygame.Surface((200, 200), pygame.SRCALPHA)
        cx, cy = 100, 100
        for dx1, dy1, dx2, dy2, color, width in self.slashes:
            x1 = int(cx + dx1 * scale)
            y1 = int(cy + dy1 * scale)
            x2 = int(cx + dx2 * scale)
            y2 = int(cy + dy2 * scale)
            r, g, b = color
            pygame.draw.line(surf, (r, g, b, alpha), (x1, y1), (x2, y2), width)
                         
            pygame.draw.line(surf, (255, 255, 255, alpha // 2),
                             (x1+2, y1+2), (x2+2, y2+2), max(1, width - 2))
        surface.blit(surf, (self.x - 100, self.y - 100))


class DivineSlashEffect:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.sx = float(start_x)
        self.sy = float(start_y)
        self.tx = float(target_x)
        self.ty = float(target_y)
        self.t = 0.0
        self.lifetime = 0.55
        self.alive = True
                         
        self.trail = []
        for i in range(12):
            fx = start_x + (target_x - start_x) * i / 11
            fy = start_y + (target_y - start_y) * i / 11 + random.randint(-18, 18)
            self.trail.append((fx, fy))

    def update(self, dt):
        self.t += dt
        if self.t >= self.lifetime:
            self.alive = False

    def draw(self, surface):
        if not self.alive:
            return
        prog = self.t / self.lifetime
        alpha = int(255 * (1.0 - prog))
                            
        beam_surf = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        dx = self.tx - self.sx
        dy = self.ty - self.sy
        length = max(1, math.hypot(dx, dy))
        nx, ny = dy / length, -dx / length          
        thickness = int(28 * (1.0 - prog * 0.5))
                           
        colors = [
            (0, 150, 255, alpha),
            (100, 200, 255, min(255, alpha + 60)),
            (200, 240, 255, min(255, alpha + 120)),
        ]
        for i, (r, g, b, a) in enumerate(colors):
            w = max(1, thickness - i * 7)
            offset = (i - 1) * 3
            pts = [
                (int(self.sx + nx * offset), int(self.sy + ny * offset)),
                (int(self.tx + nx * offset + dx * 0.15), int(self.ty + ny * offset + dy * 0.15)),
            ]
            pygame.draw.line(beam_surf, (r, g, b, a), pts[0], pts[1], w)
                        
        for i, (px, py) in enumerate(self.trail):
            r_size = int(5 + 4 * math.sin(prog * math.pi + i * 0.5))
            a = int(alpha * (0.4 + 0.6 * (i / len(self.trail))))
            pygame.draw.circle(beam_surf, (80, 180, 255, a),
                               (int(px), int(py)), max(1, r_size))
                          
        if prog > 0.3:
            impact_a = int(alpha * 1.5)
            impact_r = int(35 * (1.0 - (prog - 0.3) / 0.7))
            for r2, g2, b2, thick in [
                (255, 255, 255, 5),
                (120, 200, 255, 9),
                (0, 100, 255,  14),
            ]:
                pygame.draw.circle(beam_surf, (r2, g2, b2, min(255, impact_a)),
                                   (int(self.tx), int(self.ty)), max(1, impact_r), thick)
        surface.blit(beam_surf, (0, 0))


class CelestialFlameEffect:
    def __init__(self, src_x, src_y, target_x, target_y):
        self.sx = float(src_x)
        self.sy = float(src_y)
        self.tx = float(target_x)
        self.ty = float(target_y)
        self.t = 0.0
        self.lifetime = 0.6
        self.alive = True
                      
        self.particles = []
        for _ in range(30):
            t_offset = random.uniform(0.0, 0.5)
            spread_x = random.uniform(-25, 25)
            spread_y = random.uniform(-40, 10)
            size = random.randint(8, 22)
            self.particles.append({
                "t_start": t_offset,
                "spread_x": spread_x,
                "spread_y": spread_y,
                "size": size,
            })

    def update(self, dt):
        self.t += dt
        if self.t >= self.lifetime:
            self.alive = False

    def draw(self, surface):
        if not self.alive:
            return
        prog = self.t / self.lifetime
        surf = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        dx = self.tx - self.sx
        dy = self.ty - self.sy
                                            
        for p in self.particles:
            local_t = self.t - p["t_start"]
            if local_t < 0:
                continue
            local_prog = min(1.0, local_t / (self.lifetime - p["t_start"]))
            px = self.sx + dx * local_prog + p["spread_x"] * math.sin(local_prog * math.pi)
            py = self.sy + dy * local_prog + p["spread_y"] * math.sin(local_prog * math.pi * 1.5)
            size = int(p["size"] * (1.0 - local_prog * 0.5))
            a = int(220 * (1.0 - local_prog))
                                                           
            if size > 0:
                pygame.draw.circle(surf, (200, 240, 255, min(255, a + 40)),
                                   (int(px), int(py)), max(1, size // 2))
                pygame.draw.circle(surf, (0, 160, 255, a),
                                   (int(px), int(py)), max(1, size))
                pygame.draw.circle(surf, (0, 60, 180, a // 2),
                                   (int(px), int(py)), max(1, size + 4))
                               
        if prog > 0.5:
            blast_prog = (prog - 0.5) / 0.5
            r_blast = int(50 * blast_prog)
            a_blast = int(200 * (1.0 - blast_prog))
            pygame.draw.circle(surf, (0, 100, 255, a_blast),
                               (int(self.tx), int(self.ty)), max(1, r_blast))
            pygame.draw.circle(surf, (100, 200, 255, a_blast // 2),
                               (int(self.tx), int(self.ty)), max(1, r_blast + 12), 5)
        surface.blit(surf, (0, 0))

class BattleScene(Scene):

                                      
                                                                                               
    _ARGA_X_RATIO   = 0.20                      
    _ENEMY_X_START  = 0.58                  
    _ENEMY_X_GAP    = 0.13                      
    _CHAR_Y_RATIO   = 0.72                                                                          

                      
    _CHAR_SCALE        = 1.6
    _PARTY_DEPTH_SCALES = [1.0 * 1.6, 0.85 * 1.6, 0.85 * 1.6, 0.85 * 1.6]
    _ENEMY_SPRITE_SCALE = 1.7                                                            

                                                      
                                                    
     
                        
                      
                                            
     
    _PARTY_FORMATION = [
        (-90,  -10),                                    
        (-80,  -40),                                         
        (-170, -10),                                      
        (-160, -40),                                     
    ]

                                                               
    _PARTY_ASSET_MAP = {
        "elena":  {"idle": "elena_idle_frames",  "label": "Elena"},
        "lyra":   {"idle": "lyra_idle_frames",   "label": "Lyra"},
        "darius": {"idle": "darius_idle_frames",  "label": "Darius"},
        "reno":   {"idle": "reno_idle_frames",    "label": "Reno"},
    }

    def __init__(self, game, enemies: list, return_scene_class, context: dict = None):
        super().__init__(game)
        self._return_scene_class = return_scene_class
        self._context            = context or {}

                                                                   
        import copy
        self._enemies_data: list[dict] = copy.deepcopy(enemies)
        self._current_enemy_idx = 0

                     
                                                                        
        self._phase    = "intro"
        self._t        = 0.0
        self._anim_t   = 0.0
        self._shake_t  = 0.0
        self._shake_x  = 0

            
        self._dialogue   = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator   = NarratorBox(game.W, game.H)
        self._floats: list[FloatingText] = []

                                         
        self._skill_choices = list(ARGA_SKILLS.keys())
        self._chosen_skill  = ""

                
        W, H = game.W, game.H
        gy = int(H * self._CHAR_Y_RATIO)
        self._ground_y = gy
        self._arga_x   = int(W * self._ARGA_X_RATIO)

                                                       
                                                                                   
        self._enemy_positions = []
        self._enemy_anim = []                                                 
        for i in range(len(self._enemies_data)):
            ex = int(W * (self._ENEMY_X_START + i * self._ENEMY_X_GAP))
            self._enemy_positions.append(ex)
            self._enemy_anim.append({
                "state":    "idle",                                               
                "frame_idx": 0,
                "t":         0.0,
                "walkin_x":  float(ex),                            
                "dead_done": False,
            })

                                                                        
                                                                         
        self._party_members: list[dict] = []
        party_list = list(game.party)                                    
        for slot_idx, member_name in enumerate(party_list[:4]):
            name_lower = member_name.lower()
            if name_lower not in self._PARTY_ASSET_MAP:
                continue
            dx_px, dy_offset = self._PARTY_FORMATION[slot_idx]
            px = self._arga_x + dx_px
            py = gy + dy_offset
            self._party_members.append({
                "name":        name_lower,
                "label":       self._PARTY_ASSET_MAP[name_lower]["label"],
                "idle_attr":   self._PARTY_ASSET_MAP[name_lower]["idle"],
                "x":           px,
                "y":           py,
                "anim_offset": slot_idx * 0.4,                                  
            })

                               
        self._flash_alpha = 0
        self._flash_color = GOLD_LIGHT

                                   
        self._skill_effects: list = []

                                                          
        self._arga_attacking  = False                                        
        self._arga_attack_t   = 0.0                                
        self._arga_attack_fps = 10.0                                     

              
        try:
            self._font_name  = pygame.font.SysFont("Georgia", 18, bold=True)
            self._font_hp    = pygame.font.SysFont("Consolas", 14)
            self._font_hint  = pygame.font.SysFont("Consolas", 13)
            self._font_big   = pygame.font.SysFont("Georgia", 34, bold=True)
            self._font_title = pygame.font.SysFont("Georgia", 22, bold=True)
        except Exception:
            self._font_name  = pygame.font.Font(None, 22)
            self._font_hp    = pygame.font.Font(None, 18)
            self._font_hint  = pygame.font.Font(None, 16)
            self._font_big   = pygame.font.Font(None, 38)
            self._font_title = pygame.font.Font(None, 26)

                                                                

    @property
    def _current_enemy(self) -> dict:
        if self._current_enemy_idx < len(self._enemies_data):
            return self._enemies_data[self._current_enemy_idx]
        return {}

    @property
    def _enemies_alive(self) -> list:
        return [e for e in self._enemies_data if e.get("hp", 0) > 0]

                                                                

    def on_enter(self) -> None:
        self._transition.fade_in(color=(0, 0, 0), speed=200)
        bgm_key = self._context.get("bgm_battle", "normal_battle_theme")
        self._game.assets.play_bgm(bgm_key, loop=-1, volume=0.75)
        enc_name = self._enemies_data[0]["name"] if self._enemies_data else "Musuh"
        self._narrator.show([f"⚔  {enc_name} muncul!", "Pilih aksimu!"], 2.0)
        self._phase = "intro"

    def on_exit(self) -> None:
        pass

                                                                

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        key = event.key

                         
        if key in (pygame.K_UP, pygame.K_w):
            if self._dialogue.showing_choices:
                self._dialogue.navigate_choice(-1)
                self._game.assets.play("cursor")
        elif key in (pygame.K_DOWN, pygame.K_s):
            if self._dialogue.showing_choices:
                self._dialogue.navigate_choice(1)
                self._game.assets.play("cursor")
        elif key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
            self._on_confirm()

    def _on_confirm(self):
        try: self._game.assets.play_sfx_file("space_enter_sfx")
        except Exception: pass

        if self._phase == "intro":
            if self._t >= 0.5:
                self._show_skill_menu()
            return

        if self._phase == "player_turn":
            if self._dialogue.showing_choices:
                idx = self._dialogue.confirm_choice()
                self._chosen_skill = self._skill_choices[idx]
                self._dialogue.hide()
                self._execute_skill()
                return
            if self._dialogue.is_finished:
                self._dialogue.skip()
            return

        if self._phase in ("skill_anim", "next_enemy"):
            return                  

        if self._phase == "victory":
            if self._t >= 1.0:
                self._exit_to_scene()

                                                                

    def _show_skill_menu(self):
        self._phase = "player_turn"
        enemy = self._current_enemy
        self._dialogue.show(
            f"Musuh: {enemy['name']}  HP {enemy['hp']}/{enemy['max_hp']}",
            "Arga",
            choices=self._skill_choices
        )

    def _execute_skill(self):
        self._phase = "skill_anim"
        self._anim_t = 0.0

                                                
        self._arga_attacking = True
        self._arga_attack_t  = 0.0

        skill = ARGA_SKILLS.get(self._chosen_skill, ARGA_SKILLS["Attack"])
        self._flash_color = skill["color"]
        self._flash_alpha = 200
        self._shake_t     = 0.35

                              
        enemy = self._current_enemy
        enemy["hp"] = 0

                         
        if self._current_enemy_idx < len(self._enemy_positions):
            ex = self._enemy_positions[self._current_enemy_idx]
            self._floats.append(FloatingText(
                "Critical!",
                ex, self._ground_y - 100,
                color=skill["color"],
                speed=55, lifetime=1.6
            ))

                                 
        if self._current_enemy_idx < len(self._enemy_positions):
            ex = self._enemy_positions[self._current_enemy_idx]
            ey = self._ground_y - 60
            ax = self._arga_x
            ay = self._ground_y - 60
            if self._chosen_skill == "Attack":
                self._skill_effects.append(SlashEffect(ex, ey))
            elif self._chosen_skill == "Divine Slash":
                self._skill_effects.append(DivineSlashEffect(ax, ay, ex, ey))
            elif self._chosen_skill == "Celestial Flame":
                self._skill_effects.append(CelestialFlameEffect(ax, ay, ex, ey))

                                             
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

                                            
        try:
            self._game.assets.play_sfx_file("get_hit_sfx")
        except Exception:
            pass

    def _advance_to_next_enemy(self):
                                                                
        dead_idx = self._current_enemy_idx
        if dead_idx < len(self._enemy_anim):
            self._enemy_anim[dead_idx]["state"]     = "dead"
            self._enemy_anim[dead_idx]["frame_idx"] = 0
            self._enemy_anim[dead_idx]["t"]         = 0.0

        self._current_enemy_idx += 1
        remaining = [i for i, e in enumerate(self._enemies_data)
                     if e.get("hp", 0) > 0 and i >= self._current_enemy_idx]

        if remaining:
            self._current_enemy_idx = remaining[0]
            self._phase = "next_enemy"
            self._anim_t = 0.0
        else:
            self._start_victory()

    def _start_victory(self):
        self._phase = "victory"
        self._t = 0.0
                                                                     
        try:
            self._game.assets.play("fanfare")
        except Exception:
            pass
        self._transition.fade_out(color=(255, 240, 180), speed=60)

    def _exit_to_scene(self):
        ctx = self._context
        chapter = ctx.get("chapter")
        enc_id  = ctx.get("encounter_id", "")

                                             
        if chapter == 2:
            self._game.flags["battle_won_chapter2"] = True
        elif chapter == 3:
            self._game.flags[f"battle_won_{enc_id}"] = True
        elif chapter == "final":
                                                        
            self._game.flags[f"battle_won_{enc_id}"] = True

                               
        scene = self._return_scene_class(self._game)
        self._game.replace_scene(scene)

                                                                

    def update(self, dt: float) -> None:
        self._t      += dt
        self._anim_t += dt
        self._transition.update(dt)
        self._narrator.update(dt)
        self._dialogue.update(dt)

               
        if self._shake_t > 0:
            self._shake_t -= dt
            self._shake_x = random.randint(-6, 6) if self._shake_t > 0 else 0

                    
        if self._flash_alpha > 0:
            self._flash_alpha = max(0, self._flash_alpha - int(350 * dt))

                                                                               
        if self._arga_attacking:
            self._arga_attack_t += dt
            attack_frames = getattr(self._game.assets, "arga_attack1_frames", [])
            n = len(attack_frames) if attack_frames else 1
            one_cycle = n / self._arga_attack_fps
            if self._arga_attack_t >= one_cycle:
                self._arga_attacking = False
                self._arga_attack_t  = 0.0

                        
        for f in self._floats:
            f.update(dt)
        self._floats = [f for f in self._floats if f.alive]

                              
        for e in self._skill_effects:
            e.update(dt)
        self._skill_effects = [e for e in self._skill_effects if e.alive]

                                        
        self._update_enemy_anim(dt)

                       
        if self._phase == "intro":
            if self._t >= 1.2 and not self._narrator.visible:
                self._show_skill_menu()

        elif self._phase == "skill_anim":
            if self._anim_t >= 0.8:
                self._advance_to_next_enemy()

        elif self._phase == "next_enemy":
            if self._anim_t >= 0.5:
                self._show_skill_menu()

        elif self._phase == "victory":
                                                            
            if self._transition.done and self._t >= 0.8:
                self._exit_to_scene()

                                                                

    def draw(self, surface: pygame.Surface) -> None:
        ox = self._shake_x                

                                                        
                                                                         
        _ENC_BG_MAP = {
            "town_slimes":    "bg_town",
            "forest":         "bg_forest",
            "ruins":          "bg_ruins",
            "village":        "bg_village",
            "castle_dungeon": "bg_castle_ext",
            "demon_king":     "bg_ruang_boss",
        }
        enc_id = self._context.get("encounter_id", "")
        bg_attr = _ENC_BG_MAP.get(enc_id, "bg_battle")
        bg = getattr(self._game.assets, bg_attr, None)\
             or getattr(self._game.assets, "bg_battle", None)
        if bg:
            surface.blit(bg, (ox, 0))
        else:
            surface.fill((20, 10, 35))
                         
            pygame.draw.rect(surface, (40, 30, 60),
                             (ox, self._ground_y + 10, self._game.W, 4))

                      
        pygame.draw.line(surface, (60, 50, 90),
                         (ox, self._ground_y + 12),
                         (self._game.W + ox, self._ground_y + 12), 2)

                                                                                  
                                                                               
        depth_scales = self._PARTY_DEPTH_SCALES
        for i, member in enumerate(reversed(self._party_members)):
                                                          
            orig_idx = len(self._party_members) - 1 - i
            ds = depth_scales[orig_idx] if orig_idx < len(depth_scales) else 0.85
            self._draw_party_member(surface, member, ox, depth_scale=ds)

                     
        self._draw_arga(surface, ox)

                            
        for i, enemy in enumerate(self._enemies_data):
            self._draw_enemy(surface, i, enemy, ox)

                          
        if self._flash_alpha > 0:
            fs = pygame.Surface((self._game.W, self._game.H), pygame.SRCALPHA)
            r, g, b = self._flash_color[:3]
            fs.fill((r, g, b, self._flash_alpha))
            surface.blit(fs, (0, 0))

                              
        for e in self._skill_effects:
            e.draw(surface)

            
        self._floats_draw(surface)
        self._dialogue.draw(surface)
        self._narrator.draw(surface)
        self._transition.draw(surface)

                                         
        if self._phase == "player_turn" and self._dialogue.showing_choices:
            hint = self._font_hint.render(
                "↑↓ Pilih   SPACE/ENTER Konfirmasi", True, UI_DIMTEXT)
            surface.blit(hint, (self._game.W // 2 - hint.get_width() // 2,
                                self._game.H - 210))

    def _draw_party_member(self, surface, member: dict, ox: int, depth_scale: float = 1.0) -> None:
        assets  = self._game.assets
        px      = member["x"] + ox
        py      = member["y"]
        t_local = self._t + member["anim_offset"]
        name    = member["name"]

        sprite = None

                                                                     
        frames = getattr(assets, member["idle_attr"], None)
        if frames:
            sprite = frames[int(t_local * 6) % len(frames)]
        if sprite is None:
            sprite = getattr(assets, f"char_{name}_idle", None)

        if sprite:
                                                                     
            SPRITE_BASE_H = 96
            w0, h0 = sprite.get_size()
            if h0 > 0:
                norm_w = max(1, int(w0 * SPRITE_BASE_H / h0))
                sprite = pygame.transform.scale(sprite, (norm_w, SPRITE_BASE_H))
            w0, h0 = sprite.get_size()
            nw = max(1, int(w0 * depth_scale))
            nh = max(1, int(h0 * depth_scale))
            scaled = pygame.transform.scale(sprite, (nw, nh))
            surface.blit(scaled, (px - nw // 2, py - nh))
        else:
            _colors = {"elena": (180, 100, 200), "lyra": (100, 180, 220),
                       "darius": (200, 130, 80), "reno": (150, 200, 100)}
            col = _colors.get(name, (120, 120, 180))
            sz = int(50 * depth_scale)
            pygame.draw.rect(surface, col, (px - sz//4, py - sz, sz//2, sz))
            pygame.draw.circle(surface, col, (px, int(py - sz * 1.15)), sz//4)

                    
        nm_surf = self._font_hp.render(member["label"], True, (200, 200, 220))
        nm_surf.set_alpha(180)
        surface.blit(nm_surf, (px - nm_surf.get_width() // 2, py + 4))

    def _draw_arga(self, surface, ox):
        ax = self._arga_x + ox
        ay = self._ground_y

        assets = self._game.assets

        sprite = None
        if self._arga_attacking:
                                                                     
            attack_frames = getattr(assets, "arga_attack1_frames", [])
            if attack_frames:
                n = len(attack_frames)
                frame_idx = int(self._arga_attack_t * self._arga_attack_fps)
                frame_idx = min(frame_idx, n - 1)                           
                sprite = attack_frames[frame_idx]
        
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
                                      
            SPRITE_BASE_H = 96
            w0, h0 = sprite.get_size()
            if h0 > 0:
                norm_w = max(1, int(w0 * SPRITE_BASE_H / h0))
                sprite = pygame.transform.scale(sprite, (norm_w, SPRITE_BASE_H))
            w0, h0 = sprite.get_size()
            nw = max(1, int(w0 * sc))
            nh = max(1, int(h0 * sc))
            scaled = pygame.transform.scale(sprite, (nw, nh))
            surface.blit(scaled, (ax - nw // 2, ay - nh))
        else:
            sc = self._CHAR_SCALE
            pygame.draw.rect(surface, (70, 100, 180),
                             (ax - int(14*sc), ay - int(88*sc), int(28*sc), int(56*sc)))
            pygame.draw.circle(surface, (70, 100, 180), (ax, ay - int(96*sc)), int(14*sc))

              
        nm = self._font_name.render("Arga", True, UI_ACCENT)
        surface.blit(nm, (ax - nm.get_width() // 2, ay + 6))

    def _draw_enemy(self, surface, idx: int, enemy: dict, ox):
        if idx >= len(self._enemy_positions) or idx >= len(self._enemy_anim):
            return

        anim      = self._enemy_anim[idx]
        anim_state = anim["state"]
        is_dead   = enemy.get("hp", 0) <= 0
        is_current = (idx == self._current_enemy_idx)
        esc       = self._ENEMY_SPRITE_SCALE
        ey        = self._ground_y

                                                                  
        if anim_state == "walk_in":
            ex = int(anim["walkin_x"]) + ox
        else:
            ex = self._enemy_positions[idx] + ox

                                  
        idle_frames, walk_frames, dead_frames = _get_monster_frames(
            self._game.assets, enemy["name"])

        sprite = None
        if anim_state == "walk_in" and walk_frames:
            sprite = walk_frames[anim["frame_idx"] % len(walk_frames)]
        elif anim_state == "dead" and dead_frames:
            sprite = dead_frames[anim["frame_idx"] % len(dead_frames)]
        elif idle_frames:
            sprite = idle_frames[anim["frame_idx"] % len(idle_frames)]

        if sprite:
                                                                                 
                                                                    
            SPRITE_BASE_H = 96
            w0, h0 = sprite.get_size()
            if h0 > 0:
                norm_w = max(1, int(w0 * SPRITE_BASE_H / h0))
                sprite = pygame.transform.scale(sprite, (norm_w, SPRITE_BASE_H))
            w0, h0 = sprite.get_size()
            nw = max(1, int(w0 * esc))
            nh = max(1, int(h0 * esc))
            scaled = pygame.transform.scale(sprite, (nw, nh))
                                                          
            if anim_state == "dead" and anim["dead_done"]:
                scaled.set_alpha(60)
            w, h = scaled.get_size()
            surface.blit(scaled, (ex - w // 2, ey - h))
        else:
                               
            col = (80, 160, 80) if not is_dead else (60, 60, 60)
            fw = max(1, int(44 * esc)); fh = max(1, int(60 * esc))
            s = pygame.Surface((fw, fh), pygame.SRCALPHA)
            if anim_state == "dead" and anim["dead_done"]:
                s.set_alpha(60)
            pygame.draw.ellipse(s, col, (int(2*esc), int(fh*0.5), int(40*esc), int(22*esc)))
            pygame.draw.circle(s, col, (fw//2, int(fh*0.37)), int(18*esc))
            surface.blit(s, (ex - fw // 2, ey - fh))

                                                                
        if anim_state != "dead" and not is_dead:
            bar_w = int(60 * esc)
            bx = ex - bar_w // 2
            by = ey - int(90 * esc)
            ratio = enemy["hp"] / max(1, enemy["max_hp"])
            pygame.draw.rect(surface, (50, 0, 0),   (bx, by, bar_w, 8), border_radius=3)
            pygame.draw.rect(surface, HP_BAR if ratio > 0.4 else HP_BAR_LOW,
                             (bx, by, int(bar_w * ratio), 8), border_radius=3)

            nm = self._font_hp.render(enemy["name"], True, UI_TEXT)
            surface.blit(nm, (ex - nm.get_width() // 2, by - 16))

            if is_current and self._phase == "player_turn":
                blink = int(128 + 127 * math.sin(self._t * 5))
                ind = self._font_hint.render("▼", True, (255, 220, 80))
                ind.set_alpha(blink)
                surface.blit(ind, (ex - ind.get_width() // 2, by - 30))


    def _update_enemy_anim(self, dt: float) -> None:
        assets = self._game.assets
        WALK_SPEED = 180.0                    
        FRAME_RATE = 8.0                                      
        DEAD_RATE  = 6.0                                 

        for i, anim in enumerate(self._enemy_anim):
            if i >= len(self._enemies_data):
                break
            anim["t"] += dt
            state = anim["state"]
            enemy_name = self._enemies_data[i]["name"]
            idle_f, walk_f, dead_f = _get_monster_frames(assets, enemy_name)
            n_idle = len(idle_f) if idle_f else 1
            n_walk = len(walk_f) if walk_f else 1
            n_dead = len(dead_f) if dead_f else 1

            if state == "walk_in":
                target_x = float(self._enemy_positions[i])
                speed = WALK_SPEED
                anim["walkin_x"] = max(target_x, anim["walkin_x"] - speed * dt)
                                    
                anim["frame_idx"] = int(anim["t"] * FRAME_RATE) % n_walk
                if anim["walkin_x"] <= target_x:
                    anim["walkin_x"] = target_x
                    anim["state"]    = "idle"
                    anim["frame_idx"] = 0
                    anim["t"]         = 0.0

            elif state == "idle":
                anim["frame_idx"] = int(anim["t"] * FRAME_RATE) % n_idle

            elif state == "dead":
                                                                
                frame_target = int(anim["t"] * DEAD_RATE)
                if frame_target >= n_dead - 1:
                    anim["frame_idx"]  = n_dead - 1
                    anim["dead_done"]  = True
                else:
                    anim["frame_idx"] = frame_target

    def _floats_draw(self, surface):
        for f in self._floats:
            f.draw(surface)


                                                               
                                      
                                                               

def start_battle_scene(game, enemies: list, return_scene_class, context: dict = None):
    scene = BattleScene(
        game=game,
        enemies=enemies,
        return_scene_class=return_scene_class,
        context=context,
    )
    game.replace_scene(scene)