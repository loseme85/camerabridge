"""모델·통화·배송국가 전환과 로그인 재개 시 실제 알림 payload 회귀 검증."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_alert_drafts_and_login_resume():
    for relative in ('app/templates/beta.html', 'beta.html'):
        html = (ROOT / relative).read_text()
        names = ['wantContext', 'rememberWantDraft', 'renderWantForm', 'submitWantPayload', 'afterSaveLogin']
        functions = []
        for name in names:
            match = re.search(rf'(?:async )?function {name}\([^)]*\)\{{.*?\n    \}}', html, re.S)
            assert match, name
            functions.append(match.group(0))
        state = re.search(r'const wantState = .*?;', html).group(0)
        setup = '''
const assert = require('node:assert/strict');
const uiState = {currency: 'KRW', destination: 'KR'};
const calcState = {grade: 'B'};
const escapeHtml = x => String(x);
const wx = x => x;
const roundEstimate = x => Math.round(x);
const displayNameOf = (x, y) => y;
const sent = [];
const boardState = {member: {alerts_email: 'test@example.invalid'}};
const boardSend = async payload => { sent.push(payload); return {ok: true, data: {alerts: true}}; };
const renderValueCalc = () => {};
const openAlertsConsent = () => {throw Error('unexpected consent');};
const openSaveLogin = () => {};
const formatMoney = x => String(x);
const document = {getElementById: () => null};
const loadSaves = async () => {};
const location = {hash: ''};
const saveState = {pending: null, urls: new Set()};
'''
        checks = '''
(async () => {
  renderWantForm({id: 'm6'}, 3000000);
  const draft = {dataset: {wantContext: wantState.context}, querySelector: key => ({value: key.includes('grade') ? 'A' : '2500000'})};
  rememberWantDraft(draft);
  assert.match(renderWantForm({id: 'm6'}, 3300000), /value="2500000"/);
  assert.match(renderWantForm({id: 'm11'}, 9000000), /value="9000000"/);
  rememberWantDraft(draft); // 이전 DOM 이벤트가 새 문맥을 덮지 않는다.
  assert.equal(wantState.max, null);
  uiState.currency = 'USD';
  assert.match(renderWantForm({id: 'm11'}, 6500), /value="6500"/);
  wantState.max = '5000'; uiState.destination = 'US';
  assert.match(renderWantForm({id: 'm11'}, 6000), /value="6000"/);
  wantState.max = ''; // 직접 지운 입력은 재렌더링 때 추천값으로 돌아가지 않는다.
  assert.match(renderWantForm({id: 'm11'}, 6000), /data-want-max value=""/);
  const original = {action: 'want', entity: 'm6', name: 'M6', grade: 'A', max_total: 2500000, currency: 'KRW', dest: 'KR'};
  wantState.pending = original;
  await afterSaveLogin();
  assert.deepEqual(sent, [original]);
  assert.equal(wantState.pending, null);
  assert.equal(wantState.message, ''); // 다른 모델 화면에 신청 성공 문구가 나타나지 않는다.
})().catch(error => {console.error(error); process.exitCode = 1;});
'''
        result = subprocess.run(['node', '-e', setup + state + '\n' + '\n'.join(functions) + checks], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
