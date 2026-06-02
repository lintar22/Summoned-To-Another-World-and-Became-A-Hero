"""
scenes/town_scene.py
====================
Kota Astravia — Eksplorasi, NPC, Encounter Slime (Turn-Based).
[INHERITANCE] Scene(ABC). [POLYMORPHISM] interact() tiap NPC berbeda.

PERUBAHAN:
- Battle langsung (SPACE serang) DIHAPUS.
- Diganti dengan encounter turn-based:
  • Musuh muncul SETELAH semua NPC sudah diajak bicara.
  • Musuh berjalan masuk dari sisi KANAN layar.
  • Player berinteraksi (tekan E) dengan kelompok slime → masuk battle scene.
"""

import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox, FloatingText, PartyHUD
from entities.characters import Player, PartyNPC, TownNPC, MonsterNPC


class Chapter2Scene(Scene):
    """Chapter 2 — Kota Astravia: Eksplorasi dan Encounter Slime."""

    # Dialog Elena setelah semua NPC selesai diajak bicara
    ALL_NPC_DONE_DLGS = [
        ("Arga",  "Kotanya... ramai juga ya."),
        ("Elena", "Iya, Astravia merupakan salah satu kota terbesar yang tersisa. Banyak pengungsi dari timur datang ke sini."),
        ("Arga",  "Pengungsi?"),
        ("Elena", "Desa-desa di timur sudah jatuh. Orang-orang kehilangan rumah, keluarga..."),
        ("Arga",  "..."),
        ("Elena", "Itu sebabnya ini bukan sekadar 'misi'. Ini nyata bagi mereka."),
        ("Arga",  "Aku mulai mengerti kenapa kau ikut. Bukan karena disuruh Raja."),
        ("Elena", "Yahh... seperti itu"),
        ("Elena", "Aku tidak bisa hanya duduk diam dan menunggu dunia ku hancur begitu saja.."),
        ("Elena", "Hmm... Arga, lihat itu — ada gerakan di ujung jalan!"),
        ("SYSTEM","⚠ Sekelompok Slime muncul dari arah timur kota!"),
        ("Elena", "Mereka sudah sampai sejauh ini?!"),
        ("Arga",  "Aku tangani. Mundur dulu."),
        ("Elena", "...Hati-hati."),
    ]

    # Dialog setelah battle selesai (menang) — dipanggil oleh BattleScene saat kembali
    POST_BATTLE_DLGS = [
        ("Elena", "Cepat sekali. Bahkan aku sampai kesushan untuk membantumu."),
        ("Arga",  "Aku sendiri kaget... seolah tubuh ini bergerak sendiri."),
        ("Elena", "Mungkin itu merupakan kekuatan pedang itu. Ia menyesuaikan diri dengan pemiliknya."),
        ("Arga",  "Terasa aneh. Tapi... aku tidak benci."),
        ("Elena", "Kita harus terus maju. Tapi Arga—"),
        ("Arga",  "Apa?"),
        ("Elena", "Terima kasih. Kau melindungi warga kota tadi. Mereka tidak akan pernah tahu namamu."),
        ("Arga",  "Itu bukan alasan untuk tidak melakukannya."),
        ("Elena", "...Ya. Itu bukan alasan untuk tidak melakukannya."),
        ("SYSTEM","⚔ Menuju Chapter 3 — Hutan Verdan..."),
    ]

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
        # phase: explore → npc_done_dlg → enemy_walkin → encounter → post_battle → goto_ch3
        self._phase = "explore"
        self._dialogue = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator = NarratorBox(game.W, game.H)
        self._floats: list[FloatingText] = []
        self._party_hud = PartyHUD()

        ground_y = int(game.H * 0.6)
        self._ground_y = ground_y
        self._player = Player(200, ground_y - 55)
        self._player.before_isekai = False   # sudah dapat Holy Sword
        self._elena  = PartyNPC("Elena", 270, ground_y - 55)
        self._elena.emotion = "happy"
        self._player_speed = 150.0

        # NPC kota — semua harus diajak bicara sebelum musuh muncul
        self._npcs: list[TownNPC] = []
        self._npc_talked: set[int] = set()   # indeks NPC yang sudah diajak bicara
        # (name, target_x_world, dlg, emotion, color)
        for name, nx, dlg, em, col in [
            ("Anak Kecil",   400,  "Kakak yang punya pedang emas itu! Ayah bilang kakak datang dari dunia lain, beneran Ya?!",                    "happy",   (220, 180, 120)),
            ("Pria Tua",     600,  "Sudah lama aku tidak melihat Pedang Suci memancarkan cahaya seperti itu... semoga kita diberi keberkahan akan hal ini.",    "normal",  (160, 140, 100)),
            ("Warga Kota",   820,  "Suamiku pergi ke timur dua bulan lalu untuk melindungi kampung halamannya. Tapi.. sampai sekarang belum kembali huhu...", "sad",    (180, 140, 140)),
            ("Warga Kota 2", 1020, "Aura yang kau bawa itu... mengingatkanku pada pahlawan dalam legenda. Semoga cerita ini berakhir berbeda.", "normal",(140, 160, 180)),
        ]:
            # Spawn di luar kanan layar, walk-in ke target_x (world space)
            npc = TownNPC(name, nx, ground_y - 55, col)
            npc.set_dialogues([dlg])
            npc.emotion = em
            npc._highlight = True
            self._npcs.append(npc)

        # Encounter: 3 slime yang akan walk-in dari kanan setelah semua NPC selesai
        self._slimes: list[MonsterNPC] = []
        self._slimes_walkin_active = False
        self._slimes_walkin_done   = False
        self._slimes_interactable  = False   # True setelah walk-in selesai
        self._town_empty           = False   # True setelah warga menghilang
        self._pending_spawn        = False   # tunggu fade selesai baru spawn slime

        self._encounter_enemies = [
            {"name": "Slime", "hp": 80, "atk": 10, "def": 3, "exp": 20, "gold": 5},
            {"name": "Slime", "hp": 80, "atk": 10, "def": 3, "exp": 20, "gold": 5},
            {"name": "Slime", "hp": 80, "atk": 10, "def": 3, "exp": 20, "gold": 5},
        ]

        self._dlg_step = 0
        self._npc_done_dlg_step = 0
        self._active_npc_idx = -1   # NPC yang sedang diajak bicara

        self._cam_x = 0.0
        self._world_w = 1200

        # Apakah scene ini kembali dari battle yang menang
        self._returned_from_battle = game.flags.get("battle_won_chapter2", False)

        try:
            self._font_ui = pygame.font.SysFont("Consolas", 15)
        except Exception:
            self._font_ui = pygame.font.Font(None, 18)

    def on_enter(self) -> None:
        self._transition.fade_in(speed=180)

        # Jika kembali dari battle, langsung ke post_battle
        if self._returned_from_battle:
            self._phase = "post_battle"
            self._dlg_step = 0
            self._dialogue.show(self.POST_BATTLE_DLGS[0][1], self.POST_BATTLE_DLGS[0][0])
            self._game.flags["battle_won_chapter2"] = False
            # Elena sudah ikut, langsung aktifkan follow
            self._elena.follow(self._player)
            self._elena.follow_distance = -80
            self._elena.enable_follow()
            return

        self._narrator.show([
            "Chapter 2 — Kota Astravia",
            "← → Berjalan  |  E Bicara dengan NPC  |  E Dekati musuh → Battle"
        ], 4.0)
        # Walk-in Arga dan Elena dari kiri
        # Posisi awal diatur oleh start_walkin
        self._elena.follow(self._player)
        self._elena.follow_distance = -80
        self._elena.disable_follow()   # follow OFF dulu saat walkin berlangsung
        self.start_walkin([
            (self._player, 200),
            (self._elena, 270),
        ])

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            key = event.key
            if self._phase == "explore":
                if key == pygame.K_e:
                    self._try_interact()
            elif self._phase == "npc_done_dlg":
                if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                    self._advance_npc_done_dlg()
            elif self._phase == "encounter":
                # Tekan E saat dekat kelompok slime → masuk battle
                if key == pygame.K_e:
                    self._try_start_battle()
            elif self._phase in ("dialogue", "post_battle"):
                if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                    self._advance_dialogue()

    def _try_interact(self):
        """Coba berinteraksi dengan NPC terdekat saat fase explore."""
        if self._walkin_active:
            return
        px = self._player.x
        for i, npc in enumerate(self._npcs):
            npc_screen_x = npc.x - self._cam_x
            if abs(npc_screen_x - px) < 70:
                self._dialogue.show(npc.interact(), npc.name)
                self._phase = "dialogue"
                self._active_npc_idx = i
                self._game.assets.play("select")
                return

    def _advance_dialogue(self):
        """Advance dialog NPC biasa atau dialog post-battle."""
        if not self._dialogue.is_finished:
            self._dialogue.skip()
            return
        self._game.assets.play("cursor")

        if self._phase == "dialogue":
            # Tandai NPC sudah diajak bicara
            if self._active_npc_idx >= 0:
                self._npc_talked.add(self._active_npc_idx)
                self._npcs[self._active_npc_idx]._highlight = False
                self._active_npc_idx = -1
            self._dialogue.hide()
            self._phase = "explore"
            # Cek apakah semua NPC sudah selesai
            self._check_all_npc_done()

        elif self._phase == "post_battle":
            self._dlg_step += 1
            if self._dlg_step < len(self.POST_BATTLE_DLGS):
                spk, txt = self.POST_BATTLE_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
            else:
                self._phase = "goto_ch3"
                self._transition.fade_out(speed=200)

    def _check_all_npc_done(self):
        """Jika semua NPC sudah diajak bicara, mulai dialog transisi dan spawn musuh."""
        if len(self._npc_talked) >= len(self._npcs) and self._phase == "explore":
            self._phase = "npc_done_dlg"
            self._npc_done_dlg_step = 0
            spk, txt = self.ALL_NPC_DONE_DLGS[0]
            self._dialogue.show(txt, spk)
            self._elena.emotion = "surprised"

    def _advance_npc_done_dlg(self):
        """Advance dialog peralihan sebelum musuh muncul."""
        if not self._dialogue.is_finished:
            self._dialogue.skip()
            return
        self._game.assets.play("cursor")
        self._npc_done_dlg_step += 1
        if self._npc_done_dlg_step < len(self.ALL_NPC_DONE_DLGS):
            spk, txt = self.ALL_NPC_DONE_DLGS[self._npc_done_dlg_step]
            self._dialogue.show(txt, spk)
        else:
            # Dialog selesai → fade out, lalu warga hilang, lalu spawn slime
            self._dialogue.hide()
            self._pending_spawn = True
            self._phase = "pre_spawn_fade"
            self._transition.fade_out(speed=220)

    def _spawn_slimes_walkin(self):
        """Spawn 3 slime di luar layar kanan, lalu berjalan masuk."""
        ground_y = self._ground_y
        screen_w = self._game.W
        # Target posisi slime di world space (sesuai kamera saat ini)
        targets = [
            self._cam_x + screen_w - 140,
            self._cam_x + screen_w - 220,
            self._cam_x + screen_w - 300,
        ]
        for i, tx in enumerate(targets):
            start_x = self._cam_x + screen_w + 80 + i * 60
            m = MonsterNPC("Slime", start_x, ground_y - 35, hp=80)
            m._target_x = tx
            self._slimes.append(m)

        self._slimes_walkin_active = True
        self._slimes_interactable  = False
        self._phase = "enemy_walkin"
        self._narrator.show(["⚠ Slime muncul!", "Dekati dan tekan E untuk bertarung!"], 2.5)
        self._game.assets.play("damage")

    def _try_start_battle(self):
        """
        Cek apakah player cukup dekat dengan kelompok slime.
        Jika ya → masuk battle scene turn-based.
        Karena slime adalah satu kelompok, interaksi satu → battle semua.
        """
        if not self._slimes_interactable or not self._slimes:
            return
        # Cek slime terdekat (salah satu saja cukup karena mereka satu kelompok)
        px = self._player.x
        for slime in self._slimes:
            slime_screen_x = slime.x - self._cam_x
            if abs(slime_screen_x - px) < 100:
                self._enter_battle()
                return
        # Hint jika belum cukup dekat
        try:
            self._narrator.show(["Dekati Slime terlebih dahulu!"], 1.0)
        except Exception:
            pass

    def _enter_battle(self):
        """
        [HINT] Memanggil turn-based battle scene.
        Saat ini menampilkan pesan sementara karena BattleScene belum diimplementasi.
        Hapus blok try/except dan aktifkan start_battle_scene() setelah BattleScene jadi.
        """
        try:
            from battle.battle_scene import start_battle_scene, ENCOUNTER_TOWN_SLIMES
            start_battle_scene(
                game=self._game,
                enemies=ENCOUNTER_TOWN_SLIMES,
                return_scene_class=Chapter2Scene,
                context={"chapter": 2, "encounter_id": "town_slimes"},
            )
        except NotImplementedError:
            # [SEMENTARA] BattleScene belum ada — simulasikan menang langsung
            self._narrator.show(
                ["[BATTLE SCENE BELUM ADA]", "Anggap menang — lanjut cerita..."], 3.0
            )
            self._slimes.clear()
            self._phase = "post_battle"
            self._dlg_step = 0
            self._dialogue.show(self.POST_BATTLE_DLGS[0][1], self.POST_BATTLE_DLGS[0][0])
            self._game.assets.play("fanfare")

    def update(self, dt: float) -> None:
        self._t += dt
        self.update_walkin(dt)

        # Setelah walkin selesai → aktifkan follow elena
        if not self._walkin_active and not self._elena._follow_enabled:
            self._elena.enable_follow()

        self._transition.update(dt)
        self._dialogue.update(dt)
        self._narrator.update(dt)
        self._player.update(dt)
        self._elena.update(dt)
        for npc in self._npcs:
            npc.update(dt)

        for ft in self._floats:
            ft.update(dt)
        self._floats = [f for f in self._floats if f.alive]

        # Gerakan player (hanya saat explore atau encounter — tidak bisa gerak saat dialog)
        if self._phase in ("explore", "encounter"):
            if not self._walkin_active:
                keys = pygame.key.get_pressed()
                dx = 0
                moving_left  = keys[pygame.K_LEFT]  or keys[pygame.K_a]
                moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
                if moving_left:
                    dx = -self._player_speed * dt
                if moving_right:
                    dx = self._player_speed * dt
                self._player.x = max(60, min(self._world_w - 60, self._player.x + dx))
                # Elena mengikuti lewat sistem follow (tidak di-hardcode di sini)

                # Animasi walk / idle + flip arah
                if moving_left and not moving_right:
                    self._player.set_walking(True, False)   # jalan kiri
                elif moving_right and not moving_left:
                    self._player.set_walking(True, True)    # jalan kanan
                else:
                    self._player.set_walking(False)          # diam
            else:
                # Walk-in awal scene (dari kiri ke kanan)
                self._player.set_walking(True, True)
            target_cam = self._player.x - self._game.W * 0.3
            self._cam_x = max(0, min(self._world_w - self._game.W, target_cam))
        else:
            self._player.set_walking(False)

        # Update walk-in slime dari kanan
        if self._slimes_walkin_active:
            all_arrived = True
            for slime in self._slimes:
                tx = getattr(slime, '_target_x', slime.x)
                if slime.x > tx + 2:
                    slime.x = max(tx, slime.x - 200 * dt)
                    all_arrived = False
                else:
                    slime.x = tx
            if all_arrived and not self._slimes_walkin_done:
                self._slimes_walkin_done  = True
                self._slimes_walkin_active = False
                self._slimes_interactable  = True
                self._phase = "encounter"

        # Update slime
        for slime in self._slimes:
            slime.update(dt)

        # Fade selesai → warga hilang, fade in, spawn slime
        if self._phase == "pre_spawn_fade" and self._transition.done:
            self._town_empty = True        # sembunyikan NPC warga
            self._pending_spawn = False
            self._phase = "enemy_walkin"
            self._transition.fade_in(speed=200)
            self._spawn_slimes_walkin()

        if self._phase == "goto_ch3" and self._transition.done:
            from scenes.chapter3_scene import Chapter3Scene
            self._game.replace_scene(Chapter3Scene(self._game))

    def draw(self, surface: pygame.Surface) -> None:
        # Scroll background
        bg = self._game.assets.bg_town
        bx = int(-self._cam_x * 0.5) % self._game.W
        surface.blit(bg, (bx, 0))
        if bx > 0:
            surface.blit(bg, (bx - self._game.W, 0))

        # NPC warga (disembunyikan setelah transisi pre-spawn)
        if not self._town_empty:
            for npc in self._npcs:
                screen_x = npc.x - self._cam_x
                if -60 < screen_x < self._game.W + 60:
                    old = npc.x
                    npc.x = screen_x
                    npc.draw(surface)
                    npc.x = old

        self._player.draw(surface)
        self._elena.draw(surface)

        # Slime enemies (project ke screen space)
        for slime in self._slimes:
            screen_x = slime.x - self._cam_x
            if -60 < screen_x < self._game.W + 60:
                old = slime.x
                slime.x = screen_x
                slime.draw(surface)
                # Indikator interaksi jika cukup dekat
                if self._slimes_interactable:
                    px = self._player.x
                    if abs(screen_x - px) < 100:
                        self._draw_interact_hint(surface, int(screen_x), int(slime.y) - 60)
                slime.x = old

        for ft in self._floats:
            ft.draw(surface)

        # Tanda seru pada NPC yang belum diajak bicara
        if not self._town_empty:
            for i, npc in enumerate(self._npcs):
                if i not in self._npc_talked and self._phase == "explore":
                    screen_x = npc.x - self._cam_x
                    if 0 < screen_x < self._game.W:
                        self._draw_exclamation(surface, int(screen_x), int(npc.y) - 70)

        # Party HUD kiri atas
        self._draw_party_hud(surface)
        self._narrator.draw(surface)
        self._dialogue.draw(surface)
        self._transition.draw(surface)

        # Controls hint
        try:
            if self._phase == "explore":
                left = len(self._npcs) - len(self._npc_talked)
                hint = f"← → Jalan  |  E Bicara  |  NPC tersisa: {left}/{len(self._npcs)}"
                ctrl = self._font_ui.render(hint, True, UI_DIMTEXT)
            elif self._phase == "encounter":
                ctrl = self._font_ui.render(
                    "Dekati Slime dan tekan  E  untuk bertarung!", True, UI_ACCENT)
            else:
                ctrl = None
            if ctrl:
                surface.blit(ctrl, (self._game.W // 2 - ctrl.get_width() // 2, 8))
        except Exception:
            pass

    def _draw_interact_hint(self, surface, cx, cy):
        """Tanda [E] di atas musuh jika bisa diinteraksi."""
        try:
            f = pygame.font.SysFont("Consolas", 13, bold=True)
            t = f.render("[E] Bertarung!", True, DAMAGE_RED)
            surface.blit(t, (cx - t.get_width() // 2, cy))
        except Exception:
            pass

    def _draw_exclamation(self, surface, cx, cy):
        """Tanda ! kuning di atas NPC yang belum diajak bicara."""
        try:
            f = pygame.font.SysFont("Georgia", 20, bold=True)
            t = f.render("!", True, GOLD_LIGHT)
            alpha = int(180 + 75 * math.sin(self._t * 4))
            t.set_alpha(alpha)
            surface.blit(t, (cx - t.get_width() // 2, cy))
        except Exception:
            pass

    def _draw_party_hud(self, surface):
        members = [
            ("Arga",  self._player.hp, self._player.max_hp),
            ("Elena", self._elena.hp,  self._elena.max_hp),
        ]
        self._party_hud.draw(surface, members)
        