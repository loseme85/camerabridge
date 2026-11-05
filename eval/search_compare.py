"""검색 결과·시간 비교 (2026-11-05): 검색을 바꾸기 전후로 결과가 같은지, 얼마나 빨라졌는지 본다.

  python3 eval/search_compare.py dump before.json   # 바꾸기 전 (git stash 등)
  python3 eval/search_compare.py dump after.json    # 바꾼 뒤
  python3 eval/search_compare.py diff before.json after.json

검색어: 정답 세트 모델 이름(403개)과 첫 낱말, heldout 검색어, 한 낱말 검색어 묶음 — 550개 안팎
"""
import json, sys, time
sys.path.insert(0, '.'); sys.path.insert(0, 'api')
import search as S


def diff(a_path, b_path):
    import statistics
    a, b = json.load(open(a_path)), json.load(open(b_path))
    same = [q for q in a if q in b and a[q]['ids'] == b[q]['ids'] and a[q]['n'] == b[q]['n']]
    for q in a:
        if q in b and q not in same:
            print('다름', repr(q), '| 앞에만', [x for x in a[q]['ids'] if x not in b[q]['ids']][:3], '| 뒤에만', [x for x in b[q]['ids'] if x not in a[q]['ids']][:3])
    at = [a[q]['t'] for q in a if q in b]; bt = [b[q]['t'] for q in a if q in b]
    print(f"같음 {len(same)}/{len(at)} · 합계 {sum(at):.0f}초 → {sum(bt):.0f}초 · 중간값 {statistics.median(at):.2f} → {statistics.median(bt):.2f} · 1초 넘는 검색어 {sum(t > 1 for t in at)} → {sum(t > 1 for t in bt)}")


def dump():
    gold = json.load(open('eval/query_model_gold_v1.json'))
    qs = set()
    for m in gold['models'].values():
        qs.add(m.get('display_name') or '')
        qs.add(' '.join((m.get('display_name') or '').split()[:1]))
    for m in []:
        for k in ('queries', 'aliases', 'query'):
            v = m.get(k) if isinstance(m, dict) else None
            if isinstance(v, list): qs.update(x if isinstance(x, str) else x.get('q', '') for x in v)
            elif isinstance(v, str): qs.add(v)
    try:
        for x in json.load(open('eval/heldout_entity_queries.json'))['cases']:
            qs.add(x[0])
    except Exception:
        pass
    qs |= {'noctilux', 'summilux', 'summicron', 'elmarit', 'elmar', 'summaron', 'apo', 'visoflex', 'm6', 'm3', 'q2', 'sl2', 'mp', 'monochrom',
           '녹티룩스', '주미룩스', '주미크론', 'hood', 'case', 'leica', 'nocti', 'tri-elmar', 'super-angulon', 'hektor', 'thambar', 'm11', 'x2', 'cl'}
    qs = sorted(q for q in qs if q)
    S.search_from_params({"q": ["leica m6"], "limit": ["20"]})
    out = {}
    for q in qs:
        t = time.time()
        r = S.search_from_params({"q": [q], "limit": ["20"]})
        out[q] = {"t": round(time.time() - t, 3), "ids": [x.get('search_id') or x.get('link') or x.get('title') for x in r.get('results', [])],
                  "n": r.get('result_count'), "total": r.get('total_ranked')}
    json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False)
    print(len(qs), 'queries', round(sum(v['t'] for v in out.values()), 1), 's total')


if __name__ == '__main__':
    if sys.argv[1] == 'diff':
        diff(sys.argv[2], sys.argv[3])
    else:
        dump()
