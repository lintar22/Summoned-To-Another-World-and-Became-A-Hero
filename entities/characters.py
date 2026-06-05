
import pygame
import math
import random
from engine.base import Entity


                                                                

def _get_assets():
    try:
        from engine.game import GAME_INSTANCE
        return GAME_INSTANCE.assets if GAME_INSTANCE else None
    except Exception:
        return None


def _blit_centered(surface: pygame.Surface, sprite: pygame.Surface, cx: int, cy: int, scale: float = 1.0):
    if scale != 1.0:
        w0, h0 = sprite.get_size()
        nw, nh = int(w0 * scale), int(h0 * scale)
        sprite  = pygame.transform.scale(sprite, (nw, nh))
    w, h = sprite.get_size()
    surface.blit(sprite, (cx - w // 2, cy - h))


                                                               
                      
                                                               
class Character(Entity):

    EMOTIONS = ["normal", "happy", "sad", "surprised", "thinking", "angry", "excited"]

    def __init__(self, name: str, x: float, y: float, color: tuple):
        super().__init__(name, x, y)
        self.__emotion = "normal"
        self.__dialogue_lines: list[str] = []
        self._color = color
        self._anim_timer = 0.0
        self._bob_offset = 0.0
        self._facing_right = True
        self._highlight = False
        self._scale = 1.0
        self._draw_scale = 1.0                                                       

    @property
    def emotion(self) -> str:
        return self.__emotion

    @emotion.setter
    def emotion(self, value: str):
        if value in self.EMOTIONS:
            self.__emotion = value

    def set_dialogues(self, lines: list[str]):
        self.__dialogue_lines = lines

    def get_dialogue(self, index: int) -> str:
        if 0 <= index < len(self.__dialogue_lines):
            return self.__dialogue_lines[index]
        return ""

    def dialogue_count(self) -> int:
        return len(self.__dialogue_lines)

    def update(self, dt: float) -> None:
        self._anim_timer += dt
        self._bob_offset = math.sin(self._anim_timer * 2.5) * 3

                                                                

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        if assets:
            sprite = assets.get_character(self._name, self.__emotion, (96, 96))
            if sprite:
                _blit_centered(surface, sprite, x, y, self._draw_scale)
                self._draw_highlight(surface, x, y)
                return
        self._draw_body(surface, x, y)

                                                                 

    def _draw_highlight(self, surface, x, y):
        if self._highlight:
            hs = pygame.Surface((50, 70), pygame.SRCALPHA)
            pygame.draw.rect(hs, (255, 240, 100, 40), (0, 0, 50, 70))
            surface.blit(hs, (x - 25, y - 68))
            try:
                font = pygame.font.SysFont("Consolas", 13, bold=True)
                ind = font.render("[E]", True, (100, 200, 255))
                surface.blit(ind, (x - ind.get_width() // 2, y - 85))
            except Exception:
                pass

    def _draw_body(self, surface, x, y, scale=1.0):
        s = scale
        sz = lambda v: int(v * s)
        sh = pygame.Surface((sz(40), sz(10)), pygame.SRCALPHA)
        pygame.draw.ellipse(sh, (0, 0, 0, 60), (0, 0, sz(40), sz(10)))
        surface.blit(sh, (x - sz(20), y + sz(48) - sz(96)))
        pygame.draw.rect(surface, self._color,
                         (x - sz(14), y - sz(91), sz(28), sz(26)))
        pygame.draw.circle(surface, self._color, (x, y - sz(80)), sz(14))
        if self._highlight:
            self._draw_highlight(surface, x, y)

    def interact(self) -> str:
        return ""


                                                               
                                                    
                                                               
class Player(Character):

    ANIM_SPEEDS = {
        "walk":   0.06,                                                 
        "idle":   0.50,                                      
        "attack": 0.12,                                              
        "hurt":   0.15,
        "dead":   0.20,
        "defend": 0.25,
    }


    def __init__(self, x: float, y: float):
        super().__init__("Arga", x, y, (70, 100, 180))
        self.__hp = 9999
        self.__max_hp = 9999
        self.__level = 99

                                
        self.before_isekai = True                                                  
        self._anim_state  = "idle"                            
        self._frame_idx   = 0                               
        self._frame_timer = 0.0                                     
        self._anim_timer  = 0.0                             
        self._bob_offset  = 0.0
        self._is_walking  = False                                
        self._anim_once   = False                                                   
        self._anim_done   = False                                        

    @property
    def hp(self): return self.__hp
    @property
    def max_hp(self): return self.__max_hp
                                                                 

    def set_walking(self, moving: bool, direction_right: bool = None):
        self._is_walking = moving
        if direction_right is not None:
            if self._facing_right != direction_right:
                self._facing_right = direction_right
                                             
                self._frame_idx = 0
                self._frame_timer = 0.0
        if moving:
            self._set_anim("walk")
        else:
            self._set_anim("idle")

    def play_attack(self):
        self._set_anim("attack", once=True)

    def play_hurt(self):
        self._set_anim("hurt", once=True)

    def play_dead(self):
        self._set_anim("dead", once=True)

    def play_defend(self):
        self._set_anim("defend")

    def _set_anim(self, state: str, once: bool = False):
        if self._anim_state == state and not once:
            return
        self._anim_state  = state
        self._frame_idx   = 0
        self._frame_timer = 0.0
        self._anim_once   = once
        self._anim_done   = False

    def _get_frames(self, assets) -> list:
        if self.before_isekai:
            if self._anim_state == "walk":
                return assets.arga_walk_before_frames
            else:
                                                         
                return getattr(assets, "arga_idle_before_frames", [assets.arga_idle_before_side])
        else:
            if self._anim_state == "walk":
                return assets.arga_walk_after_frames
            elif self._anim_state == "attack":
                return assets.arga_attack1_frames
            elif self._anim_state == "hurt":
                return assets.arga_hurt_frames
            elif self._anim_state == "dead":
                return assets.arga_dead_frames
            elif self._anim_state == "defend":
                return assets.arga_defend_frames
            else:
                                                                            
                return getattr(assets, "arga_idle_after_frames", [assets.arga_idle_after_side])

    def update(self, dt: float) -> None:
        self._anim_timer += dt
                             
        if self._anim_state == "idle":
            self._bob_offset = math.sin(self._anim_timer * 2.5) * 3
        else:
            self._bob_offset = 0.0

        assets = _get_assets()
        if not assets:
            return

        frames = self._get_frames(assets)
        n = len(frames)
        if n == 0:
            return

        speed = self.ANIM_SPEEDS.get(self._anim_state, 0.12)
        self._frame_timer += dt
        if self._frame_timer >= speed:
            self._frame_timer -= speed
            if self._anim_once and self._frame_idx >= n - 1:
                                          
                self._anim_done = True
                                                 
                if self._anim_state in ("attack", "hurt"):
                    self._set_anim("idle")
                    self._frame_idx = 0
            else:
                self._frame_idx = (self._frame_idx + 1) % n

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        drawn = False

        if assets:
            frames = self._get_frames(assets)
            n = len(frames)
            if n > 0:
                idx = min(self._frame_idx, n - 1)
                sprite = frames[idx]

                                          
                if not self._facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)

                _blit_centered(surface, sprite, x, y, self._draw_scale)
                drawn = True

        if not drawn:
            self._draw_body(surface, x, y, self._draw_scale)

    def interact(self) -> str:
        return "player"


                                                               
     
                                                               
class NPC(Character):

    def __init__(self, name: str, x: float, y: float, color: tuple):
        super().__init__(name, x, y, color)
        self._dialogue_index = 0

    def interact(self) -> str:
        if self.dialogue_count() == 0:
            return "..."
        line = self.get_dialogue(self._dialogue_index)
        self._dialogue_index = (self._dialogue_index + 1) % max(1, self.dialogue_count())
        return line


class KingdomNPC(NPC):

    def __init__(self, name, x, y, color=None, role="citizen"):
        if color is None:
            color = random.choice([(180, 120, 80), (140, 100, 160),
                                   (100, 140, 100), (160, 130, 80)])
        super().__init__(name, x, y, color)
        self._role = role

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        drawn = False

        if assets:
            name_key = self._name.lower().replace(" ", "_")
            attr = f"char_npc_{name_key}"
            sprite = getattr(assets, attr, None)
            if sprite is None:
                sprite = assets.get_character(self._name, "normal", (80, 80))
            if sprite is not None:
                                          
                if not self._facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                _blit_centered(surface, sprite, x, y, self._draw_scale)
                drawn = True

        if not drawn:
            self._draw_body(surface, x, y, self._draw_scale)

        self._draw_highlight(surface, x, y)

    def interact(self) -> str:
        return super().interact()


class PartyNPC(NPC):

    COLORS = {
        "Elena":  (220, 180, 220),
        "Lyra":   (100, 140, 200),
        "Darius": (140, 130, 120),
        "Aria":   (220, 160, 200),
        "Reno":   (200, 120, 60),
    }

                                                    
    WALK_FRAME_SPEED = 0.08

    def __init__(self, char_name: str, x: float, y: float):
        col = self.COLORS.get(char_name, (150, 150, 150))
        super().__init__(char_name, x, y, col)

        self.__hp = 5000
        self.__max_hp = 5000
        self._knocked_out = False

        self._anim_state      = "idle"
        self._prev_anim_state = "idle"
        self._frame_idx       = 0
        self._frame_timer     = 0.0
        self._is_walking      = False
        self._hurt_pose = False

                                                                     
                                                                               
                                                                                            
                                                                       
                                                                             
        self.follow_target   = None
        self.follow_distance = 80
        self.follow_offset_y = 0
        self._follow_enabled = False                                                 

    @property
    def hp(self):
        return self.__hp

    @property
    def max_hp(self):
        return self.__max_hp

    @property
    def knocked_out(self):
        return self._knocked_out

    def set_walking(self, moving: bool, direction_right=None):
        self._is_walking = moving
        if direction_right is not None:
            if self._facing_right != direction_right:
                self._facing_right = direction_right
                self._frame_idx = 0
                self._frame_timer = 0.0
        if moving:
            self._anim_state = "walk"
        else:
            self._anim_state = "idle"

    def follow(self, target):
        self.follow_target = target

    def enable_follow(self):
        self._follow_enabled = True

    def disable_follow(self):
        self._follow_enabled = False

    def update(self, dt):
        super().update(dt)                                  

                                                                              
                                                                                   
                                                                                 
        if self._follow_enabled and self.follow_target is not None:
                                                                              
            target_x = self.follow_target._x + self.follow_distance
            target_y = self.follow_target._y + self.follow_offset_y
            
            diff = target_x - self._x

                                                                         
            if abs(diff) > 1:
                                                                                     
                speed = min(320.0, max(80.0, abs(diff) * 4.5))
                move  = speed * dt if diff > 0 else -speed * dt
                                     
                if abs(move) > abs(diff):
                    move = diff
                self._x += move
                self._y = target_y
                self.set_walking(True, diff > 0)
            else:
                self._x = target_x
                self._y = target_y
                self.set_walking(False)
                                                          
                self._facing_right = self.follow_target._facing_right

                                                                     
        IDLE_FRAME_SPEED = 0.18                        
        if self._anim_state == "walk":
            frame_speed = self.WALK_FRAME_SPEED
        elif self._anim_state == "idle":
            frame_speed = IDLE_FRAME_SPEED
        else:
                                                          
            if self._prev_anim_state != self._anim_state:
                self._frame_idx   = 0
                self._frame_timer = 0.0
                self._prev_anim_state = self._anim_state
            return

                                           
        if self._prev_anim_state != self._anim_state:
            self._frame_idx   = 0
            self._frame_timer = 0.0
            self._prev_anim_state = self._anim_state

        self._frame_timer += dt
        if self._frame_timer >= frame_speed:
            self._frame_timer -= frame_speed
            self._frame_idx  += 1


    def draw(self, surface: pygame.Surface) -> None:
        x      = int(self._x)
        y      = int(self._y + self._bob_offset)
        assets = _get_assets()

                                                                                
        if self._hurt_pose:
            sprite = None
            if assets:
                name_lower = self._name.lower()
                                                               
                sprite = getattr(assets, f"{name_lower}_hurt4", None)
                                                   
                if sprite is None:
                    sprite = getattr(assets, f"char_{name_lower}_hurt", None)
            if sprite is not None:
                if not self._facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                _blit_centered(surface, sprite, x, y, self._draw_scale)
            else:
                self._draw_body(surface, x, y, self._draw_scale)
            return

                                                                                 
        if self._knocked_out:
            if assets:
                name_lower = self._name.lower()
                                                            
                dead_map = {
                    "reno":   "reno_dead5",
                    "elena":  "elena_dead5",
                    "lyra":   "lyra_dead6",
                    "darius": "darius_dead7",
                }
                attr = dead_map.get(name_lower)
                dead = getattr(assets, attr, None) if attr else None
                if dead is None:
                    dead = getattr(assets, f"char_{name_lower}_hurt", None)
                if dead:
                    if not self._facing_right:
                        dead = pygame.transform.flip(dead, True, False)
                    _blit_centered(surface, dead, x, y, self._draw_scale)
                    return
            self._draw_body(surface, x, y, self._draw_scale)
            return

                                                                                 
        drawn = False
        if assets:
            name_lower  = self._name.lower()
            walk_frames = getattr(assets, f"{name_lower}_walk_frames", [])

            idle_frames = getattr(assets, f"{name_lower}_idle_frames", [])
            if self._anim_state == "walk" and walk_frames:
                sprite = walk_frames[self._frame_idx % len(walk_frames)]
            elif self._anim_state == "idle" and idle_frames:
                sprite = idle_frames[self._frame_idx % len(idle_frames)]
            else:
                sprite = getattr(assets, f"char_{name_lower}_idle", None)
                if sprite is None:
                    sprite = assets.get_character(self._name, "idle", (96, 96))

            if sprite is not None:
                if not self._facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                _blit_centered(surface, sprite, x, y, self._draw_scale)
                drawn = True

        if not drawn:
            self._draw_body(surface, x, y, self._draw_scale)

    def interact(self) -> str:
        return super().interact()

class BossNPC(NPC):

    def __init__(self, x: float, y: float):
        super().__init__("Demon King", x, y, (60, 20, 80))
        self.__hp = 50000
        self.__max_hp = 50000
        self.__phase = 1
        self._anim_timer = 0.0
        self.use_front_idle = False                                                             

    @property
    def hp(self): return self.__hp
    @property
    def max_hp(self): return self.__max_hp
    @property
    def phase(self): return self.__phase

    def update(self, dt: float) -> None:
        self._anim_timer += dt
        self._bob_offset = math.sin(self._anim_timer * 1.5) * 5

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()

        drawn = False
                                                        
                                                                                   
                                                                                               
        if getattr(self, "use_front_idle", False):
            idle_frames = getattr(assets, "demon_king_idle_frames", None) if assets else None
            if not idle_frames:
                idle_frames = getattr(assets, "demon_king_idle_side_frames", None) if assets else None
        else:
            idle_frames = getattr(assets, "demon_king_idle_side_frames", None) if assets else None
            if not idle_frames:
                idle_frames = getattr(assets, "demon_king_idle_frames", None) if assets else None
        if idle_frames:
            frame_idx = int(self._anim_timer * 6) % len(idle_frames)
            sprite = idle_frames[frame_idx]
                                                                   
            _blit_centered(surface, sprite, x, y)
            drawn = True
        elif assets and assets.char_demon_king_idle is not None:
            _blit_centered(surface, assets.char_demon_king_idle, x, y)
            drawn = True

        if not drawn:
            pygame.draw.polygon(surface, (30, 10, 40), [
                (x-40, y+80), (x+40, y+80), (x+55, y-10), (x, y-30), (x-55, y-10)
            ])
            pygame.draw.circle(surface, (50, 20, 60), (x, y - 30), 28)
            pygame.draw.polygon(surface, (80, 30, 30),
                                [(x-25, y-50), (x-15, y-80), (x-5, y-50)])
            pygame.draw.polygon(surface, (80, 30, 30),
                                [(x+5, y-50), (x+15, y-80), (x+25, y-50)])
            pygame.draw.circle(surface, (255, 30, 30), (x-10, y-32), 6)
            pygame.draw.circle(surface, (255, 30, 30), (x+10, y-32), 6)

    def interact(self) -> str:
        return "Hahaha... coba saja!"


class MonsterNPC(NPC):

    _MONSTER_ASSET_MAP = {
        "slime":    "slime",
        "mushroom": "mushroom",
        "goblin":   "goblin",
    }

    def __init__(self, name: str, x: float, y: float, hp: int = 100):
        super().__init__(name, x, y, (80, 160, 80))
        self.__hp = hp
        self.__max_hp = hp
        self._anim_state = "idle"
        self._frame_idx  = 0
        self._anim_t     = 0.0
        self._anim_speed = 8.0

    @property
    def hp(self): return self.__hp
    @property
    def max_hp(self): return self.__max_hp

    def set_walking(self, moving: bool, direction_right: bool = None):
        self._anim_state = "walk" if moving else "idle"
        if direction_right is not None:
            self._facing_right = direction_right

    def update(self, dt: float) -> None:
        super().update(dt)
        self._anim_t += dt
        self._frame_idx = int(self._anim_t * self._anim_speed)

    def draw(self, surface: pygame.Surface) -> None:
        x = int(self._x)
        y = int(self._y + self._bob_offset)
        assets = _get_assets()
        drawn = False

        if assets:
            name_lower = self._name.lower()
            monster_key = self._MONSTER_ASSET_MAP.get(name_lower, name_lower)
            sprite = getattr(assets, f"char_{monster_key}_idle", None)
            if sprite is not None:
                if not self._facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                _blit_centered(surface, sprite, x, y)
                drawn = True

        if not drawn:
            pygame.draw.ellipse(surface, (80, 200, 80),  (x-20, y-54, 40, 25))
            pygame.draw.ellipse(surface, (60, 180, 60),  (x-18, y-69, 36, 30))
            pygame.draw.circle(surface, (30, 120, 30), (x-7, y-61), 4)
            pygame.draw.circle(surface, (30, 120, 30), (x+7, y-61), 4)

                
        hp_ratio = self.__hp / max(1, self.__max_hp)
        bar_w = 40
        bar_y = y - 80
        pygame.draw.rect(surface, (60, 0, 0),    (x - bar_w//2, bar_y, bar_w, 6))
        pygame.draw.rect(surface, (50, 200, 50), (x - bar_w//2, bar_y, int(bar_w * hp_ratio), 6))

    def interact(self) -> str:
        name_lower = self._name.lower()
        reactions = {
            "slime":    "*Slime bergerak mengancam*",
            "mushroom": "*Mushroom mengeluarkan spora berbahaya*",
            "goblin":   "*Goblin mengancam dengan tombaknya*",
        }
        return reactions.get(name_lower, f"*{self._name} bersiap menyerang*")