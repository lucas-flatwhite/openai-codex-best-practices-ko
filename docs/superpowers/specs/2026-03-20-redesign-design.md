# 사이트 리디자인 스펙

**날짜:** 2026-03-20
**목표:** 현재 평이한 AI 느낌의 분리된 레이아웃을 shadcn 디자인 언어 기반의 에디토리얼 문서 리더로 재구축

---

## 1. 범위 및 제약

- **기술 스택 변경 없음:** Vanilla HTML/CSS/JS + Python 빌드 시스템 유지
- **변경 대상:** `styles.css` (완전 재작성), `script.js` (부분 수정), `build_site.py` (마크업 구조 수정)
- **마크다운 파싱 로직 유지:** build_site.py의 변환 로직은 건드리지 않음

---

## 2. 레이아웃 구조

### 전체 구조
사이드바를 완전히 제거하고 단일 컬럼 레이아웃으로 전환한다.

```
┌─────────────────────────────────────────┐
│  [sticky top bar]  제목  · 다크모드 토글  │
│  [스크롤 진행 표시줄 — 인디고]             │
├─────────────────────────────────────────┤
│                                         │
│         Hero                            │
│         배지 (OPENAI CODEX pill)         │
│         큰 제목 (3rem / 800)             │
│         부제목 + 메타 (날짜, 출처)        │
│         구분선                           │
│                                         │
│         본문 (max-width: 680px, 중앙)    │
│                                         │
│         ## 섹션 제목 + 숫자 배지          │
│         ### 소제목                       │
│         본문 텍스트...                   │
│                                         │
│         [callout 블록]                  │
│         [코드 블록]                      │
│                                         │
│         footer: 원문 링크, 빌드 시각     │
└─────────────────────────────────────────┘
```

### 레이아웃 핵심 결정
- **본문 너비:** `max-width: 680px`, `margin: 0 auto` — 읽기 최적화
- **사이드바 제거:** 목차 네비게이션 역할은 sticky top bar의 스크롤 진행 표시줄로 대체
- **모바일 드로어 제거:** 사이드바가 없으므로 불필요

---

## 3. 디자인 토큰

### 색상 (shadcn 네이밍 컨벤션)

| 토큰 | 라이트 | 다크 |
|------|--------|------|
| `--background` | `#ffffff` | `#111318` |
| `--foreground` | `#09090b` | `#fafafa` |
| `--muted` | `#f4f4f5` | `#1b1f27` |
| `--muted-foreground` | `#71717a` | `#a1a1aa` |
| `--border` | `#e4e4e7` | `#2a3040` |
| `--accent` | `#6366f1` | `#818cf8` |
| `--accent-muted` | `#eef2ff` | `#20264d` |

포인트 컬러는 **인디고 (`#6366f1`)** — 기술 문서에 적합하고 현재 브라운 계열과 차별화.

### 타이포그래피

**폰트 로딩:** Pretendard Variable은 jsDelivr CDN에서 dynamic subset으로 로드한다. `build_site.py`의 `<head>` 템플릿에 아래 `<link>`를 추가한다:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css" />
```

**폰트 패밀리:**
```css
--font-sans: "Pretendard Variable", Pretendard,
             -apple-system, BlinkMacSystemFont,
             "Apple SD Gothic Neo", "Noto Sans KR",
             sans-serif;

--font-mono: "JetBrains Mono", "Fira Code",
             "D2Coding", monospace;
```

**크기 위계:**

| 용도 | 크기 | 굵기 |
|------|------|------|
| Hero 제목 | `3rem` | `800` |
| `##` 섹션 제목 | `1.5rem` | `700` |
| `###` 소제목 | `1.25rem` | `600` |
| 본문 | `1.125rem` | `400` |
| 메타/캡션 | `0.875rem` | `500` |
| 인라인 코드 | `0.875em` | `400` |

**본문 행간:** `line-height: 1.85` — 한국어 긴 문서 읽기 최적화

---

## 4. 컴포넌트 상세

### 4-1. Sticky Top Bar
- 배경: `--background` + `backdrop-filter: blur(8px)` + 하단 `1px --border`
- 좌측: 사이트 제목 (small, `--muted-foreground`)
- 우측: 다크모드 토글 (shadcn Switch 스타일 — CSS only)
- 하단: 스크롤 진행 표시줄 (`3px`, `--accent` 색상)
- `position: sticky; top: 0; z-index: 50`

### 4-2. Hero 섹션
- **배지:** `OPENAI CODEX` — `--accent` 배경, 흰 텍스트, `border-radius: 9999px`, `padding: 2px 10px`, `font-size: 0.75rem`
- **제목:** `3rem / 800` — 모바일에서 `2rem`
- **부제목:** `--muted-foreground`, `1.125rem`
- **메타 정보:** 원문 출처, 빌드 날짜 — `0.875rem`, `--muted-foreground`
- **구분선:** `1px solid --border`, `margin: 2rem 0`

### 4-3. 섹션 제목 (`##`)
- 숫자 배지: `--accent` 배경, 흰 텍스트, `border-radius: 6px`, `padding: 2px 8px`
- 제목 텍스트: `1.5rem / 700`
- 상단 여백: `3rem` — 섹션 간 명확한 구분

### 4-4. 소제목 (`###`)
- `1.25rem / 600`
- 상단 여백: `1.75rem`

### 4-5. Callout 블록 (인용문 `>`)
- 좌측 `3px solid --accent` border
- 배경: `--accent-muted`
- `border-radius: 0 6px 6px 0`
- `padding: 1rem 1.25rem`
- 아이콘 없이 여백과 색으로만 처리

### 4-6. 코드 블록
- 배경: `--muted`
- `border-radius: 8px`
- `border: 1px solid --border`
- 상단 언어 라벨: `0.75rem`, `--muted-foreground`
- 복사 버튼 유지 (script.js)

### 4-7. 인라인 코드
- 배경: `--accent-muted`
- `border: 1px solid` (accent 계열 옅게)
- `border-radius: 4px`
- `padding: 1px 5px`
- `font-size: 0.875em`

### 4-8. 링크
- 색상: `--accent`
- 밑줄: `text-decoration-color: transparent` → hover 시 `--accent`
- `transition: 150ms ease`

### 4-9. "맨 위로" 버튼
- shadcn Button 스타일: `--accent` 배경, 흰 텍스트, `border-radius: 8px`
- `420px` 이상 스크롤 시 노출 (현재 script.js 로직 유지)

### 4-10. Footer
- 구분선 + 원문 링크 + 빌드 시각
- `--muted-foreground`, `0.875rem`
- 중앙 정렬

---

## 5. 인터랙션 & 애니메이션

- **원칙:** 최소한 — `transition: 150ms ease`
- **다크모드 전환:** `transition: background 200ms, color 200ms`
- **스크롤 진행바:** `script.js`에서 실시간 업데이트 (현재 로직 유지)
- **링크/버튼 hover:** `150ms ease`

---

## 6. 반응형

| 브레이크포인트 | 처리 |
|--------------|------|
| `> 768px` | 기본 레이아웃, Hero 제목 `3rem` |
| `≤ 768px` | Hero 제목 `2rem`, 본문 패딩 `1rem` |
| `≤ 480px` | 본문 패딩 `0.75rem` |

본문 `max-width: 680px`은 모바일에서 `width: calc(100% - 2rem)`으로 자동 처리.

---

## 7. 변경 파일 요약

| 파일 | 변경 내용 |
|------|-----------|
| `styles.css` | 완전 재작성 — shadcn 토큰 기반 |
| `script.js` | 사이드바 네비게이션 활성화 로직 (`navLinks`, `activateNavLink`, `IntersectionObserver`, `resize` 리스너) 및 모바일 드로어 코드 전체 제거. 스크롤 진행바 / 다크모드 / 맨위로 버튼 로직 유지. |
| `build_site.py` | `.side-nav` 블록 및 2단 구조(`.hero-meta`, `.doc-card`) 제거, 단일 컬럼 구조로 HTML 템플릿 재작성. `<head>`에 Pretendard CDN `<link>` 추가. `slugify`, `parse_inlines`, `parse_table` 등 파싱 함수는 변경하지 않음. |

---

## 8. 성공 기준

- Hero 섹션에 그라디언트 mesh, animated orb 등 과한 장식 요소를 사용하지 않는다
- 사이드바/드로어 등 분리된 UI 요소가 없다
- shadcn 디자인 토큰 네이밍을 그대로 따른다
- 라이트/다크 모드 모두 작동한다
- 모바일에서 읽기 편하다
- Python 빌드 시스템이 그대로 작동한다
