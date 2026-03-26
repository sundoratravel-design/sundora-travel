#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, os
PUBLIC_DIR = "public"
INDEX_PATH = os.path.join(PUBLIC_DIR, "index.html")
def read_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f: return f.read()
def write_file(filename, content):
    path = os.path.join(PUBLIC_DIR, filename)
    with open(path, "w", encoding="utf-8") as f: f.write(content)
    print(f"  ✓ {path} oluşturuldu.")
def remove_cursor(html):
    # cursor:none kaldır
    html = re.sub(r'cursor\s*:\s*none\s*;?\s*', '', html)
    # CSS cursor bloklarını kaldır
    html = re.sub(r'/\* CURSOR \*/.*?\.cur-ring\{[^}]*\}', '', html, flags=re.DOTALL)
    # cursor div HTML'lerini kaldır
    html = re.sub(r'<div id="cur"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div id="curRing"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
    # cursor JS event'lerini kaldır
    html = re.sub(r'// CURSOR\s*\nconst cur=.*?anim\}\)\(\);', '', html, flags=re.DOTALL)
    # Ekstra: herhangi bir #cur veya #curRing CSS bloğunu kaldır
    html = re.sub(r'#cur\s*\{[^}]*\}', '', html)
    html = re.sub(r'#curRing\s*\{[^}]*\}', '', html)
    html = re.sub(r'\.cur-ring\s*\{[^}]*\}', '', html)
    # mousemove ile ilgili cursor kodlarını kaldır
    html = re.sub(r'document\.addEventListener\([\'"]mousemove[\'"].*?\}\s*\)', '', html, flags=re.DOTALL)
    # Garantili fallback: CSS ile gizle VE JS ile DOM'dan sil
    html = html.replace('</head>', '<style>#cur,#curRing,.cur,.cur-ring{display:none!important;width:0!important;height:0!important;overflow:hidden!important;pointer-events:none!important}</style></head>')
    html = html.replace('</body>', '<script>(function(){var els=["cur","curRing"];els.forEach(function(id){var el=document.getElementById(id);if(el)el.parentNode.removeChild(el)});})();</script></body>')
    return html
def fix_hero_gap(html):
    # html,body margin/padding sıfırla
    html = re.sub(r'(html\s*,\s*body\s*\{[^}]*?)margin\s*:\s*[^;]+;', r'\1margin:0;', html)
    html = re.sub(r'(html\s*,\s*body\s*\{[^}]*?)padding\s*:\s*[^;]+;', r'\1padding:0;', html)
    # .hero padding-top kaldır
    html = re.sub(r'(\.hero\s*\{[^}]*?)padding-top\s*:\s*[^;]+;', r'\1padding-top:0;', html)
    # hero-photo üstündeki boşluğu sıfırla
    html = re.sub(r'(\.hero-photo\s*\{)', r'.hero-photo{margin-top:0 !important;display:block;}\n\1', html)
    # body açılış taginden hemen sonra inline style inject et - en garantili yol
    html = re.sub(r'(<body[^>]*>)', r'\1\n<style>html,body{margin:0!important;padding:0!important}.hero,.hero-wrap,.hero-section{margin-top:0!important;padding-top:0!important}.hero-photo{margin-top:0!important;display:block!important;vertical-align:top!important}</style>', html)
    return html
def update_nav_style(html):
    html = re.sub(r'\.nav\.s\{background:rgba\(248,242,234[^}]+\}', '.nav.s{background:rgba(42,32,18,.9);backdrop-filter:blur(20px);padding:.75rem 4rem .75rem 2rem;border-bottom:1px solid rgba(196,160,104,.25)}', html)
    html = re.sub(r'\.nav\.s \.nav-links a\{color:var\(--slate\)[^}]*\}', '.nav.s .nav-links a{color:rgba(255,248,235,.9);font-size:15px}', html)
    html = re.sub(r'\.nav\.s \.nav-lang\{color:var\(--smoke\)\}', '.nav.s .nav-lang{color:rgba(255,248,235,.5)}', html)
    html = re.sub(r'\.nav\.s \.nav-cta\{border-color:var\(--gold\);color:var\(--gold-dk\)\}', '.nav.s .nav-cta{border-color:rgba(222,200,152,.6);color:rgba(222,200,152,.95)}', html)
    html = re.sub(r'\.nav\.s \.nav-logo img\{filter:none;opacity:1;height:120px\}', '.nav.s .nav-logo img{filter:brightness(0) invert(1);opacity:.9;height:120px}', html)
    return html
def inject_nav_bar_bg(html):
    # Nav-links'e her zaman koyu arka plan (scroll'dan bağımsız kalıcı bar)
    # nav-links alanına sabit koyu arka plan ekle - inline style injection via CSS
    return html
def update_footer(html):
    old_soc = '<div class="ft-soc"><a href="https://instagram.com/sundoratravel" target="_blank"><svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5"></rect><circle cx="12" cy="12" r="4"></circle></svg></a></div>'
    new_soc = '''<div class="ft-soc">
      <a href="https://instagram.com/sundoratravel" target="_blank" title="Instagram"><svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5"></rect><circle cx="12" cy="12" r="4"></circle></svg></a>
      <a href="https://tiktok.com/@sundoratravel" target="_blank" title="TikTok"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.18 8.18 0 004.79 1.53V6.77a4.85 4.85 0 01-1.02-.08z"/></svg></a>
      <a href="#" title="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
    </div>'''
    html = html.replace(old_soc, new_soc)
    old_exp_col = '<div class="ft-col"><div class="ft-ch">Deneyimler</div><ul><li>Şarap &amp; Gastronomi Deneyimleri</li><li>Doğayla İç İçe</li><li>Kültürel Keşifler</li><li>Popüler Destinasyonlar</li></ul></div>'
    new_exp_col = '''<div class="ft-col"><div class="ft-ch">Deneyimler</div><ul>
      <li><a href="#">Şarap &amp; Gastronomi Deneyimleri</a></li>
      <li><a href="#">Doğayla İç İçe</a></li>
      <li><a href="#">Kültürel Keşifler</a></li>
      <li><a href="#">Popüler Destinasyonlar</a></li>
    </ul></div>'''
    html = html.replace(old_exp_col, new_exp_col)
    old_company = '<div class="ft-col"><div class="ft-ch">Company</div><ul><li>Kişiye Özel Seyahatler</li><li>Sizin İçin Seçtiklerimiz</li><li>Butik Grup Turları</li><li>Özel Seyahatini Planla</li></ul></div>'
    new_company = '''<div class="ft-col"><div class="ft-ch">Faydalı Bilgiler</div><ul>
      <li><a href="#">Mesafeli Hizmet Sözleşmesi</a></li>
      <li><a href="#">Program Değerlendirme Anketi</a></li>
      <li><a href="#">Seyahat Sigortası</a></li>
      <li><a href="#">Uçak Biletleri</a></li>
      <li><a href="#">Vize</a></li>
    </ul></div>'''
    html = html.replace(old_company, new_company)
    html = html.replace('.ft-bot{', '.ft-col ul li a{color:rgba(255,255,255,.45);text-decoration:none;transition:color .3s}.ft-col ul li a:hover{color:var(--gold-lt)}.ft-bot{')
    return html
def update_hero_image(html):
    html = re.sub(r'<img class="hero-photo" src="data:image/jpeg;base64,[^"]*"[^>]*>', '<img class="hero-photo" src="/anasayfa.jpg" alt="Sundora Travel">', html)
    return html
def remove_sections(html):
    html = re.sub(r'<section class="ig-sec">.*?</section>', '', html, flags=re.DOTALL)
    html = re.sub(r'<section class="mem-sec">.*?</section>', '', html, flags=re.DOTALL)
    html = re.sub(r'<section style="background:linear-gradient[^"]*"[^>]*>\s*<div class="wrap"><div class="intro">.*?</div>\s*</div>\s*</section>', '', html, flags=re.DOTALL)
    return html
def update_exp_section_text(html):
    # "Experience Categories" -> "Seyahat Tarzını Seç"
    html = re.sub(r'Experience Categories', 'Seyahat Tarzını Seç', html)
    # "All Experiences →" -> "Tüm Rotalar →" with correct href
    html = re.sub(
        r'<a[^>]*href=["\'][^"\']*["\'][^>]*>\s*All Experiences\s*→\s*</a>',
        '<a href="/butik-grup-turlari.html" class="exp-more">Tüm Rotalar →</a>',
        html, flags=re.DOTALL
    )
    # Also try button/span variants
    html = re.sub(r'All Experiences\s*→', 'Tüm Rotalar →', html)
    html = re.sub(
        r'(href=["\'])([^"\']*?)(["\'][^>]*>Tüm Rotalar →)',
        r'\g<1>/butik-grup-turlari.html\g<3>',
        html
    )
    return html
def update_exp_cards(html):
    cards = [('bg-h','d1','Şarap &amp; Gastronomi Deneyimleri','/sarap.jpg'),('bg-s','d2','Doğayla İç İçe','/doga.jpg'),('bg-c','d3','Kültürel Keşifler','/culture.jpg'),('bg-p','d4','Popüler Destinasyonlar','/popular.jpg')]
    for bg,d,title,img in cards:
        old_p = rf'<div class="ec fi {d} v"><div class="eci"><div class="ecb {bg}"></div><div class="eco"></div><div class="ecarr">.*?</div><div class="ecinfo"><div class="ecn">[^<]*</div><div class="ect">[^<]*</div><div class="ecs">[^<]*</div></div></div></div>'
        new_c = f'<div class="ec fi {d} v"><div class="eci"><div class="ecb {bg}" style="background-image:url(\'{img}\');background-size:cover;background-position:center"></div><div class="eco"></div><div class="ecarr"><svg viewBox="0 0 16 16"><line x1="0" y1="8" x2="12" y2="8"></line><polyline points="8,4 12,8 8,12"></polyline></svg></div><div class="ecinfo"><div class="ect">{title}</div></div></div></div>'
        html = re.sub(old_p, new_c, html, flags=re.DOTALL)
    return html
def build_new_nav(html):
    new_links = """<ul class="nav-links">
    <li><a href="/butik-grup-turlari.html">Butik Grup Turları</a></li>
    <li><a href="/rotalar.html">Rotalar</a></li>
    <li><a href="/hakkimizda.html">Hakkımızda</a></li>
    <li><a href="/iletisim.html">İletişim</a></li>
  </ul>"""
    html = re.sub(r'<ul class="nav-links">.*?</ul>', new_links, html, flags=re.DOTALL)
    m = re.search(r'<div class="nav-r">.*?</div>', html, re.DOTALL)
    if m:
        new_r = '''<div class="nav-r">
    <span class="nav-lang">TR / EN</span>
    <a href="/seyahatini-planla.html" class="nav-cta" style="text-decoration:none">Seyahatini Planla</a>
  </div>'''
        html = html[:m.start()] + new_r + html[m.end():]
    html = re.sub(r'(<div class="nav-logo">)\s*(<img)', r'\1<a href="/index.html" style="display:inline-block">\2', html)
    html = re.sub(r'(nav-logo.*?<img[^>]+>)', lambda m: m.group(0)+'</a>', html, flags=re.DOTALL)
    return html
def update_hero_btns(html):
    html = html.replace('<button class="btn-h">Deneyimleri Keşfet</button>', '<a href="/rotalar.html" class="btn-h" style="text-decoration:none">Deneyimleri Keşfet</a>')
    html = html.replace('<button class="btn-hg"><span></span>Kişiye Özel Seyahatler</button>', '<a href="/kisiye-ozel-seyahatler.html" class="btn-hg" style="text-decoration:none;display:flex;align-items:center;gap:.9rem"><span></span>Kişiye Özel Seyahatler</a>')
    return html
def extract_head(html):
    m = re.search(r'<head>(.*?)</head>', html, re.DOTALL); return m.group(1) if m else ""
def extract_nav(html):
    m = re.search(r'<nav[^>]*>.*?</nav>', html, re.DOTALL); return m.group(0) if m else ""
def extract_footer(html):
    m = re.search(r'<footer>.*?</footer>', html, re.DOTALL); return m.group(0) if m else ""
TOUR_CARDS_DATA = [("01","bg-h","Japonya & Güney Kore","Asya","12 Gün"),("02","bg-s","İtalya: Toskana Rotası","Avrupa","9 Gün"),("03","bg-c","Fas: Çöl & Medina","Afrika","8 Gün"),("04","bg-p","Maldivler Retreat","Tropik Adalar","7 Gün"),("05","bg-h","Peru & Machu Picchu","Amerika","11 Gün"),("06","bg-s","Yunanistan Adaları","Avrupa","10 Gün"),("07","bg-c","Yeni Zelanda","Avustralya","14 Gün"),("08","bg-p","Ürdün & Petra","Ortadoğu","7 Gün"),("09","bg-h","İsviçre Alpleri","Kış Bölgeleri","8 Gün"),("10","bg-s","Tanzania Safari","Safari","10 Gün"),("11","bg-c","Bali & Komodo","Asya","12 Gün"),("12","bg-p","İzlanda Aurora","Kutup Bölgeleri","6 Gün")]
def build_tour_cards():
    h=""
    for num,bg,title,region,duration in TOUR_CARDS_DATA:
        h+=f'\n    <div class="ec"><div class="eci"><div class="ecb {bg}"></div><div class="eco"></div><div class="ecarr"><svg viewBox="0 0 16 16"><line x1="0" y1="8" x2="12" y2="8"></line><polyline points="8,4 12,8 8,12"></polyline></svg></div><div class="ecinfo"><div class="ecn">{num}</div><div class="ect">{title}</div><div class="ecs">{region} · {duration}</div></div></div></div>'
    return h
PAGE_STYLES = """
<style>
/* ── RESET ── */
html,body{margin:0;padding:0}
/* ── HERO GAP FIX ── */
.hero-photo{margin-top:0 !important;padding-top:0 !important;display:block;vertical-align:top}
.hero,.hero-wrap,.hero-section{margin-top:0 !important;padding-top:0 !important}
/* ── CURSOR RESET (tüm sayfalarda) ── */
*{cursor:auto !important}
a,button,[role=button],[type=button],[type=submit],label,select{cursor:pointer !important}
/* Anasayfa cursor:none override - orijinal CSS'in üzerine bin */
html body *{cursor:auto !important}
html body a,html body button{cursor:pointer !important}

/* ── NAV BAR: anasayfada her zaman koyu, scroll'da daha koyu ── */
body{background:linear-gradient(160deg,#EDE8DC 0%,#E8E0D0 30%,#E4D8C8 60%,#EDE4D8 100%) !important;min-height:100vh}
#nav{background:rgba(28,20,10,.82) !important;backdrop-filter:blur(18px) !important;border-bottom:1px solid rgba(196,160,104,.2) !important;position:fixed !important;top:0;left:0;right:0;z-index:300}
#nav .nav-links a{color:rgba(255,248,235,.88) !important;font-size:15px}
#nav .nav-lang{color:rgba(255,248,235,.5) !important}
#nav .nav-cta{border-color:rgba(222,200,152,.55) !important;color:rgba(222,200,152,.92) !important}
#nav .nav-logo img{filter:brightness(0) invert(1) !important;opacity:.88 !important}
#nav.s{background:rgba(28,20,10,.95) !important;backdrop-filter:blur(24px) !important;border-bottom:1px solid rgba(196,160,104,.3) !important}
#nav.s .nav-links a{color:rgba(255,248,235,.98) !important}
#nav.s .nav-cta{border-color:rgba(222,200,152,.7) !important;color:rgba(222,200,152,.98) !important}
#nav.s .nav-logo img{filter:brightness(0) invert(1) !important;opacity:.95 !important}

/* ── MOBILE HAMBURGER MENU ── */
.mob-menu-btn{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer !important;padding:6px;z-index:301;position:relative}
.mob-menu-btn span{display:block;width:24px;height:1.5px;background:rgba(255,248,235,.9);transition:all .35s;border-radius:2px}
#nav .mob-menu-btn span{background:rgba(255,248,235,.9)}
#nav.s .mob-menu-btn span{background:rgba(255,248,235,.95)}
.mob-menu-btn.open span:nth-child(1){transform:translateY(6.5px) rotate(45deg)}
.mob-menu-btn.open span:nth-child(2){opacity:0;transform:scaleX(0)}
.mob-menu-btn.open span:nth-child(3){transform:translateY(-6.5px) rotate(-45deg)}
.mob-nav-overlay{position:fixed;inset:0;background:rgba(28,20,10,.97);backdrop-filter:blur(24px);z-index:299;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2.5rem;opacity:0;pointer-events:none;transition:opacity .35s ease}
.mob-nav-overlay.open{opacity:1;pointer-events:all}
.mob-nav-overlay a{font-family:'Cormorant Garamond',Georgia,serif;font-size:clamp(28px,6vw,42px);font-weight:300;color:rgba(255,248,235,.9);text-decoration:none;transition:color .3s}
.mob-nav-overlay a:hover{color:#C4A068}
.mob-nav-overlay .mob-cta{font-family:'Jost',sans-serif;font-size:10px;font-weight:300;letter-spacing:.22em;text-transform:uppercase;padding:.85rem 2.5rem;border:1px solid rgba(196,160,104,.6);color:#DEC898;margin-top:1rem}
@media(max-width:900px){.mob-menu-btn{display:flex !important}.nav-links{display:none !important}.nav-cta{display:none !important}.nav-lang{display:none !important}}

/* ── PAGE COMMON ── */
.page-section{max-width:1440px;margin:0 auto;padding:4rem 4rem 8rem}
.page-title-block{padding:11rem 0 3rem;border-bottom:1px solid rgba(196,160,104,.3);margin-bottom:5rem}
.page-title-block .lbl{color:#C4A068}
.page-title-block .lbl::before{background:#C4A068}
.page-title-block .sh{color:#28282E}
.page-title-block .sh em{color:#9A7040}

/* ── FILTER BAR (büyütülmüş) ── */
.filter-bar{display:flex;flex-wrap:wrap;gap:1.2rem;align-items:flex-end;background:rgba(255,255,255,.6);backdrop-filter:blur(12px);border:1px solid rgba(196,160,104,.28);padding:2.4rem 3rem;margin-bottom:4rem;border-radius:2px}
.filter-group{display:flex;flex-direction:column;gap:.55rem;flex:1;min-width:180px}
.filter-group label{font-size:9px;font-weight:400;letter-spacing:.28em;text-transform:uppercase;color:#C4A068}
.filter-group select,.filter-group input[type="date"]{font-family:'Jost',sans-serif;font-size:14px;font-weight:300;color:#28282E;background:transparent;border:none;border-bottom:1.5px solid rgba(196,160,104,.5);padding:.7rem 0;outline:none;cursor:pointer !important;-webkit-appearance:none;appearance:none;width:100%;transition:border-color .3s}
.filter-group select option{background:#EDE8DC;color:#28282E}
.filter-group select:focus,.filter-group input:focus{border-color:#C4A068}
.filter-btn{font-family:'Jost',sans-serif;font-size:10px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;padding:1.1rem 3rem;background:#C4A068;color:#fff;border:none;cursor:pointer !important;transition:background .3s;align-self:flex-end;white-space:nowrap;border-radius:1px}
.filter-btn:hover{background:#9A7040}

/* ── TOUR GRID ── */
.tour-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-bottom:4rem}
.ec{cursor:pointer !important;overflow:hidden}
.eci{aspect-ratio:3/4;position:relative;overflow:hidden}
.ecb{position:absolute;inset:0;transition:transform .9s cubic-bezier(.25,.46,.45,.94)}
.ec:hover .ecb{transform:scale(1.08)}
.eco{position:absolute;inset:0;background:linear-gradient(to top,rgba(10,8,20,.88) 0%,rgba(10,8,20,.05) 55%,transparent 100%)}
.ecarr{position:absolute;top:1.25rem;right:1.25rem;width:34px;height:34px;border:1px solid rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center;opacity:0;transform:translateY(-6px);transition:all .4s}
.ec:hover .ecarr{opacity:1;transform:translateY(0)}
.ecarr svg{width:12px;height:12px;stroke:rgba(255,255,255,.7);fill:none;stroke-width:1.5}
.ecinfo{position:absolute;bottom:0;left:0;right:0;padding:1.75rem 1.5rem}
.ecn{font-size:8px;font-weight:300;letter-spacing:.25em;text-transform:uppercase;color:#DEC898;margin-bottom:.6rem}
.ect{font-family:'Cormorant Garamond',Georgia,serif;font-size:21px;font-weight:300;color:#fff;line-height:1.2;margin-bottom:.35rem;transition:transform .4s}
.ec:hover .ect{transform:translateY(-3px)}
.ecs{font-size:10px;font-weight:300;letter-spacing:.06em;color:rgba(255,255,255,.42)}
.bg-h{background:linear-gradient(155deg,#7090A8 0%,#405870 45%,#203848 100%)}
.bg-s{background:linear-gradient(155deg,#708858 0%,#506840 45%,#304820 100%)}
.bg-c{background:linear-gradient(155deg,#A07858 0%,#785838 45%,#503818 100%)}
.bg-p{background:linear-gradient(155deg,#806898 0%,#604878 45%,#402858 100%)}

/* ── ABOUT (hakkimizda) ── */
.about-grid{display:grid;grid-template-columns:1fr 1fr;gap:7rem;align-items:center}
.about-img{width:100%;max-height:100%;object-fit:cover;align-self:center}
.about-text{max-width:620px}
.about-text p{font-family:'Cormorant Garamond',Georgia,serif;font-size:20px;font-style:italic;line-height:2.1;color:#3a3a46;margin-bottom:2rem}
.about-text p:first-child{font-size:24px;color:#1a1a20;font-style:normal}

/* ── CONTACT ── */
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:8rem;padding-top:2rem}
.contact-info-col h3{font-family:'Cormorant Garamond',Georgia,serif;font-size:clamp(28px,3vw,44px);font-weight:300;color:#28282E;margin-bottom:3rem;line-height:1.2}
.contact-info-col h3 em{font-style:italic;color:#9A7040}
.ci-block{margin-bottom:2.5rem}
.ci-label{font-size:8px;font-weight:400;letter-spacing:.28em;text-transform:uppercase;color:#C4A068;margin-bottom:.5rem;display:flex;align-items:center;gap:.85rem}
.ci-label::before{content:'';width:22px;height:1px;background:#C4A068}
.ci-value{font-family:'Cormorant Garamond',Georgia,serif;font-size:16px;font-weight:300;color:#28282E;line-height:1.6}
.contact-form-col h3{font-family:'Cormorant Garamond',Georgia,serif;font-size:clamp(22px,2.5vw,36px);font-weight:300;color:#28282E;margin-bottom:2.5rem;line-height:1.2}
.form-section-title{font-family:'Cormorant Garamond',Georgia,serif;font-size:20px;font-weight:300;color:#28282E;margin:2.5rem 0 1.5rem;padding-top:2rem;border-top:1px solid rgba(196,160,104,.25);font-style:italic}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
.form-group{margin-bottom:1.5rem}
.form-group label{display:block;font-size:8px;font-weight:400;letter-spacing:.28em;text-transform:uppercase;color:#C4A068;margin-bottom:.5rem}
.form-group input,.form-group select,.form-group textarea{font-family:'Jost',sans-serif;font-size:13px;font-weight:300;color:#28282E;background:transparent;border:none;border-bottom:1px solid rgba(196,160,104,.35);padding:.6rem 0;width:100%;outline:none;transition:border-color .3s;resize:none;-webkit-appearance:none;appearance:none}
.form-group select option{background:#EDE8DC}
.form-group input::placeholder,.form-group textarea::placeholder{color:rgba(40,40,46,.35)}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{border-color:#C4A068}
.form-group textarea{min-height:110px;background:rgba(255,255,255,.4);padding:.8rem;border:1px solid rgba(196,160,104,.2)}
.submit-btn{font-family:'Jost',sans-serif;font-size:9px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;padding:1rem 3rem;background:transparent;color:#28282E;border:1px solid rgba(40,40,46,.4);cursor:pointer !important;display:inline-flex;align-items:center;gap:1rem;position:relative;overflow:hidden;transition:color .4s;margin-top:.5rem}
.submit-btn::before{content:'';position:absolute;inset:0;background:#28282E;transform:translateX(-100%);transition:transform .45s cubic-bezier(.25,.46,.45,.94)}
.submit-btn span{position:relative;z-index:1}
.submit-btn:hover{color:#fff}
.submit-btn:hover::before{transform:translateX(0)}
.cta-center{text-align:center;padding:2rem 0 4rem}
.btn-e{font-size:9px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;padding:.9rem 2.25rem;border:1px solid rgba(40,40,46,.4);color:#28282E;background:transparent;cursor:pointer !important;display:inline-flex;align-items:center;gap:1rem;position:relative;overflow:hidden;transition:color .4s;text-decoration:none}
.btn-e::before{content:'';position:absolute;inset:0;background:#28282E;transform:translateX(-100%);transition:transform .45s cubic-bezier(.25,.46,.45,.94)}
.btn-e span,.btn-e svg{position:relative;z-index:1}
.btn-e:hover{color:#fff}
.btn-e:hover::before{transform:translateX(0)}

/* ── PAGE-SPECIFIC BACKGROUNDS ── */
body.page-butik{background:#8FA888 !important}
body.page-butik .page-title-block .sh,
body.page-butik .page-title-block .lbl,
body.page-butik .ect,
body.page-butik .ecs,
body.page-butik .ecn{color:#fff !important}
body.page-butik .page-title-block .sh em{color:#d4edcc !important}
body.page-butik .page-title-block{border-bottom-color:rgba(255,255,255,.3) !important}

body.page-rotalar{background:#B8CDB0 !important}
body.page-rotalar .page-title-block .sh,
body.page-rotalar .page-title-block .lbl{color:#1a3a15 !important}
body.page-rotalar .page-title-block{border-bottom-color:rgba(26,58,21,.25) !important}
body.page-rotalar .filter-bar{background:rgba(255,255,255,.45) !important;border-color:rgba(26,58,21,.2) !important}
body.page-rotalar .filter-group label{color:#3a6b35 !important}
body.page-rotalar .filter-group select,
body.page-rotalar .filter-group input[type="date"]{border-bottom-color:rgba(26,58,21,.4) !important;color:#1a3a15 !important}
body.page-rotalar .filter-btn{background:#3a6b35 !important}
body.page-rotalar .filter-btn:hover{background:#1a3a15 !important}

body.page-iletisim{background:#EDE5D8 !important}

/* ── RESPONSIVE ── */
@media(max-width:768px){.tour-grid{grid-template-columns:1fr 1fr}.contact-grid{grid-template-columns:1fr;gap:3rem}.about-grid{grid-template-columns:1fr;gap:3rem}.filter-bar{flex-direction:column}.page-section{padding:2rem 1.5rem 5rem}.page-title-block{padding:8rem 0 2rem}.form-row{grid-template-columns:1fr}}
@media(max-width:480px){.tour-grid{grid-template-columns:1fr}}
</style>
"""
MOB_HTML="""
<div class="mob-nav-overlay" id="mobNav">
  <a href="/butik-grup-turlari.html">Butik Grup Turları</a>
  <a href="/rotalar.html">Rotalar</a>
  <a href="/hakkimizda.html">Hakkımızda</a>
  <a href="/iletisim.html">İletişim</a>
  <a href="/seyahatini-planla.html" class="mob-cta">Seyahatini Planla</a>
</div>
"""
MOB_JS="""
<script>
(function(){
  var btn=document.getElementById('mobMenuBtn');
  var ov=document.getElementById('mobNav');
  if(!btn||!ov)return;
  btn.addEventListener('click',function(e){e.stopPropagation();btn.classList.toggle('open');ov.classList.toggle('open')});
  ov.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){btn.classList.remove('open');ov.classList.remove('open')})});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){btn.classList.remove('open');ov.classList.remove('open')}});
})();
</script>
"""
def inject_mob(nav):
    return nav.replace('<div class="nav-r">', '<div class="nav-r"><button class="mob-menu-btn" id="mobMenuBtn" aria-label="Menü"><span></span><span></span><span></span></button>')
def page_template(head, nav, footer, body, title="Sundora Travel", body_class=""):
    body_attr = f' class="{body_class}"' if body_class else ''
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
{head}
<title>{title} — travel &amp; beyond</title>
{PAGE_STYLES}
</head>
<body{body_attr}>
{MOB_HTML}
{inject_mob(nav)}
{body}
{footer}
<script>
const nav=document.getElementById('nav');
if(nav) window.addEventListener('scroll',function(){{nav.classList.toggle('s',scrollY>80)}});
</script>
{MOB_JS}
</body>
</html>"""
def make_rotalar(head,nav,footer):
    c=build_tour_cards()
    body=f"""
<main><div class="page-section">
  <div class="page-title-block"><div class="lbl">Keşfet</div><h1 class="sh">Tüm <em>Rotalar</em></h1></div>
  <div class="filter-bar">
    <div class="filter-group"><label>Destinasyon</label><select><option value="">Tüm Destinasyonlar</option><option>Asya</option><option>Avrupa</option><option>Afrika</option><option>Amerika</option><option>Avustralya</option><option>Ortadoğu</option><option>Kutup Bölgeleri</option></select></div>
    <div class="filter-group"><label>Tarih</label><input type="date"/></div>
    <div class="filter-group"><label>Aktivite</label><select><option value="">Tüm Aktiviteler</option><option>Kültür &amp; Sanat</option><option>Lezzet &amp; Şarap</option><option>Safari</option><option>Spa &amp; Sağlık</option><option>Tropik Adalar</option><option>Kış Bölgeleri</option></select></div>
    <div class="filter-group"><label>Seyahat Tarzı</label><select><option>Tüm Seyahat Tarzları</option><option>Grup Turu</option><option>Kişiye Özel</option></select></div>
    <button class="filter-btn">Ara</button>
  </div>
  <div class="tour-grid">{c}</div>
  <div class="cta-center"><a href="/butik-grup-turlari.html" class="btn-e"><span>Tüm Popüler Programlar</span><svg viewBox="0 0 16 16" width="12" height="12" stroke="currentColor" fill="none" stroke-width="1.5"><line x1="0" y1="8" x2="12" y2="8"></line><polyline points="8,4 12,8 8,12"></polyline></svg></a></div>
</div></main>"""
    return page_template(head,nav,footer,body,"Rotalar | Sundora Travel", body_class="page-rotalar")
def make_hakkimizda(head,nav,footer):
    body="""
<main><div class="page-section">
  <div class="page-title-block"><div class="lbl">Biz Kimiz</div><h1 class="sh">Hakkımızda</h1></div>
  <div class="about-grid">
    <div class="about-text">
      <p>Seyahat, bizim için yalnızca bir destinasyona ulaşmak değil; doğru planlandığında hayat boyu hatırlanacak bir deneyime dönüşen özel bir yolculuktur.</p>
      <p>Sundora Travel, dünya turizmine duyduğu derin ilgi, yıllara dayanan sektör tecrübesi ve global bakış açısıyla, klasik seyahat anlayışının ötesine geçmek amacıyla kurulmuştur.</p>
      <p>Ekibimiz; turizm, uluslararası satış ve global operasyonlar alanlarında, farklı coğrafyalarda deneyim kazanmış profesyonellerden oluşur. Bu birikim sayesinde, dünyanın dört bir yanında en doğru iş ortaklarıyla çalışır, her detayı titizlikle planlanmış seyahatler planlarız.</p>
      <p>Bizim için her yolculuk, kişiye özeldir. Hazır paketler yerine, misafirlerimizin beklentilerini anlayarak onlara özel rotalar oluştururuz. Çünkü gerçek lüksün; seçenek bolluğu değil, doğru seçim olduğunu biliyoruz.</p>
      <p>Sundora'nın yaklaşımı; görünmeyen detaylarda fark yaratan, süreci zahmetsiz hale getiren, ve her anında güven veren bir seyahat deneyimi sunmaktır.</p>
      <p>Bugün geldiğimiz noktada, yalnızca bir seyahat planlamıyor; misafirlerimizin beklentilerine ve hayallerine uyum sağlayan, onlara özel seyahatler planlıyoruz.</p>
    </div>
    <img src="/hakkimizda.jpg" alt="Sundora Travel" class="about-img">
  </div>
</div></main>"""
    return page_template(head,nav,footer,body,"Hakkımızda | Sundora Travel")
def make_seyahatini_planla(head,nav,footer):
    body="""
<main><div class="page-section">
  <div class="page-title-block"><div class="lbl">Başlayalım</div><h1 class="sh">Seyahatini <em>Planla</em></h1></div>
  <div class="contact-grid">
    <div class="contact-info-col">
      <h3>Size <em>özel</em> bir<br>seyahat<br>planlayalım.</h3>
      <div class="ci-block"><div class="ci-label">Adres</div><div class="ci-value">—</div></div>
      <div class="ci-block"><div class="ci-label">Telefon</div><div class="ci-value">—</div></div>
      <div class="ci-block"><div class="ci-label">E-Posta</div><div class="ci-value">support@sundoratravel.com</div></div>
    </div>
    <div class="contact-form-col">
      <h3>İletişim Detayları</h3>
      <div class="form-group"><label>İsim Soyisim</label><input type="text" placeholder="Adınız ve soyadınız"/></div>
      <div class="form-group"><label>Cep Telefonu</label><input type="tel" placeholder="+90 5__ ___ __ __"/></div>
      <div class="form-group"><label>E-Posta Adresi</label><input type="email" placeholder="ornek@mail.com"/></div>
      <div class="form-section-title">Seyahat Detayları</div>
      <div class="form-group"><label>Destinasyon</label><select><option value="">Seçiniz</option><option>Afrika</option><option>Amerika</option><option>Asya</option><option>Avrupa</option><option>Avustralya</option><option>Ortadoğu</option><option>Kutup Bölgeleri</option></select></div>
      <div class="form-row">
        <div class="form-group"><label>Ay Seçiniz</label><select><option value="">Ay</option><option>Ocak</option><option>Şubat</option><option>Mart</option><option>Nisan</option><option>Mayıs</option><option>Haziran</option><option>Temmuz</option><option>Ağustos</option><option>Eylül</option><option>Ekim</option><option>Kasım</option><option>Aralık</option></select></div>
        <div class="form-group"><label>Yıl Seçiniz</label><select><option value="">Yıl</option><option>2026</option><option>2027</option><option>2028</option><option>2029</option></select></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Kalınacak Gece Sayısı</label><input type="number" min="1" placeholder="Gece sayısı"/></div>
        <div class="form-group"><label>Kişi Sayısı</label><input type="number" min="1" placeholder="Kişi sayısı"/></div>
      </div>
      <div class="form-group"><label>Kişi Başına Bütçeniz?</label><select><option value="">Bütçe Seçiniz</option><option>Kişi başı 1500$ - 2000$</option><option>Kişi başı 2000$ - 3000$</option><option>Kişi başı 3000$ - 4000$</option><option>Kişi başı 4000$ - 5000$</option><option>Kişi başı 5000$ - 6000$</option><option>Kişi başı 6000$'dan fazla</option></select></div>
      <div class="form-group"><label>Notunuz</label><textarea placeholder="Notunuz"></textarea></div>
      <button class="submit-btn" type="button"><span>Bizimle İletişime Geç</span></button>
    </div>
  </div>
</div></main>"""
    return page_template(head,nav,footer,body,"Seyahatini Planla | Sundora Travel")
def make_butik(head,nav,footer):
    c=build_tour_cards()
    body=f"""<main><div class="page-section"><div class="page-title-block"><div class="lbl">Özenle Seçilmiş</div><h1 class="sh">Butik Grup <em>Turları</em></h1></div><div class="tour-grid">{c}</div></div></main>"""
    return page_template(head,nav,footer,body,"Butik Grup Turları | Sundora Travel", body_class="page-butik")
def make_kisiye(head,nav,footer):
    c=build_tour_cards()
    body=f"""<main><div class="page-section"><div class="page-title-block"><div class="lbl">Sadece Sizin İçin</div><h1 class="sh">Kişiye Özel <em>Seyahatler</em></h1></div><div class="tour-grid">{c}</div></div></main>"""
    return page_template(head,nav,footer,body,"Kişiye Özel Seyahatler | Sundora Travel")
def make_iletisim(head,nav,footer):
    body="""
<main><div class="page-section">
  <div class="page-title-block"><div class="lbl">Ulaşın</div><h1 class="sh"><em>İletişim</em></h1></div>
  <div class="contact-grid">
    <div class="contact-info-col">
      <h3>Birlikte <em>harika</em><br>şeyler<br>tasarlayalım.</h3>
      <div class="ci-block"><div class="ci-label">Adres</div><div class="ci-value">—</div></div>
      <div class="ci-block"><div class="ci-label">Telefon</div><div class="ci-value">—</div></div>
      <div class="ci-block"><div class="ci-label">E-Posta</div><div class="ci-value"><a href="mailto:support@sundoratravel.com" style="color:#9A7040;text-decoration:none">support@sundoratravel.com</a></div></div>
      <div class="ci-block"><div class="ci-label">Instagram</div><div class="ci-value"><a href="https://instagram.com/sundoratravel" target="_blank" style="color:#9A7040;text-decoration:none">@sundoratravel</a></div></div>
      <div class="ci-block"><div class="ci-label">TikTok</div><div class="ci-value"><a href="https://tiktok.com/@sundoratravel" target="_blank" style="color:#9A7040;text-decoration:none">@sundoratravel</a></div></div>
    </div>
    <div class="contact-form-col">
      <h3>Mesaj Gönderin</h3>
      <div class="form-group"><label>İsim Soyisim</label><input type="text" placeholder="Adınız ve soyadınız"/></div>
      <div class="form-group"><label>E-Posta</label><input type="email" placeholder="ornek@mail.com"/></div>
      <div class="form-group"><label>Mesajınız</label><textarea placeholder="Mesajınız"></textarea></div>
      <button class="submit-btn" type="button"><span>Gönder</span></button>
    </div>
  </div>
</div></main>"""
    return page_template(head,nav,footer,body,"İletişim | Sundora Travel", body_class="page-iletisim")
def main():
    print("\n🌍  Sundora Travel — Sayfa Üretici v5 Başlatıldı\n")
    if not os.path.exists(PUBLIC_DIR):
        print("HATA: public/ klasörü bulunamadı."); return
    print(f"📖  {INDEX_PATH} okunuyor...")
    html = read_index()
    print("✂️   Cursor kaldırılıyor...");         html = remove_cursor(html)
    print("🖼️   Hero boşluğu düzeltiliyor...");   html = fix_hero_gap(html)
    print("🎨  Nav arka planı güncelleniyor...");  html = update_nav_style(html)
    print("🦶  Footer güncelleniyor...");          html = update_footer(html)
    print("📸  Hero görseli güncelleniyor...");    html = update_hero_image(html)
    print("🗑️   Gereksiz bölümler kaldırılıyor..."); html = remove_sections(html)
    print("🃏  Deneyim kartları güncelleniyor..."); html = update_exp_cards(html)
    print("✏️   Metin/link güncelleniyor...");     html = update_exp_section_text(html)
    print("🔗  Nav & hero butonları güncelleniyor..."); html = build_new_nav(html); html = update_hero_btns(html)
    # Anasayfaya sayfa stillerini ekle
    html = html.replace('</head>', PAGE_STYLES + '</head>')
    # Hamburger butonunu nav-r'ye ekle
    nav_html = extract_nav(html)
    mob_nav_injected = inject_mob(nav_html)
    html = html.replace(nav_html, mob_nav_injected)
    # Mob overlay'i ve JS'i ekle - basit string replace ile
    body_open = html.find('<body')
    body_open_end = html.find('>', body_open) + 1
    html = html[:body_open_end] + '\n' + MOB_HTML + html[body_open_end:]
    html = html.replace('</body>', MOB_JS + '\n</body>')
    write_file("index.html", html)
    head=extract_head(html); nav=extract_nav(html); footer=extract_footer(html)
    print("\n📄  Sayfalar oluşturuluyor...")
    write_file("rotalar.html",              make_rotalar(head,nav,footer))
    write_file("hakkimizda.html",           make_hakkimizda(head,nav,footer))
    write_file("seyahatini-planla.html",    make_seyahatini_planla(head,nav,footer))
    write_file("butik-grup-turlari.html",   make_butik(head,nav,footer))
    write_file("kisiye-ozel-seyahatler.html", make_kisiye(head,nav,footer))
    write_file("iletisim.html",             make_iletisim(head,nav,footer))
    print("\n✅  Tüm sayfalar güncellendi!\n")
if __name__ == "__main__":
    main()
