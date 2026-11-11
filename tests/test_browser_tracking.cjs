// 실제 첫 화면·모델 페이지 수집 코드를 실행해 브라우저 저장소/전송 경계를 검사한다.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { webcrypto } = require('node:crypto');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const beta = fs.readFileSync(path.join(root, 'beta.html'), 'utf8');
const start = beta.indexOf('    const usageLog = (() => {');
const scripts = {
  home: beta.slice(start, beta.indexOf('\n    // 의견 보내기:', start)),
  model: fs.readFileSync(path.join(root, 'track.js'), 'utf8'),
};
function storage(data = new Map(), blocked = false) {
  return { data, getItem(k) { if (blocked) throw Error('blocked'); return data.get(k) ?? null; },
    setItem(k,v) { if (blocked) throw Error('blocked'); data.set(k,v); },
    removeItem(k) { if (blocked) throw Error('blocked'); data.delete(k); } };
}
function open(kind, { local = storage(), session = storage(), now = Date.UTC(2026,10,11), query = '', bot = false } = {}) {
  const listeners = {}, payloads = [];
  const context = {
    URL, URLSearchParams, Blob, Uint8Array, crypto: webcrypto,
    Date: { now: () => now }, localStorage: local, sessionStorage: session,
    location: { host: 'camerabridge.io', pathname: kind === 'home' ? '/' : '/ko/leica/m6/', search: query },
    navigator: { webdriver: bot, userAgent: 'Mozilla/5.0', sendBeacon(url, body) { assert.equal(url, '/api/usage'); payloads.push(body.text()); return true; } },
    document: { referrer: '', documentElement: { lang: 'ko', scrollHeight: 1000 }, visibilityState: 'hidden',
      addEventListener(name, fn) { listeners[name] = fn; } },
    window: { scrollY: 0, innerHeight: 800, matchMedia: () => ({matches: false}),
      addEventListener(name, fn) { listeners[name] = fn; } },
    setTimeout() {}, uiState: {locale: 'ko', currency: 'KRW'}, state: {}, isNarrowScreen: () => false,
  };
  vm.runInNewContext(scripts[kind], context);
  return { local, session, async send() { listeners.pagehide?.(); return Promise.all(payloads.splice(0).map(async p => JSON.parse(await p))); } };
}
test('첫 화면 → 모델 → 다음 날 재방문: 브라우저 유지, 방문 번호만 변경', async () => {
  const first = open('home');
  const [a] = await first.send();
  const second = open('model', {local: first.local, session: first.session});
  const [b] = await second.send();
  const next = open('home', {local: first.local, now: Date.UTC(2026,10,12)});
  const [c] = await next.send();
  assert.match(a.vid, /^[a-f0-9]{32}$/);
  assert.equal(a.vid, b.vid); assert.equal(a.sid, b.sid);
  assert.equal(a.vid, c.vid); assert.notEqual(a.sid, c.sid);
  assert.notEqual(a.vid, (await open('model').send())[0].vid);
});
for (const kind of Object.keys(scripts)) {
  test(`${kind}: 저장소 차단에도 페이지/기록 유지, 브라우저 식별 생략`, async () => {
    const page = open(kind, {local: storage(new Map(), true), session: storage(new Map(), true)});
    assert.equal((await page.send())[0].vid, null);
  });
  test(`${kind}: 1년 만료·저장소 삭제 시 새 식별값`, async () => {
    const page = open(kind), [first] = await page.send();
    const later = open(kind, {local: page.local, now: Date.UTC(2027,10,12)});
    assert.notEqual(first.vid, (await later.send())[0].vid);
    page.local.removeItem('cb_browser');
    assert.notEqual(first.vid, (await open(kind, {local: page.local}).send())[0].vid);
  });
  test(`${kind}: 기록 끄기·봇은 식별값 생성/전송 안 함`, async () => {
    const local = storage();
    await open(kind, {local}).send();
    const off = open(kind, {local, query: '?notrack=1'});
    assert.deepEqual(await off.send(), []); assert.equal(local.getItem('cb_browser'), null);
    assert.deepEqual(await open(kind, {local}).send(), []);
    assert.equal((await open(kind, {local, query: '?notrack=0'}).send()).length, 1);
    assert.deepEqual(await open(kind, {local: storage(new Map(), true), query: '?notrack=1'}).send(), []);
    const bot = open(kind, {bot: true});
    assert.deepEqual(await bot.send(), []); assert.equal(bot.local.getItem('cb_browser'), null);
  });
  test(`${kind}: 다른 탭에서 기록을 꺼도 전송 중단`, async () => {
    const page = open(kind);
    page.local.setItem('cb_notrack', '1');
    assert.deepEqual(await page.send(), []);
  });
}
