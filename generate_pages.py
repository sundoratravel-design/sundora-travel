#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sundora Travel — Çok Sayfalı Platform Oluşturucu v3
Düzeltmeler:
  1. Nav scroll arka planı beyaz değil pastel krem/bej
  2. Sayfa arka planı ana sayfayla uyumlu pastel krem-kahve
  3. Mobil hamburger menü düzeltmesi
"""

import re
import os

PUBLIC_DIR = "public"
INDEX_PATH = os.path.join(PUBLIC_DIR, "index.html")

def read_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filename, content):
    path = os.path.join(PUBLIC_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {path} oluşturuldu.")

def build_new_nav(original_html):
    new_nav_links = """<ul class="nav-links">
    <li><a href="/butik-grup-turlari.html">Butik Grup Turları</a></li>
    <li><a href="/rotalar.html">Rotalar</a></li>
    <li><a href="/hakkimizda.html">Hakkımızda</a></li>
    <li><a href="/iletisim.html">İletişim</a></li>
  </ul>"""
    updated = re.sub(
        r'<ul class="nav-links">.*?</ul>',
        new_nav_links,
        original_html,
        flags=re.DOTALL
    )
    old_nav_r = re.search(r'<div class="nav-r">.*?</div>', updated, re.DOTALL)
    if old_nav_r:
        new_nav_r = '''<div class="nav-r">
    <span class="nav-lang">TR / EN</span>
    <a href="/seyahatini-planla.html" class="nav-cta" style="text-decoration:none">Seyahatini Planla</a>
  </div>'''
        updated = updated[:old_nav_r.start()] + new_nav_r + updated[old_nav_r.end():]
    updated = re.sub(
        r'(<div class="nav-logo">)\s*(<img)',
        r'\1<a href="/index.html" style="display:inline-block">\2',
        updated
    )
    updated = re.sub(
        r'(nav-logo.*?<img[^>]+>)',
        lambda m: m.group(0) + '</a>',
        updated,
        flags=re.DOTALL
    )
    return updated

def update_hero_buttons(html):
    html = html.replace(
        '<button class="btn-h">Deneyimleri Keşfet</button>',
        '<a href="/rotalar.html" class="btn-h" style="text-decoration:none">Deneyimleri Keşfet</a>'
    )
    html = html.replace(
        '<button class="btn-hg"><span></span>Kişiye Özel Seyahatler</button>',
        '<a href="/kisiye-ozel-seyahatler.html" class="btn-hg" style="text-decoration:none;display:flex;align-items:center;gap:.9rem"><span></span>Kişiye Özel Seyahatler</a>'
    )
    return html

def extract_head(html):
    m = re.search(r'<head>(.*?)</head>', html, re.DOTALL)
    return m.group(1) if m else ""

def extract_nav(html):
    m = re.search(r'<nav[^>]*>.*?</nav>', html, re.DOTALL)
    return m.group(0) if m else ""

def extract_footer(html):
    m = re.search(r'<footer>.*?</footer>', html, re.DOTALL)
    return m.group(0) if m else ""

def extract_cursor_script(html):
    scripts = re.findall(r'<script(?!\s*src)[^>]*>.*?</script>', html, re.DOTALL)
    short = [s for s in scripts if len(s) < 2000]
    return "\n".join(short)

def extract_cursor_html(html):
    cur = re.search(r'<div id="cur"[^>]*>.*?</div>', html, re.DOTALL)
    ring = re.search(r'<div id="curRing"[^>]*>.*?</div>', html, re.DOTALL)
    result = ""
    if cur: result += cur.group(0) + "\n"
    if ring: result += ring.group(0) + "\n"
    return result

TOUR_CARDS_DATA = [
    ("01", "bg-h", "Japonya & Güney Kore", "Asya", "12 Gün"),
    ("02", "bg-s", "İtalya: Toskana Rotası", "Avrupa", "9 Gün"),
    ("03", "bg-c", "Fas: Çöl & Medina", "Afrika", "8 Gün"),
    ("04", "bg-p", "Maldivler Retreat", "Tropik Adalar", "7 Gün"),
    ("05", "bg-h", "Peru & Machu Picchu", "Amerika", "11 Gün"),
    ("06", "bg-s", "Yunanistan Adaları", "Avrupa", "10 Gün"),
    ("07", "bg-c", "Yeni Zelanda", "Avustralya", "14 Gün"),
    ("08", "bg-p", "Ürdün & Petra", "Ortadoğu", "7 Gün"),
    ("09", "bg-h", "İsviçre Alpleri", "Kış Bölgeleri", "8 Gün"),
    ("10", "bg-s", "Tanzania Safari", "Safari", "10 Gün"),
    ("11", "bg-c", "Bali & Komodo", "Asya", "12 Gün"),
    ("12", "bg-p", "İzlanda Aurora", "Kutup Bölgeleri", "6 Gün"),
]

def build_tour_cards(cards_data):
    cards_html = ""
    for num, bg, title, region, duration in cards_data:
        cards_html += f"""
    <div class="ec">
      <div class="eci">
        <div class="ecb {bg}"></div>
        <div class="eco"></div>
        <div class="ecarr">
          <svg viewBox="0 0 16 16">
            <line x1="0" y1="8" x2="12" y2="8"></line>
            <polyline points="8,4 12,8 8,12"></polyline>
          </svg>
        </div>
        <div class="ecinfo">
          <div class="ecn">{num}</div>
          <div class="ect">{title}</div>
          <div class="ecs">{region} · {duration}</div>
        </div>
      </div>
    </div>"""
    return cards_html

# ─── DÜZELTİLMİŞ STILLER ───
# 1. body arka planı → ana sayfayla uyumlu pastel krem-kahve
# 2. nav.s arka planı → bej/krem (beyaz değil)
# 3. Mobil menü düzeltmesi
PAGE_STYLES = """
<style>
/* ── SAYFA ARKA PLANI — Ana sayfayla uyumlu pastel krem-kahve ── */
body {
  background: linear-gradient(160deg, #EDE8DC 0%, #E8E0D0 30%, #E4D8C8 60%, #EDE4D8 100%) !important;
  min-height: 100vh;
}

/* ── NAV SCROLL ARKA PLANI — Beyaz değil pastel krem ── */
/* Ana sayfanın .nav.s stilini override et */
#nav.s {
  background: rgba(237,232,220,0.97) !important;
  backdrop-filter: blur(20px) !important;
  border-bottom: 1px solid rgba(196,160,104,0.2) !important;
}
#nav.s .nav-logo img { filter: none !important; opacity: 1 !important; }
#nav.s .nav-links a { color: #505060 !important; }
#nav.s .nav-lang { color: #909098 !important; }
#nav.s .nav-cta { border-color: #C4A068 !important; color: #9A7040 !important; }

/* ── MOBİL HAMBURGER MENÜ ── */
.mob-menu-btn {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  z-index: 301;
  position: relative;
}
.mob-menu-btn span {
  display: block;
  width: 24px;
  height: 1.5px;
  background: rgba(255,255,255,0.9);
  transition: all .35s;
  border-radius: 2px;
}
#nav.s .mob-menu-btn span { background: #505060; }
.mob-menu-btn.open span:nth-child(1) { transform: translateY(6.5px) rotate(45deg); }
.mob-menu-btn.open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
.mob-menu-btn.open span:nth-child(3) { transform: translateY(-6.5px) rotate(-45deg); }

.mob-nav-overlay {
  position: fixed;
  inset: 0;
  background: rgba(237,232,220,0.98);
  backdrop-filter: blur(24px);
  z-index: 299;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2.5rem;
  opacity: 0;
  pointer-events: none;
  transition: opacity .35s ease;
}
.mob-nav-overlay.open {
  opacity: 1;
  pointer-events: all;
}
.mob-nav-overlay a {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(28px, 6vw, 42px);
  font-weight: 300;
  letter-spacing: .06em;
  color: #28282E;
  text-decoration: none;
  transition: color .3s;
}
.mob-nav-overlay a:hover { color: #C4A068; }
.mob-nav-overlay .mob-cta {
  font-family: 'Jost', sans-serif;
  font-size: 10px;
  font-weight: 300;
  letter-spacing: .22em;
  text-transform: uppercase;
  padding: .85rem 2.5rem;
  border: 1px solid rgba(196,160,104,0.6);
  color: #9A7040;
  margin-top: 1rem;
}

@media (max-width: 900px) {
  .mob-menu-btn { display: flex !important; }
  .nav-links { display: none !important; }
  .nav-cta { display: none !important; }
  .nav-lang { display: none !important; }
}

/* ── SAYFA BÖLÜM ── */
.page-section { max-width: 1440px; margin: 0 auto; padding: 4rem 4rem 8rem; }

/* ── SAYFA BAŞLIK ── */
.page-title-block {
  padding: 11rem 0 3rem;
  border-bottom: 1px solid rgba(196,160,104,0.3);
  margin-bottom: 5rem;
}
.page-title-block .lbl { color: #C4A068; }
.page-title-block .lbl::before { background: #C4A068; }
.page-title-block .sh { color: #28282E; }
.page-title-block .sh em { color: #9A7040; }

/* ── FİLTRE ALANI ── */
.filter-bar {
  display: flex; flex-wrap: wrap; gap: 1rem; align-items: flex-end;
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(196,160,104,0.22);
  padding: 2rem 2.5rem;
  margin-bottom: 4rem;
}
.filter-group { display: flex; flex-direction: column; gap: .45rem; flex: 1; min-width: 160px; }
.filter-group label { font-size: 8px; font-weight: 400; letter-spacing: .28em; text-transform: uppercase; color: #C4A068; }
.filter-group select,
.filter-group input[type="date"] {
  font-family: 'Jost', sans-serif; font-size: 12px; font-weight: 300;
  color: #28282E; background: transparent;
  border: none; border-bottom: 1px solid rgba(196,160,104,0.4);
  padding: .55rem 0; outline: none; cursor: pointer;
  -webkit-appearance: none; appearance: none; width: 100%;
  transition: border-color .3s;
}
.filter-group select option { background: #EDE8DC; color: #28282E; }
.filter-group select:focus,
.filter-group input:focus { border-color: #C4A068; }
.filter-btn {
  font-family: 'Jost', sans-serif; font-size: 9px; font-weight: 400;
  letter-spacing: .22em; text-transform: uppercase;
  padding: .9rem 2.5rem; background: #C4A068; color: #fff;
  border: none; cursor: pointer; transition: background .3s;
  align-self: flex-end; white-space: nowrap;
}
.filter-btn:hover { background: #9A7040; }

/* ── TUR KARTLARI ── */
.tour-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.5rem; margin-bottom: 4rem; }
.ec { cursor: pointer; overflow: hidden; }
.eci { aspect-ratio: 3/4; position: relative; overflow: hidden; }
.ecb { position: absolute; inset: 0; transition: transform .9s cubic-bezier(.25,.46,.45,.94); }
.ec:hover .ecb { transform: scale(1.08); }
.eco { position: absolute; inset: 0; background: linear-gradient(to top, rgba(10,8,20,.88) 0%, rgba(10,8,20,.05) 55%, transparent 100%); }
.ecarr {
  position: absolute; top: 1.25rem; right: 1.25rem;
  width: 34px; height: 34px;
  border: 1px solid rgba(255,255,255,.18);
  display: flex; align-items: center; justify-content: center;
  opacity: 0; transform: translateY(-6px); transition: all .4s;
}
.ec:hover .ecarr { opacity: 1; transform: translateY(0); }
.ecarr svg { width: 12px; height: 12px; stroke: rgba(255,255,255,.7); fill: none; stroke-width: 1.5; }
.ecinfo { position: absolute; bottom: 0; left: 0; right: 0; padding: 1.75rem 1.5rem; }
.ecn { font-size: 8px; font-weight: 300; letter-spacing: .25em; text-transform: uppercase; color: #DEC898; margin-bottom: .6rem; }
.ect { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 21px; font-weight: 300; color: #fff; line-height: 1.2; margin-bottom: .35rem; transition: transform .4s; }
.ec:hover .ect { transform: translateY(-3px); }
.ecs { font-size: 10px; font-weight: 300; letter-spacing: .06em; color: rgba(255,255,255,.42); }
.bg-h { background: linear-gradient(155deg,#7090A8 0%,#405870 45%,#203848 100%); }
.bg-s { background: linear-gradient(155deg,#708858 0%,#506840 45%,#304820 100%); }
.bg-c { background: linear-gradient(155deg,#A07858 0%,#785838 45%,#503818 100%); }
.bg-p { background: linear-gradient(155deg,#806898 0%,#604878 45%,#402858 100%); }

/* ── HAKKIMIZDA ── */
.about-text { max-width: 780px; }
.about-text p { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 17px; font-style: italic; line-height: 2.1; color: #505060; margin-bottom: 2rem; }
.about-text p:first-child { font-size: 22px; color: #28282E; font-style: normal; }

/* ── İLETİŞİM FORM ── */
.contact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8rem; padding-top: 2rem; }
.contact-info-col h3 { font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(28px,3vw,44px); font-weight: 300; color: #28282E; margin-bottom: 3rem; line-height: 1.2; }
.contact-info-col h3 em { font-style: italic; color: #9A7040; }
.ci-block { margin-bottom: 2.5rem; }
.ci-label { font-size: 8px; font-weight: 400; letter-spacing: .28em; text-transform: uppercase; color: #C4A068; margin-bottom: .5rem; display: flex; align-items: center; gap: .85rem; }
.ci-label::before { content: ''; width: 22px; height: 1px; background: #C4A068; }
.ci-value { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 16px; font-weight: 300; color: #28282E; line-height: 1.6; }
.contact-form-col h3 { font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(22px,2.5vw,36px); font-weight: 300; color: #28282E; margin-bottom: 2.5rem; line-height: 1.2; }
.form-group { margin-bottom: 1.75rem; }
.form-group label { display: block; font-size: 8px; font-weight: 400; letter-spacing: .28em; text-transform: uppercase; color: #C4A068; margin-bottom: .5rem; }
.form-group input,
.form-group textarea {
  font-family: 'Jost', sans-serif; font-size: 14px; font-weight: 300;
  color: #28282E; background: transparent;
  border: none; border-bottom: 1px solid rgba(196,160,104,0.35);
  padding: .6rem 0; width: 100%; outline: none;
  transition: border-color .3s; resize: none;
}
.form-group input::placeholder,
.form-group textarea::placeholder { color: rgba(40,40,46,0.35); }
.form-group input:focus,
.form-group textarea:focus { border-color: #C4A068; }
.form-group textarea { min-height: 120px; background: rgba(255,255,255,0.4); padding: .8rem; border: 1px solid rgba(196,160,104,0.2); }
.submit-btn {
  font-family: 'Jost', sans-serif; font-size: 9px; font-weight: 400;
  letter-spacing: .22em; text-transform: uppercase;
  padding: 1rem 3rem; background: transparent;
  color: #28282E; border: 1px solid rgba(40,40,46,0.4);
  cursor: pointer; display: inline-flex; align-items: center; gap: 1rem;
  position: relative; overflow: hidden; transition: color .4s; margin-top: .5rem;
}
.submit-btn::before { content: ''; position: absolute; inset: 0; background: #28282E; transform: translateX(-100%); transition: transform .45s cubic-bezier(.25,.46,.45,.94); }
.submit-btn span { position: relative; z-index: 1; }
.submit-btn:hover { color: #fff; }
.submit-btn:hover::before { transform: translateX(0); }

/* ── CTA BUTONU ── */
.cta-center { text-align: center; padding: 2rem 0 4rem; }
.btn-e {
  font-size: 9px; font-weight: 400; letter-spacing: .22em; text-transform: uppercase;
  padding: .9rem 2.25rem; border: 1px solid rgba(40,40,46,0.4);
  color: #28282E; background: transparent; cursor: pointer;
  display: inline-flex; align-items: center; gap: 1rem;
  position: relative; overflow: hidden; transition: color .4s; text-decoration: none;
}
.btn-e::before { content: ''; position: absolute; inset: 0; background: #28282E; transform: translateX(-100%); transition: transform .45s cubic-bezier(.25,.46,.45,.94); }
.btn-e span, .btn-e svg { position: relative; z-index: 1; }
.btn-e:hover { color: #fff; }
.btn-e:hover::before { transform: translateX(0); }

/* ── MOBİL RESPONSIVE ── */
@media (max-width: 768px) {
  .tour-grid { grid-template-columns: 1fr 1fr; }
  .contact-grid { grid-template-columns: 1fr; gap: 3rem; }
  .filter-bar { flex-direction: column; }
  .page-section { padding: 2rem 1.5rem 5rem; }
  .page-title-block { padding: 8rem 0 2rem; }
}
@media (max-width: 480px) {
  .tour-grid { grid-template-columns: 1fr; }
}
</style>
"""

MOB_MENU_HTML = """
<div class="mob-nav-overlay" id="mobNav">
  <a href="/butik-grup-turlari.html">Butik Grup Turları</a>
  <a href="/rotalar.html">Rotalar</a>
  <a href="/hakkimizda.html">Hakkımızda</a>
  <a href="/iletisim.html">İletişim</a>
  <a href="/seyahatini-planla.html" class="mob-cta">Seyahatini Planla</a>
</div>
"""

MOB_MENU_SCRIPT = """
<script>
(function(){
  var btn = document.getElementById('mobMenuBtn');
  var overlay = document.getElementById('mobNav');
  if(!btn || !overlay) return;
  btn.addEventListener('click', function(e){
    e.stopPropagation();
    btn.classList.toggle('open');
    overlay.classList.toggle('open');
  });
  overlay.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click', function(){
      btn.classList.remove('open');
      overlay.classList.remove('open');
    });
  });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape'){
      btn.classList.remove('open');
      overlay.classList.remove('open');
    }
  });
})();
</script>
"""

def inject_mob_btn(nav_html):
    return nav_html.replace(
        '<div class="nav-r">',
        '<div class="nav-r"><button class="mob-menu-btn" id="mobMenuBtn" aria-label="Menü"><span></span><span></span><span></span></button>'
    )

def page_template(head_content, nav_html, footer_html, cursor_html,
                  cursor_script, page_body, page_title="Sundora Travel"):
    nav_with_btn = inject_mob_btn(nav_html)
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
{head_content}
<title>{page_title} — travel &amp; beyond</title>
{PAGE_STYLES}
</head>
<body>
{cursor_html}
{MOB_MENU_HTML}
{nav_with_btn}
{page_body}
{footer_html}
{cursor_script}
<script>
const nav=document.getElementById('nav');
if(nav) window.addEventListener('scroll',function(){{nav.classList.toggle('s',scrollY>80)}});
</script>
{MOB_MENU_SCRIPT}
</body>
</html>"""

def make_rotalar(head, nav, footer, cursor_html, cursor_script):
    cards_html = build_tour_cards(TOUR_CARDS_DATA)
    body = f"""
<main>
  <div class="page-section">
    <div class="page-title-block">
      <div class="lbl">Keşfet</div>
      <h1 class="sh">Tüm <em>Rotalar</em></h1>
    </div>
    <div class="filter-bar">
      <div class="filter-group">
        <label>Destinasyon</label>
        <select><option value="">Tüm Destinasyonlar</option><option>Asya</option><option>Avrupa</option><option>Afrika</option><option>Amerika</option><option>Avustralya</option><option>Ortadoğu</option><option>Kutup Bölgeleri</option></select>
      </div>
      <div class="filter-group">
        <label>Tarih</label>
        <input type="date" />
      </div>
      <div class="filter-group">
        <label>Aktivite</label>
        <select><option value="">Tüm Aktiviteler</option><option>Kültür &amp; Sanat</option><option>Lezzet &amp; Şarap</option><option>Safari</option><option>Spa &amp; Sağlık</option><option>Tropik Adalar</option><option>Kış Bölgeleri</option></select>
      </div>
      <div class="filter-group">
        <label>Seyahat Tarzı</label>
        <select><option>Tüm Seyahat Tarzları</option><option>Grup Turu</option><option>Kişiye Özel</option></select>
      </div>
      <button class="filter-btn">Ara</button>
    </div>
    <div class="tour-grid">{cards_html}</div>
    <div class="cta-center">
      <a href="/butik-grup-turlari.html" class="btn-e">
        <span>Tüm Popüler Programlar</span>
        <svg viewBox="0 0 16 16" width="12" height="12" stroke="currentColor" fill="none" stroke-width="1.5"><line x1="0" y1="8" x2="12" y2="8"></line><polyline points="8,4 12,8 8,12"></polyline></svg>
      </a>
    </div>
  </div>
</main>"""
    return page_template(head, nav, footer, cursor_html, cursor_script, body, "Rotalar | Sundora Travel")

def make_hakkimizda(head, nav, footer, cursor_html, cursor_script):
    body = """
<main>
  <div class="page-section">
    <div class="page-title-block">
      <div class="lbl">Biz Kimiz</div>
      <h1 class="sh">Hakkımızda</h1>
    </div>
    <div class="about-text">
      <p>Seyahat, bizim için yalnızca bir destinasyona ulaşmak değil; doğru kurgulandığında hayat boyu hatırlanacak bir deneyime dönüşen özel bir yolculuktur.</p>
      <p>Sundora Travel, dünya turizmine duyduğu derin ilgi, yıllara dayanan sektör tecrübesi ve global bakış açısıyla, klasik seyahat anlayışının ötesine geçmek amacıyla kuruldu.</p>
      <p>Ekibimiz; turizm, uluslararası satış ve global operasyonlar alanlarında yetişmiş, farklı coğrafyalarda deneyim kazanmış profesyonellerden oluşur. Bu birikim sayesinde, dünyanın dört bir yanında en doğru iş ortaklarıyla çalışır, her detayı titizlikle planlanmış seyahatler tasarlarız.</p>
      <p>Bizim için her yolculuk, kişiye özeldir. Hazır paketler yerine, misafirlerimizin beklentilerini anlayarak onlara özel rotalar oluştururuz. Çünkü gerçek lüksün; seçenek bolluğu değil, doğru seçim olduğunu biliyoruz.</p>
      <p>Sundora'nın yaklaşımı; görünmeyen detaylarda fark yaratan, süreci zahmetsiz hale getiren, ve her anında güven veren bir seyahat deneyimi sunmaktır.</p>
      <p>Bugün geldiğimiz noktada, yalnızca bir seyahat planlamıyor; misafirlerimizin tarzına, beklentilerine ve hayallerine uyum sağlayan, onlara özel hikâyeler tasarlıyoruz.</p>
    </div>
  </div>
</main>"""
    return page_template(head, nav, footer, cursor_html, cursor_script, body, "Hakkımızda | Sundora Travel")

def make_seyahatini_planla(head, nav, footer, cursor_html, cursor_script):
    body = """
<main>
  <div class="page-section">
    <div class="page-title-block">
      <div class="lbl">Başlayalım</div>
      <h1 class="sh">Seyahatini <em>Planla</em></h1>
    </div>
    <div class="contact-grid">
      <div class="contact-info-col">
        <h3>Size <em>özel</em><br>bir yolculuk<br>tasarlayalım.</h3>
        <div class="ci-block"><div class="ci-label">Adres</div><div class="ci-value">—</div></div>
        <div class="ci-block"><div class="ci-label">Telefon</div><div class="ci-value">—</div></div>
        <div class="ci-block"><div class="ci-label">E-Posta</div><div class="ci-value">support@sundoratravel.com</div></div>
      </div>
      <div class="contact-form-col">
        <h3>İletişim Detayları</h3>
        <div class="form-group"><label>İsim Soyisim</label><input type="text" placeholder="Adınız ve soyadınız" /></div>
        <div class="form-group"><label>Cep Telefonu</label><input type="tel" placeholder="+90 5__ ___ __ __" /></div>
        <div class="form-group"><label>E-Posta Adresi</label><input type="email" placeholder="ornek@mail.com" /></div>
        <div class="form-group"><label>Notunuz</label><textarea placeholder="Notunuz"></textarea></div>
        <button class="submit-btn" type="button"><span>Bizimle İletişime Geç</span></button>
      </div>
    </div>
  </div>
</main>"""
    return page_template(head, nav, footer, cursor_html, cursor_script, body, "Seyahatini Planla | Sundora Travel")

def make_butik_grup_turlari(head, nav, footer, cursor_html, cursor_script):
    cards_html = build_tour_cards(TOUR_CARDS_DATA)
    body = f"""
<main>
  <div class="page-section">
    <div class="page-title-block">
      <div class="lbl">Özenle Seçilmiş</div>
      <h1 class="sh">Butik Grup <em>Turları</em></h1>
    </div>
    <div class="tour-grid">{cards_html}</div>
  </div>
</main>"""
    return page_template(head, nav, footer, cursor_html, cursor_script, body, "Butik Grup Turları | Sundora Travel")

def make_kisiye_ozel(head, nav, footer, cursor_html, cursor_script):
    cards_html = build_tour_cards(TOUR_CARDS_DATA)
    body = f"""
<main>
  <div class="page-section">
    <div class="page-title-block">
      <div class="lbl">Sadece Sizin İçin</div>
      <h1 class="sh">Kişiye Özel <em>Seyahatler</em></h1>
    </div>
    <div class="tour-grid">{cards_html}</div>
  </div>
</main>"""
    return page_template(head, nav, footer, cursor_html, cursor_script, body, "Kişiye Özel Seyahatler | Sundora Travel")

def make_iletisim(head, nav, footer, cursor_html, cursor_script):
    body = """
<main>
  <div class="page-section">
    <div class="page-title-block">
      <div class="lbl">Ulaşın</div>
      <h1 class="sh"><em>İletişim</em></h1>
    </div>
    <div class="contact-grid">
      <div class="contact-info-col">
        <h3>Birlikte <em>harika</em><br>şeyler<br>tasarlayalım.</h3>
        <div class="ci-block"><div class="ci-label">Adres</div><div class="ci-value">—</div></div>
        <div class="ci-block"><div class="ci-label">Telefon</div><div class="ci-value">—</div></div>
        <div class="ci-block"><div class="ci-label">E-Posta</div><div class="ci-value">support@sundoratravel.com</div></div>
        <div class="ci-block"><div class="ci-label">Instagram</div><div class="ci-value"><a href="https://instagram.com/sundoratravel" target="_blank" style="color:#9A7040;text-decoration:none">@sundoratravel</a></div></div>
      </div>
      <div class="contact-form-col">
        <h3>Mesaj Gönderin</h3>
        <div class="form-group"><label>İsim Soyisim</label><input type="text" placeholder="Adınız ve soyadınız" /></div>
        <div class="form-group"><label>E-Posta</label><input type="email" placeholder="ornek@mail.com" /></div>
        <div class="form-group"><label>Mesajınız</label><textarea placeholder="Mesajınız"></textarea></div>
        <button class="submit-btn" type="button"><span>Gönder</span></button>
      </div>
    </div>
  </div>
</main>"""
    return page_template(head, nav, footer, cursor_html, cursor_script, body, "İletişim | Sundora Travel")

def main():
    print("\n🌍  Sundora Travel — Sayfa Üretici v3 Başlatıldı\n")
    if not os.path.exists(PUBLIC_DIR):
        print(f"HATA: '{PUBLIC_DIR}' klasörü bulunamadı.")
        return
    print(f"📖  {INDEX_PATH} okunuyor...")
    original_html = read_index()
    print("✏️   Header & logo linkleri güncelleniyor...")
    updated_html = build_new_nav(original_html)
    print("✏️   Hero butonları güncelleniyor...")
    updated_html = update_hero_buttons(updated_html)
    write_file("index.html", updated_html)
    head = extract_head(updated_html)
    nav = extract_nav(updated_html)
    footer = extract_footer(updated_html)
    cursor_html = extract_cursor_html(updated_html)
    cursor_script = extract_cursor_script(updated_html)
    print("\n📄  Yeni sayfalar oluşturuluyor...")
    write_file("rotalar.html", make_rotalar(head, nav, footer, cursor_html, cursor_script))
    write_file("hakkimizda.html", make_hakkimizda(head, nav, footer, cursor_html, cursor_script))
    write_file("seyahatini-planla.html", make_seyahatini_planla(head, nav, footer, cursor_html, cursor_script))
    write_file("butik-grup-turlari.html", make_butik_grup_turlari(head, nav, footer, cursor_html, cursor_script))
    write_file("kisiye-ozel-seyahatler.html", make_kisiye_ozel(head, nav, footer, cursor_html, cursor_script))
    write_file("iletisim.html", make_iletisim(head, nav, footer, cursor_html, cursor_script))
    print("\n✅  Tüm sayfalar başarıyla güncellendi!\n")

if __name__ == "__main__":
    main()
