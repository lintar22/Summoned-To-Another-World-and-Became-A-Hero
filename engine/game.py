import pygame
from engine.colors import *
from engine.assets import AssetManager

                                                                        
GAME_INSTANCE = None


class Game:

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.W, self.H = screen.get_size()
        self.running = True
        self.FPS = 60

        self.assets = AssetManager(self.W, self.H)

                                                                          
        global GAME_INSTANCE
        GAME_INSTANCE = self

        self._scene_stack: list = []

                           
        self.player_name = "Arga"
        self.inventory: list[str] = []
        self.flags: dict = {}                    
        self.party: list[str] = []                      
        self.choice_result: str = ""                                           

        self._boot()

    def _boot(self):
        from scenes.menu_scene import MenuScene
        self.push_scene(MenuScene(self))

    def push_scene(self, scene) -> None:
        scene.on_enter()
        self._scene_stack.append(scene)

    def pop_scene(self) -> None:
        if self._scene_stack:
            self._scene_stack[-1].on_exit()
            self._scene_stack.pop()
        if not self._scene_stack:
            self.running = False

    def replace_scene(self, scene) -> None:
        if self._scene_stack:
            self._scene_stack[-1].on_exit()
            self._scene_stack.pop()
        self.push_scene(scene)

    @property
    def current_scene(self):
        return self._scene_stack[-1] if self._scene_stack else None

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.current_scene:
                    self.current_scene.handle_event(event)

            if self.current_scene:
                self.current_scene.update(dt)
                self.current_scene.draw(self.screen)

            pygame.display.flip()
