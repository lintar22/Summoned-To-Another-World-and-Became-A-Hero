
import pygame
import math
import random
from engine.base import Scene
from engine.colors import *
from ui.components import DialogueBox, TransitionScreen, NarratorBox, FloatingText, PartyHUD
from entities.characters import Player, PartyNPC, MonsterNPC


class Chapter3Scene(Scene):

    RENO_DLGS = [
    ("Reno",   "Sial— ada berapa ekor lagi?! Ini tidak masuk akal!"),
    ("Arga",   "Hei. Kau kenapa!?."),
    ("Reno",   "Ha?! Siapa kamu—"),
    ("Elena",  "Arga, tunggu! Disana banyak sekali monsternya!"),
    ("Arga",   "Iya, mari kita bantu dia!."),
    ]

    RENO_POST_BATTLE = [
        ("Reno",   "...Gila. hanya dalam sekejap. Semuanya habis begitu saja."),
        ("Reno",   "Hei, nama kamu siapa?"),
        ("Arga",   "Arga."),
        ("Reno",   "Aku Reno. Petarung bebas dari utara. Sudah tiga bulan aku menjelajai hutan ini sendirian."),
        ("Arga",   "Sendirian tiga bulan?"),
        ("Reno",   "Iya. Aku sedang mencari kelompok pahlawan yang katanya akan menuju ke kastil Raja Iblis tapi tidak ketemu-ketemu."),
        ("Reno",   "Kalian yang dimaksud, kan? Boleh aku ikut? Aku tidak minta apa-apa."),
        ("Arga",   "Kamu tidak takut?"),
        ("Reno",   "Takut itu memang pasti. Tapi daripada diem doang disini, mending aku ikut dengan kalian."),
        ("Arga",   "...Baiklah. Selamat datang Reno, semoga kita bisa saling membantu yah."),
        ("SYSTEM", "Reno bergabung dengan party!"),
    ]

    LYRA_DLGS = [
        ("Lyra",   "HEI! Jangan mendekat kesini!!."),
        ("Arga",   "Kenapa?"),
        ("Lyra",   "Disini ada artefak yang sangat amat kuno dan itu sangat sensitif terhadap mana yang asing."),
        ("Arga",   "...Hm. Seperti ini?"),
        ("SYSTEM", "💥 BOOM!"),
        ("Lyra",   "...Aku bilang jangan mendekat."),
        ("Lyra",   "Hati-Hati. Ada tiga sumber mana bergerak dari sana."),
        ("Arga",   "Kamu bisa bertarung kan?"),
        ("Lyra",   "Mending tanyain itu pada dirimu sendiri."),
    ]

    LYRA_POST_BATTLE = [
        ("Lyra", "Kekuatanmu aneh."),
        ("Lyra", "Tidak seperti penyihir, tapi juga tidak seperti ksatria biasa."),
        ("Arga", "Aku anggap itu pujian."),
        ("Lyra", "Jangan terlalu percaya diri."),
        ("Reno", "Wah, baru kenal udah galak."),
        ("Lyra", "Dan kamu terlalu banyak bicara."),
        ("Reno", "Uwahk serem."),
        ("Elena", "Lyra... kamu berasal dari guild Bintang Hitam, bukan?"),
        ("Lyra", "...Masih ada yang mengenali lambang itu rupanya."),
        ("Elena", "Guild itu cukup terkenal beberapa tahun lalu."),
        ("Lyra", "Dulu."),
        ("Lyra", "Sekarang nama itu tidak berarti apa-apa."),
        ("Arga", "...Apa yang terjadi?"),
        ("Lyra", "Pasukan iblis menyerang markas kami."),
        ("Lyra", "Kami pikir kami siap menghadapi mereka."),
        ("Lyra", "Kami salah."),
        ("Lyra", "...Ketua guild kami gugur hari itu."),
        ("Lyra", "Dia bertahan sampai orang terakhir berhasil melarikan diri."),
        ("Lyra", "Dan setelah semuanya berakhir... tidak ada yang peduli."),
        ("Lyra", "Tidak ada bantuan."),
        ("Lyra", "Tidak ada apapun."),
        ("Lyra", "Hanya reruntuhan dan nama-nama yang perlahan dilupakan."),
        ("Reno", "..."),
        ("Elena", "...Maafkan aku."),
        ("Lyra", "Tidak perlu."),
        ("Lyra", "Belas kasihan tidak akan menghidupkan mereka kembali."),
        ("Arga", "Jadi sejak saat itu kamu berjalan sendirian?"),
        ("Lyra", "Ya."),
        ("Lyra", "Lebih mudah begitu."),
        ("Lyra", "Tidak perlu kehilangan siapa pun lagi."),
        ("Arga", "Dan juga tidak ada yang akan menolongmu saat keadaan menjadi buruk."),
        ("Lyra", "..."),
        ("Reno", "Dia ada benarnya."),
        ("Lyra", "Aku tidak meminta pendapatmu."),
        ("Reno", "Nah, itu dia. Yang tadi sempat hilang."),
        ("Lyra", "..."),
        ("Lyra", "Hei."),
        ("Lyra", "Sebenarnya kalian ini siapa?"),
        ("Lyra", "Kalian bahkan tidak mengenalku."),
        ("Lyra", "Tapi tetap bertarung seolah nyawa kalian saling bergantung."),
        ("Arga", "Kami juga tidak benar-benar mengenalmu."),
        ("Lyra", "...Lalu kenapa membantuku?"),
        ("Arga", "Karena kamu bertarung di sisi kami."),
        ("Arga", "Kadang itu sudah cukup."),
        ("Elena", "Tidak semua orang harus punya alasan rumit untuk saling membantu."),
        ("Lyra", "...Hm."),
        ("Reno", "Kalau dipikir-pikir, kita memang kelompok yang aneh."),
        ("Lyra", "Itu satu-satunya hal yang masuk akal dari kalian."),
        ("Arga", "Kalau begitu bagaimana?"),
        ("Arga", "Masih ingin berjalan sendirian?"),
        ("Lyra", "..."),
        ("Lyra", "Aku sudah terlalu lama berjalan tanpa tujuan."),
        ("Lyra", "Dan untuk pertama kalinya setelah sekian lama... aku tidak merasa harus melakukannya sendirian."),
        ("Reno", "Aku anggap itu sebagai 'ya'."),
        ("Lyra", "Jangan membuatku menyesal mengambil keputusan ini."),
        ("Arga", "Tidak ada jaminan."),
        ("Lyra", "...Hah. Setidaknya kamu jujur."),
        ("SYSTEM", "Lyra bergabung dengan party.")

    ]

    DARIUS_DLGS = [
        ("Darius", "Kugh.. Kalian— pergi dari sini! Bawa warga desa ke utara! Aku yang akan menahan mereka di sini!"),
        ("Arga",   "Ada berapa warga yang tersisa?"),
        ("Darius", "Tidak penting! Pergi saja!"),
        ("Reno",   "Kita tidak bisa tinggalkan orang sendirian di sini—"),
        ("Darius", "Ini DESAKU. Akulah yang harus menjaganya. Kalian tidak punya urusan di sini!"),
        ("Arga",   "Kamu tidak akan bisa menahan semua ini seorang diri!."),
        ("Darius", "Aku sudah tahan seharian. Aku bi—"),
        ("Reno",   "Mereka datang lagi dari timur! Jauh lebih banyak dari tadi!"),
        ("Arga",   "Hei kamu! Biarkan kami membantumu. Setelah ini baru kita bicara."),
    ]

    DARIUS_POST_BATTLE = [
        ("Darius", "...Kenapa kalian masih di sini? Bukankah urusan kalian sudah selesai?"),
        ("Elena", "Meninggalkan seseorang sendirian setelah pertempuran seperti ini bukan kebiasaan kami."),
        ("Darius", "Aku tidak membutuhkan belas kasihanmu wanita."),
        ("Arga", "Kalau itu rasa kasihan, kami sudah pergi sejak tadi."),
        ("Darius", "..."),
        ("Arga", "Dan juga, kau terlalu kasar dengan Putri Kerajaan sialan."),
        ("Darius", "HA! PUTRI KERAJAAN?, JADI KALIAN ADALAH KELOMPOK PAHLAWAN YANG DIBICARAKAN ITU?!"),
        ("Arga", "Ya, Aku Arga."),
        ("Reno", "Reno disini."),
        ("Lyra", "Lyra."),
        ("Arga", "Dan yang terakhir."),
        ("Elena", "Namaku Elena Von Astaravia."),
        ("Darius", "Wahai tuan putri, mohon maafkan ketidaksopanan yang sudah kuucapkan tadi."),
        ("Elena", "Ngapapa ko."),
        ("Arga", "Hei, siapa namamu?"),
        ("Darius", "Aku Darius."),
        ("Arga", " Hei Darius desa ini sudah kosong, kan?"),
        ("Darius", "Ya. Warga terakhir meninggalkannya tiga hari yang lalu."),
        ("Darius", "Mereka memohon agar aku ikut pergi bersama mereka."),
        ("Darius", "Tapi aku tidak sanggup meninggalkan tempat ini begitu saja."),
        ("Darius", "Setiap rumah di sini menyimpan kenangan. Setiap jalannys pernah dipenuhi suara orang-orang yang kini entah berada di mana."),
        ("Elena", "...Kau bertahan sendirian demi menjaga desa yang bahkan sudah ditinggalkan."),
        ("Darius", "Seseorang harus tetap berdiri sampai akhir."),
        ("Arga", "Lalu sekarang apa yang akan kau lakukan?"),
        ("Darius", "...Aku tidak tahu."),
        ("Darius", "Selama ini aku hanya bertarung agar desa ini tetap ada."),
        ("Darius", "Tapi sekarang bahkan alasan itu sudah hilang."),
        ("Arga", "Kalau begitu, ikutlah bersama kami."),
        ("Darius", "...Apa?"),
        ("Arga", "Kalau kau benar-benar ingin melindungi orang lain, masih ada banyak tempat yang membutuhkan pedangmu."),
        ("Arga", "Masih ada banyak desa yang bisa mengalami nasib yang sama."),
        ("Arga", "Dan kami tidak bisa menghentikan semuanya sendirian."),
        ("Darius", "...Kau mengajakku bergabung?"),
        ("Arga", "Bukan mengajak."),
        ("Arga", "Aku memintamu."),
        ("Darius", "..."),
        ("Darius", "Kalian bahkan tidak mengenalku."),
        ("Elena", "Mungkin."),
        ("Elena", "Tapi seseorang yang tetap bertahan menjaga desa kosong seorang diri selama berhari-hari bukanlah orang jahat."),
        ("Reno", "Dan terus terang, kita memang butuh petarung sekuat dirimu."),
        ("Lyra", "Untuk sekali ini aku setuju dengan Reno."),
        ("Reno", "Hei, kenapa kedengarannya seperti hinaan?"),
        ("Darius", "..."),
        ("Darius", "Aneh."),
        ("Darius", "Aku menghabiskan bertahun-tahun menjaga desa ini."),
        ("Darius", "Tapi saat akhirnya semuanya berakhir... justru orang-orang asing yang memberiku alasan untuk terus melangkah."),
        ("Arga", "..."),
        ("Darius", "Aku tidak tahu apakah aku pantas berjalan bersama kalian."),
        ("Darius", "Aku gagal melindungi tempat yang paling ingin kulindungi."),
        ("Arga", "Kalau itu yang kau sebut gagal, aku tidak ingin membayangkan seperti apa bentuk keberhasilanmu."),
        ("Elena", "Tidak semua yang hilang bisa diselamatkan, Darius."),
        ("Elena", "Tapi masih ada banyak hal yang bisa kau lindungi mulai hari ini."),
        ("Darius", "..."),
        ("Darius", "Mungkin kalian benar."),
        ("Darius", "Aku tidak bisa terus berdiri di antara puing-puing ini dan berpura-pura bahwa masa lalu masih ada."),
        ("Darius", "Desa ini sudah memilih jalannya."),
        ("Darius", "Dan kurasa... sekarang giliranku untuk memilih jalan milikku."),
        ("Reno", "Nah, itu baru kedengarannya seperti seorang petarung!"),
        ("Lyra", "Jangan rusak suasananya."),
        ("Reno", "Aku cuma berusaha memberi semangat."),
        ("Darius", "Haha"),
        ("Darius", "Baiklah."),
        ("Darius", "Aku akan ikut dengan kalian."),
        ("Darius", "Jika masih ada orang yang membutuhkanku... maka aku tidak akan menyia-nyiakan kesempatan itu."),
        ("Arga", "Senang mendengarnya."),
        ("Elena", "Selamat datang."),
        ("Reno", "Fiyuhhh! Akhirnya ada orang normal di kelompok ini."),
        ("Lyra", "Kupikir itu justru mengurangi jumlah orang normal menjadi nol."),
        ("Darius", "...Aku mulai mengerti kenapa kalian bisa bertahan sejauh ini."),
        ("SYSTEM", "Darius bergabung dengan party.")

    ]

                                                                                
    ENEMY_WARNING = {
        "forest":  [
            ("Reno",   "...Tunggu. Aku cium bau sesuatu."),
            ("Elena",  "Dari arah timur! Ada gerombolan Monster!"),
            ("SYSTEM", "Monster muncul dari balik pohon!"),
        ],
        "ruins":   [
            ("Lyra",   "Energi sihir kuno ini mulai bereaksi..."),
            ("Arga",   "Hati-hati semua. Ada yang datang dari arah sana!"),
            ("SYSTEM", "Monster bangkit dari reruntuhan!"),
        ],
        "village": [
            ("Darius", "Suara langkah kaki... mereka datang lagi sialan!"),
            ("Reno",   "Banyak monster yang mau datang kesini, hati-hati semuanya!"),
            ("SYSTEM", "Gerombolan monster menyerbu dari arah timur!"),
        ],
    }

    CAMPFIRE_DLGS = [
        ("Arga", "Akhirnya bisa duduk sebentar juga."),
        ("Reno", "Baru juga sampai di sini, sudah mengeluh capek."),
        ("Arga", "Aku lebih suka menyebutnya menghargai waktu istirahat."),
        ("Lyra", "...Besok kita langsung kembali ke kerajaan?"),
        ("Elena", "Ya."),
        ("Lyra", "Tapikan kita sekarang berada sangat jauh dari kerajaan"),
        ("Lyra", "Butuh waktu 2 minggu agar bisa sampai ke sana."),
        ("Lyra", "Bahkan bisa lebih karna sekarang pasukan raja iblis sudah mulai bergerak"),
        ("Elena", "Tapi Kita harus melaporkan apa yang terjadi di desa ini secepat mungkin."),
        ("Darius", "Kalau laporan itu membuat mereka akhirnya bergerak, mungkin pengorbanan desa itu tidak sia-sia."),
        ("Reno", "Kedengarannya aku tidak akan pernah terbiasa mendengar caramu bicara."),
        ("Darius", "Lalu jangan biasakan."),
        ("Reno", "Nah, itu lebih parah."),
        ("Arga", "Menurutmu Raja akan mempercayai laporan kita?"),
        ("Elena", "Seharusnya."),
        ("Elena", "Kita punya saksi, bukti, dan sekarang juga punya seseorang yang melihat semuanya secara langsung."),
        ("Darius", "...Aku akan mengatakan apa yang kulihat."),
        ("Darius", "Tidak lebih dan tidak kurang."),
        ("Lyra", "Semoga saja para bangsawan itu benar-benar mendengarkan."),
        ("Lyra", "Terlalu banyak orang mati karena mereka terlambat bertindak."),
        ("Elena", "..."),
        ("Arga", "Kalau mereka tidak mendengarkan, kita cari cara lain."),
        ("Reno", "Nah, itu baru semangat."),
        ("Reno", "Tapi semoga saja kita tidak perlu menerobos istana atau semacamnya."),
        ("Lyra", "Aneh sekali. Untuk pertama kalinya aku setuju denganmu."),
        ("Reno", "Aku akan menganggap itu pujian."),
        ("Darius", "..."),
        ("Darius", "Kalian tahu."),
        ("Darius", "Beberapa jam lalu aku mengira akan menghabiskan sisa hidupku sendirian di desa itu."),
        ("Darius", "Sekarang aku malah duduk di sekitar api unggun bersama orang-orang yang bahkan belum kukenal seminggu."),
        ("Arga", "Menyesal sudah ikut?"),
        ("Darius", "...Belum."),
        ("Reno", "Wah, kemajuan besar."),
        ("Elena", "hahaha."),
        ("Arga", "Terima kasih sudah mempercayai kami, Darius."),
        ("Darius", "Aku tidak mempercayai kalian."),
        ("Reno", "Tuh kan."),
        ("Darius", "...Belum sepenuhnya."),
        ("Darius", "Tapi aku percaya pada keputusan yang kuambil."),
        ("Lyra", "Hmph."),
        ("Lyra", "Kurasa itu sudah cukup."),
        ("Elena", "Besok perjalanan masih panjang."),
        ("Arga", "Ya."),
        ("Arga", "Kita kembali ke kerajaan, menyampaikan semua yang kita tahu, lalu lihat ke mana jalan membawa kita setelah itu."),
        ("Reno", "Dan sekarang, semuanya tidur."),
        ("Lyra", "Akhirnya ada satu ide bagus darimu hari ini."),
        ("Reno", "Aku akan menganggap itu pujian juga."),
        ("SYSTEM", "★ Party beristirahat sebelum melanjutkan perjalanan kembali ke Kerajaan.")

    ]

    MONTAGE_TEXT = [
        "Sebulan telah berlalu sejak mereka meninggalkan Desa Karavel...",
        "Jalan yang mereka tempuh untuk kembali ke kerajaan tidak mudah.",
        "Monster dan iblis ada dimana-mana.",
        "Namun tak satu pun mampu menghentikan langkah mereka.",
        "Di sepanjang perjalanan, mereka tertawa bersama...",
        "Berjuang bersama...",
        "Dan tumbuh menjadi sahabat yang dapat saling mempercayai.",
        "Kini, tujuan akhir itu akhirnya terlihat.",
        "Kastil Raja Iblis berdiri megah di kejauhan.",
        "Pertarungan yang menentukan nasib dunia sudah menanti.",
        "Dan untuk pertama kalinya...",
        "Mereka tidak melangkah demi sebuah ramalan.",
        "Mereka melangkah demi orang-orang yang mereka sayangi."
    ]

    def __init__(self, game):
        super().__init__(game)
        self._t = 0.0
                                                                        
                                                                                
        self._sub_phase = "forest"
        self._prev_phase = ""
        self._dlg_step = 0
        self._dialogue = DialogueBox(game.W, game.H)
        self._transition = TransitionScreen(game.W, game.H)
        self._narrator = NarratorBox(game.W, game.H)
        self._floats: list[FloatingText] = []
        self._party_hud = PartyHUD()

                                                                         
        self._ground_y_forest   = int(game.H * 0.82)
        self._ground_y_village  = int(game.H * 0.82)
        self._ground_y_campfire = int(game.H * 0.82)
        self._ground_y_ruins    = int(game.H * 0.82)
        ground_y = self._ground_y_forest                 
        self._ground_y = ground_y

        self._player = Player(-80, ground_y - 55)
        self._player.before_isekai = False                           
        self._elena  = PartyNPC("Elena",  -140, ground_y - 55)
        self._reno   = PartyNPC("Reno",    700, ground_y - 55)
        self._lyra   = PartyNPC("Lyra",    700, ground_y - 55)
        self._darius = PartyNPC("Darius",  700, ground_y - 55)
        self._reno_joined   = False
        self._lyra_joined   = False
        self._darius_joined = False
        self._party_display = ["Arga", "Elena"]

                                         
        self._enemies: list[MonsterNPC] = []
        self._enemy_walkin_active = False
        self._enemy_walkin_done   = False
        self._enemies_interactable = False
        self._warning_dlg_step = 0
        self._warning_phase = ""                               

        self._battle_anim  = 0.0
        self._slash_active = False
        self._slash_timer  = 0.0
        self._shake_timer  = 0.0
        self._shake_x      = 0

        self._montage_step  = 0
        self._montage_timer = 0.0

        self._fire_particles: list[dict] = []

        self._pending_phase = ""
        self._waiting_fade  = False

        try:
            self._font_ui  = pygame.font.SysFont("Consolas", 15)
            self._font_ch  = pygame.font.SysFont("Georgia", 34, bold=True)
            self._font_mon = pygame.font.SysFont("Georgia", 20, italic=True)
        except Exception:
            self._font_ui  = pygame.font.Font(None, 18)
            self._font_ch  = pygame.font.Font(None, 38)
            self._font_mon = pygame.font.Font(None, 22)

    def on_enter(self) -> None:
        flags = self._game.flags
        W = self._game.W

                                                                               
                                                                                 
                                                                                 

        if flags.pop("battle_won_forest", False):
                                                                        
            self._sub_phase = "forest_post"
            self._apply_ground_y("forest"); self._set_phase_scale("forest")
            self._transition.fade_in(speed=200)
            self._player._x          = int(W * 0.30)
            self._player._facing_right = True
            self._elena._x           = int(W * 0.20)
            self._elena._facing_right = True
            self._reno._x            = int(W * 0.60)
            self._reno._facing_right  = False
            self._reno._hurt_pose    = False
                                                                                    
            self._elena.follow(self._player);  self._elena.follow_distance  = -80
            self._reno.follow(self._player);   self._reno.follow_distance   =  80
            self._lyra.follow(self._player);   self._lyra.follow_distance   = -160
            self._darius.follow(self._player); self._darius.follow_distance =  160
            for ch in (self._elena, self._reno, self._lyra, self._darius):
                ch.disable_follow()
            self._dialogue.show(self.RENO_POST_BATTLE[0][1], self.RENO_POST_BATTLE[0][0])
            self._game.assets.play_bgm("reno_theme", loop=-1, volume=0.7)
            return

        if flags.pop("battle_won_ruins", False):
                                                                     
            self._sub_phase = "ruins_post"
            self._reno_joined = True
            self._party_display.append("Reno")
            self._apply_ground_y("ruins"); self._set_phase_scale("ruins")
            self._transition.fade_in(speed=200)
            self._player._x           = int(W * 0.22)
            self._player._facing_right = True
            self._elena._x            = int(W * 0.14)
            self._elena._facing_right  = True
            self._reno._x             = int(W * 0.31)
            self._reno._facing_right   = True
            self._lyra._x             = int(W * 0.55)
            self._lyra._facing_right   = False
                                                                                    
            self._elena.follow(self._player);  self._elena.follow_distance  = -80
            self._reno.follow(self._player);   self._reno.follow_distance   =  80
            self._lyra.follow(self._player);   self._lyra.follow_distance   = -160
            self._darius.follow(self._player); self._darius.follow_distance =  160
            for ch in (self._elena, self._reno, self._lyra, self._darius):
                ch.disable_follow()
            self._dialogue.show(self.LYRA_POST_BATTLE[0][1], self.LYRA_POST_BATTLE[0][0])
            self._game.assets.play_bgm("lyra_theme", loop=-1, volume=0.7)
            return

        if flags.pop("battle_won_village", False):
                                                                 
            self._sub_phase = "village_post"
            self._reno_joined  = True
            self._lyra_joined  = True
            self._party_display.append("Reno")
            self._party_display.append("Lyra")
            self._apply_ground_y("village"); self._set_phase_scale("village")
            self._transition.fade_in(speed=200)
            self._player._x            = int(W * 0.22)
            self._player._facing_right  = True
            self._elena._x             = int(W * 0.13)
            self._elena._facing_right   = True
            self._reno._x              = int(W * 0.31)
            self._reno._facing_right    = True
            self._lyra._x              = int(W * 0.40)
            self._lyra._facing_right    = True
            self._darius._x            = int(W * 0.60)
            self._darius._facing_right  = False
            self._darius._hurt_pose    = False
                                                                                    
            self._elena.follow(self._player);  self._elena.follow_distance  = -80
            self._reno.follow(self._player);   self._reno.follow_distance   =  80
            self._lyra.follow(self._player);   self._lyra.follow_distance   = -160
            self._darius.follow(self._player); self._darius.follow_distance =  160
            for ch in (self._elena, self._reno, self._lyra, self._darius):
                ch.disable_follow()
            self._dialogue.show(self.DARIUS_POST_BATTLE[0][1], self.DARIUS_POST_BATTLE[0][0])
                                                                             
            self._game.assets.play_bgm("darius_theme", loop=-1, volume=0.6)
            try:
                self._game.assets.play_sfx_file("api_theme", volume=0.5)
            except Exception:
                pass
            return
        self._transition.fade_in(speed=160)
        self._game.assets.play_bgm("reno_theme", loop=-1, volume=0.7)
        self._narrator.show(["Chapter 3 — Teman Baru", "Hutan Verdan"], 3.0)
        self._dialogue.show(self.RENO_DLGS[0][1], self.RENO_DLGS[0][0])
                                                                       
        self._reno._hurt_pose   = True
        self._reno._facing_right = False                                              
        self._reno._x           = self._game.W * 0.62                          
                                              
        self._elena.follow(self._player);  self._elena.follow_distance  = -80
        self._reno.follow(self._player);   self._reno.follow_distance   =  80
        self._lyra.follow(self._player);   self._lyra.follow_distance   = -160
        self._darius.follow(self._player); self._darius.follow_distance =  160
                                                               
        for ch in (self._elena, self._reno, self._lyra, self._darius):
            ch.disable_follow()
        self.start_walkin([
            (self._player, 200),
            (self._elena,  280),
        ])

    def _apply_ground_y(self, phase_base: str):
        gy_map = {
            "forest":   self._ground_y_forest,
            "ruins":    self._ground_y_ruins,
            "village":  self._ground_y_village,
            "campfire": self._ground_y_campfire,
        }
        new_gy = gy_map.get(phase_base, self._ground_y_forest)
        self._ground_y = new_gy
        for ch in (self._player, self._elena, self._reno, self._lyra, self._darius):
            ch._y = new_gy - 55
        for enemy in self._enemies:
            enemy._y = new_gy - 35

    def _set_phase_scale(self, phase_base: str):
        self.set_char_scale(
            self._player, self._elena,
            self._reno, self._lyra, self._darius,
            scale=1.6
        )

    def _go_to_phase(self, new_phase: str):
        self._pending_phase = new_phase
        self._waiting_fade = True
        self._transition.fade_out(speed=280)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            key = event.key
            if self._walkin_active or self._waiting_fade or self._enemy_walkin_active:
                return
            if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                                                                           
                if self._sub_phase.endswith("_encounter"):
                    pass
                else:
                    self._advance()
            elif key == pygame.K_e:
                if self._sub_phase.endswith("_encounter"):
                    self._try_start_battle()

    def _advance(self):
        self._game.assets.play("cursor")
        try: self._game.assets.play_sfx_file("space_enter_sfx")
        except Exception: pass
        if not self._dialogue.is_finished:
            self._dialogue.skip()
            return

        if self._sub_phase == "forest":
            self._dlg_step += 1
            if self._dlg_step < len(self.RENO_DLGS):
                spk, txt = self.RENO_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == 4:
                    self._game.assets.play("damage")
            else:
                self._start_enemy_warning("forest")

        elif self._sub_phase == "forest_warning":
            self._advance_warning()

        elif self._sub_phase == "forest_post":
                                                                  
            self._reno._hurt_pose = False

            self._dlg_step += 1
            if self._dlg_step < len(self.RENO_POST_BATTLE):
                spk, txt = self.RENO_POST_BATTLE[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == len(self.RENO_POST_BATTLE) - 1:
                    self._reno_joined = True
                    self._party_display.append("Reno")
                    self._game.party.append("Reno")
                    self._game.assets.play("fanfare")
                    self._reno.enable_follow()
            else:
                self._go_to_phase("ruins")

        elif self._sub_phase == "ruins":
            self._dlg_step += 1
            if self._dlg_step < len(self.LYRA_DLGS):
                spk, txt = self.LYRA_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == 4:
                    self._game.assets.play("damage")
                    self._shake_timer = 0.4
                    self._floats.append(FloatingText("BOOM!", self._game.W//2, 200, DAMAGE_RED))
            else:
                self._start_enemy_warning("ruins")

        elif self._sub_phase == "ruins_warning":
            self._advance_warning()

        elif self._sub_phase == "ruins_post":
            self._dlg_step += 1
            if self._dlg_step < len(self.LYRA_POST_BATTLE):
                spk, txt = self.LYRA_POST_BATTLE[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == len(self.LYRA_POST_BATTLE) - 1:
                    self._lyra_joined = True
                    self._party_display.append("Lyra")
                    self._game.party.append("Lyra")
                    self._game.assets.play("fanfare")
                    self._lyra.enable_follow()
            else:
                self._go_to_phase("village")

        elif self._sub_phase == "village":
            self._dlg_step += 1
            if self._dlg_step < len(self.DARIUS_DLGS):
                spk, txt = self.DARIUS_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
            else:
                self._start_enemy_warning("village")

        elif self._sub_phase == "village_warning":
            self._advance_warning()

        elif self._sub_phase == "village_post":
            self._dlg_step += 1
            if self._dlg_step < len(self.DARIUS_POST_BATTLE):
                spk, txt = self.DARIUS_POST_BATTLE[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == len(self.DARIUS_POST_BATTLE) - 1:
                    self._darius_joined = True
                    self._party_display.append("Darius")
                    self._game.party.append("Darius")
                    self._game.assets.play("fanfare")
                    self._darius.enable_follow()
            else:
                self._go_to_phase("campfire")

        elif self._sub_phase == "campfire":
            self._dlg_step += 1
            if self._dlg_step < len(self.CAMPFIRE_DLGS):
                spk, txt = self.CAMPFIRE_DLGS[self._dlg_step]
                self._dialogue.show(txt, spk)
                if self._dlg_step == 18:
                    self._game.flags["arga_chose_friends"] = True
                    self._elena.emotion = "happy"
                elif self._dlg_step == 27:
                    self._game.assets.play("fanfare")
            else:
                self._dlg_step = 0
                self._go_to_phase("montage")

        elif self._sub_phase == "montage":
            self._montage_step += 1
            if self._montage_step >= len(self.MONTAGE_TEXT):
                self._go_to_phase("goto_ch3")

                                                                                 

    def _start_enemy_warning(self, phase_name: str):
        self._sub_phase = f"{phase_name}_warning"
        self._warning_phase = phase_name
        self._warning_dlg_step = 0
        dlgs = self.ENEMY_WARNING[phase_name]
        spk, txt = dlgs[0]
        self._dialogue.show(txt, spk)
        self._game.assets.play("damage")

    def _advance_warning(self):
        if not self._dialogue.is_finished:
            self._dialogue.skip()
            return
        self._game.assets.play("cursor")
        dlgs = self.ENEMY_WARNING[self._warning_phase]
        self._warning_dlg_step += 1
        if self._warning_dlg_step < len(dlgs):
            spk, txt = dlgs[self._warning_dlg_step]
            self._dialogue.show(txt, spk)
        else:
                                                              
            self._dialogue.hide()
            self._spawn_enemies_walkin(self._warning_phase)

    def _spawn_enemies_walkin(self, phase_name: str):
        self._enemies.clear()
        self._enemy_walkin_active = True
        self._enemy_walkin_done   = False
        self._enemies_interactable = False
        screen_w = self._game.W
        ground_y = self._ground_y

        if phase_name == "forest":
                                       
            configs = [
                ("Goblin", screen_w + 60,  screen_w - 160, 100),
                ("Goblin", screen_w + 140, screen_w - 260, 100),
            ]
        elif phase_name == "ruins":
                                                                   
            configs = [
                ("Minotaur", screen_w + 60,  screen_w - 140, 180),
                ("Minotaur", screen_w + 140, screen_w - 240, 180),
                ("Minotaur", screen_w + 220, screen_w - 340, 180),
            ]
        elif phase_name == "village":
                                                                                
            configs = [
                ("Goblin",   screen_w + 60,  screen_w - 130, 80),
                ("Goblin",   screen_w + 130, screen_w - 210, 80),
                ("Goblin",   screen_w + 200, screen_w - 290, 80),
                ("Minotaur", screen_w + 290, screen_w - 400, 160),
            ]
        else:
            configs = []

        for name, start_x, target_x, hp in configs:
            m = MonsterNPC(name, float(start_x), ground_y - 35, hp=hp)
            m._target_x = float(target_x)
            self._enemies.append(m)

        self._sub_phase = f"{phase_name}_encounter"
        self._narrator.show(["Musuh datang!", "Dekati dan tekan  E  untuk bertarung!"], 2.5)

                                                
        if phase_name == "ruins":
            self._game.assets.play_bgm("encounter_ruins", loop=-1, volume=0.8)
        elif phase_name == "village":
            self._game.assets.play_bgm("encounter_lorong", loop=-1, volume=0.8)

    def _try_start_battle(self):
        if not self._enemies_interactable or not self._enemies:
            return
        px = self._player._x
        for enemy in self._enemies:
            if abs(enemy.x - px) < 120:
                try: self._game.assets.play_sfx_file("interact_boss_sfx")
                except Exception: pass
                self._enter_battle()
                return
        self._narrator.show(["Dekati musuh terlebih dahulu!"], 1.0)

    def _enter_battle(self):
        phase_map = {
            "forest_encounter":  ("ENCOUNTER_FOREST_MONSTERS",  "forest"),
            "ruins_encounter":   ("ENCOUNTER_RUINS_TRAP",        "ruins"),
            "village_encounter": ("ENCOUNTER_VILLAGE_MONSTERS",  "village"),
        }
        enc_const, enc_id = phase_map.get(self._sub_phase, ("ENCOUNTER_FOREST_MONSTERS", "?"))

                                       
        bgm_battle_map = {
            "ruins":    "encounter_ruins",
            "village":  "encounter_lorong",
        }
        bgm_battle = bgm_battle_map.get(enc_id, "normal_battle_theme")

        try:
            from battle.battle_scene import start_battle_scene
            import battle.battle_scene as bs
            enemies = getattr(bs, enc_const)
            start_battle_scene(
                game=self._game,
                enemies=enemies,
                return_scene_class=Chapter3Scene,
                context={
                    "chapter": 3,
                    "sub_phase": self._sub_phase,
                    "encounter_id": enc_id,
                    "bgm_battle": bgm_battle,
                },
            )
        except NotImplementedError:
                                                                            
            self._narrator.show(
                ["[BATTLE SCENE BELUM ADA]", "Anggap menang — lanjut cerita..."], 2.5
            )
            self._enemies.clear()
            self._enemies_interactable = False
                                                                 
            next_map = {
                "forest_encounter":  "forest_post",
                "ruins_encounter":   "ruins_post",
                "village_encounter": "village_post",
            }
            next_phase = next_map.get(self._sub_phase, "campfire")
            self._go_to_phase(next_phase)

                                                                                

    def update(self, dt: float) -> None:
        self._t += dt
        self._battle_anim += dt
        self._transition.update(dt)
        self._dialogue.update(dt)
        self._narrator.update(dt)
        self.update_walkin(dt)

                                                
        if self._walkin_active:
            self._player.set_walking(True, True)

                                  
        if self._enemy_walkin_active:
            all_arrived = True
            for enemy in self._enemies:
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
            if all_arrived and not self._enemy_walkin_done:
                self._enemy_walkin_done    = True
                self._enemy_walkin_active  = False
                self._enemies_interactable = True

                                                                
        if self._waiting_fade and self._transition.done:
            self._waiting_fade = False
            self._sub_phase = self._pending_phase
            self._pending_phase = ""
            self._dlg_step = 0
            self._slash_active = False
            self._enemies.clear()
            self._enemies_interactable = False

                                                                    
            def _disable_all_follow():
                for ch in (self._elena, self._reno, self._lyra, self._darius):
                    ch.disable_follow()

            if self._sub_phase == "forest_post":
                self._apply_ground_y("forest")
                self._set_phase_scale("forest")
                self._transition.fade_in(speed=200)
                self._game.assets.play_bgm("reno_theme", loop=-1, volume=0.7)
                                                                        
                W = self._game.W
                self._player._x          = int(W * 0.30)
                self._player._facing_right = True
                self._elena._x           = int(W * 0.20)
                self._elena._facing_right = True
                self._reno._x            = int(W * 0.60)
                self._reno._facing_right  = False
                self._reno._hurt_pose    = False                         
                                                                   
                for ch in (self._elena, self._reno):
                    ch.disable_follow()
                self._dialogue.show(self.RENO_POST_BATTLE[0][1], self.RENO_POST_BATTLE[0][0])

            elif self._sub_phase == "ruins":
                self._apply_ground_y("ruins")
                self._set_phase_scale("ruins")
                self._transition.fade_in(speed=200)
                self._game.assets.play_bgm("lyra_theme", loop=-1, volume=0.7)
                self._narrator.show(["Reruntuhan Sihir — Lyra"], 2.5)
                self._dialogue.show(self.LYRA_DLGS[0][1], self.LYRA_DLGS[0][0])
                _disable_all_follow()
                                                                             
                W = self._game.W
                self._lyra._x            = int(W * 0.68)
                self._lyra._facing_right  = False                                  
                self._lyra.disable_follow()
                                                           
                self.start_walkin([
                    (self._player, 200),
                    (self._elena,  280),
                    (self._reno,   360),
                ])

            elif self._sub_phase == "ruins_post":
                self._apply_ground_y("ruins")
                self._set_phase_scale("ruins")
                self._transition.fade_in(speed=200)
                self._game.assets.play_bgm("lyra_theme", loop=-1, volume=0.7)
                                                                       
                W = self._game.W
                self._player._x           = int(W * 0.22)
                self._player._facing_right = True
                self._elena._x            = int(W * 0.14)
                self._elena._facing_right  = True
                self._reno._x             = int(W * 0.31)
                self._reno._facing_right   = True
                self._lyra._x             = int(W * 0.55)
                self._lyra._facing_right   = False                                  
                for ch in (self._elena, self._reno, self._lyra):
                    ch.disable_follow()
                self._dialogue.show(self.LYRA_POST_BATTLE[0][1], self.LYRA_POST_BATTLE[0][0])

            elif self._sub_phase == "village":
                self._apply_ground_y("village")
                self._set_phase_scale("village")
                self._transition.fade_in(speed=200)
                self._game.assets.play_bgm("darius_theme", loop=-1, volume=0.6)
                self._game.assets.play_sfx_file("api_theme", volume=0.5)
                self._narrator.show(["Desa Terbakar — Darius"], 2.5)
                self._dialogue.show(self.DARIUS_DLGS[0][1], self.DARIUS_DLGS[0][0])
                _disable_all_follow()
                                                                                          
                W = self._game.W
                self._darius._x            = int(W * 0.68)
                self._darius._facing_right  = False
                self._darius._hurt_pose    = True
                self._darius.disable_follow()
                                              
                self.start_walkin([
                    (self._player, 200),
                    (self._elena,  280),
                    (self._reno,   360),
                    (self._lyra,   440),
                ])

            elif self._sub_phase == "village_post":
                self._apply_ground_y("village")
                self._set_phase_scale("village")
                self._transition.fade_in(speed=200)
                                                                                            
                self._game.assets.play_bgm("darius_theme", loop=-1, volume=0.6)
                try:
                    self._game.assets.play_sfx_file("api_theme", volume=0.5)
                except Exception:
                    pass
                                                                                
                W = self._game.W
                self._player._x            = int(W * 0.22)
                self._player._facing_right  = True
                self._elena._x             = int(W * 0.13)
                self._elena._facing_right   = True
                self._reno._x              = int(W * 0.31)
                self._reno._facing_right    = True
                self._lyra._x              = int(W * 0.40)
                self._lyra._facing_right    = True
                self._darius._x            = int(W * 0.60)
                self._darius._facing_right  = False
                self._darius._hurt_pose    = False                         
                for ch in (self._elena, self._reno, self._lyra, self._darius):
                    ch.disable_follow()
                self._dialogue.show(self.DARIUS_POST_BATTLE[0][1], self.DARIUS_POST_BATTLE[0][0])

            elif self._sub_phase == "campfire":
                self._apply_ground_y("campfire")
                self._set_phase_scale("campfire")
                self._transition.fade_in(speed=180)
                self._game.assets.play_bgm("campfire_theme", loop=-1, volume=0.7)
                self._narrator.show(["Malam Sebelum Perang", "Api Unggun Party"], 3.0)
                self._dialogue.show(self.CAMPFIRE_DLGS[0][1], self.CAMPFIRE_DLGS[0][0])

                _disable_all_follow()

                self._lyra._y   = self._ground_y - 30
                self._elena._y  = self._ground_y - 60

                self._player._y = self._ground_y

                self._reno._y   = self._ground_y - 60
                self._darius._y = self._ground_y - 30

                cx = self._game.W // 2

                self.start_walkin([
                        (self._lyra,   cx - 180),
                        (self._elena,  cx - 80),
                        (self._player, cx),
                        (self._reno,   cx + 80),
                        (self._darius, cx + 180),
                    ])
                
            elif self._sub_phase == "montage":
                self._transition.fade_in(speed=150)
                self._montage_step = 0
                self._montage_timer = 0.0
            elif self._sub_phase == "goto_ch3":
                from scenes.chapter_final_scene import ChapterFinalScene
                self._game.replace_scene(ChapterFinalScene(self._game))
                return

                         
        if self._sub_phase not in ("montage", "goto_ch3"):
            self._player.update(dt)
            self._elena.update(dt)
            if self._reno_joined or self._sub_phase in ("ruins", "ruins_warning", "ruins_encounter",
                                                         "forest_post", "ruins_post",
                                                         "village", "village_warning", "village_encounter",
                                                         "village_post", "campfire"):
                self._reno.update(dt)
            if self._lyra_joined or self._sub_phase in ("ruins", "ruins_warning", "ruins_encounter",
                                                          "ruins_post", "village", "village_warning",
                                                          "village_encounter", "village_post", "campfire"):
                self._lyra.update(dt)
            if self._darius_joined or self._sub_phase in ("village", "village_warning", "village_encounter",
                                                            "village_post", "campfire"):
                self._darius.update(dt)

                                                                            
                                                                                           
        _follow_ok = {"forest_encounter", "ruins_encounter", "village_encounter"}
        if not self._walkin_active and self._sub_phase in _follow_ok:
            if not self._elena._follow_enabled:
                self._elena.enable_follow()
            if self._reno_joined and not self._reno._follow_enabled:
                self._reno.enable_follow()
            if self._lyra_joined and not self._lyra._follow_enabled:
                self._lyra.enable_follow()
            if self._darius_joined and not self._darius._follow_enabled:
                self._darius.enable_follow()

                        
        for enemy in self._enemies:
            enemy.update(dt)

                                                                        
        if self._walkin_active:
            pass                                    
        elif self._sub_phase.endswith("_encounter") and not self._enemy_walkin_active:
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
                                                                           

                                 
            if moving_left and not moving_right:
                self._player.set_walking(True, False)
            elif moving_right and not moving_left:
                self._player.set_walking(True, True)
            else:
                self._player.set_walking(False)
        elif not self._walkin_active:
            self._player.set_walking(False)

        if self._slash_active:
            self._slash_timer += dt
            if self._slash_timer > 0.6:
                self._slash_active = False

        if self._shake_timer > 0:
            self._shake_timer -= dt
            self._shake_x = random.randint(-5, 5) if self._shake_timer > 0 else 0
        else:
            self._shake_x = 0

        for ft in self._floats:
            ft.update(dt)
        self._floats = [f for f in self._floats if f.alive]

        if self._sub_phase == "montage":
            self._montage_timer += dt
            if self._montage_timer > 2.8 and self._transition.done:
                self._montage_timer = 0.0
                self._montage_step = min(self._montage_step + 1, len(self.MONTAGE_TEXT) - 1)

        if self._sub_phase == "village" or self._sub_phase.startswith("village"):
            self._spawn_fire(dt)
            for p in self._fire_particles:
                p['y'] -= p['speed'] * dt
                p['x'] += p['vx'] * dt
                p['life'] -= dt
            self._fire_particles = [p for p in self._fire_particles if p['life'] > 0]

    def _spawn_fire(self, dt):
        for _ in range(int(8 * dt * 60)):
            W = self._game.W; ox = random.choice([int(W*0.094), int(W*0.219), int(W*0.484), int(W*0.625)])
            self._fire_particles.append({
                'x': ox + random.randint(-20, 20),
                'y': self._ground_y,
                'vx': random.uniform(-20, 20),
                'speed': random.uniform(60, 120),
                'life': random.uniform(0.5, 1.5),
                'max_life': 1.5,
                'r': random.randint(4, 10),
                'col': random.choice([(255,100,20), (255,180,20), (255,60,0)]),
            })

                                                                                
    _PHASE_SCALE = {
        "forest":   1.6,
        "ruins":    1.6,
        "village":  1.6,
        "campfire": 1.6,
    }

    def _draw_char_scaled(self, surface, char, scale=1.6):
        self.draw_char_scaled(surface, char, scale)

                                                                               

    def draw(self, surface: pygame.Surface) -> None:
        sx = self._shake_x

                                                   
        phase_base = self._sub_phase.replace("_warning", "").replace("_encounter", "").replace("_post", "")
        _sc = self._PHASE_SCALE.get(phase_base, 1.6)

        if phase_base in ("forest", "ruins", "village", "campfire"):
            bg_map = {
                "forest":   self._game.assets.bg_forest,
                "ruins":    self._game.assets.bg_ruins,
                "village":  self._game.assets.bg_village,
                "campfire": self._game.assets.bg_campfire,
            }
            bg = bg_map.get(phase_base, self._game.assets.bg_forest)
            surface.blit(bg, (sx, 0))
        elif self._sub_phase == "montage":
            self._draw_montage(surface)
        else:
            surface.blit(self._game.assets.bg_forest, (0, 0))

                      
        if phase_base == "village":
            for p in self._fire_particles:
                life_r = p['life'] / p['max_life']
                alpha = int(200 * life_r)
                sz = max(1, int(p['r'] * life_r))
                fs = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
                pygame.draw.circle(fs, (*p['col'], alpha), (sz, sz), sz)
                surface.blit(fs, (int(p['x']) - sz, int(p['y']) - sz))

                                                    
        if self._sub_phase not in ("montage", "goto_ch3"):
            self._draw_char_scaled(surface, self._player, _sc)
            self._draw_char_scaled(surface, self._elena,  _sc)

            if phase_base in ("forest",):
                self._draw_char_scaled(surface, self._reno, _sc)
            elif phase_base in ("ruins",):
                self._draw_char_scaled(surface, self._reno, _sc)
                self._draw_char_scaled(surface, self._lyra, _sc)
            elif phase_base in ("village",):
                self._draw_char_scaled(surface, self._reno,   _sc)
                self._draw_char_scaled(surface, self._lyra,   _sc)
                self._draw_char_scaled(surface, self._darius, _sc)
            elif phase_base == "campfire":
                self._draw_char_scaled(surface, self._reno,   _sc)
                self._draw_char_scaled(surface, self._lyra,   _sc)
                self._draw_char_scaled(surface, self._darius, _sc)
                self._draw_campfire(surface)

                        
        for enemy in self._enemies:
            self._draw_char_scaled(surface, enemy, 1.7)
                                 
            if self._enemies_interactable:
                px = self._player._x
                if abs(enemy.x - px) < 120:
                    self._draw_interact_hint(surface, int(enemy.x), int(enemy.y) - int(80 * 1.7))

        for ft in self._floats:
            ft.draw(surface)

        self._narrator.draw(surface)
        self._dialogue.draw(surface)
        members = [("Arga", self._player.hp, self._player.max_hp),
                  ("Elena", self._elena.hp, self._elena.max_hp)]
        if "Reno"   in self._party_display: members.append(("Reno",   self._reno.hp,   self._reno.max_hp))
        if "Lyra"   in self._party_display: members.append(("Lyra",   self._lyra.hp,   self._lyra.max_hp))
        if "Darius" in self._party_display: members.append(("Darius", self._darius.hp, self._darius.max_hp))
        self._party_hud.draw(surface, members)
        
        self._transition.draw(surface)

                      
        lbl_map = {
            "forest":   "Hutan Verdan",
            "ruins":    "Reruntuhan Sihir Kuno",
            "village":  "Desa Karavel",
            "campfire": "Malam Hari",
            "montage":  "Dua Bulan Berlalu...",
        }
        lbl = lbl_map.get(phase_base, "")
        if lbl:
            try:
                t = self._font_ui.render(lbl, True, UI_ACCENT)
                surface.blit(t, (self._game.W // 2 - t.get_width() // 2, 8))
            except Exception:
                pass

                        
        if self._sub_phase.endswith("_encounter") and self._enemies_interactable:
            try:
                h = self._font_ui.render(
                    "← → Jalan  |  E Bertarung saat dekat musuh!", True, UI_ACCENT)
                surface.blit(h, (self._game.W // 2 - h.get_width() // 2, self._game.H - 30))
            except Exception:
                pass

    def _draw_interact_hint(self, surface, cx, cy):
        try:
            f = pygame.font.SysFont("Consolas", 13, bold=True)
            t = f.render("[E] Bertarung!", True, DAMAGE_RED)
            surface.blit(t, (cx - t.get_width() // 2, cy))
        except Exception:
            pass

    def _draw_campfire(self, surface):
        cx = self._game.W // 2
        cy = self._ground_y - 10
        t = self._t
        pygame.draw.line(surface, (80, 50, 30), (cx - 20, cy), (cx + 20, cy - 30), 5)
        pygame.draw.line(surface, (80, 50, 30), (cx + 20, cy), (cx - 20, cy - 30), 5)
                              
        glow = pygame.Surface((160, 160), pygame.SRCALPHA)
        alpha = int(40 + 20 * math.sin(t * 4))
        pygame.draw.circle(glow, (255, 160, 60, alpha), (80, 80), 80)
        surface.blit(glow, (cx - 80, cy - 90))

    def _draw_montage(self, surface):
        surface.fill((10, 8, 20))
        random.seed(42)
        for _ in range(100):
            sx = random.randint(0, self._game.W)
            sy = random.randint(0, self._game.H)
            a = int(128 + 127 * math.sin(self._t * 2 + sx))
            try:
                s = pygame.Surface((4, 4), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 255, 220, a), (2, 2), 2)
                surface.blit(s, (sx, sy))
            except Exception:
                pass
        pygame.draw.line(surface, (60, 40, 100), (80, self._game.H // 2 - 40),
                         (self._game.W - 80, self._game.H // 2 - 40), 1)
        pygame.draw.line(surface, (60, 40, 100), (80, self._game.H // 2 + 40),
                         (self._game.W - 80, self._game.H // 2 + 40), 1)
        if self._montage_step < len(self.MONTAGE_TEXT):
            txt = self.MONTAGE_TEXT[self._montage_step]
            try:
                fade_in_t = min(1.0, self._montage_timer / 0.8)
                alpha = int(255 * fade_in_t)
                rendered = self._font_ch.render(txt, True, GOLD_LIGHT)
                rendered.set_alpha(alpha)
                surface.blit(rendered, (self._game.W // 2 - rendered.get_width() // 2,
                                        self._game.H // 2 - rendered.get_height() // 2))
                hint = self._font_ui.render("[SPACE] Lanjut", True, UI_DIMTEXT)
                hint.set_alpha(alpha)
                surface.blit(hint, (self._game.W // 2 - hint.get_width() // 2,
                                    self._game.H // 2 + 60))
            except Exception:
                pass