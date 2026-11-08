// 방문 기록 (모델 시세 페이지용): 어디서 왔는지·본 페이지·매장 링크 클릭을 /api/usage 로 (IP·쿠키 없음)
// 첫 화면(beta.html usageLog)과 같은 규칙: 같은 탭이면 sessionStorage 'cb_visit' 로 한 방문으로 묶음,
// 바깥 사이트에서 다시 들어오거나 30분 넘게 지나면 새 방문. ?notrack=1 로 연 브라우저와 검색엔진 로봇은 기록 안 함.
(function () {
  try {
    var flag = new URLSearchParams(location.search).get('notrack');
    if (flag === '1') localStorage.setItem('cb_notrack', '1');
    if (flag === '0') localStorage.removeItem('cb_notrack');
    if (localStorage.getItem('cb_notrack') === '1') return;
  } catch (error) {}
  if (navigator.webdriver || /bot|crawl|spider|slurp|headless|lighthouse|preview/i.test(navigator.userAgent || '')) return;

  var visit = null;
  try { visit = JSON.parse(sessionStorage.getItem('cb_visit') || 'null'); } catch (error) {}
  var outside = '';
  try {
    if (document.referrer) {
      var ref = new URL(document.referrer);
      if (ref.host !== location.host) outside = (ref.host + ref.pathname).replace(/\/$/, '').slice(0, 160);
    }
  } catch (error) {}
  if (!visit || !visit.sid || outside || Date.now() - (visit.last || 0) > 30 * 60 * 1000) {
    var utm = [];
    try { new URLSearchParams(location.search).forEach(function (value, key) { if (key.indexOf('utm_') === 0) utm.push(key + '=' + value); }); } catch (error) {}
    visit = { sid: Math.random().toString(36).slice(2, 10) + Date.now().toString(36), t0: Date.now(), referrer: outside,
              landing: location.pathname + (utm.length ? '?' + utm.join('&') : ''), part: 0 };
  }
  function save() { visit.last = Date.now(); try { sessionStorage.setItem('cb_visit', JSON.stringify(visit)); } catch (error) {} }
  save();

  var slug = (location.pathname.match(/\/leica\/([^/]+)\//) || [])[1] || '';
  var seconds = function () { return Math.round((Date.now() - visit.t0) / 1000); };
  var clicks = [], sends = 0, sentAt = 0, scrollMax = 0;
  function trackScroll() {
    var h = document.documentElement.scrollHeight || 1;
    scrollMax = Math.max(scrollMax, Math.min(100, Math.round((window.scrollY + window.innerHeight) / h * 100)));
  }
  window.addEventListener('scroll', trackScroll, { passive: true });
  setTimeout(trackScroll, 1500);

  function send() {
    // 첫 번째는 보기만 해도, 그 뒤로는 새 클릭이 있거나 지난번보다 15초 넘게 더 머물렀을 때 (2026-11-08: 머문 시간이 처음 탭을 벗어난 순간으로 남던 것)
    if (sends >= 8 || (sends > 0 && !clicks.length && seconds() - sentAt < 15)) return;
    sends += 1;
    sentAt = seconds();
    visit.part = (visit.part || 0) + 1;
    save();
    var body = JSON.stringify({
      sid: visit.sid, part: visit.part, page: location.pathname, locale: document.documentElement.lang || '',
      referrer: visit.referrer, landing: visit.landing, duration_s: seconds(), scroll: scrollMax, searches: [], clicks: clicks,
      mobile: window.matchMedia ? window.matchMedia('(max-width: 720px)').matches : false
    });
    clicks = [];
    try {
      if (!(navigator.sendBeacon && navigator.sendBeacon('/api/usage', new Blob([body], { type: 'application/json' })))) {
        fetch('/api/usage', { method: 'POST', headers: { 'content-type': 'application/json' }, body: body, keepalive: true }).catch(function () {});
      }
    } catch (error) {}
  }

  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[href^="http"]');
    if (!link) return;
    var host = '';
    try { host = new URL(link.href).host; } catch (error) { return; }
    if (!host || host === location.host) return;
    clicks.push({ host: host, entity: slug, q: '', s: seconds() });
  }, true);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') send(); });
  window.addEventListener('pagehide', send);
})();
