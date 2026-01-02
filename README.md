# studyforme (static vercel starter)

단일 페이지(index.html)를 Vercel에 **정적 배포**하기 위한 최소 구성입니다.

## 로컬에서 확인
- Python: `python -m http.server 5173`
- 접속: `http://localhost:5173`

## Vercel 배포
1. GitHub에 이 폴더 내용을 그대로 업로드(push)
2. Vercel → New Project → 해당 레포 선택
3. Framework Preset: **Other**
4. Build Command: 없음
5. Output Directory: 없음(루트에 index.html)

## 배포 후 해야 할 것
- `index.html`에서 아래 값을 실제 도메인으로 바꾸세요.
  - `https://YOUR-DOMAIN-HERE/` → 예: `https://your-project.vercel.app/`

## (선택) 아임웹 의존 줄이기(마이그레이션 준비)
`tools/download_assets.py`를 로컬에서 실행하면(인터넷 필요),
허용 도메인(imweb CDN 등)에서 정적 리소스를 내려받아 `assets/`로 로컬화하고,
치환된 HTML을 `index.localized.html`로 생성합니다.
