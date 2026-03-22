[![Deploy](https://img.shields.io/github/actions/workflow/status/lucas-flatwhite/openai-codex-best-practices-ko/deploy.yml?branch=main&label=Deploy&logo=githubactions)](https://github.com/lucas-flatwhite/openai-codex-best-practices-ko/actions/workflows/deploy.yml)
[![GitHub Pages](https://img.shields.io/github/deployments/lucas-flatwhite/openai-codex-best-practices-ko/github-pages?label=GitHub%20Pages&logo=github)](https://lucas-flatwhite.github.io/openai-codex-best-practices-ko/)

# OpenAI Codex Docs in Korean

OpenAI의 Codex 관련 문서를 한국어로 정리하고, 읽기 쉬운 정적 웹페이지로 함께 제공하는 저장소입니다. 원문의 구조와 링크는 최대한 유지하면서 설명 텍스트는 한국어로 옮기고, GitHub Pages에서 바로 읽을 수 있도록 빌드합니다.

사이트:

- [Best Practices](https://lucas-flatwhite.github.io/openai-codex-best-practices-ko/)
- [Designing Delightful Frontends with GPT-5.4](https://lucas-flatwhite.github.io/openai-codex-best-practices-ko/designing-delightful-frontends-with-gpt-5-4.html)

## 포함 문서

| 문서 | 한국어 페이지 | 원문 |
| --- | --- | --- |
| OpenAI Codex - Best Practices | [바로 읽기](https://lucas-flatwhite.github.io/openai-codex-best-practices-ko/) | [developers.openai.com/codex/learn/best-practices](https://developers.openai.com/codex/learn/best-practices) |
| Designing Delightful Frontends with GPT-5.4 | [바로 읽기](https://lucas-flatwhite.github.io/openai-codex-best-practices-ko/designing-delightful-frontends-with-gpt-5-4.html) | [developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4) |

## 이 저장소에서 하는 일

- OpenAI 문서를 한국어 마크다운으로 정리합니다.
- 여러 문서를 하나의 일관된 웹 UI로 빌드합니다.
- 각 문서 페이지 상단에서 다른 문서로 바로 이동할 수 있게 연결합니다.
- 원문 링크와 로컬 마크다운 원고를 함께 제공합니다.

## 로컬에서 빌드하기

정적 사이트는 Python 표준 라이브러리만으로 빌드합니다.

```bash
python3 scripts/build_site.py
```

빌드 결과:

- `dist/index.html`
- `dist/designing-delightful-frontends-with-gpt-5-4.html`
- `dist/*.ko.md`
- `dist/styles.css`
- `dist/script.js`

## 저장소 구조

```text
docs/
  openai-codex-best-practices.en.md
  openai-codex-best-practices.ko.md
  designing-delightful-frontends-with-gpt-5-4.en.md
  designing-delightful-frontends-with-gpt-5-4.ko.md
scripts/
  build_site.py
dist/
styles.css
script.js
```

## 작업 메모

- 번역 시 명령어, 옵션, 경로, 코드 블록, 변수명, 고유 명칭은 원문을 유지합니다.
- 설명 텍스트와 문맥 중심 표현만 한국어로 옮깁니다.
- 웹사이트는 `scripts/build_site.py`가 `docs/*.ko.md`를 읽어 정적 HTML로 생성합니다.

## 배포

GitHub Actions로 사이트를 빌드하고 GitHub Pages에 배포합니다.
