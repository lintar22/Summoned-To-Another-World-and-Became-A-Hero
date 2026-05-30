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


class BattleEntity(ABC):

    @abstractmethod
    def use_skill(self, skill_name: str, target) -> dict:
        """Gunakan skill terhadap target, return dict hasil (damage, effect)."""
        pass

    @abstractmethod
    def take_damage(self, amount: int) -> int:
        """Terima damage, return actual damage diterima."""
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass


class Scene(ABC):

    def __init__(self, game):
        self._game = game
        self._entities: list[Entity] = []
        self._finished = False
        # Walk-in system
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
        """Update walk-in. Return True jika sudah selesai."""
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
                # Aktifkan animasi walk ke kanan jika karakter punya set_walking
                if hasattr(ch, 'set_walking'):
                    ch.set_walking(True, True)
                all_done = False
            else:
                ch._x = tx
                entry['done'] = True
                # Hentikan animasi walk saat sampai tujuan
                if hasattr(ch, 'set_walking'):
                    ch.set_walking(False)
        if all_done:
            self._walkin_active = False
        return not self._walkin_active

    @property
    def walkin_done(self) -> bool:
        return not self._walkin_active

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
