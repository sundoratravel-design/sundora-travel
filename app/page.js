import "./sundora.css";

export default function Home() {
  return (
    <main>
      <nav className="nav">
        <div className="logo">Sundora<span>.</span>Travel</div>
        <ul className="nav-links">
          <li><a href="#">Turlar</a></li>
          <li><a href="#">Deneyimler</a></li>
          <li><a href="#">Sundora Özel</a></li>
          <li><a href="#">Hakkımızda</a></li>
        </ul>
        <button className="nav-cta">Tur Planla</button>
      </nav>
      <section className="hero">
        <div className="hero-left">
          <div className="hero-tag">Butik Seyahat Acentası</div>
          <h1 className="hero-h1">Her Yolculuk<br/>Bir <em>Hikâye</em><br/>Taşır</h1>
          <p className="hero-sub">Sundora ile seyahat etmek, sadece bir yere varmak değil — hayatınıza işleyen anları birlikte yaratmaktır.</p>
          <div className="hero-actions">
            <button className="btn-primary">Turları Keşfet</button>
            <button className="btn-ghost">Bize Yazın →</button>
          </div>
        </div>
        <div className="hero-right">
          <div className="hero-visual"></div>
          <div className="hero-gold-line"></div>
          <div className="hero-caption">
            <div className="hero-caption-loc">Serengeti, Tanzania</div>
            <div className="hero-caption-title">Özel Safari Rotası · 10 Gece</div>
          </div>
        </div>
      </section>
      <div className="stats">
        <div className="stat"><div className="stat-num">12+</div><div className="stat-label">Destinasyon</div></div>
        <div className="stat"><div className="stat-num">100%</div><div className="stat-label">Özel Planlama</div></div>
        <div className="stat"><div className="stat-num">TR · EN</div><div className="stat-label">İki Dil Desteği</div></div>
        <div className="stat"><div className="stat-num">24/7</div><div className="stat-label">Yolculuk Desteği</div></div>
      </div>
      <section className="section">
        <div className="section-header">
          <div><div className="section-tag">Öne Çıkan Turlar</div><h2 className="section-h2">Seçilmiş Rotalar</h2></div>
          <button className="see-all">Tümünü Gör →</button>
        </div>
        <div className="tours-grid">
          <div className="tour-card tour-big">
            <div className="tour-img img-africa"><div className="tour-badge">En Çok Tercih Edilen</div><div className="tour-nights">10 Gece</div></div>
            <div className="tour-region">Afrika · Tanzania</div>
            <div className="tour-name">Serengeti&apos;nin Sessiz Kalbi</div>
            <div className="tour-desc">Savananın ufkuna uzanan gün batımlarında, vahşi yaşamın ortasında lüks çadır konaklama.</div>
          </div>
          <div className="tour-card">
            <div className="tour-img img-ocean"><div className="tour-badge">Yeni</div><div className="tour-nights">7 Gece</div></div>
            <div className="tour-region">Asya · Maledivler</div>
            <div className="tour-name">Mercanların Sessizliği</div>
            <div className="tour-desc">Turkuaz suların üzerinde, dünyadan kopuk bir ada dinlencesi.</div>
          </div>
          <div className="tour-card">
            <div className="tour-img img-europe"><div className="tour-badge">Butik Grup</div><div className="tour-nights">8 Gece</div></div>
            <div className="tour-region">Avrupa · Toskana</div>
            <div className="tour-name">Toskana&apos;nın Kadim Tadı</div>
            <div className="tour-desc">Şarap, zeytin ve tarih — İtalya&apos;nın kırsalında butik kültür turu.</div>
          </div>
        </div>
      </section>
      <div className="philosophy">
        <div className="phil-left">
          <div className="section-tag">Felsefemiz</div>
          <p className="phil-quote">&ldquo;Seyahat bir ayrıcalık değil, bir bakış açısıdır.&rdquo;</p>
          <p className="phil-body">Sundora olarak her rotayı, her konaklamayı ve her deneyimi yalnızca size özel bir hikâye gibi tasarlıyoruz.</p>
          <button className="btn-outline">Bizi Tanıyın</button>
        </div>
        <div className="phil-right">
          <div className="pillar"><div className="pillar-num">01</div><div><div className="pillar-title">Kişiye Özel Rota</div><div className="pillar-desc">Her yolculuk sizin için sıfırdan tasarlanır.</div></div></div>
          <div className="pillar"><div className="pillar-num">02</div><div><div className="pillar-title">Yerel Bağlantı</div><div className="pillar-desc">Gidilen yerin dokusunu hissettiren rehberler.</div></div></div>
          <div className="pillar"><div className="pillar-num">03</div><div><div className="pillar-title">Sürekli Destek</div><div className="pillar-desc">Yolculuğun her anında, 7 gün yanınızdayız.</div></div></div>
        </div>
      </div>
      <div className="testimonial">
        <span className="quote-mark">&ldquo;</span>
        <p className="quote-text">Sundora ile yaptığımız Tanzanya turu, hayatımda gördüğüm en iyi organizasyondu. Her detay düşünülmüştü — bize sadece hissetmek kaldı.</p>
        <div className="quote-author"><span>—</span> Ayşe K., İstanbul · Kurumsal Tur Grubu</div>
      </div>
      <footer className="footer">
        <div><div className="footer-logo">Sundora<span>.</span>Travel</div><p className="footer-tagline">Hayalinizdeki yolculuğu birlikte tasarlayalım.</p></div>
        <div><div className="footer-heading">Turlar</div><ul className="footer-links"><li>Afrika Safaris</li><li>Tropikal Adalar</li><li>Avrupa Kültür</li><li>Grup Turları</li></ul></div>
        <div><div className="footer-heading">Şirket</div><ul className="footer-links"><li>Hakkımızda</li><li>Felsefemiz</li><li>Blog</li><li>İletişim</li></ul></div>
        <div><div className="footer-heading">İletişim</div><ul className="footer-links"><li>info@sundoratravel.com</li><li>+90 212 000 00 00</li><li>İstanbul, Türkiye</li></ul></div>
      </footer>
      <div className="footer-bottom">
        <div className="footer-copy">© 2026 Sundora Travel.</div>
        <div className="lang-switch"><button className="lang-btn active">TR</button><button className="lang-btn">EN</button></div>
      </div>
    </main>
  );
}
