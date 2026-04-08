// ============================================================
// common.js - ヘッダー・フッター共通パーツ
// career-life-design/assets/js/common.js
// ============================================================

(function () {

  // ── ヘッダーHTML ──────────────────────────────────────────
  var headerHTML = `
<header class="site-header">
  <div class="header-inner">
    <a class="site-logo" href="/">
      協進化ジャーナル
      <span>Career &amp; Life Design Lab</span>
    </a>
    <nav class="header-nav">
      <a href="/journal/">ジャーナル</a>
      <a href="/books/">書籍</a>
      <a href="/qa/">Q&amp;A</a>
      <a href="/shop/">ショップ</a>
      <a href="/about/">研究所</a>
      <a href="/contact/">お問い合わせ</a>
    </nav>
  </div>
</header>`;

  // ── フッターHTML ──────────────────────────────────────────
  var footerHTML = `
<footer class="site-footer">
  <div class="footer-inner">
    <p class="footer-logo">協進化ジャーナル</p>
    <p class="footer-tagline">生きることは、育てること。</p>
    <div class="footer-links">
      <a href="/journal/">ジャーナル</a>
      <a href="/books/">書籍</a>
      <a href="/qa/">Q&amp;A</a>
      <a href="/shop/">ショップ</a>
      <a href="/about/">研究所</a>
      <a href="https://kyoshinkajournal.substack.com" target="_blank">Substack</a>
      <a href="/contact/">お問い合わせ</a>
    </div>
  </div>
  <div class="footer-bottom">
    <p class="footer-copy">© 2026 キャリア＆ライフデザイン研究所</p>
    <p class="footer-copy" style="margin-top:8px;font-size:0.75rem;">
      <a href="/legal/" style="color:#aaa;text-decoration:none;margin:0 8px;">特定商取引法に基づく表示</a>
      <a href="/privacy/" style="color:#aaa;text-decoration:none;margin:0 8px;">プライバシーポリシー</a>
    </p>
  </div>
</footer>`;

  // ── 挿入 ─────────────────────────────────────────────────
  var headerEl = document.getElementById('site-header');
  if (headerEl) headerEl.outerHTML = headerHTML;

  var footerEl = document.getElementById('site-footer');
  if (footerEl) footerEl.outerHTML = footerHTML;

  // ── 現在のページをナビでアクティブ表示 ───────────────────
  var path = window.location.pathname;
  document.querySelectorAll('.header-nav a').forEach(function(a) {
    if (a.getAttribute('href') !== '/' && path.startsWith(a.getAttribute('href'))) {
      a.style.color = 'var(--gold)';
      a.style.fontWeight = '700';
    }
  });

})();
