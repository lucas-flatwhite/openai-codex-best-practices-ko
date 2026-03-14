![GitHub last commit](https://img.shields.io/github/last-commit/lucas-flatwhite/openai-codex-best-practices-ko)

# OpenAI Codex - Best Practices 한국어

이 저장소는 OpenAI의 [`Codex Best Practices`](https://developers.openai.com/codex/learn/best-practices) 문서를 한국어로 정리해, 단일 페이지 GitHub Pages로 제공하기 위한 프로젝트입니다.

`docs/openai-codex-best-practices.en.md`는 OpenAI 원문 최신본이며, `docs/openai-codex-best-practices.ko.md`는 해당 문서의 한국어 버전입니다. 프롬프트 구성, 계획 수립, `AGENTS.md`, 설정 관리, 테스트와 리뷰, MCP, 스킬, 자동화, 세션 운영까지 Codex를 개발 워크플로우 안에서 안정적으로 활용하는 방법을 담고 있습니다.

이 저장소의 목적은 번역 원고를 보관하는 것에 그치지 않습니다. 원고를 정적 페이지로 빌드하고, 라이트/다크 모드를 지원하는 읽기 환경을 제공하며, `main` 브랜치 변경 시 GitHub Actions를 통해 GitHub Pages에 자동 배포되도록 구성되어 있습니다.

이 문서를 통해 다음과 같은 내용을 빠르게 파악하실 수 있습니다.

- 더 나은 결과를 얻기 위한 Codex 프롬프팅 방식
- 복잡한 작업을 계획 중심으로 다루는 방법
- 반복 지침을 구조화하고 재사용하는 방법
- 테스트, 검증, 리뷰를 포함한 신뢰 가능한 작업 흐름
- MCP, 스킬, 자동화를 활용해 Codex를 워크플로우에 정착시키는 관점

사이트의 콘텐츠 소스는 `docs/openai-codex-best-practices.ko.md`이며, 페이지는 `scripts/build_site.py`로 생성됩니다.

배포된 페이지는 다음 주소에서 확인하실 수 있습니다.

- https://lucas-flatwhite.github.io/openai-codex-best-practices-ko/
