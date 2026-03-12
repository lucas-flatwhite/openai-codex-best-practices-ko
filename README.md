# openai-codex-best-practices-ko

`openai-codex-best-practices.md`를 소스 원고로 사용하는 단일 페이지 GitHub Pages 사이트입니다. 원고가 바뀌면 `scripts/build_site.py`가 HTML을 다시 생성하고, `main` 브랜치에 푸시되면 GitHub Actions가 자동으로 배포합니다.

## 파일 구조

- `openai-codex-best-practices.md`: 페이지 원고
- `scripts/build_site.py`: markdown 원고를 `dist/index.html`로 렌더링
- `styles.css`: 라이트/다크 모드를 포함한 페이지 스타일
- `script.js`: 테마 토글과 현재 섹션 하이라이트
- `.github/workflows/deploy.yml`: GitHub Pages 배포 워크플로우

## 로컬 빌드

```bash
python3 scripts/build_site.py
```

빌드가 끝나면 `dist/index.html`이 생성됩니다.

## 배포 방식

- `main` 브랜치에 변경 사항이 푸시되면 GitHub Actions가 실행됩니다.
- 워크플로우는 `dist/`를 GitHub Pages 아티팩트로 업로드하고 배포합니다.
- 저장소의 GitHub Pages 설정은 `Source: GitHub Actions`로 맞추면 됩니다.

## 콘텐츠 갱신 흐름

1. `openai-codex-best-practices.md`를 수정합니다.
2. 필요하면 로컬에서 `python3 scripts/build_site.py`로 확인합니다.
3. `main`에 반영하면 자동으로 새 버전이 배포됩니다.
