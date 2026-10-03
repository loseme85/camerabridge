# camerabridge-relay

GitHub Actions(미국 서버)에서 접속이 막히는 일본 사이트를 Vercel 도쿄(hnd1)에서 대신 받아 주는 중계 서버.
카메라브릿지 본 사이트와는 다른 Vercel 프로젝트 `camerabridge-relay`.

- 호출: `GET /api/fetch?url=<대상 주소>` + 헤더 `x-relay-key: <RELAY_KEY>`, 대상 사이트에 보낼 헤더는 `x-relay-headers: {"헤더": "값"}`(JSON)
- 허용 사이트만 (`api/fetch.py`의 `ALLOWED_HOSTS`). 사이트 추가 = 한 줄 추가 후 다시 배포
- 비밀 키: Vercel 프로젝트 환경변수 `RELAY_KEY`, GitHub 저장소 비밀값 `RELAY_KEY`·`RELAY_URL`
- 배포: 이 폴더에서 `npx vercel deploy --prod` (본 사이트 git 배포와 별개)
