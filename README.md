<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Summoned To Another World and Became A Hero — README</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Source+Code+Pro:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --gold:    #c9a84c;
    --gold2:   #e8c97a;
    --gold3:   #f5e199;
    --bg0:     #0a0812;
    --bg1:     #100e1c;
    --bg2:     #16122a;
    --bg3:     #1e1838;
    --bg4:     #251f46;
    --ink:     #e8dfc8;
    --ink2:    #b8a98a;
    --ink3:    #7a6d55;
    --purple:  #8b5cf6;
    --purple2: #c4b5fd;
    --blue:    #60a5fa;
    --teal:    #2dd4bf;
    --red:     #f87171;
    --rose:    #fda4af;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg0);
    color: var(--ink);
    font-family: 'Crimson Text', Georgia, serif;
    font-size: 18px;
    line-height: 1.75;
    max-width: 900px;
    margin: 0 auto;
    padding: 3rem 2rem 6rem;
  }

  /* ── ORNAMENTAL DIVIDER ── */
  .divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.5rem 0;
    color: var(--gold);
    font-size: 1.1rem;
    letter-spacing: 0.15em;
  }
  .divider::before, .divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold), transparent);
  }

  /* ── CORNER FRAME ── */
  .frame {
    position: relative;
    border: 1px solid var(--gold);
    border-radius: 4px;
    padding: 2.5rem 2rem;
    margin: 2rem 0;
    background: linear-gradient(135deg, rgba(201,168,76,0.04) 0%, transparent 50%);
  }
  .frame::before, .frame::after,
  .frame .corner-br, .frame .corner-bl {
    content: '';
    position: absolute;
    width: 16px;
    height: 16px;
    border-color: var(--gold2);
    border-style: solid;
  }
  .frame::before  { top: -1px;    left: -1px;   border-width: 2px 0 0 2px; }
  .frame::after   { top: -1px;    right: -1px;  border-width: 2px 2px 0 0; }
  .frame .corner-br { bottom: -1px; right: -1px;  border-width: 0 2px 2px 0; }
  .frame .corner-bl { bottom: -1px; left: -1px;   border-width: 0 0 2px 2px; }

  /* ── HERO HEADER ── */
  .hero {
    text-align: center;
    padding: 4rem 1rem 3rem;
    position: relative;
    overflow: hidden;
  }
  .hero-stars {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }
  .star {
    position: absolute;
    width: 2px;
    height: 2px;
    border-radius: 50%;
    background: var(--gold3);
    animation: twinkle var(--d, 3s) ease-in-out infinite var(--delay, 0s);
    opacity: 0.4;
  }
  @keyframes twinkle {
    0%, 100% { opacity: 0.1; transform: scale(0.8); }
    50%       { opacity: 0.8; transform: scale(1.4); }
  }

  .sword-deco {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .sword-line {
    width: 120px;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold));
  }
  .sword-line.right {
    background: linear-gradient(to left, transparent, var(--gold));
  }
  .sword-icon {
    font-size: 2rem;
    color: var(--gold);
    text-shadow: 0 0 20px rgba(201,168,76,0.6);
    animation: glow-pulse 2s ease-in-out infinite;
  }
  @keyframes glow-pulse {
    0%, 100% { text-shadow: 0 0 10px rgba(201,168,76,0.3); }
    50%       { text-shadow: 0 0 30px rgba(201,168,76,0.8), 0 0 60px rgba(201,168,76,0.3); }
  }

  .title-main {
    font-family: 'Cinzel', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: var(--gold2);
    letter-spacing: 0.06em;
    line-height: 1.2;
    text-shadow: 0 0 40px rgba(201,168,76,0.3);
    margin-bottom: 0.5rem;
  }
  .title-sub {
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    color: var(--ink3);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
  }
  .quote {
    font-style: italic;
    color: var(--ink2);
    font-size: 1rem;
    max-width: 560px;
    margin: 0 auto;
    border-left: 2px solid var(--gold);
    padding-left: 1rem;
    text-align: left;
  }
  .quote-attr {
    font-size: 0.85rem;
    color: var(--ink3);
    margin-top: 0.25rem;
    font-style: normal;
  }

  /* ── INFO TABLE ── */
  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1px;
    background: var(--gold);
    border: 1px solid var(--gold);
    border-radius: 4px;
    overflow: hidden;
    margin: 1.5rem 0;
  }
  .info-cell {
    background: var(--bg1);
    padding: 0.8rem 1rem;
  }
  .info-cell .label {
    font-family: 'Cinzel', serif;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.2rem;
  }
  .info-cell .value {
    color: var(--ink);
    font-size: 1rem;
  }

  /* ── SECTION HEADING ── */
  h2.section {
    font-family: 'Cinzel', serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--gold2);
    letter-spacing: 0.12em;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
  }
  h2.section .rune {
    width: 32px;
    height: 32px;
    background: var(--bg3);
    border: 1px solid var(--gold);
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
  }

  h3.sub {
    font-family: 'Cinzel', serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--purple2);
    letter-spacing: 0.1em;
    margin: 1.5rem 0 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  h3.sub::before {
    content: '';
    width: 6px;
    height: 6px;
    background: var(--purple);
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 0 8px var(--purple);
  }

  /* ── SYNOPSIS ── */
  .synopsis-text p {
    color: var(--ink2);
    margin-bottom: 0.9rem;
  }
  .synopsis-text p:first-child::first-letter {
    font-family: 'Cinzel', serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: var(--gold);
    float: left;
    line-height: 0.75;
    margin: 0.15em 0.1em 0 0;
    text-shadow: 0 0 20px rgba(201,168,76,0.4);
  }
  .emphasis {
    color: var(--gold3);
    font-weight: 600;
  }

  /* ── FEATURE CARDS ── */
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
  }
  .feature-card {
    background: var(--bg2);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 6px;
    padding: 1.2rem;
    transition: border-color 0.2s, background 0.2s;
  }
  .feature-card:hover {
    border-color: rgba(201,168,76,0.6);
    background: var(--bg3);
  }
  .feature-card .f-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }
  .feature-card .f-title {
    font-family: 'Cinzel', serif;
    font-size: 0.88rem;
    color: var(--gold2);
    letter-spacing: 0.1em;
    margin-bottom: 0.4rem;
  }
  .feature-card .f-desc {
    font-size: 0.9rem;
    color: var(--ink2);
    line-height: 1.55;
  }

  /* ── CHARACTER TABLE ── */
  .party-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 0.75rem;
    margin: 1rem 0;
  }
  .party-card {
    background: var(--bg3);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 6px;
    padding: 0.9rem;
    text-align: center;
  }
  .party-card .p-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: 1.5px solid var(--gold);
    margin: 0 auto 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    background: var(--bg4);
  }
  .party-card .p-name {
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    color: var(--gold3);
    letter-spacing: 0.08em;
  }
  .party-card .p-role {
    font-size: 0.78rem;
    color: var(--ink3);
    font-style: italic;
  }

  /* ── ENDING CARDS ── */
  .ending-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 1rem 0;
  }
  .ending-card {
    border-radius: 6px;
    padding: 1.2rem;
    border: 1px solid;
  }
  .ending-card.true {
    background: rgba(45,212,191,0.06);
    border-color: rgba(45,212,191,0.35);
  }
  .ending-card.bad {
    background: rgba(248,113,113,0.06);
    border-color: rgba(248,113,113,0.35);
  }
  .ending-card .e-label {
    font-family: 'Cinzel', serif;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
  }
  .ending-card.true .e-label { color: var(--teal); }
  .ending-card.bad  .e-label { color: var(--red); }
  .ending-card .e-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--ink);
    margin-bottom: 0.3rem;
  }
  .ending-card .e-desc {
    font-size: 0.88rem;
    color: var(--ink2);
    font-style: italic;
  }

  /* ── OOP SECTION ── */
  .oop-block {
    background: var(--bg2);
    border-left: 3px solid var(--purple);
    border-radius: 0 6px 6px 0;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
  }
  .oop-block .oop-title {
    font-family: 'Cinzel', serif;
    font-size: 0.9rem;
    color: var(--purple2);
    letter-spacing: 0.1em;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .oop-block .badge {
    background: rgba(139,92,246,0.2);
    color: var(--purple2);
    font-size: 0.65rem;
    font-family: 'Source Code Pro', monospace;
    padding: 2px 8px;
    border-radius: 99px;
    border: 1px solid rgba(139,92,246,0.4);
    letter-spacing: 0.05em;
  }
  .oop-block .oop-desc {
    color: var(--ink2);
    font-size: 0.95rem;
    margin-bottom: 0.6rem;
  }

  /* ── CODE BLOCK ── */
  pre {
    background: #0d0b18;
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: 6px;
    padding: 1rem 1.25rem;
    overflow-x: auto;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.82rem;
    line-height: 1.6;
    margin: 0.75rem 0;
  }
  .kw  { color: #c792ea; }
  .fn  { color: #82aaff; }
  .str { color: #c3e88d; }
  .cm  { color: #546e7a; }
  .nb  { color: var(--gold2); }
  .op  { color: #89ddff; }

  /* ── HIERARCHY TREE ── */
  .tree {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.83rem;
    color: var(--ink2);
    background: #0d0b18;
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: 6px;
    padding: 1rem 1.25rem;
    line-height: 1.8;
    margin: 0.75rem 0;
  }
  .tree .node-root  { color: var(--gold2); }
  .tree .node-class { color: var(--blue); }
  .tree .node-leaf  { color: var(--teal); }
  .tree .node-comment { color: var(--ink3); }

  /* ── CONTROLS TABLE ── */
  .controls-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.92rem;
    margin: 1rem 0;
  }
  .controls-table th {
    font-family: 'Cinzel', serif;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: var(--gold);
    text-align: left;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid rgba(201,168,76,0.3);
    text-transform: uppercase;
  }
  .controls-table td {
    padding: 0.55rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: var(--ink2);
  }
  .controls-table tr:last-child td { border-bottom: none; }
  .kbd {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.8rem;
    background: var(--bg4);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 4px;
    padding: 1px 8px;
    color: var(--gold3);
  }

  /* ── STRUCTURE TREE ── */
  .dir-tree {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.8rem;
    background: #0d0b18;
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    line-height: 2;
    color: var(--ink2);
  }
  .dir-folder { color: var(--gold2); }
  .dir-file   { color: var(--blue); }
  .dir-comment{ color: var(--ink3); }

  /* ── TECH PILLS ── */
  .tech-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.75rem 0;
  }
  .pill {
    background: var(--bg3);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 99px;
    padding: 3px 14px;
    font-size: 0.82rem;
    color: var(--gold3);
    font-family: 'Source Code Pro', monospace;
  }

  /* ── INSTALL BLOCK ── */
  .install-block {
    background: #0d0b18;
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 6px;
    overflow: hidden;
    margin: 1rem 0;
  }
  .install-block .ib-header {
    background: var(--bg3);
    padding: 0.4rem 1rem;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.72rem;
    color: var(--ink3);
    letter-spacing: 0.1em;
    border-bottom: 1px solid rgba(201,168,76,0.15);
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .install-block .ib-header::before {
    content: '';
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--red);
    box-shadow: 14px 0 0 #f59e0b, 28px 0 0 #4ade80;
  }
  .install-block code {
    display: block;
    padding: 1rem 1.25rem;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.85rem;
    color: var(--teal);
    line-height: 1.9;
  }
  .install-block code .prompt { color: var(--gold); }
  .install-block code .comment { color: var(--ink3); }

  /* ── FOOTER ── */
  .footer {
    text-align: center;
    padding-top: 3rem;
    color: var(--ink3);
    font-size: 0.85rem;
    font-style: italic;
  }
  .footer .footer-deco {
    font-family: 'Cinzel', serif;
    font-size: 1.2rem;
    color: var(--gold);
    margin-bottom: 0.5rem;
    letter-spacing: 0.3em;
  }
</style>
</head>
<body>

<!-- ══════════════ HERO ══════════════ -->
<div class="hero">
  <div class="hero-stars" id="stars-container"></div>

  <div class="sword-deco">
    <div class="sword-line"></div>
    <div class="sword-icon">⚔</div>
    <div class="sword-line right"></div>
  </div>

  <h1 class="title-main">Summoned To Another World<br>and Became A Hero</h1>
  <p class="title-sub">⸻ &nbsp;Visual Novel · RPG Turn-Based &nbsp;⸻</p>

  <blockquote class="quote">
    "Aku cuma pelajar biasa. Aku bahkan gak bisa masak nasi dengan benar."
    <p class="quote-attr">— Arga, saat pertama kali dipanggil ke dunia Astravia</p>
  </blockquote>
</div>

<div class="divider">✦ &nbsp;INFORMASI GAME&nbsp; ✦</div>

<!-- ══════════════ INFO ══════════════ -->
<div class="info-grid">
  <div class="info-cell"><p class="label">Judul</p><p class="value">Summoned To Another World and Became A Hero</p></div>
  <div class="info-cell"><p class="label">Tipe</p><p class="value">Visual Novel / RPG Turn-Based</p></div>
  <div class="info-cell"><p class="label">Genre</p><p class="value">Isekai Fantasy · Adventure · Story-Driven</p></div>
  <div class="info-cell"><p class="label">Engine</p><p class="value">Python + Pygame</p></div>
  <div class="info-cell"><p class="label">Resolusi</p><p class="value">1280 × 720</p></div>
  <div class="info-cell"><p class="label">Bahasa</p><p class="value">Indonesia</p></div>
</div>

<div class="divider">✦ &nbsp;SINOPSIS&nbsp; ✦</div>

<!-- ══════════════ SYNOPSIS ══════════════ -->
<div class="frame">
  <span class="corner-br"></span>
  <span class="corner-bl"></span>
  <div class="synopsis-text">
    <p>
      <span class="emphasis">Arga</span> — seorang pelajar biasa — sedang berjalan pulang di malam hujan ketika tiba-tiba tersedot ke dalam dunia lain bernama <span class="emphasis">Astravia</span>. Ia tiba di hadapan Raja Aldric beserta seluruh ksatria dan penyihir kerajaan, yang mengklaim telah memanggil seorang pahlawan melalui ritual kuno.
    </p>
    <p>
      Dunia Astravia berada di ambang kehancuran. <span class="emphasis">Raja Iblis (Demon King)</span> telah bergerak — kerajaan-kerajaan jatuh satu per satu, desa dibakar, ribuan nyawa hilang. Ramalan kuno berkata hanya pahlawan dari dunia lain yang bisa menghentikannya.
    </p>
    <p>
      Tanpa Arga minta, <span class="emphasis">Pedang Suci</span> terbang sendiri dan memilih dirinya. Dengan kekuatan yang ia tak pernah bayangkan, Arga harus memilih: melarikan diri dari takdir, atau menanggung beban sebagai satu-satunya harapan dunia ini.
    </p>
    <p>
      Bersama Elena, Lyra, Darius, dan Reno — party yang ia kumpulkan di tengah perjalanan — Arga melintasi kota Astravia, hutan berbahaya, reruntuhan kuno, hingga kastil Demon King itu sendiri.
      <strong style="color: var(--gold3); font-style: italic;">Setiap pilihanmu menentukan akhir cerita.</strong>
    </p>
  </div>
</div>

<div class="divider">✦ &nbsp;FITUR&nbsp; ✦</div>

<!-- ══════════════ FEATURES ══════════════ -->
<div class="feature-grid">
  <div class="feature-card">
    <div class="f-icon">📜</div>
    <div class="f-title">Narasi Visual Novel</div>
    <div class="f-desc">Dialog bergaya visual novel dengan typewriter effect, narrator box sinematik, dan latar yang berubah dinamis sesuai lokasi.</div>
  </div>
  <div class="feature-card">
    <div class="f-icon">🗺️</div>
    <div class="f-title">Sistem Chapter & Eksplorasi</div>
    <div class="f-desc">5+ chapter dari Opening, Kerajaan, Kota Astravia, Hutan, Reruntuhan, hingga Kastil Demon King — tiap chapter dengan multiple phase.</div>
  </div>
  <div class="feature-card">
    <div class="f-icon">⚔️</div>
    <div class="f-title">Battle Turn-Based</div>
    <div class="f-desc">Mode Normal vs. monster biasa dan mode Boss vs. Demon King. Pilih skill: Attack, Divine Slash, atau Celestial Flame.</div>
  </div>
  <div class="feature-card">
    <div class="f-icon">🧑‍🤝‍🧑</div>
    <div class="f-title">Sistem Party Dinamis</div>
    <div class="f-desc">Arga, Elena, Lyra, Darius, Reno — party NPC mengikuti hero dengan sistem catch-up otomatis dan Party HUD real-time.</div>
  </div>
  <div class="feature-card">
    <div class="f-icon">📊</div>
    <div class="f-title">Status Window RPG</div>
    <div class="f-desc">Window status ala RPG klasik: HP, MP, ATK, DEF, SPD, Level, EXP — terbuka di momen plot penting.</div>
  </div>
  <div class="feature-card">
    <div class="f-icon">🔀</div>
    <div class="f-title">Multiple Ending</div>
    <div class="f-desc">True End dan Bad End — pilihan kritis di tengah cerita langsung memengaruhi jalannya akhir game.</div>
  </div>
  <div class="feature-card">
    <div class="f-icon">🎭</div>
    <div class="f-title">Animasi Multi-Frame</div>
    <div class="f-desc">Dua set animasi Arga (sebelum/sesudah Pedang Suci). State: idle, walk, attack, hurt, dead, defend — dengan flip sprite otomatis.</div>
  </div>
  <div class="feature-card">
    <div class="f-icon">✨</div>
    <div class="f-title">Efek Visual</div>
    <div class="f-desc">Hujan dinamis, magic circle, transition fade, floating text (damage/EXP), efek api, dan bobbing animation karakter.</div>
  </div>
</div>

<!-- ── CHARACTERS ── -->
<h3 class="sub" style="margin-top:2rem;">Karakter Party</h3>
<div class="party-list">
  <div class="party-card">
    <div class="p-avatar">🗡️</div>
    <div class="p-name">Arga</div>
    <div class="p-role">Hero · Player Character</div>
  </div>
  <div class="party-card">
    <div class="p-avatar">✨</div>
    <div class="p-name">Elena</div>
    <div class="p-role">Heroine · Mage</div>
  </div>
  <div class="party-card">
    <div class="p-avatar">🏹</div>
    <div class="p-name">Lyra</div>
    <div class="p-role">Archer · Ranger</div>
  </div>
  <div class="party-card">
    <div class="p-avatar">🛡️</div>
    <div class="p-name">Darius</div>
    <div class="p-role">Knight · Tank</div>
  </div>
  <div class="party-card">
    <div class="p-avatar">🔥</div>
    <div class="p-name">Reno</div>
    <div class="p-role">Pejuang · Late Joiner</div>
  </div>
  <div class="party-card" style="border-color:rgba(248,113,113,0.35);">
    <div class="p-avatar" style="border-color:var(--red);">👿</div>
    <div class="p-name" style="color:var(--rose);">Demon King</div>
    <div class="p-role">Boss · Antagonist</div>
  </div>
</div>

<!-- ── ENDINGS ── -->
<h3 class="sub" style="margin-top:2rem;">Multiple Ending</h3>
<div class="ending-grid">
  <div class="ending-card true">
    <div class="e-label">✦ True End</div>
    <div class="e-title">Ending Terbaik</div>
    <div class="e-desc">Diraih melalui pilihan kritis yang tepat — dunia Astravia diselamatkan dan Arga menemukan jalannya.</div>
  </div>
  <div class="ending-card bad">
    <div class="e-label">✦ Bad End</div>
    <div class="e-title">Ending Gelap</div>
    <div class="e-desc">Pilihan yang salah membawa kehancuran — kota Astravia runtuh dan sang hero kalah melawan takdir.</div>
  </div>
</div>

<div class="divider">✦ &nbsp;KONSEP OOP&nbsp; ✦</div>

<!-- ══════════════ OOP ══════════════ -->

<!-- 1. Abstraction -->
<div class="oop-block">
  <div class="oop-title">
    <span>1. Abstraction</span>
    <span class="badge">engine/base.py</span>
  </div>
  <p class="oop-desc">
    Dua kelas abstrak menjadi fondasi seluruh sistem. <code style="color:var(--blue);font-family:'Source Code Pro',monospace;">Entity</code> dan <code style="color:var(--blue);font-family:'Source Code Pro',monospace;">Scene</code> mendefinisikan kontrak yang wajib diimplementasikan semua turunannya — tanpa bisa diinstansiasi langsung.
  </p>
  <pre><span class="kw">from</span> <span class="nb">abc</span> <span class="kw">import</span> <span class="fn">ABC</span>, <span class="fn">abstractmethod</span>

<span class="kw">class</span> <span class="fn">Entity</span>(<span class="fn">ABC</span>):
    <span class="op">@abstractmethod</span>
    <span class="kw">def</span> <span class="fn">update</span>(<span class="nb">self</span>, dt: <span class="nb">float</span>) -> <span class="nb">None</span>: ...
    <span class="op">@abstractmethod</span>
    <span class="kw">def</span> <span class="fn">draw</span>(<span class="nb">self</span>, surface) -> <span class="nb">None</span>: ...
    <span class="op">@abstractmethod</span>
    <span class="kw">def</span> <span class="fn">interact</span>(<span class="nb">self</span>) -> <span class="nb">str</span>: ...</pre>
</div>

<!-- 2. Inheritance -->
<div class="oop-block" style="border-left-color: var(--blue);">
  <div class="oop-title" style="color: var(--blue);">
    <span>2. Inheritance</span>
    <span class="badge" style="background:rgba(96,165,250,0.15);color:var(--blue);border-color:rgba(96,165,250,0.35);">entities/characters.py</span>
  </div>
  <p class="oop-desc">Hierarki pewarisan yang dalam dan terstruktur — setiap subclass mewarisi perilaku induknya tanpa duplikasi kode.</p>
  <div class="tree">
<span class="node-root">Entity</span> <span class="node-comment">(ABC)</span>
<span class="node-comment">└──</span> <span class="node-class">Character</span>
<span class="node-comment">    ├──</span> <span class="node-leaf">Player</span>         <span class="node-comment">← Hero: Arga</span>
<span class="node-comment">    └──</span> <span class="node-class">NPC</span>
<span class="node-comment">        ├──</span> <span class="node-leaf">KingdomNPC</span>  <span class="node-comment">← warga kota biasa</span>
<span class="node-comment">        ├──</span> <span class="node-leaf">PartyNPC</span>    <span class="node-comment">← Elena, Lyra, Darius, Reno</span>
<span class="node-comment">        ├──</span> <span class="node-leaf">BossNPC</span>     <span class="node-comment">← Demon King</span>
<span class="node-comment">        └──</span> <span class="node-leaf">MonsterNPC</span>  <span class="node-comment">← Slime, Goblin, Minotaur…</span>

<span class="node-root">Scene</span> <span class="node-comment">(ABC)</span>
<span class="node-comment">├──</span> <span class="node-leaf">OpeningScene</span>
<span class="node-comment">├──</span> <span class="node-leaf">Chapter1Scene</span>
<span class="node-comment">├──</span> <span class="node-leaf">Chapter2Scene</span>  <span class="node-comment">(TownScene)</span>
<span class="node-comment">├──</span> <span class="node-leaf">Chapter3Scene</span>
<span class="node-comment">├──</span> <span class="node-leaf">ChapterFinalScene</span>
<span class="node-comment">├──</span> <span class="node-leaf">BattleScene</span>
<span class="node-comment">├──</span> <span class="node-leaf">BossBattleScene</span>
<span class="node-comment">├──</span> <span class="node-leaf">TrueEndScene</span>
<span class="node-comment">└──</span> <span class="node-leaf">BadEndScene</span>
  </div>
</div>

<!-- 3. Encapsulation -->
<div class="oop-block" style="border-left-color: var(--teal);">
  <div class="oop-title" style="color: var(--teal);">
    <span>3. Encapsulation</span>
    <span class="badge" style="background:rgba(45,212,191,0.12);color:var(--teal);border-color:rgba(45,212,191,0.35);">private &amp; property</span>
  </div>
  <p class="oop-desc">Atribut sensitif dilindungi dengan naming convention <code style="color:var(--teal);font-family:'Source Code Pro',monospace;">__private</code> dan diakses secara terkontrol melalui <code style="color:var(--teal);font-family:'Source Code Pro',monospace;">@property</code>.</p>
  <pre><span class="kw">class</span> <span class="fn">Player</span>(<span class="fn">Character</span>):
    <span class="kw">def</span> <span class="fn">__init__</span>(<span class="nb">self</span>, x, y):
        <span class="nb">self</span>.__hp     = <span class="nb">9999</span>   <span class="cm"># private</span>
        <span class="nb">self</span>.__level  = <span class="nb">99</span>

    <span class="op">@property</span>
    <span class="kw">def</span> <span class="fn">hp</span>(<span class="nb">self</span>): <span class="kw">return</span> <span class="nb">self</span>.__hp  <span class="cm"># akses lewat property</span>

<span class="kw">class</span> <span class="fn">Character</span>(<span class="fn">Entity</span>):
    <span class="op">@emotion.setter</span>
    <span class="kw">def</span> <span class="fn">emotion</span>(<span class="nb">self</span>, value: <span class="nb">str</span>):
        <span class="kw">if</span> value <span class="kw">in</span> <span class="nb">self</span>.EMOTIONS:  <span class="cm"># validasi dulu</span>
            <span class="nb">self</span>.__emotion = value</pre>
</div>

<!-- 4. Polymorphism -->
<div class="oop-block" style="border-left-color: var(--gold);">
  <div class="oop-title" style="color: var(--gold2);">
    <span>4. Polymorphism</span>
    <span class="badge" style="background:rgba(201,168,76,0.12);color:var(--gold2);border-color:rgba(201,168,76,0.35);">method override</span>
  </div>
  <p class="oop-desc">Method yang sama berperilaku berbeda tergantung kelas yang dipanggil:</p>
  <pre><span class="cm"># interact() — beda hasil di tiap kelas</span>
<span class="fn">Player</span>.interact()     <span class="op">→</span> <span class="str">"player"</span>
<span class="fn">KingdomNPC</span>.interact() <span class="op">→</span> <span class="str">baris dialog warga</span>
<span class="fn">BossNPC</span>.interact()    <span class="op">→</span> <span class="str">"Hahaha... coba saja!"</span>
<span class="fn">MonsterNPC</span>.interact() <span class="op">→</span> <span class="str">"*Slime bergerak mengancam*"</span>

<span class="cm"># draw() — setiap entitas merender dirinya sendiri</span>
<span class="fn">Player</span>.draw()         <span class="op">→</span> multi-frame + flip sprite
<span class="fn">BossNPC</span>.draw()        <span class="op">→</span> frame cycling animasi idle
<span class="fn">MonsterNPC</span>.draw()     <span class="op">→</span> sprite + HP bar di atas kepala</pre>
</div>

<!-- 5. Composition -->
<div class="oop-block" style="border-left-color: var(--rose);">
  <div class="oop-title" style="color: var(--rose);">
    <span>5. Composition</span>
    <span class="badge" style="background:rgba(253,164,175,0.12);color:var(--rose);border-color:rgba(253,164,175,0.35);">has-a relationship</span>
  </div>
  <p class="oop-desc">Objek kompleks dibangun dari komponen-komponen yang lebih kecil, bukan pewarisan tunggal:</p>
  <pre><span class="fn">Game</span>
<span class="cm">  ├──</span> <span class="fn">AssetManager</span>         <span class="cm"># loader sprite &amp; audio</span>
<span class="cm">  ├──</span> list[<span class="fn">Scene</span>]          <span class="cm"># scene stack</span>
<span class="cm">  └──</span> dict <span class="fn">flags</span>           <span class="cm"># flag cerita global</span>

<span class="fn">Scene</span>
<span class="cm">  ├──</span> <span class="fn">DialogueBox</span>          <span class="cm"># typewriter dialog</span>
<span class="cm">  ├──</span> <span class="fn">TransitionScreen</span>     <span class="cm"># fade in/out</span>
<span class="cm">  ├──</span> <span class="fn">NarratorBox</span>          <span class="cm"># narasi sinematik</span>
<span class="cm">  ├──</span> <span class="fn">PartyHUD</span>             <span class="cm"># status HP party</span>
<span class="cm">  └──</span> list[<span class="fn">Entity</span>]        <span class="cm"># semua entitas di scene</span>

<span class="fn">PartyNPC</span>
<span class="cm">  └──</span> follow_target → <span class="fn">Player</span>  <span class="cm"># referensi ke objek lain</span></pre>
</div>

<!-- 6. Singleton -->
<div class="oop-block" style="border-left-color: var(--red);">
  <div class="oop-title" style="color: var(--red);">
    <span>6. Singleton Pattern</span>
    <span class="badge" style="background:rgba(248,113,113,0.12);color:var(--red);border-color:rgba(248,113,113,0.35);">engine/game.py</span>
  </div>
  <p class="oop-desc"><code style="color:var(--red);font-family:'Source Code Pro',monospace;">GAME_INSTANCE</code> bertindak sebagai global singleton, memungkinkan akses <code style="color:var(--red);font-family:'Source Code Pro',monospace;">AssetManager</code> dari mana saja tanpa perlu passing referensi.</p>
  <pre><span class="fn">GAME_INSTANCE</span> = <span class="nb">None</span>   <span class="cm"># singleton global</span>

<span class="kw">class</span> <span class="fn">Game</span>:
    <span class="kw">def</span> <span class="fn">__init__</span>(<span class="nb">self</span>, ...):
        <span class="kw">global</span> <span class="fn">GAME_INSTANCE</span>
        <span class="fn">GAME_INSTANCE</span> = <span class="nb">self</span>   <span class="cm"># set sekali, diakses mana saja</span>

<span class="cm"># Di entities/characters.py — tanpa import Game langsung</span>
<span class="kw">def</span> <span class="fn">_get_assets</span>():
    <span class="kw">from</span> <span class="nb">engine.game</span> <span class="kw">import</span> <span class="fn">GAME_INSTANCE</span>
    <span class="kw">return</span> <span class="fn">GAME_INSTANCE</span>.assets</pre>
</div>

<div class="divider">✦ &nbsp;STRUKTUR PROYEK&nbsp; ✦</div>

<!-- ══════════════ STRUCTURE ══════════════ -->
<div class="dir-tree">
<span class="dir-folder">Summoned-To-Another-World-and-Became-A-Hero/</span>
│
├── <span class="dir-file">main.py</span>                    <span class="dir-comment"># Entry point</span>
├── <span class="dir-folder">engine/</span>
│   ├── <span class="dir-file">base.py</span>                <span class="dir-comment"># Entity &amp; Scene ABC</span>
│   ├── <span class="dir-file">game.py</span>                <span class="dir-comment"># Game loop &amp; scene manager</span>
│   ├── <span class="dir-file">assets.py</span>              <span class="dir-comment"># Asset loader (AssetManager)</span>
│   └── <span class="dir-file">colors.py</span>              <span class="dir-comment"># Konstanta warna</span>
│
├── <span class="dir-folder">entities/</span>
│   └── <span class="dir-file">characters.py</span>          <span class="dir-comment"># Hierarki karakter</span>
│
├── <span class="dir-folder">scenes/</span>
│   ├── <span class="dir-file">opening_scene.py</span>       <span class="dir-comment"># Cutscene pembuka</span>
│   ├── <span class="dir-file">chapter1_scene.py</span>      <span class="dir-comment"># The Summoning</span>
│   ├── <span class="dir-file">town_scene.py</span>          <span class="dir-comment"># Chapter 2 — Kota Astravia</span>
│   ├── <span class="dir-file">chapter3_scene.py</span>      <span class="dir-comment"># Chapter 3 — Perjalanan</span>
│   ├── <span class="dir-file">chapter_final_scene.py</span> <span class="dir-comment"># Dungeon &amp; Boss Intro</span>
│   ├── <span class="dir-file">true_end_scene.py</span>      <span class="dir-comment"># Ending terbaik</span>
│   └── <span class="dir-file">bad_end_scene.py</span>       <span class="dir-comment"># Ending gelap</span>
│
├── <span class="dir-folder">battle/</span>
│   ├── <span class="dir-file">battle_scene.py</span>        <span class="dir-comment"># Battle turn-based normal</span>
│   └── <span class="dir-file">boss_battle_scene.py</span>   <span class="dir-comment"># Boss battle (Demon King)</span>
│
├── <span class="dir-folder">ui/</span>
│   └── <span class="dir-file">components.py</span>          <span class="dir-comment"># DialogueBox, BattleUI, HUD, dst.</span>
│
└── <span class="dir-folder">assets/</span>                    <span class="dir-comment"># Sprite, background, audio</span>
    ├── <span class="dir-folder">backgrounds/</span>
    └── <span class="dir-folder">characters/</span>
</div>

<div class="divider">✦ &nbsp;CARA MENJALANKAN&nbsp; ✦</div>

<!-- ══════════════ INSTALL ══════════════ -->
<div class="install-block">
  <div class="ib-header">terminal</div>
  <code>
<span class="prompt">#</span> <span class="comment">Install dependency</span>
<span class="prompt">$</span> pip install pygame

<span class="prompt">#</span> <span class="comment">Jalankan game</span>
<span class="prompt">$</span> python main.py
  </code>
</div>

<h3 class="sub">Kontrol</h3>
<table class="controls-table">
  <tr><th>Tombol</th><th>Fungsi</th></tr>
  <tr><td><span class="kbd">Space</span> / <span class="kbd">Enter</span></td><td>Lanjutkan dialog · Konfirmasi pilihan</td></tr>
  <tr><td><span class="kbd">↑</span> <span class="kbd">↓</span></td><td>Navigasi pilihan menu</td></tr>
  <tr><td><span class="kbd">E</span></td><td>Interaksi dengan NPC di kota</td></tr>
  <tr><td><span class="kbd">A</span> / <span class="kbd">D</span></td><td>Gerak kiri / kanan saat eksplorasi</td></tr>
</table>

<h3 class="sub" style="margin-top:1.5rem;">Teknologi</h3>
<div class="tech-pills">
  <span class="pill">Python 3.x</span>
  <span class="pill">Pygame</span>
  <span class="pill">ABC — Abstract Base Class</span>
  <span class="pill">OOP</span>
  <span class="pill">Sprite Animation</span>
  <span class="pill">Turn-Based Battle</span>
</div>

<!-- ══════════════ FOOTER ══════════════ -->
<div class="divider">✦ ✦ ✦</div>
<div class="footer">
  <p class="footer-deco">⚔ ✦ ⚔</p>
  <p>Dibuat sebagai proyek game berbasis Python dengan implementasi konsep Object-Oriented Programming.</p>
  <p style="margin-top:0.3rem; color:var(--ink3);">Teknik Informatika · Universitas Negeri Surabaya</p>
</div>

<script>
  const c = document.getElementById('stars-container');
  for (let i = 0; i < 60; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    s.style.cssText = `
      left:${Math.random()*100}%;
      top:${Math.random()*100}%;
      --d:${2+Math.random()*4}s;
      --delay:-${Math.random()*4}s;
      width:${1+Math.random()*2}px;
      height:${1+Math.random()*2}px;
    `;
    c.appendChild(s);
  }
</script>
</body>
</html>
