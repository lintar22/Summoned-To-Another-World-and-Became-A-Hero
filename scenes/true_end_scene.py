"""
scenes/true_end_scene.py
========================
TRUE ENDING — Dipanggil setelah boss dikalahkan di final chapter.
Alur:
  rest        → Arga & Elena kelelahan, istirahat di tempat bos mati
  proposal    → Arga melamar Elena (idle hadap-hadapan)
  return_trip → Perjalanan pulang ke kerajaan (walkin)
  royal_hall  → Arga minta hadiah ke Raja, Raja setujui pernikahan
  town_wedding→ Perayaan di kota, Arga & Elena dalam pakaian pengantin
  final       → Layar penutup

[ASSET PENGANTIN]
  Tambahkan folder idle frames ke assets/characters/heroes/:
    arga/wedding/idle1.png ... idle4.png   → arga_wedding_idle_frames
    elena/wedding/idle1.png ... idle4.png  → elena_wedding_idle_frames
  Animasi loop otomatis dengan kecepatan 0.15 detik/frame (sama seperti NPC lain).
  Jika folder tidak ada, scene menggunakan fallback primitif warna-warni.
"""

import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox


# ─── Dialog per fase ───────────────────────────────────────────────────────────

REST_DLGS = [
    ("SYSTEM",  "⚔ Raja Iblis telah dikalahkan."),
    ("Reno",    "Ha... ha... kita... menang..."),
    ("Lyra",    "...ahh...cape bangett. Tapi....syulurlahh."),
    ("Darius",  "Bagus. Semua selamat. Itu yang paling penting."),
    ("Elena",   "Arga... kamu gapapa?"),
    ("Arga",    "Iya. Aku cuma cape aja."),
    ("Elena",   "Syukurlah..."),
    ("Reno",    "Kalian berdua tuh, seriusan deh. UDAH UDAH DUDUK, KITA ISTIRAJAT DULU!"),
    ("Lyra",    "hahaha...Biarkan mereka. Mereka yang paling banyak menanggung bebannya."),
]

PROPOSAL_DLGS = [
    ("SYSTEM", "Di tengah perayaan kemenangan, lima orang berdiri bersama seperti biasanya."),
    ("Arga", "Elena."),
    ("Elena", "Hm?"),
    ("Elena", "...Kenapa ekspresimu serius begitu?"),
    ("Arga", "...Karena ini serius."),
    ("Reno", "Oh tidak."),
    ("Lyra", "...Aku punya firasat buruk."),
    ("Darius", "Aku juga."),
    ("Elena", "Kalian bertiga kenapa malah ikut tegang?"),
    ("Arga", "...Aku tidak tahu harus mulai dari mana."),
    ("Reno", "Dari awal mungkin?"),
    ("Lyra", "Diam sebentar, Reno."),
    ("Arga", "*menghela napas*"),
    ("Arga", "Aku datang dari dunia lain."),
    ("Arga", "Aku dipanggil ke dunia ini sebagai pahlawan."),
    ("Arga", "Awalnya aku pikir semua ini cuma tentang mengalahkan Raja Iblis lalu pulang."),
    ("Arga", "Tapi semakin lama... aku sadar ada alasan lain kenapa aku tetap berjalan sampai sejauh ini."),
    ("Elena", "..."),
    ("Arga", "Aku bukan ksatria hebat."),
    ("Arga", "Bukan bangsawan."),
    ("Arga", "Bahkan aku sering tidak tahu apa yang harus kulakukan."),
    ("Reno", "Nah itu baru Arga yang kukenal."),
    ("Lyra", "Benar."),
    ("Arga", "Hei."),
    ("Elena", "*menahan tawa kecil*"),
    ("Arga", "Tapi ada satu hal yang selalu aku yakini."),
    ("Arga", "Setiap kali aku hampir menyerah..."),
    ("Arga", "Setiap kali aku takut..."),
    ("Arga", "Kau selalu ada di sisiku."),
    ("Elena", "...Arga."),
    ("Arga", "Dan tanpa kusadari, kau sudah menjadi alasan terbesar kenapa aku ingin terus maju."),
    ("SYSTEM", "Wajah Elena mulai memerah."),
    ("Reno", "Oh ini bagus."),
    ("Lyra", "Diam."),
    ("Reno", "Aku diam."),
    ("Arga", "Elena."),
    ("Arga", "Aku mencintaimu."),
    ("SYSTEM", "Elena langsung membeku di tempat."),
    ("Elena", "A-Arga...?"),
    ("Arga", "Aku mencintaimu."),
    ("Arga", "Lebih dari apa pun."),
    ("SYSTEM", "Wajah Elena kini menjadi semerah apel."),
    ("Elena", "J-Jangan mengatakannya dua kali!"),
    ("Reno", "Wah, merah banget."),
    ("Lyra", "Aku tidak tahu manusia bisa semerah itu."),
    ("Elena", "K-Kalian berdua diam!"),
    ("Darius", "Hahaha."),
    ("Arga", "Dan karena itu..."),
    ("SYSTEM", "Suasana di sekitar mereka mendadak sunyi."),
    ("Arga", "Maukah kamu menjadi istriku?"),
    ("SYSTEM", "Mata Elena membelalak."),
    ("Elena", "..."),
    ("Elena", "...Eh?"),
    ("Elena", "...EH?!"),
    ("Reno", "AHAHAHA dia langsung korslet tuh."),
    ("Lyra", "Kurasa otaknya berhenti bekerja."),
    ("Elena", "A-Aku tidak!"),
    ("Elena", "Aku cuma...!"),
    ("Elena", "Ini...!"),
    ("Elena", "K-Kenapa sekarang?!"),
    ("Arga", "Karena aku tidak ingin menunggu lebih lama lagi."),
    ("Reno", "Dia benar-benar mau pingsan."),
    ("Lyra", "Kalau pingsan sekarang aku tidak akan kaget."),
    ("Elena", "B-Bisakah kalian berhenti berkomentar?!"),
    ("Darius", "Kurasa tidak."),
    ("Elena", "Darius?! Bahkan kamu juga?!"),
    ("Darius", "Kesempatan seperti ini jarang terjadi."),
    ("Elena", "Kalian semua jahat..."),
    ("SYSTEM", "Elena menarik napas panjang beberapa kali."),
    ("SYSTEM", "Matanya sedikit berkaca-kaca."),
    ("Elena", "...Bodoh."),
    ("Arga", "Hm?"),
    ("Elena", "Kenapa baru sekarang menanyakannya?"),
    ("Elena", "Aku sudah menunggu sejak lama, tahu."),
    ("Arga", "..."),
    ("Reno", "TUNGGU."),
    ("Reno", "SEJAK LAMA?!"),
    ("Lyra", "Jadi selama ini cuma mereka berdua yang tidak sadar?"),
    ("Darius", "Ternyata memang begitu."),
    ("Elena", "A-Ah..."),
    ("Elena", "Lupakan yang barusan!"),
    ("Arga", "*tertawa kecil*"),
    ("Arga", "Jadi...?"),
    ("SYSTEM", "Elena menatap Arga beberapa saat."),
    ("SYSTEM", "Lalu tersenyum dengan wajah yang masih merah."),
    ("Elena", "Iya."),
    ("Arga", "..."),
    ("Elena", "Tentu saja iya."),
    ("Elena", "Seribu kali iya kalau perlu."),
    ("Reno", "YEAHHHHHHH!!!"),
    ("Reno", "AKHIRNYA!!"),
    ("Reno", "AKU MENUNGGU MOMEM INI SEJAK BERABAD-ABAD!"),
    ("Lyra", "Padahal baru kenal beberapa bulan."),
    ("Reno", "DETAIL CUMA DETAIL KECILLLL! KECIL!"),
    ("Lyra", "*tersenyum tipis*"),
    ("Lyra", "Selamat, Elena."),
    ("Lyra", "Kau pantas mendapatkan kebahagiaan setelah semua yang terjadi."),
    ("Darius", "Dan kau juga, Arga."),
    ("Darius", "Aku tidak pernah pandai soal kata-kata."),
    ("Darius", "Tapi kurasa tidak ada orang yang lebih pantas berdiri di samping Elena selain dirimu."),
    ("Reno", "Jadi kapan pestanya?"),
    ("Elena", "Reno."),
    ("Reno", "Ya?"),
    ("Elena", "Diam."),
    ("Reno", "Baik."),
    ("SYSTEM", "Tawa mereka bergema di bawah langit yang akhirnya damai."),
    ("SYSTEM", "Untuk pertama kalinya, tidak ada perang yang menunggu di esok hari."),
    ("SYSTEM", "Hanya masa depan yang bisa mereka jalani bersama."),
]

RETURN_DLGS = [
    ("Reno",    "Hei, kita harus kasih tahu Raja sebelum kalian bikin rencana apapun!"),
    ("Arga",    "Benar juga. Kita pulang dulu."),
    ("Elena",   "Arga... terima kasih. Untuk segalanya."),
    ("Arga",    "Itu seharusnya aku yang bilang ke kamu."),
]

ROYAL_HALL_DLGS = [
    ("SYSTEM", "Gerbang kerajaan terbuka lebar saat para pahlawan kembali."),
    ("SYSTEM", "Kabar kemenangan mereka telah menyebar lebih cepat daripada angin."),
    ("SYSTEM", "Untuk pertama kalinya setelah bertahun-tahun, tidak ada lagi bayang-bayang perang."),
    ("King Aldric", "Para pahlawan..."),
    ("King Aldric", "Kalian benar-benar kembali."),
    ("Arga", "Kami kembali, Yang Mulia."),
    ("King Aldric", "...Dan Raja Iblis?"),
    ("SYSTEM", "Arga saling berpandangan dengan anggota party lainnya."),
    ("Arga", "Sudah berakhir."),
    ("Arga", "Raja Iblis telah dikalahkan."),
    ("SYSTEM", "Aula kerajaan menjadi sunyi selama beberapa detik."),
    ("SYSTEM", "Seolah semua orang berusaha memastikan bahwa mereka tidak salah dengar."),
    ("King Aldric", "...Puji syukur."),
    ("SYSTEM", "Raja menutup matanya sesaat."),
    ("SYSTEM", "Beban yang selama bertahun-tahun berada di pundaknya akhirnya terangkat."),
    ("King Aldric", "Kalian telah melakukan sesuatu yang bahkan para legenda hanya berani ceritakan."),
    ("King Aldric", "Kalian menyelamatkan kerajaan ini."),
    ("King Aldric", "Tidak."),
    ("King Aldric", "Kalian menyelamatkan dunia ini."),
    ("Reno", "*berbisik*"),
    ("Reno", "Wah, kedengarannya keren kalau diucapkan begitu."),
    ("Lyra", "Karena memang keren, bodoh."),
    ("King Aldric", "*tertawa kecil*"),
    ("King Aldric", "Sebagai Raja Astravia, aku berutang lebih banyak daripada yang mungkin bisa kubayar."),
    ("King Aldric", "Emas, tanah, gelar bangsawan."),
    ("King Aldric", "Apa pun yang kalian inginkan, katakanlah."),
    ("King Aldric", "Terutama dirimu, Arga."),
    ("King Aldric", "Kaulah yang memimpin perjalanan ini sampai akhir."),
    ("Arga", "..."),
    ("Elena", "*melirik Arga*"),
    ("Reno", "..."),
    ("Lyra", "..."),
    ("Darius", "..."),
    ("Reno", "Tunggu."),
    ("Reno", "Kenapa aku merasa dia sudah menyiapkan sesuatu?"),
    ("Lyra", "Karena wajahnya mencurigakan."),
    ("Arga", "*menghela napas pelan*"),
    ("Arga", "Sebenarnya... ada satu hal yang ingin saya minta."),
    ("King Aldric", "Katakan saja."),
    ("Arga", "Apa pun jawaban Anda nanti, saya tetap berterima kasih atas semua yang telah kerajaan berikan kepada saya."),
    ("King Aldric", "...Aku mendengarkan."),
    ("Arga", "Yang Mulia."),
    ("Arga", "Saya tidak menginginkan emas."),
    ("Arga", "Saya tidak menginginkan tanah ataupun gelar."),
    ("Arga", "Saya hanya menginginkan satu hal."),
    ("SYSTEM", "Arga menoleh ke arah Elena."),
    ("SYSTEM", "Wajah Elena langsung memerah saat menyadari ke mana arah pembicaraan ini."),
    ("Elena", "A-Arga...?"),
    ("Arga", "Izinkan saya menikahi Putri-mu Elena, Yang Mulia."),
    ("SYSTEM", "Keheningan langsung menyelimuti aula."),
    ("Reno", "..."),
    ("Lyra", "..."),
    ("Darius", "..."),
    ("Reno", "AKHIRNYA DIA BILANG JUGA."),
    ("Lyra", "Keras sekali."),
    ("Elena", "R-Reno!"),
    ("SYSTEM", "Wajah Elena semakin merah."),
    ("King Aldric", "..."),
    ("Elena", "A-Ayah..."),
    ("King Aldric", "Jadi itu yang kau inginkan."),
    ("Arga", "...Ya, Yang Mulia."),
    ("King Aldric", "Dan kau sungguh yakin?"),
    ("Arga", "Lebih yakin daripada apa pun."),
    ("SYSTEM", "Raja terdiam sejenak."),
    ("SYSTEM", "Lalu perlahan menoleh ke arah putrinya."),
    ("King Aldric", "Dan bagaimana denganmu, Elena?"),
    ("Elena", "E-Eh?!"),
    ("Elena", "K-Kenapa malah bertanya padaku?!"),
    ("King Aldric", "Karena ini menyangkut hidupmu."),
    ("Elena", "Aku..."),
    ("SYSTEM", "Elena menunduk."),
    ("SYSTEM", "Wajahnya sudah semerah tomat."),
    ("Reno", "Dia bakal meledak."),
    ("Lyra", "Diam."),
    ("Elena", "Aku..."),
    ("Elena", "...Tidak keberatan."),
    ("Reno", "TIDAK KEBERATAN KATANYA."),
    ("Elena", "RENO!"),
    ("SYSTEM", "Tawa kecil terdengar dari berbagai sudut aula."),
    ("King Aldric", "Hahaha..."),
    ("King Aldric", "Aku rasa aku sudah mendapatkan jawabannya."),
    ("King Aldric", "Arga."),
    ("King Aldric", "Sejak pertama kali bertemu, aku melihat bagaimana kau selalu menempatkan keselamatan Elena di atas dirimu sendiri."),
    ("King Aldric", "Aku melihat bagaimana kau melindunginya dalam setiap laporan yang kudengar."),
    ("King Aldric", "Dan yang lebih penting..."),
    ("King Aldric", "Aku melihat bagaimana putriku memandangmu."),
    ("SYSTEM", "Elena langsung menutup wajahnya."),
    ("Elena", "Ayah... tolong hentikan..."),
    ("King Aldric", "Apa salahku? Aku hanya mengatakan yang sebenarnya."),
    ("Reno", "Wah, ternyata Raja juga suka menggoda."),
    ("Lyra", "Turun-temurun rupanya."),
    ("Elena", "Kalian semua bersekongkol, ya?!"),
    ("King Aldric", "*tersenyum hangat*"),
    ("King Aldric", "Tidak ada ayah yang ingin menghalangi kebahagiaan anaknya."),
    ("King Aldric", "Terlebih lagi jika orang yang dipilihnya adalah pahlawan yang menyelamatkan dunia."),
    ("King Aldric", "Dengan ini..."),
    ("King Aldric", "Aku merestui pernikahan kalian."),
    ("King Aldric", "Selamat, Arga."),
    ("King Aldric", "Dan selamat untukmu juga, Elena."),
    ("SYSTEM", "Seluruh aula langsung dipenuhi tepuk tangan dan sorakan."),
    ("Reno", "YEAHHHHHH!!!"),
    ("Reno", "RAJA PALING BIJAK YANG PERNAH HIDUP!!"),
    ("Lyra", "Baru lima detik lalu kau memanggilnya tua."),
    ("Reno", "Itu masa lalu."),
    ("Darius", "*tersenyum tipis*"),
    ("Darius", "Keputusan yang tepat, Paduka."),
    ("Lyra", "...Terima kasih, Yang Mulia."),
    ("Elena", "*tersenyum malu*"),
    ("Elena", "Terima kasih, Ayah."),
    ("Arga", "...Saya tidak akan mengecewakan kepercayaan Anda Yang Mulia."),
    ("King Aldric", "Aku tahu."),
    ("King Aldric", "Karena kau tidak pernah melakukannya sampai hari ini."),
    ("SYSTEM", "Dan untuk pertama kalinya sejak kedatangannya ke dunia ini..."),
    ("SYSTEM", "Arga tidak merasa seperti seorang pahlawan yang tersesat."),
    ("SYSTEM", "Ia akhirnya menemukan tempat yang bisa ia sebut rumah.")

]

TOWN_DLGS = [
    ("SYSTEM", "Matahari bersinar cerah di atas ibu kota Astravia."),
    ("SYSTEM", "Jalan-jalan utama dipenuhi bunga, pita warna-warni, dan ribuan warga yang datang dari berbagai penjuru kerajaan."),
    ("SYSTEM", "Hari itu bukan hanya perayaan kemenangan atas Raja Iblis."),
    ("SYSTEM", "Hari itu adalah hari pernikahan sang pahlawan dan sang putri."),
    ("Warga", "Hidup Pahlawan Arga!"),
    ("Warga", "Hidup Putri Elena!"),
    ("Warga", "Semoga bahagia selamanya!"),
    ("SYSTEM", "Sorak-sorai menggema di seluruh kota."),
    ("SYSTEM", "Anak-anak berlarian sambil membawa bendera kerajaan."),
    ("Anak Kecil", "Kak Arga ganteng banget pakai baju itu!"),
    ("Anak Kecil", "Kak Elena cantiiik banget!"),
    ("Anak Kecil", "Aku juga mau nikah kayak gitu nanti!"),
    ("Warga", "*tertawa*"),
    ("Warga", "Belum cukup tinggi untuk memikirkan itu, Nak."),
    ("Reno", "HAHAHAHA!"),
    ("Reno", "Ini dia! Ini yang namanya pesta!"),
    ("Reno", "Makanan gratis! Musik! Kembang api!"),
    ("Reno", "Aku bisa hidup seperti ini selamanya!"),
    ("Lyra", "Tidak heran persediaan makanan kerajaan berkurang drastis."),
    ("Reno", "Hei."),
    ("Reno", "Hari ini aku tamu kehormatan."),
    ("Lyra", "Tidak."),
    ("Lyra", "Kau hanya tamu."),
    ("Reno", "Ughh jahatnyaa hiks hiks...."),
    ("Darius", "*tersenyum tipis*"),
    ("Darius", "Meski begitu, senang melihat semuanya berakhir seperti ini."),
    ("Darius", "Setelah semua yang telah kita lalui..."),
    ("Darius", "Kurasa pemandangan seperti ini memang pantas kita dapatkan."),
    ("Lyra", "...Ya."),
    ("Lyra", "Aku tidak pernah membayangkan akan melihat hari seperti ini."),
    ("Lyra", "Tidak setelah kehilangan begitu banyak orang."),
    ("Darius", "Begitulah hidup."),
    ("Darius", "Kadang ia mengambil banyak hal dari kita."),
    ("Darius", "Tapi sesekali... ia juga memberi sesuatu kembali."),
    ("Elena", "...Aku tidak menyangka akan sebanyak ini."),
    ("Arga", "Aku juga."),
    ("Elena", "Semua orang memperhatikan kita."),
    ("Elena", "Jujur saja, aku sedikit malu."),
    ("SYSTEM", "Pipi Elena mulai memerah."),
    ("Arga", "Sedikit?"),
    ("Elena", "Baiklah."),
    ("Elena", "Sangat malu."),
    ("Arga", "*tertawa kecil*"),
    ("Arga", "Tapi mereka datang karena mereka menyayangimu."),
    ("Elena", "..."),
    ("Arga", "Dan karena mereka ingin melihatmu bahagia."),
    ("Elena", "Kamu juga ya."),
    ("Arga", "Aku apa?"),
    ("Elena", "Kalau sudah begini suka bicara hal-hal yang bikin jantungku susah tenang."),
    ("Arga", "Aku hanya jujur."),
    ("Elena", "Nah itu masalahnya."),
    ("Elena", "Aduh... sekarang mereka makin heboh."),
    ("Arga", "Mungkin karena mereka senang."),
    ("Elena", "Atau mungkin karena mereka suka menggodaku."),
    ("Reno", "AKU DENGAR ITU!"),
    ("Reno", "DAN AKU MEMANG SENANG MENGGODAMU!"),
    ("Elena", "RENO!"),
    ("SYSTEM", "Tawa pecah di antara para warga."),
    ("Lyra", "Kurasa dia tidak akan pernah berubah."),
    ("Darius", "Syukurlah."),
    ("Darius", "Dunia akan terasa terlalu sunyi kalau dia berubah."),
    ("Reno", "Lihat? Bahkan Darius mengakuinya."),
    ("Lyra", "Jangan besar kepala."),
    ("Reno", "Terlambat."),
    ("SYSTEM", "Musik kembali dimainkan."),
    ("SYSTEM", "Pasangan-pasangan mulai menari di alun-alun."),
    ("SYSTEM", "Anak-anak berlarian mengejar kelopak bunga yang tertiup angin."),
    ("Warga", "Lihat mereka."),
    ("Warga", "Akhirnya kita bisa tersenyum lagi."),
    ("Warga", "Akhirnya perang benar-benar berakhir."),
    ("SYSTEM", "Para warga bersorak, tertawa, bernyanyi, dan merayakan bersama."),
    ("SYSTEM", "Tidak ada lagi ketakutan akan perang."),
    ("SYSTEM", "Tidak ada lagi bayangan Raja Iblis."),
    ("SYSTEM", "Hanya kedamaian yang telah lama mereka perjuangkan."),
    ("SYSTEM", "Dan di tengah lautan kebahagiaan itu, sang pahlawan akhirnya menggenggam tangan orang yang paling berarti baginya."),
    ("SYSTEM", "🌸 HAPPY ENDING"),
    ("SYSTEM", "🌅 Dunia yang hampir tenggelam kini kembali bersinar karena mereka.")

]


class TrueEndScene(Scene):
    """
    True Ending Scene.
    Dipanggil oleh final_chapter_scene setelah boss dikalahkan.
    """

    def __init__(self, game):
        super().__init__(game)
        self._t        = 0.0
        self._dlg_step = 0
        # Fase: rest → proposal → return_trip → royal_hall → town_wedding → final
        self._phase    = "rest"

        self._dialogue   = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator   = NarratorBox(game.W, game.H)

        # Partikel kembang api & konfeti
        self._fireworks: list[dict] = []
        self._fw_timer  = 0.0
        self._confetti: list[dict] = []
        self._final_alpha = 0
        self._final_timer = 0.0

        # Karakter
        from entities.characters import Player, PartyNPC, KingdomNPC
        W, H = game.W, game.H
        self._ground_y = int(H * 0.82)
        gy = self._ground_y

        # Posisi awal: seperti setelah pertempuran (di singgasana boss)
        self._player = Player(W // 2 - 60, gy - 55)
        self._player.before_isekai = False
        self._elena  = PartyNPC("Elena",  W // 2 + 60, gy - 55)
        self._reno   = PartyNPC("Reno",   W // 2 - 160, gy - 55)
        self._lyra   = PartyNPC("Lyra",   W // 2 + 160, gy - 55)
        self._darius = PartyNPC("Darius", W // 2 - 240, gy - 55)
        self._king   = KingdomNPC("King Aldric", W // 2, int(H * 0.30), (200, 160, 60))

        # NPC warga kota spesifik dari town scene (tampil di fase town_wedding)
        # Posisi: kiri layar x=80,180 dan kanan layar x=W-180,W-80
        # Party berada di tengah (x ≈ 380-810), jadi NPC di pinggir kiri & kanan
        self._npc_child   = KingdomNPC("Anak Kecil",   80,        gy - 40, (220, 180, 120))
        self._npc_oldman  = KingdomNPC("Pria Tua",     185,       gy - 40, (160, 140, 100))
        self._npc_woman   = KingdomNPC("Warga Kota",   W - 185,   gy - 40, (180, 140, 140))
        self._npc_soldier = KingdomNPC("Warga Kota 2", W - 80,    gy - 40, (140, 160, 180))
        # Menghadap ke dalam (ke arah pasangan pengantin di tengah)
        self._npc_child._facing_right   = True
        self._npc_oldman._facing_right  = True
        self._npc_woman._facing_right   = False
        self._npc_soldier._facing_right = False

        # Animasi idle hardcode NPC warga (loop seperti town_scene)
        self._npc_anim_timer   = 0.0
        self._npc_anim_speed   = 0.18   # detik per frame
        self._npc_child_frame  = 0
        self._npc_oldman_frame = 0
        self._npc_woman_frame  = 0
        self._npc_soldier_frame= 0

        # Backward compat (tidak dipakai lagi tapi aman)
        self._townsfolk: list = []

        # Wedding idle animation state (sprite beranimasi loop seperti NPC lain)
        self._wedding_anim_timer  = 0.0
        self._wedding_anim_speed  = 0.15   # detik per frame
        self._wedding_arga_frame  = 0
        self._wedding_elena_frame = 0

        # Konfeti awal (akan aktif di fase town_wedding)
        for _ in range(80):
            self._confetti.append({
                'x':         float(random.randint(0, W)),
                'y':         float(random.randint(-80, H)),
                'vx':        random.uniform(-35, 35),
                'vy':        random.uniform(50, 120),
                'col':       random.choice([
                                 (255, 80, 80), (80, 200, 80), (80, 120, 255),
                                 (255, 220, 80), (255, 80, 200), (255, 255, 255)
                             ]),
                'size':      random.randint(6, 13),
                'rot':       random.uniform(0, 360),
                'rot_speed': random.uniform(-130, 130),
            })

        try:
            self._font_big   = pygame.font.SysFont("Georgia", 52, bold=True)
            self._font_sub   = pygame.font.SysFont("Georgia", 26, italic=True)
            self._font_quote = pygame.font.SysFont("Georgia", 20, italic=True)
            self._font_ui    = pygame.font.SysFont("Consolas", 14)
        except Exception:
            self._font_big   = pygame.font.Font(None, 56)
            self._font_sub   = pygame.font.Font(None, 30)
            self._font_quote = pygame.font.Font(None, 22)
            self._font_ui    = pygame.font.Font(None, 16)

        # Pending phase transition
        self._pending_phase = ""
        self._waiting_fade  = False

    # ── Asset wedding idle frames ────────────────────────────────────────────

    def _get_wedding_frames(self, char: str) -> list:
        """Ambil list frame animasi idle wedding dari assets."""
        if char == "arga":
            frames = getattr(self._game.assets, "arga_wedding_idle_frames", [])
        else:
            frames = getattr(self._game.assets, "elena_wedding_idle_frames", [])
        return frames if frames else []

    # ── Transisi antar fase ──────────────────────────────────────────────────

    def _go_to_phase(self, new_phase: str, fade_speed: int = 220):
        self._pending_phase = new_phase
        self._waiting_fade  = True
        self._transition.fade_out(speed=fade_speed)

    # ── Lifecycle ────────────────────────────────────────────────────────────

    def on_enter(self) -> None:
        self._transition.fade_in(color=(255, 255, 255), speed=180)
        self._narrator.show(["TRUE ENDING", "Savior of the World"], 3.0)
        self._dialogue.show(REST_DLGS[0][1], REST_DLGS[0][0])
        # Semua karakter idle dari awal
        self._player.set_walking(False)
        for ch in (self._elena, self._reno, self._lyra, self._darius):
            ch.set_walking(False)
            ch.disable_follow()
        # Set ukuran karakter utama 1.6 seperti scene lainnya
        self.set_char_scale(
            self._player, self._elena, self._reno, self._lyra, self._darius,
            scale=1.6
        )
        try:
            self._game.assets.play("fanfare")
        except Exception:
            pass

    # ── Input ────────────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                if self._waiting_fade:
                    return
                if self._phase == "final":
                    # Kembali ke opening / title
                    from scenes.opening_scene import OpeningScene
                    self._game.replace_scene(OpeningScene(self._game))
                    return
                if not self._dialogue.is_finished:
                    self._dialogue.skip()
                else:
                    self._advance()

    # ── Advance dialog ───────────────────────────────────────────────────────

    def _advance(self):
        try:
            self._game.assets.play("cursor")
        except Exception:
            pass

        if self._phase == "rest":
            self._dlg_step += 1
            if self._dlg_step < len(REST_DLGS):
                spk, txt = REST_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
            else:
                # Masuk proposal: Elena & Arga hadap-hadapan
                self._dlg_step = 0
                self._go_to_phase("proposal")

        elif self._phase == "proposal":
            self._dlg_step += 1
            if self._dlg_step < len(PROPOSAL_DLGS):
                spk, txt = PROPOSAL_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                # Efek suara saat lamaran diterima
                if self._dlg_step == 10:
                    try:
                        self._game.assets.play("magic")
                    except Exception:
                        pass
                    self._elena.emotion = "happy"
                    self._player.emotion = "happy"
            else:
                self._dlg_step = 0
                self._go_to_phase("return_trip")

        elif self._phase == "return_trip":
            self._dlg_step += 1
            if self._dlg_step < len(RETURN_DLGS):
                spk, txt = RETURN_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
            else:
                self._dlg_step = 0
                self._go_to_phase("royal_hall")

        elif self._phase == "royal_hall":
            self._dlg_step += 1
            if self._dlg_step < len(ROYAL_HALL_DLGS):
                spk, txt = ROYAL_HALL_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == 12:  # Raja setujui
                    try:
                        self._game.assets.play("fanfare")
                    except Exception:
                        pass
            else:
                self._dlg_step = 0
                self._go_to_phase("town_wedding")

        elif self._phase == "town_wedding":
            self._dlg_step += 1
            if self._dlg_step < len(TOWN_DLGS):
                spk, txt = TOWN_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == 9:
                    try:
                        self._game.assets.play("magic")
                    except Exception:
                        pass
            else:
                # Masuk layar akhir
                self._phase = "final"
                self._final_timer = 0.0
                self._dialogue.hide()

    # ── Update ───────────────────────────────────────────────────────────────

    def update(self, dt: float) -> None:
        self._t += dt
        self._transition.update(dt)
        self._dialogue.update(dt)
        self._narrator.update(dt)

        # Handle fade done → ganti phase
        if self._waiting_fade and self._transition.done:
            self._waiting_fade  = False
            self._phase         = self._pending_phase
            self._pending_phase = ""
            self._dlg_step      = 0
            self._on_phase_enter()

        # Update karakter
        self._player.update(dt)
        self._elena.update(dt)
        self._reno.update(dt)
        self._lyra.update(dt)
        self._darius.update(dt)
        self._king.update(dt)
        self._npc_child.update(dt)
        self._npc_oldman.update(dt)
        self._npc_woman.update(dt)
        self._npc_soldier.update(dt)

        # Animasi idle hardcode NPC warga (aktif di town_wedding & final)
        if self._phase in ("town_wedding", "final"):
            self._npc_anim_timer += dt
            if self._npc_anim_timer >= self._npc_anim_speed:
                self._npc_anim_timer = 0.0
                assets = self._game.assets
                child_f   = getattr(assets, "citizen_child_idle_frames", [])
                oldman_f  = getattr(assets, "oldman_idle_frames",        [])
                woman_f   = getattr(assets, "citizen_man_idle_frames",   [])
                soldier_f = getattr(assets, "soldier_idle_frames",       [])
                if child_f:   self._npc_child_frame   = (self._npc_child_frame   + 1) % len(child_f)
                if oldman_f:  self._npc_oldman_frame  = (self._npc_oldman_frame  + 1) % len(oldman_f)
                if woman_f:   self._npc_woman_frame   = (self._npc_woman_frame   + 1) % len(woman_f)
                if soldier_f: self._npc_soldier_frame = (self._npc_soldier_frame + 1) % len(soldier_f)

            # Animasi idle wedding Arga & Elena
            self._wedding_anim_timer += dt
            if self._wedding_anim_timer >= self._wedding_anim_speed:
                self._wedding_anim_timer = 0.0
                arga_frames  = self._get_wedding_frames("arga")
                elena_frames = self._get_wedding_frames("elena")
                if arga_frames:
                    self._wedding_arga_frame  = (self._wedding_arga_frame  + 1) % len(arga_frames)
                if elena_frames:
                    self._wedding_elena_frame = (self._wedding_elena_frame + 1) % len(elena_frames)

        # Walk-in untuk return_trip
        self.update_walkin(dt)

        # Animasi walk saat walkin aktif
        if self._walkin_active:
            self._player.set_walking(True, True)
        elif self._phase == "return_trip":
            # Aktifkan follow setelah walkin selesai
            if not self._elena._follow_enabled:
                self._elena.follow(self._player)
                self._elena.follow_distance  = -90
                self._elena.enable_follow()
            if not self._reno._follow_enabled:
                self._reno.follow(self._player)
                self._reno.follow_distance   = -170
                self._reno.enable_follow()
            if not self._lyra._follow_enabled:
                self._lyra.follow(self._player)
                self._lyra.follow_distance   = -250
                self._lyra.enable_follow()
            if not self._darius._follow_enabled:
                self._darius.follow(self._player)
                self._darius.follow_distance = -330
                self._darius.enable_follow()
        else:
            # Fase lain — matikan follow, karakter idle di posisinya
            if not self._walkin_active:
                self._player.set_walking(False)

        # Konfeti (aktif di town_wedding & final)
        if self._phase in ("town_wedding", "final"):
            for c in self._confetti:
                c['x'] += c['vx'] * dt
                c['y'] += c['vy'] * dt
                c['rot'] += c['rot_speed'] * dt
                if c['y'] > self._game.H + 20:
                    c['y'] = -15.0
                    c['x'] = float(random.randint(0, self._game.W))

            # Kembang api
            self._fw_timer += dt
            if self._fw_timer > 0.55:
                self._fw_timer = 0.0
                self._spawn_firework()
            for fw in self._fireworks:
                fw['age'] += dt
                for p in fw['particles']:
                    p[0] += p[2] * dt
                    p[1] += p[3] * dt
                    p[3] += 110 * dt
            self._fireworks = [fw for fw in self._fireworks if fw['age'] < 1.4]

        # Final fade-in teks
        if self._phase == "final":
            self._final_timer += dt
            self._final_alpha  = min(255, int(255 * self._final_timer / 2.0))

    def _on_phase_enter(self):
        """Dipanggil tepat setelah fase berganti (setelah fade selesai)."""
        # Pastikan karakter utama selalu di skala 1.6 di semua fase
        self.set_char_scale(
            self._player, self._elena, self._reno, self._lyra, self._darius,
            scale=1.6
        )

        if self._phase == "proposal":
            self._transition.fade_in(speed=180)
            self._narrator.show(["Di Tengah Singgasana yang Sunyi..."], 2.0)
            self._dialogue.show(PROPOSAL_DLGS[0][1], PROPOSAL_DLGS[0][0])
            # Posisikan Arga & Elena hadap-hadapan, party agak menjauh
            W, H = self._game.W, self._game.H
            gy = self._ground_y
            self._player._x = W // 2 - 70
            self._elena._x  = W // 2 + 70
            self._reno._x   = 80
            self._lyra._x   = W - 80
            self._darius._x = 40
            # Facing: Arga kanan, Elena kiri, party menghadap tengah
            self._player._facing_right = True
            self._elena._facing_right  = False
            self._reno._facing_right   = True
            self._lyra._facing_right   = False
            self._darius._facing_right = True
            # Matikan follow semua di fase ini
            for ch in (self._elena, self._reno, self._lyra, self._darius):
                ch.disable_follow()
            self._player.set_walking(False)

        elif self._phase == "return_trip":
            self._transition.fade_in(speed=200)
            self._narrator.show(["Perjalanan Pulang ke Astravia"], 2.5)
            self._dialogue.show(RETURN_DLGS[0][1], RETURN_DLGS[0][0])
            # Semua jalan masuk dari kiri
            W = self._game.W
            self.start_walkin([
                (self._player, W // 2 - 60),
                (self._elena,  W // 2 + 30),
                (self._reno,   W // 2 - 150),
                (self._lyra,   W // 2 + 120),
                (self._darius, W // 2 - 230),
            ])

        elif self._phase == "royal_hall":
            self._transition.fade_in(speed=180)
            self._narrator.show(["Balairung Kerajaan Astravia"], 2.5)
            self._dialogue.show(ROYAL_HALL_DLGS[0][1], ROYAL_HALL_DLGS[0][0])
            try:
                self._game.assets.play("fanfare")
            except Exception:
                pass
            # Posisi di balairung: Raja di atas, party di bawah
            W, H = self._game.W, self._game.H
            gy = self._ground_y
            self._king._x     = W // 2
            self._king._y     = int(H * 0.28)
            self._player._x   = W // 2 - 60
            self._elena._x    = W // 2 + 60
            self._reno._x     = W // 2 - 160
            self._lyra._x     = W // 2 + 160
            self._darius._x   = W // 2 - 250
            # Semua menghadap raja (kanan)
            for ch in (self._player, self._elena, self._reno, self._lyra, self._darius):
                if hasattr(ch, "_facing_right"):
                    ch._facing_right = True
                if hasattr(ch, "disable_follow"):
                    ch.disable_follow()
            self._player.set_walking(False)

        elif self._phase == "town_wedding":
            self._transition.fade_in(color=(255, 255, 255), speed=200)
            self._narrator.show(["Kota Astravia — Hari Perayaan"], 2.5)
            self._dialogue.show(TOWN_DLGS[0][1], TOWN_DLGS[0][0])
            try:
                self._game.assets.play("fanfare")
            except Exception:
                pass
            W, H = self._game.W, self._game.H
            gy = self._ground_y
            # Arga & Elena di tengah dalam gaun pengantin (sprite wedding)
            self._player._x = W // 2 - 50
            self._elena._x  = W // 2 + 50
            self._player.emotion = "happy"
            self._elena.emotion  = "happy"
            self._reno._x   = W // 2 - 170
            self._lyra._x   = W // 2 + 170
            self._darius._x = W // 2 - 260
            # Facing: Arga kanan, Elena kiri (hadap-hadapan), party ke tengah
            self._player._facing_right = True
            self._elena._facing_right  = False
            self._reno._facing_right   = True
            self._lyra._facing_right   = False
            self._darius._facing_right = True
            for ch in (self._elena, self._reno, self._lyra, self._darius):
                ch.disable_follow()
            self._player.set_walking(False)

        elif self._phase == "final":
            self._transition.fade_in(speed=100)

    # ── Spawn kembang api ────────────────────────────────────────────────────

    def _spawn_firework(self):
        cx  = random.randint(80, self._game.W - 80)
        cy  = random.randint(30, 200)
        col = random.choice([
            (255, 220, 80), (255, 100, 100), (100, 220, 255),
            (200, 255, 120), (255, 120, 200), (200, 200, 255),
        ])
        parts = []
        for _ in range(22):
            angle = random.uniform(0, math.pi * 2)
            spd   = random.uniform(70, 200)
            parts.append([float(cx), float(cy),
                           math.cos(angle) * spd, math.sin(angle) * spd])
        self._fireworks.append({'cx': cx, 'cy': cy, 'col': col,
                                'particles': parts, 'age': 0.0})

    # ── Draw ─────────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        W, H = self._game.W, self._game.H

        # Background per fase
        if self._phase in ("rest", "proposal"):
            surface.blit(self._game.assets.bg_ruang_boss_rusak, (0, 0))
        elif self._phase in ("return_trip", "royal_hall"):
            surface.blit(self._game.assets.bg_belairung, (0, 0))
        else:  # town_wedding, final
            surface.blit(self._game.assets.bg_hari_pernikahan, (0, 0))

        # ── Fase REST ────────────────────────────────────────────────────────
        if self._phase == "rest":
            # Semua karakter dalam keadaan lelah (emotion sad/normal, bisa saja
            # karakter sudah punya state hurt — gambar saja biasa)
            for ch in (self._darius, self._lyra, self._reno, self._elena, self._player):
                ch.draw(surface)
            # Label kelelahan di atas kepala
            self._draw_tired_labels(surface)

        # ── Fase PROPOSAL ────────────────────────────────────────────────────
        elif self._phase == "proposal":
            # Party di pinggir, Arga & Elena berhadapan di tengah (idle front)
            self._reno.draw(surface)
            self._lyra.draw(surface)
            self._darius.draw(surface)
            # Arga menghadap kanan, Elena menghadap kiri (flip horizontal)
            self._player.draw(surface)
            self._draw_elena_facing(surface, face_left=True)
            # Efek hati di antara mereka
            self._draw_proposal_hearts(surface)

        # ── Fase RETURN TRIP ─────────────────────────────────────────────────
        elif self._phase == "return_trip":
            for ch in (self._darius, self._lyra, self._reno, self._elena, self._player):
                ch.draw(surface)

        # ── Fase ROYAL HALL ──────────────────────────────────────────────────
        elif self._phase == "royal_hall":
            self._king.draw(surface)
            for ch in (self._darius, self._lyra, self._reno, self._elena, self._player):
                ch.draw(surface)

        # ── Fase TOWN WEDDING ────────────────────────────────────────────────
        elif self._phase in ("town_wedding", "final"):
            # Kembang api & konfeti
            self._draw_fireworks(surface)
            self._draw_confetti(surface)

            # NPC warga kota — digambar dengan sprite animasi hardcode
            # Kiri layar (menghadap kanan)
            self._draw_npc_frame(surface, "citizen_child_idle_frames", self._npc_child_frame,
                                 int(self._npc_child._x), int(self._npc_child._y),
                                 facing_right=self._npc_child._facing_right)
            self._draw_npc_frame(surface, "oldman_idle_frames", self._npc_oldman_frame,
                                 int(self._npc_oldman._x), int(self._npc_oldman._y),
                                 facing_right=self._npc_oldman._facing_right)
            # Kanan layar (menghadap kiri)
            self._draw_npc_frame(surface, "citizen_man_idle_frames", self._npc_woman_frame,
                                 int(self._npc_woman._x), int(self._npc_woman._y),
                                 facing_right=self._npc_woman._facing_right)
            self._draw_npc_frame(surface, "soldier_idle_frames", self._npc_soldier_frame,
                                 int(self._npc_soldier._x), int(self._npc_soldier._y),
                                 facing_right=self._npc_soldier._facing_right)
            # Party
            self._reno.draw(surface)
            self._lyra.draw(surface)
            self._darius.draw(surface)

            # Arga & Elena dengan sprite pengantin (atau fallback primitif)
            if self._phase == "town_wedding":
                self._draw_wedding_characters(surface)
            else:
                self._draw_wedding_characters(surface)

            # Efek hati di atas pasangan pengantin
            if self._phase == "town_wedding":
                self._draw_wedding_hearts(surface)

        # ── Overlay FINAL ────────────────────────────────────────────────────
        if self._phase == "final":
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, min(160, self._final_alpha)))
            surface.blit(ov, (0, 0))
            if self._final_alpha > 80:
                a2 = min(255, (self._final_alpha - 80) * 3)
                lines = [
                    (self._font_big,   "The Summoned Hero",          GOLD_LIGHT, 150),
                    (self._font_big,   "Saved the World.",            GOLD_LIGHT, 215),
                    (self._font_sub,   "— TRUE ENDING —",             UI_ACCENT,  300),
                    (self._font_quote, "[ SPACE / ENTER untuk keluar ]", UI_DIMTEXT, 420),
                ]
                for font, text, col, y in lines:
                    surf = font.render(text, True, col)
                    surf.set_alpha(a2)
                    surface.blit(surf, (W // 2 - surf.get_width() // 2, y))

        # UI umum
        self._narrator.draw(surface)
        self._dialogue.draw(surface)
        self._transition.draw(surface)

        # Label lokasi
        lbl_map = {
            "rest":         "Singgasana Kegelapan — Setelah Pertempuran",
            "proposal":     "Singgasana Kegelapan — Momen Berdua",
            "return_trip":  "Perjalanan Pulang ke Astravia",
            "royal_hall":   "Balairung Kerajaan Astravia",
            "town_wedding": "Kota Astravia — Hari Pernikahan",
        }
        lbl = lbl_map.get(self._phase, "")
        if lbl:
            try:
                t = self._font_ui.render(lbl, True, UI_ACCENT)
                surface.blit(t, (W // 2 - t.get_width() // 2, 8))
            except Exception:
                pass

    # ── Draw NPC frame helper ────────────────────────────────────────────────

    def _draw_npc_frame(self, surface, frames_attr, frame_idx, x, y,
                        scale=1.4, facing_right=True):
        """Gambar NPC dari frame list di assets, normalisasi ke 96px.
        Skala 1.4 sedikit lebih kecil dari karakter utama agar perspektif wajar.
        """
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

    # ── Helper draw ──────────────────────────────────────────────────────────

    def _draw_tired_labels(self, surface: pygame.Surface):
        """Label kelelahan di atas kepala karakter saat fase rest."""
        chars_labels = [
            (self._player, "Arga"),
            (self._elena,  "Elena"),
            (self._reno,   "Reno"),
            (self._lyra,   "Lyra"),
            (self._darius, "Darius"),
        ]
        try:
            f = pygame.font.SysFont("Georgia", 14, italic=True)
            for ch, name in chars_labels:
                txt = f.render("z z z", True, (180, 200, 255))
                # Posisi mengambang naik turun
                offset_y = int(math.sin(self._t * 2 + hash(name) % 10) * 5)
                surface.blit(txt, (int(ch._x) - txt.get_width() // 2,
                                   int(ch._y) - 75 + offset_y))
        except Exception:
            pass

    def _draw_elena_facing(self, surface: pygame.Surface, face_left: bool = True):
        """Gambar Elena menghadap kiri (flip) untuk scene proposal."""
        # Elena draw biasa, lalu flip jika perlu
        # Karena sistem draw karakter memakai sprite internal, kita buat surface temp
        tmp = pygame.Surface((self._game.W, self._game.H), pygame.SRCALPHA)
        self._elena.draw(tmp)
        if face_left:
            tmp = pygame.transform.flip(tmp, True, False)
            # Setelah flip, posisi x berubah — kita blit dengan offset
            # flip horizontal: pixel di x menjadi (W - x - 1)
            # karena kita flip seluruh surface, blit langsung ke surface
        surface.blit(tmp, (0, 0))

    def _draw_proposal_hearts(self, surface: pygame.Surface):
        """Efek hati animasi antara Arga & Elena."""
        mid_x = (self._player._x + self._elena._x) // 2
        try:
            for i in range(4):
                hx = int(mid_x + math.sin(self._t * 1.8 + i * 1.2) * 25)
                hy = int(self._ground_y - 100 - i * 22 + math.cos(self._t * 2 + i) * 8)
                alpha = int(180 + 75 * math.sin(self._t * 2.5 + i))
                s = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 100, 140, alpha), (10, 10), 8)
                surface.blit(s, (hx - 10, hy - 10))
        except Exception:
            pass

    def _draw_wedding_characters(self, surface: pygame.Surface):
        """
        Gambar Arga & Elena dalam pakaian pengantin dengan animasi idle.
        Menggunakan arga_wedding_idle_frames / elena_wedding_idle_frames dari assets.
        Fallback ke primitif jika frames tidak tersedia.
        """
        SPRITE_BASE_H = 96   # tinggi normalisasi (sama dengan NPC lain)
        SCALE         = 1.6  # sama dengan skala karakter utama

        px, py = int(self._player._x), int(self._player._y)
        ex, ey = int(self._elena._x),  int(self._elena._y)

        arga_frames  = self._get_wedding_frames("arga")
        elena_frames = self._get_wedding_frames("elena")

        # ── Arga ──
        if arga_frames:
            img = arga_frames[self._wedding_arga_frame % len(arga_frames)]
            orig_w, orig_h = img.get_size()
            if orig_h > 0:
                norm_w  = int(orig_w * SPRITE_BASE_H / orig_h)
                norm_img = pygame.transform.scale(img, (norm_w, SPRITE_BASE_H))
                new_w   = int(norm_w * SCALE)
                new_h   = int(SPRITE_BASE_H * SCALE)
                scaled  = pygame.transform.scale(norm_img, (new_w, new_h))
                # Arga menghadap kanan (default, tidak di-flip)
                surface.blit(scaled, (px - new_w // 2, py - new_h))
        else:
            self._draw_primitive_groom(surface, px, py)

        # ── Elena ──
        if elena_frames:
            img = elena_frames[self._wedding_elena_frame % len(elena_frames)]
            orig_w, orig_h = img.get_size()
            if orig_h > 0:
                norm_w  = int(orig_w * SPRITE_BASE_H / orig_h)
                norm_img = pygame.transform.scale(img, (norm_w, SPRITE_BASE_H))
                new_w   = int(norm_w * SCALE)
                new_h   = int(SPRITE_BASE_H * SCALE)
                scaled  = pygame.transform.scale(norm_img, (new_w, new_h))
                # Elena menghadap kiri (flip horizontal)
                scaled  = pygame.transform.flip(scaled, True, False)
                surface.blit(scaled, (ex - new_w // 2, ey - new_h))
        else:
            self._draw_primitive_bride(surface, ex, ey)

        # Label nama di bawah pasangan
        try:
            f = pygame.font.SysFont("Georgia", 14, bold=True)
            for name, cx in [("Arga", px), ("Elena", ex)]:
                t = f.render(name, True, GOLD_LIGHT)
                surface.blit(t, (cx - t.get_width() // 2, py + 25))
        except Exception:
            pass


    def _draw_primitive_groom(self, surface: pygame.Surface, cx: int, cy: int):
        """Jas pengantin sederhana (primitif) untuk Arga."""
        # Kepala
        pygame.draw.circle(surface, (220, 180, 140), (cx, cy - 55), 16)
        # Badan jas putih
        body = pygame.Surface((44, 55), pygame.SRCALPHA)
        pygame.draw.rect(body, (240, 240, 250, 240), (0, 0, 44, 55), border_radius=4)
        # Dasi kupu-kupu emas
        pygame.draw.polygon(body, (200, 160, 30),
                            [(18, 10), (22, 16), (18, 22), (10, 16)])
        pygame.draw.polygon(body, (200, 160, 30),
                            [(26, 10), (22, 16), (26, 22), (34, 16)])
        surface.blit(body, (cx - 22, cy - 45))
        # Celana hitam
        pygame.draw.rect(surface, (30, 30, 40),
                         pygame.Rect(cx - 14, cy + 8, 28, 30), border_radius=3)
        # Rambut
        pygame.draw.arc(surface, (60, 40, 20),
                        pygame.Rect(cx - 16, cy - 73, 32, 24),
                        0, math.pi, 4)

    def _draw_primitive_bride(self, surface: pygame.Surface, cx: int, cy: int):
        """Gaun pengantin sederhana (primitif) untuk Elena."""
        # Kepala
        pygame.draw.circle(surface, (230, 190, 150), (cx, cy - 55), 15)
        # Mahkota sederhana
        crown_pts = [
            (cx - 12, cy - 72), (cx - 8, cy - 80), (cx, cy - 85),
            (cx + 8, cy - 80), (cx + 12, cy - 72),
        ]
        pygame.draw.polygon(surface, (220, 185, 30), crown_pts)
        # Gaun putih mengembang
        skirt = pygame.Surface((70, 70), pygame.SRCALPHA)
        pygame.draw.ellipse(skirt, (255, 245, 250, 230), (0, 10, 70, 60))
        surface.blit(skirt, (cx - 35, cy - 15))
        # Badan gaun
        body = pygame.Surface((36, 45), pygame.SRCALPHA)
        pygame.draw.rect(body, (250, 240, 248, 240), (0, 0, 36, 45), border_radius=5)
        # Pita merah muda di pinggang
        pygame.draw.rect(body, (255, 160, 180, 200),
                         pygame.Rect(0, 28, 36, 8), border_radius=3)
        surface.blit(body, (cx - 18, cy - 45))
        # Rambut panjang
        for i in range(3):
            ox = (i - 1) * 8
            pygame.draw.line(surface, (140, 80, 30),
                             (cx + ox, cy - 62), (cx + ox + 4, cy + 5), 3)

    def _draw_wedding_hearts(self, surface: pygame.Surface):
        """Hati besar di atas pasangan pengantin saat perayaan."""
        mid_x = (self._player._x + self._elena._x) / 2
        try:
            for i in range(6):
                hx = int(mid_x + math.sin(self._t * 1.5 + i * 1.05) * 35)
                hy = int(self._ground_y - 120 - i * 18
                         + math.cos(self._t * 2.0 + i * 0.9) * 10)
                sz = random.choice([10, 12, 14])
                alpha = int(160 + 95 * math.sin(self._t * 3 + i))
                s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 100, 130, alpha), (sz, sz), sz)
                surface.blit(s, (hx - sz, hy - sz))
        except Exception:
            pass

    def _draw_fireworks(self, surface: pygame.Surface):
        for fw in self._fireworks:
            alpha = int(255 * (1 - fw['age'] / 1.4))
            for p in fw['particles']:
                s = pygame.Surface((8, 8), pygame.SRCALPHA)
                pygame.draw.circle(s, (*fw['col'], alpha), (4, 4), 4)
                surface.blit(s, (int(p[0]) - 4, int(p[1]) - 4))

    def _draw_confetti(self, surface: pygame.Surface):
        for c in self._confetti:
            s = pygame.Surface((c['size'], c['size']), pygame.SRCALPHA)
            pygame.draw.rect(s, (*c['col'], 200), (0, 0, c['size'], c['size']))
            surface.blit(s, (int(c['x']), int(c['y'])))
