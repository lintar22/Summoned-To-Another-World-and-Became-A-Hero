"""
scenes/chapter_final_scene.py
==============================
Chapter Final — Kastil Raja Iblis.

ALUR:
  pre_battle      → dialog dengan King Aldric di aula kerajaan
  dungeon         → dialog jalan di lorong kastil
  dungeon_warning → peringatan sebelum encounter Dark Knight
  dungeon_encounter → player jalan, tekan E untuk battle Dark Knight
                      (masuk BattleScene biasa, kembali ke sini dengan
                       flag "battle_won_castle_dungeon" → otomatis lanjut
                       ke boss_intro tanpa loop)
  boss_intro      → dialog cutscene pertemuan Demon King
  boss_intro_encounter → player jalan mendekati boss, tekan E
                         → masuk BossBattleScene (menentukan ending)
"""

import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox, FloatingText, PartyHUD


class ChapterFinalScene(Scene):
    """Final Chapter: Kastil Raja Iblis → Dark Knight → Demon King."""

    # ── Dialog pre-battle (King Aldric) ───────────────────────

    PRE_BATTLE_DLGS = [
        ("King Aldric", "Jadi kalian berhasil kembali."),
        ("Arga", "Untungnya begitu."),
        ("King Aldric", "Aku sudah membaca laporan kalian."),
        ("King Aldric", "Desa yang hancur, pergerakan pasukan iblis, dan benteng-benteng yang mulai terancam."),
        ("King Aldric", "...Keadaannya lebih buruk dari yang kuduga."),
        ("Darius", "Itu baru sebagian kecil dari apa yang terjadi di luar sana."),
        ("SYSTEM", "Ruang aula menjadi hening sejenak."),
        ("King Aldric", "Meski begitu, kalian sudah melakukan banyak hal."),
        ("King Aldric", "Lebih banyak daripada yang bisa kuharapkan setahun lalu."),
        ("King Aldric", "Jujur saja, waktu itu aku bahkan tidak yakin kerajaan ini bisa bertahan."),
        ("Reno", "Wah, langsung berat begitu ya pembukaannya."),
        ("Lyra", "Kalau tidak kuat dengar kenyataan, keluar saja."),
        ("Reno", "Aku cuma bercanda."),
        ("King Aldric", "*tersenyum tipis*"),
        ("King Aldric", "Bagaimanapun juga, sekarang kita punya kesempatan."),
        ("King Aldric", "Mata-mata kami akhirnya menemukan lokasi Raja Iblis."),
        ("Elena", "...Jadi benar-benar sudah waktunya."),
        ("King Aldric", "Ya."),
        ("King Aldric", "Dia berada di utara."),
        ("King Aldric", "Dan kalau laporan ini benar, dia tidak berniat bersembunyi lagi."),
        ("Arga", "..."),
        ("King Aldric", "Aku tidak akan memaksa kalian."),
        ("King Aldric", "Kalian sudah melakukan lebih dari cukup."),
        ("King Aldric", "Tapi jika ada seseorang yang bisa menghentikan semua ini, itu adalah kalian."),
        ("Darius", "Pilihan kami sudah dibuat sejak lama."),
        ("Lyra", "Kalau kita berhenti sekarang, semua yang sudah terjadi jadi sia-sia."),
        ("Reno", "Lagipula kita sudah sejauh ini."),
        ("Reno", "Nanggung kalau pulang sekarang."),
        ("Lyra", "Rencanamu selalu terdengar terlalu sederhana."),
        ("Reno", "Karena memang sederhana."),
        ("Lyra", "Tidak. Itu namanya bodoh."),
        ("Reno", "Detail kecil."),
        ("Elena", "hahhh....."),
        ("King Aldric", "hahaha..."),
        ("King Aldric", "Meski situasinya seperti ini, aku senang kalian masih bisa tersenyum."),
        ("King Aldric", "Jangan kehilangan itu."),
        ("King Aldric", "Dunia sudah terlalu lama hidup dalam ketakutan."),
        ("King Aldric", "Atas nama kerajaan."),
        ("King Aldric", "Atas nama mereka yang telah gugur."),
        ("King Aldric", "Dan atas nama mereka yang masih berharap melihat hari esok."),
        ("King Aldric", "Aku mempercayakan masa depan dunia kepada kalian."),
        ("Arga", "...Kami akan kembali."),
        ("Darius", "Dan kali ini, kami akan mengakhirinya."),
        ("Lyra", "Bagaimanapun caranya."),
        ("Reno", "Nah, itu baru semangat."),
        ("Elena", "Ayo."),
        ("Elena", "Kita masih punya perjalanan panjang."),
        ("Reno", "Baiklah."),
        ("Reno", "Tujuan berikutnya: Kastil Raja Iblis."),
        ("Lyra", "Untuk seseorang yang selalu bercanda, kau terdengar cukup serius hari ini."),
        ("Reno", "...Ya."),
        ("Reno", "Kurasa sekarang memang waktunya serius."),
        ("Darius", "Kalau begitu jangan mati sebelum pertarungan dimulai."),
        ("Reno", "Aku bisa bilang hal yang sama padamu."),
        ("Elena", "*tersenyum kecil*"),
        ("Arga", "Ayo pergi."),
        ("Arga", "Kita akhiri semuanya."),
        ("SYSTEM", "Merekapun akhirnya meninggalkan aula kerajaan."),
        ("SYSTEM", "Langkah mereka bergema di lorong-lorong istana yang sunyi."),
        ("SYSTEM", "⚔ Kelompok Pahlawan memulai perjalanan menuju Kastil Raja Iblis."),
        ("SYSTEM", "⚔ CHAPTER FINAL — DEMON KING CASTLE"),
    ]

    # ── Dialog lorong dungeon ──────────────────────────────────

    DUNGEON_DLGS = [
        ("Reno",   "Monster di mana-mana! Tapi kita sudah terlalu jauh untuk mundur!"),
        ("Lyra",   "Simpan tenagamu. Ini bukan boss yang sesungguhnya."),
        ("Darius", "Aku yang di depan. Arga, kau di tengah lindungi Elena."),
        ("Arga",   "Ya, ayo kita masuk bersama-sama!."),
        ("Elena",  "Lorong ini... terasa seperti kuburan."),
        ("Lyra",   "Karena memang begitu. Ini merupakan sisa-sisa jiwa yang terserap Raja Iblis."),
        ("SYSTEM", "🚪 Pintu besar di ujung lorong... terbuka perlahan."),
    ]

    # ── Dialog pertemuan Demon King ────────────────────────────

    BOSS_INTRO = [
        ("Demon King", "Jadi... inikah sang pahlawan dari dunia lain."),
        ("Demon King", "Satu manusia kecil yang berani datang ke singgasanaku."),
        ("Arga",       "Aku datang untuk mengakhiri semuanya. Ini berakhir hari ini."),
        ("Demon King", "Hahaha... kalimat yang sudah kudengar ratusan kali."),
        ("Demon King", "Tapi baiklah. Aku ingin lihat seberapa jauh kamu bisa bertahan."),
        ("Elena",      "Arga... aku bersamamu."),
    ]

    # ──────────────────────────────────────────────────────────

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
        self._phase = "pre_battle"
        self._dlg_step = 0

        self._dialogue   = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator   = NarratorBox(game.W, game.H)
        self._party_hud  = PartyHUD()
        self._floats: list[FloatingText] = []

        self._pending_phase = ""
        self._waiting_fade  = False

        from entities.characters import Player, PartyNPC, BossNPC, KingdomNPC
        ground_y = int(game.H * 0.82)
        self._ground_y = ground_y

        self._player   = Player(-80, ground_y - 55)
        self._player.before_isekai = False
        self._elena    = PartyNPC("Elena",   -140, ground_y - 55)
        self._reno     = PartyNPC("Reno",    -200, ground_y - 55)
        self._lyra     = PartyNPC("Lyra",    -260, ground_y - 55)
        self._darius   = PartyNPC("Darius",  -320, ground_y - 55)
        self._boss     = BossNPC(game.W // 2, ground_y - 100)

        # NPC Kerajaan di sisi kanan layar (pre_battle — Malam Sebelum Perang)
        # Party walkin ke x: 200-520, jadi NPC kerajaan ditempatkan mulai x=750
        #   King Aldric : x=750, Mage : x=900, Knight : x=1060
        self._king_npc   = KingdomNPC("King Aldric", 750,  ground_y - 55, (180, 150, 80))
        self._mage_npc   = KingdomNPC("Mage",        900,  ground_y - 55, (100, 120, 180))
        self._knight_npc = KingdomNPC("Knight",      1060, ground_y - 55, (120, 140, 120))

        # Semua NPC kerajaan menghadap kiri (ke arah party)
        self._king_npc._facing_right   = False
        self._mage_npc._facing_right   = False
        self._knight_npc._facing_right = False

        # Animasi idle hardcode NPC kerajaan (loop seperti di chapter1)
        self._npc_anim_timer   = 0.0
        self._npc_anim_speed   = 0.18   # detik per frame
        self._npc_king_frame   = 0
        self._npc_mage_frame   = 0
        self._npc_knight_frame = 0

        # Dungeon encounter state
        self._dungeon_enemies: list = []
        self._dungeon_walkin_active        = False
        self._dungeon_walkin_done          = False
        self._dungeon_enemies_interactable = False
        self._dungeon_warn_step            = 0

        try:
            self._font_ui = pygame.font.SysFont("Consolas", 15)
        except Exception:
            self._font_ui = pygame.font.Font(None, 18)

    # ── Lifecycle ─────────────────────────────────────────────

    def on_enter(self) -> None:
        self._transition.fade_in(speed=150)
        self._narrator.show(["Chapter Final", "Kastil Raja Iblis"], 3.0)

        # ── Cek apakah baru kembali dari dungeon battle ──
        # Kalau flag castle_dungeon sudah di-set, skip langsung ke boss_intro
        if self._game.flags.get("battle_won_castle_dungeon"):
            self._phase = "boss_intro"
            self._dlg_step = 0
            self._transition.fade_in(speed=160)
            self._narrator.show(["⚔ FINAL BOSS", "DEMON KING"], 2.5)
            self._dialogue.show(self.BOSS_INTRO[0][1], self.BOSS_INTRO[0][0])
            try: self._game.assets.play("damage")
            except Exception: pass
            for ch in (self._elena, self._reno, self._lyra, self._darius):
                ch.disable_follow()
            for ch, tx in [(self._player, 160), (self._elena, 240),
                           (self._reno, 320), (self._lyra, 400), (self._darius, 480)]:
                ch._x = -80
            self.start_walkin([
                (self._player, 160), (self._elena, 240),
                (self._reno, 320), (self._lyra, 400), (self._darius, 480),
            ])
            return

        # Normal: mulai dari pre_battle
        self._dialogue.show(self.PRE_BATTLE_DLGS[0][1], self.PRE_BATTLE_DLGS[0][0])
        self._elena.follow(self._player);  self._elena.follow_distance  = -80
        self._reno.follow(self._player);   self._reno.follow_distance   =  80
        self._lyra.follow(self._player);   self._lyra.follow_distance   = -160
        self._darius.follow(self._player); self._darius.follow_distance =  160
        for ch in (self._elena, self._reno, self._lyra, self._darius):
            ch.disable_follow()
        self.start_walkin([
            (self._player,  200), (self._elena, 280),
            (self._reno,    360), (self._lyra,  440), (self._darius, 520),
        ])

    def on_exit(self) -> None:
        pass

    # ── Event ─────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        key = event.key

        if key in (pygame.K_UP, pygame.K_w):
            if self._dialogue.showing_choices:
                self._dialogue.navigate_choice(-1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            if self._dialogue.showing_choices:
                self._dialogue.navigate_choice(1)
        elif key == pygame.K_e:
            if self._phase == "dungeon_encounter":
                self._try_start_dungeon_battle()
            elif self._phase == "boss_intro_encounter":
                self._enter_boss_battle()
        elif key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
            if self._walkin_active or self._waiting_fade:
                return
            if self._phase in ("dungeon_encounter", "boss_intro_encounter"):
                return  # harus pakai E
            self._advance()

    def _advance(self):
        try: self._game.assets.play("cursor")
        except Exception: pass

        if not self._dialogue.is_finished:
            self._dialogue.skip()
            return

        if self._phase == "pre_battle":
            self._dlg_step += 1
            if self._dlg_step < len(self.PRE_BATTLE_DLGS):
                spk, txt = self.PRE_BATTLE_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == 11:
                    try: self._game.assets.play("fanfare")
                    except Exception: pass
            else:
                self._dlg_step = 0
                self._go_to_phase("dungeon")

        elif self._phase == "dungeon":
            self._dlg_step += 1
            if self._dlg_step < len(self.DUNGEON_DLGS):
                spk, txt = self.DUNGEON_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
            else:
                self._phase = "dungeon_warning"
                self._dungeon_warn_step = 0
                self._dialogue.show("Monster-monster menghalangi jalan ke ruang Raja Iblis!", "Reno")
                try: self._game.assets.play("damage")
                except Exception: pass

        elif self._phase == "dungeon_warning":
            _warns = [
                ("Reno",   "Monster-monster menghalangi jalan ke ruang Raja Iblis!"),
                ("Lyra",   "Ada banyak monster. Hati-Hati!"),
                ("Darius", "Biarkan aku tahan satu. Kalian tangani yang lain!"),
                ("SYSTEM", "Monster muncul dari kegelapan lorong!"),
            ]
            self._dungeon_warn_step += 1
            if self._dungeon_warn_step < len(_warns):
                spk, txt = _warns[self._dungeon_warn_step]
                self._dialogue.show(txt, spk)
            else:
                self._dialogue.hide()
                self._spawn_dungeon_enemies()

        elif self._phase == "boss_intro":
            self._dlg_step += 1
            if self._dlg_step < len(self.BOSS_INTRO):
                spk, txt = self.BOSS_INTRO[self._dlg_step]
                self._dialogue.show(txt, spk)
            else:
                self._phase = "boss_intro_encounter"
                self._dialogue.hide()
                self._narrator.show(["⚔ Dekati Demon King dan tekan  E  untuk memulai pertempuran!"], 2.5)
                try: self._game.assets.play("damage")
                except Exception: pass

    # ── Phase transition ──────────────────────────────────────

    def _go_to_phase(self, new_phase: str):
        self._pending_phase = new_phase
        self._waiting_fade  = True
        self._transition.fade_out(speed=240)

    # ── Dungeon encounter ─────────────────────────────────────

    def _spawn_dungeon_enemies(self):
        from entities.characters import MonsterNPC
        screen_w = self._game.W
        configs = [
            ("Minotaur", float(screen_w + 80),  float(screen_w - 180), 220),
            ("Minotaur", float(screen_w + 180), float(screen_w - 300), 220),
        ]
        for name, start_x, target_x, hp in configs:
            m = MonsterNPC(name, start_x, self._ground_y - 45, hp=hp)
            m._target_x = target_x
            self._dungeon_enemies.append(m)
        self._dungeon_walkin_active        = True
        self._dungeon_walkin_done          = False
        self._dungeon_enemies_interactable = False
        self._phase = "dungeon_encounter"
        self._narrator.show(["Minotaur menghalangi!", "Dekati dan tekan  E  untuk bertarung!"], 2.5)

    def _try_start_dungeon_battle(self):
        if not self._dungeon_enemies_interactable:
            return
        px = self._player._x
        for enemy in self._dungeon_enemies:
            if abs(enemy.x - px) < 130:
                self._enter_dungeon_battle()
                return
        self._narrator.show(["Dekati Dark Knight terlebih dahulu!"], 1.0)

    def _enter_dungeon_battle(self):
        from battle.battle_scene import start_battle_scene, ENCOUNTER_CASTLE_DUNGEON
        start_battle_scene(
            game=self._game,
            enemies=ENCOUNTER_CASTLE_DUNGEON,
            return_scene_class=self.__class__,
            context={"chapter": "final", "encounter_id": "castle_dungeon"},
        )

    # ── Boss encounter ────────────────────────────────────────

    def _enter_boss_battle(self):
        from battle.boss_battle_scene import start_boss_battle
        start_boss_battle(self._game)

    # ── Update ────────────────────────────────────────────────

    def update(self, dt: float) -> None:
        self._t += dt
        self._transition.update(dt)
        self._dialogue.update(dt)
        self._narrator.update(dt)
        self.update_walkin(dt)

        if self._walkin_active:
            self._player.set_walking(True, True)

        # Handle fade-out selesai → ganti phase
        if self._waiting_fade and self._transition.done:
            self._waiting_fade  = False
            self._phase         = self._pending_phase
            self._pending_phase = ""
            self._dlg_step      = 0

            if self._phase == "dungeon":
                self._transition.fade_in(speed=200)
                self._narrator.show(["Lorong Kastil Raja Iblis", "Menuju Singgasana Kegelapan..."], 2.5)
                self._dialogue.show(self.DUNGEON_DLGS[0][1], self.DUNGEON_DLGS[0][0])
                for ch in (self._elena, self._reno, self._lyra, self._darius):
                    ch.disable_follow()
                for ch in (self._player, self._elena, self._reno, self._lyra, self._darius):
                    ch._x = -80
                # Paksa idle menghadap depan di lorong (bukan idle samping)
                self._player.use_front_idle = True
                self.start_walkin([
                    (self._player, 180), (self._elena,  270),
                    (self._reno,   360), (self._lyra,   450), (self._darius, 540),
                ])

            elif self._phase == "boss_intro":
                self._player.use_front_idle = False  # reset ke side idle saat boss intro
                self._transition.fade_in(speed=160)
                self._narrator.show(["⚔ FINAL BOSS", "DEMON KING"], 2.5)
                self._dialogue.show(self.BOSS_INTRO[0][1], self.BOSS_INTRO[0][0])
                try: self._game.assets.play("damage")
                except Exception: pass
                for ch in (self._elena, self._reno, self._lyra, self._darius):
                    ch.disable_follow()
                for ch in (self._player, self._elena, self._reno, self._lyra, self._darius):
                    ch._x = -80
                self.start_walkin([
                    (self._player, 160), (self._elena, 240),
                    (self._reno,   320), (self._lyra,  400), (self._darius, 480),
                ])

        # Update karakter
        self._player.update(dt)
        self._elena.update(dt)
        self._reno.update(dt)
        self._lyra.update(dt)
        self._darius.update(dt)
        if self._phase not in ("pre_battle", "dungeon", "dungeon_warning", "dungeon_encounter"):
            self._boss.update(dt)

        # Animasi idle hardcode NPC kerajaan di pre_battle (loop King, Mage, Knight)
        if self._phase == "pre_battle":
            self._npc_anim_timer += dt
            if self._npc_anim_timer >= self._npc_anim_speed:
                self._npc_anim_timer = 0.0
                assets = self._game.assets
                king_f  = getattr(assets, "king_aldric_idle_frames", [])
                mage_f  = getattr(assets, "mage_idle_frames",        [])
                kngt_f  = getattr(assets, "knight_idle_frames",      [])
                if king_f:  self._npc_king_frame   = (self._npc_king_frame   + 1) % len(king_f)
                if mage_f:  self._npc_mage_frame   = (self._npc_mage_frame   + 1) % len(mage_f)
                if kngt_f:  self._npc_knight_frame = (self._npc_knight_frame + 1) % len(kngt_f)

        # Aktifkan follow setelah walkin selesai
        if not self._walkin_active:
            for ch in (self._elena, self._reno, self._lyra, self._darius):
                if not ch._follow_enabled:
                    ch.enable_follow()

        # Walk-in dungeon enemies dari kanan
        if self._dungeon_walkin_active:
            all_arrived = True
            for enemy in self._dungeon_enemies:
                tx = getattr(enemy, '_target_x', enemy.x)
                if enemy.x > tx + 2:
                    enemy.x = max(tx, enemy.x - 220 * dt)
                    if hasattr(enemy, 'set_walking'):
                        enemy.set_walking(True, True)
                    all_arrived = False
                else:
                    enemy.x = tx
                    if hasattr(enemy, 'set_walking'):
                        enemy.set_walking(False)
            if all_arrived and not self._dungeon_walkin_done:
                self._dungeon_walkin_done          = True
                self._dungeon_walkin_active        = False
                self._dungeon_enemies_interactable = True

        for enemy in self._dungeon_enemies:
            enemy.update(dt)

        # Kontrol player saat encounter (bisa jalan)
        if self._phase in ("dungeon_encounter", "boss_intro_encounter") and not self._walkin_active:
            keys = pygame.key.get_pressed()
            moving_left  = keys[pygame.K_LEFT]  or keys[pygame.K_a]
            moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
            dx = 0
            if moving_left:  dx = -160 * dt
            if moving_right: dx =  160 * dt
            if dx != 0:
                self._player._x = max(60, min(self._game.W - 60, self._player._x + dx))
            if moving_left and not moving_right:
                self._player.set_walking(True, False)
            elif moving_right and not moving_left:
                self._player.set_walking(True, True)
            else:
                self._player.set_walking(False)
        elif not self._walkin_active:
            self._player.set_walking(False)

        for ft in self._floats:
            ft.update(dt)
        self._floats = [f for f in self._floats if f.alive]

    # ── Draw helpers ─────────────────────────────────────────────

    def _draw_npc_frame(self, surface, frames_attr, frame_idx, x, y,
                        scale=1.6, facing_right=True):
        """Gambar NPC dari frame list di assets, normalisasi ke 96px (identik dengan ch1)."""
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

    # ── Draw ──────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        # Background
        if self._phase == "pre_battle":
            bg_pre = (getattr(self._game.assets, "bg_belairung", None)
                      or getattr(self._game.assets, "bg_throne_room", None))
            if bg_pre:
                surface.blit(bg_pre, (0, 0))
            else:
                surface.fill((30, 20, 50))
        elif self._phase in ("dungeon", "dungeon_warning", "dungeon_encounter"):
            bg_dng = getattr(self._game.assets, "bg_castle_ext", None)
            if bg_dng:
                surface.blit(bg_dng, (0, 0))
            else:
                surface.fill((20, 15, 30))
        else:
            # boss_intro, boss_intro_encounter → pakai bg ruang boss
            bg_boss = (getattr(self._game.assets, "bg_ruang_boss", None)
                       or getattr(self._game.assets, "bg_castle_int", None))
            if bg_boss:
                surface.blit(bg_boss, (0, 0))
            else:
                surface.fill((15, 5, 25))

        # Pre-battle: NPC Kerajaan (animasi hardcode) + party
        if self._phase == "pre_battle":
            # Knight paling kanan → gambar duluan agar King di depan
            self._draw_npc_frame(surface, "knight_idle_frames",      self._npc_knight_frame,
                                 int(self._knight_npc._x), int(self._knight_npc._y),
                                 facing_right=self._knight_npc._facing_right)
            self._draw_npc_frame(surface, "mage_idle_frames",        self._npc_mage_frame,
                                 int(self._mage_npc._x),   int(self._mage_npc._y),
                                 facing_right=self._mage_npc._facing_right)
            self._draw_npc_frame(surface, "king_aldric_idle_frames", self._npc_king_frame,
                                 int(self._king_npc._x),   int(self._king_npc._y),
                                 facing_right=self._king_npc._facing_right)
            # Party (digambar setelah NPC agar tampak di depan)
            self.draw_char_scaled(surface, self._darius, 1.6)
            self.draw_char_scaled(surface, self._lyra,   1.6)
            self.draw_char_scaled(surface, self._reno,   1.6)
            self.draw_char_scaled(surface, self._elena,  1.6)
            self.draw_char_scaled(surface, self._player, 1.6)

        # Dungeon
        elif self._phase in ("dungeon", "dungeon_warning", "dungeon_encounter"):
            self.draw_char_scaled(surface, self._player, 1.6)
            self.draw_char_scaled(surface, self._elena,  1.6)
            self.draw_char_scaled(surface, self._reno,   1.6)
            self.draw_char_scaled(surface, self._lyra,   1.6)
            self.draw_char_scaled(surface, self._darius, 1.6)
            for enemy in self._dungeon_enemies:
                self.draw_char_scaled(surface, enemy, 1.7)
                if self._dungeon_enemies_interactable and abs(enemy.x - self._player._x) < 130:
                    try:
                        f = pygame.font.SysFont("Consolas", 13, bold=True)
                        t = f.render("[E] Bertarung!", True, DAMAGE_RED)
                        surface.blit(t, (int(enemy.x) - t.get_width() // 2, int(enemy.y) - 70))
                    except Exception:
                        pass
            if self._phase == "dungeon_encounter" and self._dungeon_enemies_interactable:
                try:
                    f = pygame.font.SysFont("Consolas", 14)
                    h = f.render("← → Jalan  |  E Bertarung saat dekat Dark Knight!", True, UI_ACCENT)
                    surface.blit(h, (self._game.W // 2 - h.get_width() // 2, self._game.H - 30))
                except Exception:
                    pass

        # Boss intro / encounter
        else:
            self.draw_char_scaled(surface, self._boss,   2.2)
            self.draw_char_scaled(surface, self._player, 1.6)
            self.draw_char_scaled(surface, self._elena,  1.6)
            self.draw_char_scaled(surface, self._reno,   1.6)
            self.draw_char_scaled(surface, self._lyra,   1.6)
            self.draw_char_scaled(surface, self._darius, 1.6)

            if self._phase == "boss_intro_encounter":
                boss_dist = abs(self._boss.x - self._player._x)
                if boss_dist < 150:
                    try:
                        f = pygame.font.SysFont("Consolas", 13, bold=True)
                        t = f.render("[E] Mulai Battle!", True, DAMAGE_RED)
                        surface.blit(t, (int(self._boss.x) - t.get_width() // 2, int(self._boss.y) - 80))
                    except Exception:
                        pass
                try:
                    f = pygame.font.SysFont("Consolas", 14)
                    h = f.render("← → Jalan  |  E Bertarung saat dekat Demon King!", True, UI_ACCENT)
                    surface.blit(h, (self._game.W // 2 - h.get_width() // 2, self._game.H - 30))
                except Exception:
                    pass

        # Floating texts
        for ft in self._floats:
            ft.draw(surface)

        # UI
        self._narrator.draw(surface)
        self._dialogue.draw(surface)
        members = [
            ("Arga",   self._player.hp, self._player.max_hp),
            ("Elena",  self._elena.hp,  self._elena.max_hp),
            ("Reno",   self._reno.hp,   self._reno.max_hp),
            ("Lyra",   self._lyra.hp,   self._lyra.max_hp),
            ("Darius", self._darius.hp, self._darius.max_hp),
        ]
        self._party_hud.draw(surface, members)
        self._transition.draw(surface)

        # Label lokasi
        lbl_map = {
            "pre_battle":          "Aula Kerajaan Astravia — Malam Sebelum Perang",
            "dungeon":             "Lorong Kastil Raja Iblis",
            "dungeon_warning":     "Lorong Kastil Raja Iblis",
            "dungeon_encounter":   "Lorong Kastil — Monster Menghalangi!",
            "boss_intro":          "Singgasana Kegelapan — Demon King",
            "boss_intro_encounter":"Singgasana Kegelapan — Kalahkan Demon King!",
        }
        lbl = lbl_map.get(self._phase, "")
        if lbl:
            try:
                t = self._font_ui.render(lbl, True, UI_ACCENT)
                surface.blit(t, (self._game.W // 2 - t.get_width() // 2, 8))
            except Exception:
                pass
