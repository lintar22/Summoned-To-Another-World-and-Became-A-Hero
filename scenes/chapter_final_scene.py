"""
scenes/chapter_final_scene.py
==============================
Chapter Final — Demon King Castle: Pre-battle, Final Boss, Pilihan, True/Bad End.
FIX: Walk-in karakter, background tidak hilang saat transisi, fade-in setelah fadeout.
[INHERITANCE] Scene(ABC). [POLYMORPHISM] BossNPC.use_skill() dan BossNPC.draw() berbeda.
"""

import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox, FloatingText, BattleUI, PartyHUD


class ChapterFinalScene(Scene):
    """Final Chapter: Kastil Raja Iblis, Final Battle, Branching Ending."""

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
        ("Lyra", "Kau benar-benar tidak bisa serius, ya?"),
        ("Reno", "Aku serius."),
        ("Reno", "Sedikit."),
        ("Elena", "*tertawa kecil*"),
        ("Elena", "Takut?"),
        ("Arga", "...Sedikit."),
        ("Arga", "Kau juga?"),
        ("Elena", "Jelas."),
        ("Elena", "Aku akan lebih khawatir kalau tidak ada yang takut menghadapi Raja Iblis."),
        ("Reno", "Nah, aku tidak takut."),
        ("Lyra", "Karena otakmu tidak sampai ke sana."),
        ("Reno", "Sakit juga ternyata."),
        ("Darius", "Takut bukan masalah."),
        ("Darius", "Yang penting kita tetap melangkah."),
        ("Arga", "...Benar juga."),
        ("King Aldric", "Kalau begitu, aku tidak akan menahan kalian lebih lama."),
        ("King Aldric", "Pasukan kerajaan akan mengawal kalian sampai perbatasan utara."),
        ("King Aldric", "Setelah itu, jalan menuju kastil sepenuhnya berada di wilayah musuh."),
        ("Elena", "Jadi mulai dari sana, kita benar-benar sendirian."),
        ("King Aldric", "Ya."),
        ("King Aldric", "Aku berharap bisa mengirim lebih banyak bantuan."),
        ("Darius", "Pasukan biasa hanya akan menjadi korban."),
        ("Darius", "Kita semua tahu itu."),
        ("King Aldric", "...Benar."),
        ("Lyra", "Setidaknya dia jujur."),
        ("Reno", "Nah, kalau begitu tidak ada lagi yang perlu dibahas."),
        ("Reno", "Kita datang, kita menang, lalu pulang sebagai pahlawan."),
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
        ("SYSTEM", "⚔ CHAPTER FINAL — DEMON KING CASTLE")
        

    ]

    DUNGEON_DLGS = [
        ("Reno",   "Monster di mana-mana! Tapi kita sudah terlalu jauh untuk mundur!"),
        ("Lyra",   "Simpan tenagamu. Ini bukan boss yang sesungguhnya."),
        ("Darius", "Aku yang di depan. Arga, kau di tengah lindungi Elena."),
        ("Arga",   "Ya, ayo kita masuk bersama-sama!."),
        ("Elena",  "Lorong ini... terasa seperti kuburan."),
        ("Lyra",   "Karena memang begitu. Ini merupakan sisa-sisa jiwa yang terserap Raja Iblis."),
        ("SYSTEM", "🚪 Pintu besar di ujung lorong... terbuka perlahan."),
    ]

    BOSS_INTRO = [
        ("Demon King", "Jadi... inikah sang pahlawan dari dunia lain."),
        ("Demon King", "Satu manusia kecil yang berani datang ke singgasanaku."),
        ("Arga",       "Aku datang untuk mengakhiri semuanya. Ini berakhir hari ini."),
        ("Demon King", "Hahaha... kalimat yang sudah kudengar ratusan kali."),
        ("Demon King", "Tapi baiklah. Aku ingin lihat seberapa jauh kamu bisa bertahan."),
        ("Elena",      "Arga... aku bersamamu."),
    ]

    PHASE1_DLGS = [
        ("Reno",   "SERANG! Jangan beri dia kesempatan!"),
        ("Lyra",   "Barrier-nya kuat. butuh terobosan besar!"),
        ("Darius", "Aku tahan serangan kanannya! Kalian serang kiri!"),
    ]

    ELENA_HIT_DLGS = [
        ("SYSTEM", "⚡ Raja Iblis melepaskan serangan kelap gelap ke arah Elena!"),
        ("Elena",  "Ar... ga...!"),
        ("SYSTEM", "💀 PILIHAN KRITIS — Apa yang kamu lakukan?"),
    ]

    TRUE_P1 = [
        ("Arga",       "Elena!!"),
        ("SYSTEM",     "🛡 Arga melempar dirinya menutupi Elena dengan tubuhnya!"),
        ("Elena",      "Arga... bodoh... kenapa kau..."),
        ("Arga",       "Aku tidak akan kehilangan siapa pun lagi. TIDAK AKAN!"),
        ("Reno",       "SEKARANG! Dia terbuka! SERANG BERSAMA!!"),
        ("Lyra",       "Aku buka jalannya — ASTRAL BREAK!"),
        ("Darius",     "PEDANG UNTUK DUNIA — MAJUUUU!!"),
        ("Arga",       "CELESTIAL OVERDRIVE!!!"),
        ("SYSTEM",     "✨ LIMIT BREAK — Cahaya emas membelah singgasana kegelapan!"),
        ("Demon King", "Mustahil... kekuatan manusia... tidak seharusnya sebesar..."),
        ("SYSTEM",     "💀 Raja Iblis hancur menjadi debu cahaya."),
    ]

    BAD_P1 = [
        ("Arga",       "Kalau dia mati sekarang — semuanya selesai! SERANG!"),
        ("SYSTEM",     "Elena terkena serangan penuh Raja Iblis..."),
        ("Elena",      "Ar... ga... kenapa..."),
        ("Reno",       "ELENA!! Kau gila, Arga?!"),
        ("Lyra",       "Tidak... tidak mungkin..."),
        ("SYSTEM",     "Raja Iblis tertawa. Party mulai kewalahan satu per satu."),
        ("Darius",     "...Maaf. Aku gagal melindungi."),
        ("SYSTEM",     "Reno tumbang. Lyra kehabisan mana. Darius hancur."),
        ("Arga",       "...Aku salah. Aku salah satu kali saja..."),
        ("Demon King", "Hahaha... manusia tetap manusia. Haus kemenangan hingga akhir."),
        ("SYSTEM",     "Raja Iblis menancapkan tangannya ke dada Arga."),
    ]

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
        # phase: pre_battle → dungeon → boss_intro → phase1 → attacking_boss
        #        → elena_hit → choice → true_end/bad_end → ending
        self._phase = "pre_battle"
        self._dlg_step = 0
        self._dialogue = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator   = NarratorBox(game.W, game.H)
        self._battle_ui  = BattleUI(game.W, game.H)
        self._floats: list[FloatingText] = []
        self._party_hud = PartyHUD()

        from entities.characters import Player, PartyNPC, BossNPC, TownNPC
        ground_y = int(game.H * 0.72)
        self._ground_y = ground_y

        # Semua karakter dimulai di luar layar (akan walkin)
        self._player   = Player(-80, ground_y - 55)
        self._player.before_isekai = False   # sudah dapat Holy Sword
        self._elena    = PartyNPC("Elena",   -140, ground_y - 55)
        self._reno     = PartyNPC("Reno",    -200, ground_y - 55)
        self._lyra     = PartyNPC("Lyra",    -260, ground_y - 55)
        self._darius   = PartyNPC("Darius",  -320, ground_y - 55)
        self._boss     = BossNPC(self._game.W // 2, ground_y - 100)
        self._king_npc = TownNPC("King Aldric", game.W // 2, ground_y - 55, (180, 150, 80))

        self._boss_hp_ratio = 1.0
        self._boss_phase    = 1
        self._battle_round  = 0
        self._slash_timer   = 0.0
        self._slash_active  = False
        self._shake_timer   = 0.0
        self._shake_x       = 0
        self._particles: list[dict] = []
        self._ending_route  = ""
        self._ending_timer  = 0.0

        self._pending_phase = ""
        self._waiting_fade  = False

        try:
            self._font_ch  = pygame.font.SysFont("Georgia", 36, bold=True)
            self._font_end = pygame.font.SysFont("Georgia", 46, bold=True)
            self._font_sub = pygame.font.SysFont("Georgia", 22, italic=True)
            self._font_ui  = pygame.font.SysFont("Consolas", 15)
        except Exception:
            self._font_ch  = pygame.font.Font(None, 40)
            self._font_end = pygame.font.Font(None, 50)
            self._font_sub = pygame.font.Font(None, 26)
            self._font_ui  = pygame.font.Font(None, 18)

    def on_enter(self) -> None:
        self._transition.fade_in(speed=150)
        self._narrator.show(["Chapter Final", "Kastil Raja Iblis"], 3.0)
        self._dialogue.show(self.PRE_BATTLE_DLGS[0][1], self.PRE_BATTLE_DLGS[0][0])
        # Walk-in semua party + king
        self.start_walkin([
            (self._player,   200),
            (self._elena,    290),
            (self._reno,     380),
            (self._lyra,     470),
            (self._darius,   560),
        ])

    def _go_to_phase(self, new_phase: str):
        self._pending_phase = new_phase
        self._waiting_fade = True
        self._transition.fade_out(speed=240)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key in (pygame.K_UP, pygame.K_w):
                if self._dialogue.showing_choices:
                    self._dialogue.navigate_choice(-1)
            elif key in (pygame.K_DOWN, pygame.K_s):
                if self._dialogue.showing_choices:
                    self._dialogue.navigate_choice(1)
            elif key == pygame.K_e:
                # Interaksi dengan boss atau dungeon enemies
                if self._phase == "dungeon_encounter":
                    self._try_start_dungeon_battle()
                elif self._phase == "boss_intro_encounter":
                    self._enter_boss_battle()
            elif key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                if self._walkin_active or self._waiting_fade:
                    return
                if self._phase in ("dungeon_encounter", "boss_intro_encounter"):
                    return  # Harus pakai E
                self._advance()

    def _advance(self):
        self._game.assets.play("cursor")

        # Choice handler
        if self._dialogue.showing_choices:
            choice = self._dialogue.confirm_choice()
            self._dialogue.hide()
            self._ending_route = "true" if choice == 0 else "bad"
            self._phase = "true_end" if choice == 0 else "bad_end"
            self._dlg_step = 0
            dlgs = self.TRUE_P1 if self._phase == "true_end" else self.BAD_P1
            self._dialogue.show(dlgs[0][1], dlgs[0][0])
            if choice == 0:
                self._game.assets.play("magic")
            else:
                self._game.assets.play("damage")
            return

        if not self._dialogue.is_finished:
            self._dialogue.skip()
            return

        if self._phase == "pre_battle":
            self._dlg_step += 1
            if self._dlg_step < len(self.PRE_BATTLE_DLGS):
                spk, txt = self.PRE_BATTLE_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == 11:
                    self._game.assets.play("fanfare")
            else:
                self._dlg_step = 0
                self._go_to_phase("dungeon")

        elif self._phase == "dungeon":
            self._dlg_step += 1
            if self._dlg_step < len(self.DUNGEON_DLGS):
                spk, txt = self.DUNGEON_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
            else:
                # Semua dialog dungeon selesai → tampilkan warning Dark Knight
                self._phase = "dungeon_warning"
                self._dungeon_warn_step = 0
                self._dialogue.show("Monster-monster menghalangi jalan ke singgasana!", "Reno")
                self._game.assets.play("damage")

        elif self._phase == "dungeon_warning":
            self._dungeon_warn_step = getattr(self, '_dungeon_warn_step', 0) + 1
            _dungeon_warns = [
                ("Reno",   "Monster-monster menghalangi jalan ke singgasana!"),
                ("Lyra",   "Ada banyak monster. Hati-Hati!"),
                ("Darius", "Biarkan aku tahan satu. Kalian tangani yang lain!"),
                ("SYSTEM", "⚠ Monster muncul dari kegelapan lorong!"),
            ]
            if self._dungeon_warn_step < len(_dungeon_warns):
                spk, txt = _dungeon_warns[self._dungeon_warn_step]
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
                # Semua dialog boss intro selesai → player harus interaksi dengan boss
                self._phase = "boss_intro_encounter"
                self._dialogue.hide()
                self._narrator.show(["⚔ Dekati Demon King dan tekan  E  untuk memulai pertempuran!"], 2.5)
                self._game.assets.play("damage")

        elif self._phase == "boss_intro_encounter":
            pass  # Hanya bisa dimulai lewat tekan E (handle_event)

        elif self._phase == "phase1":
            self._dlg_step += 1
            if self._dlg_step < len(self.PHASE1_DLGS):
                spk, txt = self.PHASE1_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == 3:  # Divine Slash
                    self._slash_active = True
                    self._slash_timer  = 0.0
                    self._shake_timer  = 0.4
                    self._game.assets.play("slash")
                    self._floats.append(FloatingText("DIVINE SLASH!", self._game.W // 2, 160, GOLD_LIGHT))
            else:
                self._do_boss_attack()

        elif self._phase == "attacking_boss":
            self._battle_round += 1
            if self._battle_round < 4:
                dmg = random.randint(8000, 14000)
                self._boss.take_damage(dmg)
                self._boss_hp_ratio = self._boss.hp / self._boss.max_hp
                self._spawn_particles(self._boss.x, self._boss.y)
                self._floats.append(FloatingText(f"-{dmg}", self._boss.x, self._boss.y - 40, GOLD_LIGHT))
                self._slash_active = True
                self._slash_timer  = 0.0
                self._shake_timer  = 0.3
                self._game.assets.play("slash")
                skills = ["Divine Slash", "Celestial Flame", "Holy Barrier", "Time Acceleration"]
                skill = skills[self._battle_round % len(skills)]
                self._dialogue.show(f"[{skill}] — Serang bersama!", "Arga")
                if self._boss_hp_ratio < 0.5 and self._boss_phase == 1:
                    self._boss_phase = 2
                    self._narrator.show(["⚠ Boss masuk Phase 2!", "Kekuatannya berlipat ganda!"], 2.0)
                    self._game.assets.play("damage")
            else:
                # Elena terkena
                self._phase = "elena_hit"
                self._dlg_step = 0
                self._dialogue.show(self.ELENA_HIT_DLGS[0][1], self.ELENA_HIT_DLGS[0][0])
                self._elena.take_damage(4000)
                self._elena.emotion = "sad"
                self._game.assets.play("damage")
                self._shake_timer = 0.6

        elif self._phase == "elena_hit":
            self._dlg_step += 1
            if self._dlg_step < len(self.ELENA_HIT_DLGS) - 1:
                spk, txt = self.ELENA_HIT_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
            else:
                self._dialogue.show(
                    "Elena terkena serangan keras! Apa yang kamu lakukan?",
                    "SYSTEM",
                    choices=[
                        "Lindungi Elena Segera!",
                        "Terus Serang Raja Iblis!"
                    ]
                )

        elif self._phase in ("true_end", "bad_end"):
            dlgs = self.TRUE_P1 if self._phase == "true_end" else self.BAD_P1
            self._dlg_step += 1
            if self._dlg_step < len(dlgs):
                spk, txt = dlgs[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._phase == "true_end":
                    if self._dlg_step == 7:  # CELESTIAL OVERDRIVE
                        self._slash_active = True
                        self._slash_timer  = 0.0
                        self._game.assets.play("magic")
                        self._game.assets.play("fanfare")
                        self._spawn_big_particles()
                    elif self._dlg_step == 10:  # Boss kalah
                        self._boss.take_damage(999999)
                        self._boss_hp_ratio = 0
                        self._game.assets.play("flash")
                else:  # bad_end
                    if self._dlg_step == 7:
                        self._darius.take_damage(99999)
                    elif self._dlg_step == 10:
                        self._game.assets.play("damage")
            else:
                self._phase = "ending"
                self._ending_timer = 0.0
                self._transition.fade_out(color=(0, 0, 0), speed=130)

        elif self._phase == "ending":
            pass

    def _do_boss_attack(self):
        self._phase = "attacking_boss"
        self._dlg_step = 0
        dmg = random.randint(6000, 10000)
        self._boss.take_damage(dmg)
        self._boss_hp_ratio = self._boss.hp / self._boss.max_hp
        self._slash_active = True
        self._slash_timer  = 0.0
        self._shake_timer  = 0.35
        self._game.assets.play("slash")
        self._floats.append(FloatingText(f"-{dmg}", self._boss.x, self._boss.y - 40, GOLD_LIGHT))
        self._dialogue.show("Divine Slash! Pertarungan dimulai!", "Arga")

    # ── Dungeon & Boss Encounter (Turn-Based) ─────────────────────────────────

    def _spawn_dungeon_enemies(self):
        """Spawn 2 Dark Knight dari kanan — dungeon encounter walk-in."""
        from entities.characters import MonsterNPC
        ground_y = self._ground_y
        screen_w = self._game.W
        self._dungeon_enemies: list = []
        configs = [
            ("Dark Knight", float(screen_w + 80),  float(screen_w - 180), 220),
            ("Dark Knight", float(screen_w + 180), float(screen_w - 300), 220),
        ]
        for name, start_x, target_x, hp in configs:
            m = MonsterNPC(name, start_x, ground_y - 45, hp=hp)
            m._target_x = target_x
            self._dungeon_enemies.append(m)
        self._dungeon_walkin_active        = True
        self._dungeon_walkin_done          = False
        self._dungeon_enemies_interactable = False
        self._phase = "dungeon_encounter"
        self._narrator.show(["⚠ Dark Knight menghalangi!", "Dekati dan tekan  E  untuk bertarung!"], 2.5)

    def _try_start_dungeon_battle(self):
        """Cek jarak player ke Dark Knight — interaksi kelompok."""
        if not getattr(self, '_dungeon_enemies_interactable', False):
            return
        px = self._player._x
        for enemy in getattr(self, '_dungeon_enemies', []):
            if abs(enemy.x - px) < 130:
                self._enter_dungeon_battle()
                return
        self._narrator.show(["Dekati Dark Knight terlebih dahulu!"], 1.0)

    def _enter_dungeon_battle(self):
        """
        [HINT] Masuk turn-based battle untuk encounter Dark Knight di dungeon.
        Hapus fallback NotImplementedError setelah BattleScene diimplementasi.
        """
        try:
            from battle.battle_scene import start_battle_scene, ENCOUNTER_CASTLE_DUNGEON
            start_battle_scene(
                game=self._game,
                enemies=ENCOUNTER_CASTLE_DUNGEON,
                return_scene_class=self.__class__,
                context={"chapter": "final", "encounter_id": "castle_dungeon"},
            )
        except NotImplementedError:
            # [SEMENTARA] Simulasi menang — lanjut ke boss intro
            self._narrator.show(
                ["[BATTLE SCENE BELUM ADA]", "Anggap menang — lanjut ke boss..."], 2.5
            )
            setattr(self, '_dungeon_enemies', [])
            self._dungeon_enemies_interactable = False
            self._dlg_step = 0
            self._go_to_phase("boss_intro")

    def _enter_boss_battle(self):
        """
        [HINT] Masuk turn-based battle untuk Demon King (boss final).
        Interaksi player dengan Boss NPC → masuk battle.
        Hapus fallback NotImplementedError setelah BattleScene diimplementasi.
        """
        try:
            from battle.battle_scene import start_battle_scene, ENCOUNTER_DEMON_KING
            start_battle_scene(
                game=self._game,
                enemies=ENCOUNTER_DEMON_KING,
                return_scene_class=self.__class__,
                context={"chapter": "final", "encounter_id": "demon_king", "is_boss": True},
            )
        except NotImplementedError:
            # [SEMENTARA] Simulasi — lanjut ke phase pilihan kritis
            self._narrator.show(
                ["[BATTLE SCENE BELUM ADA]", "Langsung ke pilihan kritis..."], 2.0
            )
            self._phase = "elena_hit"
            self._dlg_step = 0
            self._dialogue.show(self.ELENA_HIT_DLGS[0][1], self.ELENA_HIT_DLGS[0][0])
            self._game.assets.play("damage")

    def _spawn_particles(self, cx, cy):
        for _ in range(20):
            self._particles.append({
                'x': cx, 'y': cy,
                'vx': random.uniform(-180, 180),
                'vy': random.uniform(-200, 50),
                'life': random.uniform(0.4, 1.2),
                'max_life': 1.2,
                'size': random.randint(3, 7),
                'col': random.choice([(255, 220, 80), (255, 160, 40), (255, 240, 200)]),
            })

    def _spawn_big_particles(self):
        for _ in range(60):
            self._particles.append({
                'x': random.randint(0, self._game.W),
                'y': random.randint(0, self._game.H),
                'vx': random.uniform(-100, 100),
                'vy': random.uniform(-300, -50),
                'life': random.uniform(0.8, 2.0),
                'max_life': 2.0,
                'size': random.randint(4, 12),
                'col': random.choice([(255, 240, 120), (200, 240, 255), (255, 200, 80)]),
            })

    def update(self, dt: float) -> None:
        self._t += dt
        self._transition.update(dt)
        self._dialogue.update(dt)
        self._narrator.update(dt)

        self.update_walkin(dt)

        # Animasi walk selama walkin aktif (masuk scene)
        if self._walkin_active:
            self._player.set_walking(True, True)

        # Handle fade-out done → switch phase
        if self._waiting_fade and self._transition.done:
            self._waiting_fade = False
            self._phase = self._pending_phase
            self._pending_phase = ""
            self._dlg_step = 0

            if self._phase == "dungeon":
                self._transition.fade_in(speed=200)
                self._narrator.show(["Lorong Kastil Raja Iblis", "Menuju Singgasana Kegelapan..."], 2.5)
                self._dialogue.show(self.DUNGEON_DLGS[0][1], self.DUNGEON_DLGS[0][0])
                # Party jalan masuk dari kiri ke kanan
                for ch, tx in [(self._player, 180), (self._elena, 270),
                               (self._reno, 360), (self._lyra, 450), (self._darius, 540)]:
                    ch._x = -80
                self.start_walkin([
                    (self._player, 180),
                    (self._elena,  270),
                    (self._reno,   360),
                    (self._lyra,   450),
                    (self._darius, 540),
                ])
            elif self._phase == "boss_intro":
                self._transition.fade_in(speed=160)
                self._narrator.show(["⚔ FINAL BOSS", "DEMON KING"], 2.5)
                self._dialogue.show(self.BOSS_INTRO[0][1], self.BOSS_INTRO[0][0])
                self._game.assets.play("damage")
                # Party masuk dari kiri, boss sudah di tengah-kanan
                for ch, tx in [(self._player, 160), (self._elena, 240),
                               (self._reno, 320), (self._lyra, 400), (self._darius, 480)]:
                    ch._x = -80
                self.start_walkin([
                    (self._player, 160),
                    (self._elena,  240),
                    (self._reno,   320),
                    (self._lyra,   400),
                    (self._darius, 480),
                ])

        # Update karakter
        self._player.update(dt)
        self._elena.update(dt)
        self._reno.update(dt)
        self._lyra.update(dt)
        self._darius.update(dt)
        if self._phase not in ("pre_battle", "dungeon", "dungeon_warning", "dungeon_encounter"):
            self._boss.update(dt)

        # Walk-in dungeon enemies dari kanan
        if getattr(self, '_dungeon_walkin_active', False):
            all_arrived = True
            for enemy in getattr(self, '_dungeon_enemies', []):
                tx = getattr(enemy, '_target_x', enemy.x)
                if enemy.x > tx + 2:
                    enemy.x = max(tx, enemy.x - 220 * dt)
                    all_arrived = False
                else:
                    enemy.x = tx
            if all_arrived and not getattr(self, '_dungeon_walkin_done', True):
                self._dungeon_walkin_done          = True
                self._dungeon_walkin_active        = False
                self._dungeon_enemies_interactable = True

        # Update dungeon enemies
        for enemy in getattr(self, '_dungeon_enemies', []):
            enemy.update(dt)

        # Gerakan player saat dungeon_encounter dan boss_intro_encounter
        if self._phase in ("dungeon_encounter", "boss_intro_encounter") and not self._walkin_active:
            keys = pygame.key.get_pressed()
            dx = 0
            moving_left  = keys[pygame.K_LEFT]  or keys[pygame.K_a]
            moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
            if moving_left:
                dx = -160 * dt
            if moving_right:
                dx = 160 * dt
            if dx != 0:
                self._player._x = max(60, min(self._game.W - 60, self._player._x + dx))
                self._elena._x  = self._player._x + 70

            # Animasi walk + flip arah
            if moving_left and not moving_right:
                self._player.set_walking(True, False)
            elif moving_right and not moving_left:
                self._player.set_walking(True, True)
            else:
                self._player.set_walking(False)
        else:
            self._player.set_walking(False)

        # boss_intro → setelah semua dialog, boss interactable
        if self._phase == "boss_intro":
            pass  # Dihandle di _advance; setelah dialog habis → boss_intro_encounter

        if self._slash_active:
            self._slash_timer += dt
            if self._slash_timer > 0.6:
                self._slash_active = False

        if self._shake_timer > 0:
            self._shake_timer -= dt
            self._shake_x = random.randint(-6, 6) if self._shake_timer > 0 else 0
        else:
            self._shake_x = 0

        for p in self._particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['vy'] += 120 * dt
            p['life'] -= dt
        self._particles = [p for p in self._particles if p['life'] > 0]

        for ft in self._floats:
            ft.update(dt)
        self._floats = [f for f in self._floats if f.alive]

        if self._phase == "ending":
            self._ending_timer += dt
            if self._ending_timer > 2.2 and self._transition.done:
                if self._ending_route == "true":
                    from scenes.true_end_scene import TrueEndScene
                    self._game.replace_scene(TrueEndScene(self._game))
                else:
                    from scenes.bad_end_scene import BadEndScene
                    self._game.replace_scene(BadEndScene(self._game))

    def draw(self, surface: pygame.Surface) -> None:
        sx = self._shake_x

        # Background berdasarkan phase — SELALU tampilkan background, tidak pernah hitam
        if self._phase == "pre_battle":
            surface.blit(self._game.assets.bg_throne_room, (sx, 0))
        elif self._phase in ("dungeon", "dungeon_warning", "dungeon_encounter"):
            surface.blit(self._game.assets.bg_castle_ext, (sx, 0))
        elif self._phase == "ending":
            surface.blit(self._game.assets.bg_castle_int, (sx, 0))
        else:
            # boss_intro, boss_intro_encounter, phase1, attacking_boss, elena_hit, true_end, bad_end
            surface.blit(self._game.assets.bg_castle_int, (sx, 0))

        # Pre-battle: King di tengah, party di kiri
        if self._phase == "pre_battle":
            self._king_npc.draw(surface)
            self._player.draw(surface)
            self._elena.draw(surface)
            self._reno.draw(surface)
            self._lyra.draw(surface)
            self._darius.draw(surface)

        # Dungeon walk + encounter
        elif self._phase in ("dungeon", "dungeon_warning", "dungeon_encounter"):
            self._player.draw(surface)
            self._elena.draw(surface)
            self._reno.draw(surface)
            self._lyra.draw(surface)
            self._darius.draw(surface)
            # Gambar Dark Knight enemies
            for enemy in getattr(self, '_dungeon_enemies', []):
                enemy.draw(surface)
                if getattr(self, '_dungeon_enemies_interactable', False):
                    if abs(enemy.x - self._player._x) < 130:
                        try:
                            f = pygame.font.SysFont("Consolas", 13, bold=True)
                            t = f.render("[E] Bertarung!", True, DAMAGE_RED)
                            surface.blit(t, (int(enemy.x) - t.get_width() // 2, int(enemy.y) - 70))
                        except Exception:
                            pass
            # Hint encounter
            if self._phase == "dungeon_encounter" and getattr(self, '_dungeon_enemies_interactable', False):
                try:
                    f = pygame.font.SysFont("Consolas", 14)
                    h = f.render("← → Jalan  |  E Bertarung saat dekat Dark Knight!", True, UI_ACCENT)
                    surface.blit(h, (self._game.W // 2 - h.get_width() // 2, self._game.H - 30))
                except Exception:
                    pass

        # Boss fight phases — boss_intro (dialog) dan boss_intro_encounter (interaktif)
        elif self._phase not in ("ending",):
            self._boss.draw(surface)
            self._player.draw(surface)
            self._elena.draw(surface)
            self._reno.draw(surface)
            self._lyra.draw(surface)
            self._darius.draw(surface)

            # Hint interaksi boss saat boss_intro_encounter
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

            # Boss HP bar
            self._battle_ui.draw_enemy_bar(surface, self._boss)
            self._battle_ui.draw_player_hud(surface, self._player)

            # Slash efek besar
            if self._slash_active:
                alpha = int(255 * max(0, 1 - self._slash_timer / 0.6))
                s = pygame.Surface((self._game.W, self._game.H), pygame.SRCALPHA)
                pygame.draw.polygon(s, (255, 240, 100, alpha), [
                    (80,  self._game.H - 60),
                    (self._boss.x - 30, self._boss.y - 70),
                    (self._boss.x + 30, self._boss.y - 70),
                    (130, self._game.H - 60),
                ])
                # True End OVERDRIVE — cahaya penuh layar
                if self._phase == "true_end" and self._dlg_step >= 7:
                    full_glow = pygame.Surface((self._game.W, self._game.H), pygame.SRCALPHA)
                    glow_a = min(alpha, 180)
                    full_glow.fill((255, 240, 120, glow_a))
                    surface.blit(full_glow, (0, 0))
                surface.blit(s, (0, 0))

            # Elena KO indicator
            if self._phase in ("elena_hit", "true_end", "bad_end") and hasattr(self._elena, 'knocked_out') and self._elena.knocked_out:
                try:
                    f = pygame.font.SysFont("Georgia", 16)
                    t = f.render("Elena — KO!", True, HP_BAR_LOW)
                    surface.blit(t, (self._elena.x - t.get_width() // 2, self._elena.y - 70))
                except Exception:
                    pass

            # Phase 2 indicator
            if self._boss_phase == 2:
                try:
                    f = pygame.font.SysFont("Georgia", 14, bold=True)
                    t = f.render("⚠ PHASE 2 — ENRAGE", True, DAMAGE_RED)
                    surface.blit(t, (self._game.W // 2 - t.get_width() // 2, 55))
                except Exception:
                    pass

        # Partikel
        for p in self._particles:
            alpha = int(255 * p['life'] / p['max_life'])
            sz = max(1, p['size'])
            s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p['col'], alpha), (sz, sz), sz)
            surface.blit(s, (int(p['x']) - sz, int(p['y']) - sz))

        for ft in self._floats:
            ft.draw(surface)

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
            "pre_battle":    "Aula Kerajaan Astravia — Malam Sebelum Perang",
            "dungeon":             "Lorong Kastil Raja Iblis",
            "dungeon_warning":     "Lorong Kastil Raja Iblis",
            "dungeon_encounter":   "Lorong Kastil — Monster Menghalangi!",
            "boss_intro":          "Singgasana Kegelapan — Final Boss",
            "boss_intro_encounter":"Singgasana Kegelapan — ⚔ Dekati Demon King!",
            "phase1":        "Final Battle — Phase 1",
            "attacking_boss":"Final Battle",
            "elena_hit":     "Final Battle — CRISIS!",
            "true_end":      "TRUE END ROUTE",
            "bad_end":       "BAD END ROUTE",
        }
        lbl = lbl_map.get(self._phase, "")
        if lbl and self._phase != "ending":
            try:
                t = self._font_ui.render(lbl, True, UI_ACCENT)
                surface.blit(t, (self._game.W // 2 - t.get_width() // 2, 8))
            except Exception:
                pass
