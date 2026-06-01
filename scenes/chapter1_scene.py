"""
scenes/chapter1_scene.py
========================
Chapter 1 — The Summoning: Aula Kerajaan, Pedang Suci, Status Window, Elena.
[INHERITANCE] Mewarisi Scene (ABC).
"""

import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, StatusWindow, NarratorBox, FloatingText, PartyHUD
from entities.characters import Player, PartyNPC, BossNPC, TownNPC


class Chapter1Scene(Scene):
    """Aula Kerajaan Astravia — The Summoning."""

    DIALOGUES = [
    ("Knight A",    "Dia muncul! Akhirnya Ritualnya berhasil!"),
    ("Mage",        "Cahaya dari lingkaran sihir itu... luar biasa sekali. Ramalan benar-benar menjadi nyata."),
    ("Arga",        "...Hah? Apa... apa ini?"),
    ("Arga",        "Barusan aku di perasaan lagi di jalan mau pulang, tapi kok sekarang—"),
    ("Arga",        "Ini mimpi, kan? Ini pasti mimpi."),
    ("King Aldric", "Selamat datang, anak muda. Ah tidak.."),
    ("King Aldric", "Wahai Pahlawan, Maafkan kami karena memanggil tanpa izin."),
    ("Arga",        "Memanggil? Maksudnya apaan... kalian yang bikin aku ada di sini?!"),
    ("King Aldric", "Benar. Dan aku mohon kau dengarkan dulu sebelum menghakimi kami."),
    ("King Aldric", "Namaku Aldric. Raja Kerajaan Astravia. Dan dunia ini sedang benar-benar diambang kehancuran."),
    ("Arga",        "...Dunia ini?"),
    ("King Aldric", "Raja Iblis — makhluk yang lahir dari kebencian yang ada di dunia ini — mulai bergerak."),
    ("King Aldric", "Satu per satu kerajaan jatuh. Desa-desa dibakar. Ribuan nyawa hilang."),
    ("King Aldric", "Ramalan kuno berkata: hanya pahlawan dari dunia lain yang bisa menghentikannya."),
    ("Arga",        "Tunggu— pahlawan? Maksudnya aku?"),
    ("Arga",        "Aku itu cuma pelajar biasa. Aku bahkan gak bisa masak nasi dengan benar."),
    ("King Aldric", "Kami tahu ini terdengar mustahil. Tapi lihat... pedang itu merespons kehadiranmu."),
    ("SYSTEM",      "✨ Pedang Suci melayang perlahan dari altar — menuju ke arah Arga..."),
    ("Knight A",    "Lihat itu! Itu Pedang Suci...! Ia benar-benar merespon sang pahlawan!"),
    ("Knight B",    "Dalam catatan sejarah, ini belum pernah terjadi selama 500 tahun!"),
    ("Mage",        "Mana yang terpancar dari tubuhnya... ini bukan mana manusia biasa."),
    ("Arga",        "Apa ini... kenapa pedang ini mendekat sendiri ke tanganku?"),
]

    # Index dialog saat pedang mulai "merespons" (indeks 16 = SYSTEM dialog)
    SWORD_APPEAR_STEP = 16

    SWORD_CHOICE = ["Ambil Pedang (YES)", "Tolak (NO)"]

    AFTER_SWORD = [
    ("SYSTEM",      "⚡ Cahaya emas memenuhi ruangan — dinding batu bergetar!"),
    ("Arga",        "Apa— apa yang terjadi pada tanganku?!"),
    ("Arga",        "Rasanya seperti... seperti ada sesuatu yang masuk ke dalam diriku."),
    ("Mage",        "Pedang Suci telah memilih tuannya. Kekuatan ramalan tersegel dalam dirinya."),
    ("Knight B",    "Ini... luar biasa. Aku hidup untuk menyaksikan momen ini."),
    ("King Aldric", "Kau tidak harus menerimanya sepenuhnya sekarang."),
    ("King Aldric", "Tapi nasib dunia ini sudah ada di genggaman tanganmu, anak muda."),
    ("Arga",        "...Aku tidak punya pilihan lain, kan."),
    ("King Aldric", "Selalu ada pilihan. Tapi kadang satu pilihan membawa bobot yang berbeda."),
]

    ELENA_DIALOGUES = [
    ("Elena",       "Ayah... jadi... dia orangnya?"),
    ("King Aldric", "Benar. Dia yang dipilih pedang itu."),
    ("Elena",       "..."),
    ("Elena",       "Maaf, aku tidak bermaksud menatap terlalu lama. Ini hanya... di luar dugaan."),
    ("Arga",        "Aku juga di luar dugaan soal semuanya."),
    ("Elena",       "Namaku Elena. Putri kerajaan Astravia."),
    ("Arga",        "Arga. Dari... yah, tampaknya dari dunia yang berbeda."),
    ("Elena",       "Arga... boleh aku bertanya sesuatu?"),
    ("Arga",        "Silakan."),
    ("Elena",       "Apakah kau benar-benar bersedia mengemban ini semua? Karena aku tidak ingin kau merasa dipaksa."),
    ("Arga",        "Jujur saja... aku masih belum tahu. Ini terlalu tiba-tiba."),
    ("Elena",       "Kalau begitu, setidaknya jangan lakukan sendiri."),
    ("Elena",       "Bolehkah aku ikut bersamamu? Aku mungkin tidak sekuat pedangmu, tapi aku tahu dunia ini lebih baik darimu."),
    ("Arga",        "Kau... minta izin padaku?"),
    ("Elena",       "Bukankah itu hal yang wajar? Kita belum saling kenal."),
    ("Arga",        "...Baiklah. Aku tidak keberatan punya pemandu yang tahu jalan."),
    ("Elena",       "Hm. Jawaban yang cukup jujur. Aku suka itu."),
    ("SYSTEM",      "✨ Elena memutuskan untuk menemani perjalanan Arga."),
]

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
        self._phase = "arrival"
        self._dialogue = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._status_win = StatusWindow(game.W, game.H)
        self._narrator = NarratorBox(game.W, game.H)
        self._floats: list[FloatingText] = []
        self._party_hud = PartyHUD()

        # Arga jatuh dari atas (summoned)
        self._player = Player(game.W//2, -80)
        self._player.emotion = "surprised"
        self._player.before_isekai = True   # sebelum Holy Sword = asset lama

        # Elena dan King mulai dari luar layar untuk walk-in
        # King masuk dari kanan, Elena masuk dari kiri nanti saat fase elena
        self._elena = PartyNPC("Elena", game.W + 80, int(game.H*0.6)-55)
        self._king = TownNPC("King Aldric", game.W + 150, int(game.H*0.45)-55, (180,150,80))
        self._king.emotion = "normal"

        self._dlg_step = 0
        self._phase_timer = 0.0

        # Sword: hanya tampil saat step dialog >= SWORD_APPEAR_STEP
        self._sword_visible = False
        self._sword_y = 200.0
        self._sword_glow = 0.0

        self._show_status = False
        self._particles: list[dict] = []
        self._choice_made = False

        # Walk-in King dari kanan setelah Arga mendarat
        self._king_walkin_done = False
        self._king_target_x = float(game.W // 2)

        # Walk-in Elena: hanya saat fase elena
        self._elena_walkin_done = False
        self._elena_target_x = float(game.W * 0.7)
        self._elena_walkin_active = False

        try:
            self._font_chapter = pygame.font.SysFont("Georgia", 36, bold=True)
            self._font_system  = pygame.font.SysFont("Consolas", 16)
        except Exception:
            self._font_chapter = pygame.font.Font(None, 40)
            self._font_system  = pygame.font.Font(None, 18)

    def on_enter(self) -> None:
        self._transition.fade_in(color=(255, 255, 255), speed=220)
        self._narrator.show(["Chapter 1 — The Summoning", "Aula Kerajaan Astravia"], 3.0)
        # Arga jatuh dari atas (disummon) — animasi jatuh vertikal
        self._arga_fall_y = -80.0
        self._arga_falling = True
        # Belum tampilkan dialog — tunggu Arga mendarat dulu
        self._landing_dialogue_queued = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            key = event.key
            # Blokir input saat animasi landing atau king walk-in
            if getattr(self, '_arga_falling', False):
                return
            if not self._king_walkin_done:
                return
            if key in (pygame.K_UP, pygame.K_w):
                if self._dialogue.showing_choices:
                    self._dialogue.navigate_choice(-1)
            elif key in (pygame.K_DOWN, pygame.K_s):
                if self._dialogue.showing_choices:
                    self._dialogue.navigate_choice(1)
            elif key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                self._advance()
            elif key == pygame.K_TAB:
                if self._phase in ("sword_taken", "status_show", "elena", "goto_town"):
                    self._show_status = not self._show_status
                    self._status_win.visible = self._show_status

    def _advance(self):
        self._game.assets.play("cursor")
        if self._phase == "arrival":
            if self._dialogue.showing_choices:
                choice = self._dialogue.confirm_choice()
                if choice == 0:
                    # Ambil pedang — ganti ke asset setelah isekai!
                    self._phase = "sword_taken"
                    self._sword_visible = False  # pedang "diambil" — hilang dari layar
                    self._player.before_isekai = False  # ← SWITCH KE ASSET AFTER ISEKAI
                    self._player.play_attack()           # animasi attack sekali
                    self._dialogue.hide()
                    self._game.assets.play("flash")
                    self._spawn_particles(self._game.W//2, 200)
                    self._game.assets.play("fanfare")
                    pygame.time.delay(100)
                    self._dialogue.show(self.AFTER_SWORD[0][1], self.AFTER_SWORD[0][0])
                    self._dlg_step = 0
                else:
                    # Tolak → sistem paksa
                    self._dialogue.show(
                        "Kau tidak bisa menolak takdir.",
                        "SYSTEM"
                    )
                    self._choice_made = True
                return

            if not self._dialogue.is_finished:
                self._dialogue.skip()
                return

            self._dlg_step += 1
            if self._dlg_step < len(self.DIALOGUES):
                spk, txt = self.DIALOGUES[self._dlg_step]
                # Aktifkan pedang saat step >= SWORD_APPEAR_STEP
                if self._dlg_step >= self.SWORD_APPEAR_STEP:
                    self._sword_visible = True
                if self._dlg_step == len(self.DIALOGUES)-1:
                    # Offer sword choice
                    self._dialogue.show(
                        "✨ Pedang Suci melayang ke hadapanmu.\nAmbil Pedang Suci?",
                        "SYSTEM",
                        choices=self.SWORD_CHOICE
                    )
                else:
                    self._dialogue.show(txt, spk)
            else:
                self._sword_visible = True
                self._dialogue.show(
                    "✨ Pedang Suci melayang ke hadapanmu.\nAmbil Pedang Suci?",
                    "SYSTEM",
                    choices=self.SWORD_CHOICE
                )

        elif self._phase == "sword_taken":
            if not self._dialogue.is_finished:
                self._dialogue.skip()
                return
            self._dlg_step += 1
            if self._dlg_step < len(self.AFTER_SWORD):
                spk, txt = self.AFTER_SWORD[self._dlg_step]
                self._dialogue.show(txt, spk)
                self._game.assets.play("fanfare")
            else:
                # Semua dialog AFTER_SWORD selesai → tampilkan status window
                self._phase = "status_show"
                self._show_status = True
                self._status_win.visible = True
                self._dialogue.show(
                    "Kekuatan pedang suci telah tersegel dalam dirimu.",
                    "SYSTEM"
                )

        elif self._phase == "status_show":
            if not self._dialogue.is_finished:
                self._dialogue.skip()
                return
            self._show_status = False
            self._phase = "elena"
            self._dlg_step = 0
            # Mulai walk-in Elena dari kiri
            self._elena._x = -80.0
            self._elena_walkin_active = True
            self._elena_walkin_done = False
            # Tunda dialog sampai Elena tiba
            self._elena_arrived_dialogue_queued = True

        elif self._phase == "elena":
            # Blokir advance selama Elena masih berjalan masuk
            if self._elena_walkin_active:
                return
            if not self._dialogue.is_finished:
                self._dialogue.skip()
                return
            self._dlg_step += 1
            if self._dlg_step < len(self.ELENA_DIALOGUES):
                spk, txt = self.ELENA_DIALOGUES[self._dlg_step]
                self._dialogue.show(txt, spk)
                if "Elena" in spk:
                    self._elena.emotion = "happy" if self._dlg_step > 2 else "normal"
            else:
                # Lanjut ke town scene
                self._game.party.append("Elena")
                self._phase = "goto_town"
                self._transition.fade_out(speed=200)
                self._narrator.show(["Objective: Jelajahi Kota Astravia"], 2.0)

    def _spawn_particles(self, cx, cy):
        for _ in range(30):
            angle = random.uniform(0, math.pi*2)
            speed = random.uniform(80, 200)
            self._particles.append({
                'x': float(cx), 'y': float(cy),
                'vx': math.cos(angle)*speed, 'vy': math.sin(angle)*speed,
                'life': random.uniform(0.5, 1.5),
                'max_life': 1.5,
                'col': random.choice([GOLD_LIGHT, HOLY_WHITE, (255,230,150)]),
                'size': random.randint(3, 7),
            })

    def update(self, dt: float) -> None:
        self._t += dt
        self._phase_timer += dt

        # ── Animasi Arga jatuh dari atas (summoned) ──────────────
        if getattr(self, '_arga_falling', False):
            target_y = int(self._game.H * 0.6) - 55
            self._arga_fall_y = min(target_y, self._arga_fall_y + 420 * dt)
            self._player._y = self._arga_fall_y
            if self._arga_fall_y >= target_y:
                self._arga_falling = False
                self._player._y = target_y
                # Setelah Arga mendarat, mulai walk-in King dari kanan
                self._king._x = float(self._game.W + 150)
                self._king_walkin_done = False

        # ── Walk-in King dari kanan ───────────────────────────────
        if not self._king_walkin_done and not getattr(self, '_arga_falling', True):
            tx = self._king_target_x
            if self._king._x > tx + 2:
                self._king._x = max(tx, self._king._x - 260 * dt)
                self._king._facing_right = False   # King jalan ke kiri
                # Aktifkan animasi walk King (jalan ke kiri = direction_right=False)
                if hasattr(self._king, 'set_walking'):
                    self._king.set_walking(True, False)
            else:
                self._king._x = tx
                self._king_walkin_done = True
                self._king._facing_right = True    # King sudah tiba, hadap kanan (ke Arga)
                # Hentikan animasi walk King
                if hasattr(self._king, 'set_walking'):
                    self._king.set_walking(False)
                # King tiba → mulai dialog
                if not getattr(self, '_landing_dialogue_queued', False):
                    self._landing_dialogue_queued = True
                    self._dialogue.show(self.DIALOGUES[0][1], self.DIALOGUES[0][0])

        # ── Walk-in Elena dari kiri (fase elena) ─────────────────
        if self._elena_walkin_active:
            tx = self._elena_target_x
            if self._elena._x < tx - 2:
                self._elena._x = min(tx, self._elena._x + 260 * dt)
                self._elena._facing_right = True   # Elena jalan ke kanan
                # Aktifkan animasi walk Elena
                if hasattr(self._elena, 'set_walking'):
                    self._elena.set_walking(True, True)
            else:
                self._elena._x = tx
                self._elena_walkin_active = False
                self._elena_walkin_done = True
                self._elena._facing_right = False  # Elena sudah tiba, hadap kiri (ke Arga)
                # Hentikan animasi walk Elena
                if hasattr(self._elena, 'set_walking'):
                    self._elena.set_walking(False)
                # Elena tiba → mulai dialog elena
                if getattr(self, '_elena_arrived_dialogue_queued', False):
                    self._elena_arrived_dialogue_queued = False
                    spk, txt = self.ELENA_DIALOGUES[0]
                    self._dialogue.show(txt, spk)
                    self._elena.emotion = "thinking"

        self._transition.update(dt)
        self._dialogue.update(dt)
        self._narrator.update(dt)
        self._status_win.update(dt)

        # Update walking state player (dia tidak bergerak di scene ini, tapi animasi idle jalan)
        self._player.set_walking(False)
        self._player.update(dt)
        self._elena.update(dt)
        self._king.update(dt)

        # Pedang mengambang (animasi berjalan terus, visibilitas dikontrol _sword_visible)
        self._sword_y = 180 + math.sin(self._t * 2) * 15
        self._sword_glow = abs(math.sin(self._t * 3))

        # Partikel
        for p in self._particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['vy'] += 150*dt
            p['life'] -= dt
        self._particles = [p for p in self._particles if p['life'] > 0]

        # Float texts
        for ft in self._floats:
            ft.update(dt)
        self._floats = [ft for ft in self._floats if ft.alive]

        # ── Transisi ke town setelah fade out selesai ─────────────
        if self._phase == "goto_town" and self._transition.done:
            from scenes.town_scene import Chapter2Scene
            self._game.replace_scene(Chapter2Scene(self._game))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._game.assets.bg_throne_room, (0,0))

        self._king.draw(surface)
        self._player.draw(surface)
        if self._phase in ("elena","goto_town","status_show"):
            self._elena.draw(surface)

        # Pedang suci — HANYA muncul saat _sword_visible = True
        if self._sword_visible:
            self._draw_sword(surface)

        # Partikel
        for p in self._particles:
            alpha = int(255 * p['life'] / p['max_life'])
            s = pygame.Surface((p['size']*2,p['size']*2),pygame.SRCALPHA)
            pygame.draw.circle(s, (*p['col'],alpha),(p['size'],p['size']),p['size'])
            surface.blit(s,(int(p['x'])-p['size'],int(p['y'])-p['size']))

        self._narrator.draw(surface)
        self._dialogue.draw(surface)
        members = [("Arga", self._player.hp, self._player.max_hp)]
        if self._game.flags.get("elena_joined"):
            members.append(("Elena", self._elena.hp, self._elena.max_hp))
        self._party_hud.draw(surface, members)
        self._transition.draw(surface)

        for ft in self._floats:
            ft.draw(surface)

        # Chapter label
        try:
            ch_txt = self._font_chapter.render("Chapter 1 — The Summoning", True, UI_ACCENT)
            ch_txt.set_alpha(100)
            surface.blit(ch_txt,(self._game.W//2-ch_txt.get_width()//2, 15))
        except Exception:
            pass

        # Status window
        if self._show_status:
            self._status_win.draw(surface, self._player)

    def _draw_sword(self, surface):
        """Gambar Pedang Suci menggunakan asset dari assets/holy_sword/."""
        sx = self._game.W // 2
        sy = int(self._sword_y)
        assets = self._game.assets

        # ── Glow dari holy_sword_glow.png ─────────────────────────
        glow_r = int(40 + self._sword_glow * 20)
        try:
            glow_sprite = assets.holy_sword_glow
            if glow_sprite:
                alpha = int(80 + self._sword_glow * 120)
                glow_copy = glow_sprite.copy()
                glow_copy.set_alpha(alpha)
                gw, gh = glow_copy.get_size()
                surface.blit(glow_copy, (sx - gw // 2, sy - gh // 2))
            else:
                raise AttributeError
        except Exception:
            # Fallback glow
            gs = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(gs, (255, 230, 100, int(60 * self._sword_glow)),
                               (glow_r, glow_r), glow_r)
            surface.blit(gs, (sx - glow_r, sy - glow_r))

        # ── Sprite pedang dari holy_sword.png ─────────────────────
        try:
            sword_sprite = assets.holy_sword
            if sword_sprite:
                sw, sh = sword_sprite.get_size()
                surface.blit(sword_sprite, (sx - sw // 2, sy - sh + 20))
                return
        except Exception:
            pass

        # Fallback: gambar pedang primitif
        pygame.draw.polygon(surface, (220, 220, 240),
                            [(sx, sy-60), (sx-6, sy+40), (sx+6, sy+40)])
        pygame.draw.rect(surface, (200, 170, 50), (sx-20, sy+35, 40, 10))
        pygame.draw.rect(surface, (140, 110, 40), (sx-6, sy+44, 12, 22))
        s2 = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(s2, (255, 250, 150, 180), (10, 10), 10)
        surface.blit(s2, (sx - 10, sy - 70))
