# README 개선 스펙

**날짜:** 2026-03-20
**목표:** 사이트를 우연히 발견한 한국어 개발자가 스크롤 없이 핵심을 파악하고 링크로 이동할 수 있도록 개선

---

## 1. 독자 및 목적

- **1차 독자:** GitHub에서 저장소를 발견한 한국어 사용 개발자
- **목적:** 프로젝트가 무엇인지 즉시 파악 → 사이트 링크로 이동

---

## 2. 구조 변경

### 현재 구조
1. 뱃지 (last commit)
2. 제목
3. 설명 2문단
4. 불릿 5개
5. 기술 노트
6. 배포 링크 (맨 아래)

### 새 구조
1. 뱃지 행 (last commit + GitHub Pages 배포 상태)
2. 제목
3. **사이트 링크 — 굵게, 눈에 띄게** ← 현재 맨 아래에서 올림 (설명보다 앞)
4. 한 줄 설명 (무엇인지)
5. 본문 요약 (1~2문장 — 어떤 내용인지)
6. 다루는 내용 (불릿, 5개 → 5개 유지하되 표현 간결화)
7. 푸터 한 줄 (원문 출처 · 빌드 방식)

---

## 3. 뱃지

- **유지:** `![GitHub last commit]` — 현행 그대로
- **추가:** GitHub Pages 배포 상태 배지
  ```
  [![GitHub Pages](https://img.shields.io/github/deployments/lucas-flatwhite/openai-codex-best-practices-ko/github-pages?label=GitHub%20Pages&logo=github)](https://lucas-flatwhite.github.io/openai-codex-best-practices-ko/)
  ```
- **제거 없음:** 기존 뱃지 그대로 유지, 하나만 추가

---

## 4. 사이트 링크 처리

제목 바로 아래, 설명보다 앞에 위치:

```markdown
**→ [사이트에서 읽기](https://lucas-flatwhite.github.io/openai-codex-best-practices-ko/)**
```

굵게 + 화살표로 시선을 끈다. 별도 섹션이나 헤딩 없이 인라인으로.

---

## 5. 설명 압축

현재 2문단(약 150자) → 1문단(약 60자)으로 압축:

> OpenAI의 Codex Best Practices를 한국어로 정리한 단일 페이지 문서입니다. 프롬프트 구성부터 자동화까지, Codex를 실전 워크플로우에 정착시키는 방법을 담고 있습니다.

---

## 6. 불릿 리스트

현재 5개 그대로 유지, 표현만 간결화:

- 더 나은 결과를 위한 프롬프팅 방식
- 복잡한 작업을 계획 중심으로 다루는 방법
- `AGENTS.md`로 반복 지침을 구조화하는 방법
- 테스트·검증·리뷰로 신뢰 가능한 작업 흐름 만들기
- MCP·스킬·자동화로 Codex를 워크플로우에 정착시키기

---

## 7. 푸터

기술 노트를 구분선 뒤 한 줄로 압축:

```markdown
---
원문: [OpenAI Codex Best Practices](https://developers.openai.com/codex/learn/best-practices) · 빌드: `scripts/build_site.py` · 배포: GitHub Actions → GitHub Pages
```

---

## 8. 성공 기준

- 사이트 링크가 스크롤 없이 보인다
- README 전체 길이가 현재보다 짧다
- 기술 정보(빌드 방법 등)는 유지되되 방해가 되지 않는다
