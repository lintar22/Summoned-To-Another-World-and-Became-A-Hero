from abc import ABC, abstractmethod
import pygame


class Entity(ABC):

    def __init__(self, name: str, x: float, y: float):
        self._name = name
        self._x = x
        self._y = y
        self._active = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = value

    @property
    def active(self) -> bool:
        return self._active

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    @abstractmethod
    def interact(self) -> str:
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._name}>"


class Scene(ABC):

    def __init__(self, game):
        self._game = game
        self._entities: list[Entity] = []
        self._finished = False
                        
        self._walkin_active = False
        self._walkin_timer = 0.0
        self._walkin_chars = []

    @property
    def finished(self) -> bool:
        return self._finished

    def start_walkin(self, chars_with_targets: list):
        
        self._walkin_active = True
        self._walkin_timer = 0.0
        self._walkin_chars = []
        for i, (ch, tx) in enumerate(chars_with_targets):
            ch._x = -80 - i * 50
            self._walkin_chars.append({
                'char': ch,
                'target_x': tx,
                'delay': i * 0.18,
                'done': False,
            })

    def update_walkin(self, dt: float) -> bool:
        if not self._walkin_active:
            return True
        self._walkin_timer += dt
        all_done = True
        for entry in self._walkin_chars:
            if self._walkin_timer < entry['delay']:
                all_done = False
                continue
            ch = entry['char']
            tx = entry['target_x']
            if ch._x < tx - 2:
                ch._x = min(tx, ch._x + 260 * dt)
                                                                                
                if hasattr(ch, 'set_walking'):
                    ch.set_walking(True, True)
                all_done = False
            else:
                ch._x = tx
                entry['done'] = True
                                                          
                if hasattr(ch, 'set_walking'):
                    ch.set_walking(False)
        if all_done:
            self._walkin_active = False
        return not self._walkin_active

    @property
    def walkin_done(self) -> bool:
        return not self._walkin_active


    def set_char_scale(self, *chars, scale: float = 1.5):
        for ch in chars:
            if hasattr(ch, "_draw_scale"):
                ch._draw_scale = scale

    def draw_char_scaled(self, surface: pygame.Surface, char, scale: float = 1.6) -> None:
        from entities.characters import _get_assets
        assets = _get_assets()
        if assets is None:
            char.draw(surface)
            return

        x = int(char._x)
        y = int(char._y + getattr(char, "_bob_offset", 0))

        sprite = self._get_char_sprite(char, assets)

        if sprite is not None:
                                               
            if not getattr(char, "_facing_right", True):
                sprite = pygame.transform.flip(sprite, True, False)
                                                                             
            from entities.characters import MonsterNPC as _MonsterNPC
            if isinstance(char, _MonsterNPC):
                SPRITE_BASE_H = 96
                w0, h0 = sprite.get_size()
                if h0 > 0:
                    norm_w = max(1, int(w0 * SPRITE_BASE_H / h0))
                    sprite = pygame.transform.scale(sprite, (norm_w, SPRITE_BASE_H))
            w0, h0 = sprite.get_size()
            nw = max(1, int(w0 * scale))
            nh = max(1, int(h0 * scale))
            scaled = pygame.transform.scale(sprite, (nw, nh))
            surface.blit(scaled, (x - nw // 2, y - nh))
        else:
                                                   
            if hasattr(char, "_draw_body"):
                char._draw_body(surface, x, y, scale)
            else:
                char.draw(surface)

    def _get_char_sprite(self, char, assets) -> pygame.Surface | None:
        name_lower = getattr(char, "_name", "").lower().replace(" ", "_")

                                                                                 
        if hasattr(char, "before_isekai"):
            if hasattr(char, "_get_frames"):
                frames = char._get_frames(assets)
                if frames:
                    idx = min(getattr(char, "_frame_idx", 0), len(frames) - 1)
                    return frames[idx]
                      
            return (getattr(assets, "arga_idle_after_side", None)
                    or getattr(assets, "arga_idle_before_side", None))

                                                                                 
        if hasattr(char, "_knocked_out"):
                      
            if char._knocked_out:
                dead_map = {"reno": "reno_dead5", "elena": "elena_dead5",
                            "lyra": "lyra_dead6", "darius": "darius_dead7"}
                attr = dead_map.get(name_lower)
                spr = getattr(assets, attr, None) if attr else None
                return spr or getattr(assets, f"char_{name_lower}_hurt", None)

                       
            if getattr(char, "_hurt_pose", False):
                                                                 
                if name_lower == "darius":
                    spr = getattr(assets, "darius_hurt5", None)
                else:
                    spr = getattr(assets, f"{name_lower}_hurt4", None)
                return spr or getattr(assets, f"char_{name_lower}_hurt", None)

                                
            anim_state = getattr(char, "_anim_state", "idle")
            frame_idx  = getattr(char, "_frame_idx", 0)
            if anim_state == "walk":
                frames = getattr(assets, f"{name_lower}_walk_frames", [])
                if frames:
                    return frames[frame_idx % len(frames)]
            idle_frames = getattr(assets, f"{name_lower}_idle_frames", [])
            if idle_frames:
                return idle_frames[frame_idx % len(idle_frames)]
            return getattr(assets, f"char_{name_lower}_idle", None)

                                                                                 
        if hasattr(char, "_phase") or name_lower in ("demon_king", "boss"):
                                                                                    
            if getattr(char, "use_front_idle", False):
                idle_frames = (getattr(assets, "demon_king_idle_frames", None)
                               or getattr(assets, "demon_king_idle_side_frames", None))
            else:
                idle_frames = (getattr(assets, "demon_king_idle_side_frames", None)
                               or getattr(assets, "demon_king_idle_frames", None))
            if idle_frames:
                anim_t = getattr(char, "_anim_timer", 0.0)
                idx = int(anim_t * 6) % len(idle_frames)
                return idle_frames[idx]
            return getattr(assets, "char_demon_king_idle", None)

                                                                                    
        attr = f"char_npc_{name_lower}"
        spr = getattr(assets, attr, None)
        if spr:
            return spr

                                                                                 
        anim_state = getattr(char, "_anim_state", "idle")
        frame_idx  = getattr(char, "_frame_idx", 0)
        for key in (name_lower, name_lower.replace(" ", "_"),
                    name_lower.replace(" ", "").replace("-", "")):
            if anim_state == "walk":
                walk_frames = getattr(assets, f"{key}_walk_frames", [])
                if walk_frames:
                    return walk_frames[frame_idx % len(walk_frames)]
            idle_frames = getattr(assets, f"{key}_idle_frames", [])
            if idle_frames:
                return idle_frames[frame_idx % len(idle_frames)]
            spr = getattr(assets, f"char_{key}_idle", None)
            if spr:
                return spr

        return None

    @abstractmethod
    def on_enter(self) -> None:
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    def on_exit(self) -> None:
        pass