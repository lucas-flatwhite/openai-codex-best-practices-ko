# Designing Delightful Frontends with GPT-5.4

> GPT-5.4로 더 매력적인 프런트엔드 만들기

**원문 출처:** [https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4)

---

GPT-5.4는 이전 모델들보다 더 뛰어난 웹 개발자이며, 더 시각적으로 매력적이고 더 과감한 프런트엔드를 생성할 수 있습니다. 특히 OpenAI는 UI 역량과 이미지 활용 능력 향상에 초점을 맞춰 GPT-5.4를 학습시켰습니다. 적절한 가이드를 제공하면, 이 모델은 섬세한 디테일과 잘 다듬어진 인터랙션, 아름다운 이미지를 갖춘 실서비스 수준의 프런트엔드를 만들어낼 수 있습니다.

웹 디자인은 결과의 범위가 매우 넓습니다. 훌륭한 디자인은 절제와 발명을 함께 다룹니다. 오랜 시간 검증된 패턴을 바탕으로 하되, 그 안에 새로운 무언가를 더해야 합니다. GPT-5.4는 이런 폭넓은 디자인 스펙트럼을 학습했고, 웹사이트를 구성하는 다양한 방식을 이해합니다.

프롬프트가 충분히 구체적이지 않으면 모델은 학습 데이터에서 자주 등장한 패턴으로 되돌아가는 경향이 있습니다. 그중 일부는 검증된 관습이지만, 상당수는 단지 과도하게 자주 등장했을 뿐인 습관이기도 합니다. 그 결과는 대체로 그럴듯하고 기능적이지만, 구조가 지나치게 평범해지고, 시각적 위계가 약해지며, 머릿속에서 기대한 디자인 수준에 미치지 못하는 선택으로 흘러갈 수 있습니다.

이 가이드는 GPT-5.4가 여러분이 원하는 디자인 방향으로 더 정확히 움직이도록 유도하는 실용적인 기법을 설명합니다.

---

## 목차

1. [모델 개선 사항](#모델-개선-사항)
2. [실전 팁 빠른 시작](#실전-팁-빠른-시작)
3. [더 나은 디자인을 위한 기법](#더-나은-디자인을-위한-기법)
4. [Frontend Skill로 전체 흐름 묶기](#frontend-skill로-전체-흐름-묶기)
5. [핵심 요약](#핵심-요약)

---

## 모델 개선 사항

GPT-5.4는 [여러 축에서](https://openai.com/index/introducing-gpt-5-4/) 개선되었지만, 프런트엔드 작업과 관련해서는 특히 다음 세 가지 실질적인 향상에 집중했습니다.

- 디자인 과정 전반에서 더 강력해진 이미지 이해 능력
- 더 완전하고 기능적으로 탄탄한 앱과 웹사이트 생성
- 스스로 작업을 검사하고 테스트하고 검증하기 위한 도구 활용 능력 향상

### 이미지 이해와 도구 활용

GPT-5.4는 이미지 검색 및 이미지 생성 도구를 네이티브하게 사용할 수 있도록 학습되었습니다. 덕분에 시각적 추론을 디자인 과정에 직접 통합할 수 있습니다. 최상의 결과를 원한다면, 최종 에셋을 고르기 전에 먼저 무드보드나 여러 개의 시각적 옵션을 생성하도록 지시하는 것이 좋습니다.

이미지가 담아야 할 속성, 예를 들어 스타일, 색상 팔레트, 구도, 분위기를 명시적으로 설명하면 더 강한 시각적 레퍼런스로 모델을 유도할 수 있습니다. 또한 이미 생성한 이미지를 재사용하라고 하거나, 새 비주얼을 만들기 위해 이미지 생성 도구를 호출하라고 하거나, 필요 시 특정 외부 이미지를 참조하라고 지시하는 프롬프트를 함께 포함하는 것이 좋습니다.

```text
Default to using any uploaded/pre-generated images. Otherwise use the image generation tool to create visually stunning image artifacts. Do not reference or link to web images unless the user explicitly asks for them.
```

### 기능 완성도 향상

이 모델은 더 완전하고 기능적으로 건전한 앱을 개발하도록 학습되었습니다. 따라서 긴 호흡의 작업에서도 더 높은 신뢰성을 기대할 수 있습니다. 이전에는 불가능하다고 느꼈던 게임이나 복잡한 사용자 경험도 이제는 한두 번의 턴 안에서 현실적인 결과로 이어질 수 있습니다.

### Computer Use와 검증

GPT-5.4는 컴퓨터 사용(computer use)을 위해 학습된 OpenAI의 첫 메인라인 모델입니다. 인터페이스를 네이티브하게 탐색할 수 있으며, Playwright 같은 도구와 결합하면 자신의 작업을 반복적으로 점검하고, 동작을 검증하고, 구현을 다듬을 수 있습니다. 그 결과 더 길고 더 자율적인 개발 워크플로우가 가능해집니다.

이 기능이 실제로 어떻게 동작하는지는 [launch video](https://openai.com/index/introducing-gpt-5-4/?video=1170427106%20)에서 확인하실 수 있습니다.

Playwright는 특히 프런트엔드 개발에서 큰 가치를 발휘합니다. 렌더링된 페이지를 검사하고, 여러 viewport를 테스트하고, 앱 흐름을 탐색하고, 상태나 내비게이션 문제를 찾아내는 데 유용합니다. Playwright 도구나 스킬을 제공하면 GPT-5.4가 더 세련되고 기능적으로 완성된 인터페이스를 만들 가능성이 크게 높아집니다. 향상된 이미지 이해 능력 덕분에, 레퍼런스 UI가 주어졌을 때 시각적으로 자신의 작업을 검증하고 실제 결과가 참조 이미지와 일치하는지도 확인할 수 있습니다.

---

## 실전 팁 빠른 시작

이 문서에서 몇 가지만 가져가고 싶다면, 우선 아래 항목부터 적용해 보세요.

1. 시작은 낮은 추론 수준(low reasoning level)으로 선택합니다.
2. 디자인 시스템과 제약 조건을 미리 정의합니다. 예를 들어 타이포그래피, 색상 팔레트, 레이아웃 등이 있습니다.
3. 스크린샷 같은 시각적 레퍼런스나 무드보드를 제공해 모델이 따를 시각적 가드레일을 마련합니다.
4. 콘텐츠 작성 방향을 잡아 줄 수 있도록 내러티브나 콘텐츠 전략을 먼저 정해 둡니다.

아래는 시작할 때 사용할 수 있는 프롬프트 예시입니다.

```text
## Frontend tasks

When doing frontend design tasks, avoid generic, overbuilt layouts.

**Use these hard rules:**
- One composition: The first viewport must read as one composition, not a dashboard (unless it's a dashboard).
- Brand first: On branded pages, the brand or product name must be a hero-level signal, not just nav text or an eyebrow. No headline should overpower the brand.
- Brand test: If the first viewport could belong to another brand after removing the nav, the branding is too weak.
- Typography: Use expressive, purposeful fonts and avoid default stacks (Inter, Roboto, Arial, system).
- Background: Don't rely on flat, single-color backgrounds; use gradients, images, or subtle patterns to build atmosphere.
- Full-bleed hero only: On landing pages and promotional surfaces, the hero image should be a dominant edge-to-edge visual plane or background by default. Do not use inset hero images, side-panel hero images, rounded media cards, tiled collages, or floating image blocks unless the existing design system clearly requires it.
- Hero budget: The first viewport should usually contain only the brand, one headline, one short supporting sentence, one CTA group, and one dominant image. Do not place stats, schedules, event listings, address blocks, promos, "this week" callouts, metadata rows, or secondary marketing content in the first viewport.
- No hero overlays: Do not place detached labels, floating badges, promo stickers, info chips, or callout boxes on top of hero media.
- Cards: Default: no cards. Never use cards in the hero. Cards are allowed only when they are the container for a user interaction. If removing a border, shadow, background, or radius does not hurt interaction or understanding, it should not be a card.
- One job per section: Each section should have one purpose, one headline, and usually one short supporting sentence.
- Real visual anchor: Imagery should show the product, place, atmosphere, or context. Decorative gradients and abstract backgrounds do not count as the main visual idea.
- Reduce clutter: Avoid pill clusters, stat strips, icon rows, boxed promos, schedule snippets, and multiple competing text blocks.
- Use motion to create presence and hierarchy, not noise. Ship at least 2-3 intentional motions for visually led work.
- Color & Look: Choose a clear visual direction; define CSS variables; avoid purple-on-white defaults. No purple bias or dark mode bias.
- Ensure the page loads properly on both desktop and mobile.
- For React code, prefer modern patterns including useEffectEvent, startTransition, and useDeferredValue when appropriate if used by the team. Do not add useMemo/useCallback by default unless already used; follow the repo's React Compiler guidance.

Exception: If working within an existing website or design system, preserve the established patterns, structure, and visual language.
```

---

## 더 나은 디자인을 위한 기법

### 디자인 원칙부터 시작하기

H1 헤드라인은 하나만 둘 것, 섹션은 여섯 개를 넘기지 않을 것, 서체는 최대 두 개까지 사용할 것, 강조 색상은 하나만 둘 것, 첫 화면 위에는 기본 CTA 하나만 둘 것 같은 제약을 먼저 정의해 보세요.

### 시각적 레퍼런스 제공하기

스크린샷이나 무드보드 같은 레퍼런스는 모델이 레이아웃의 리듬, 타이포그래피 스케일, 간격 시스템, 이미지 처리 방식을 추론하는 데 도움을 줍니다. 아래는 GPT-5.4가 사용자의 검토를 위해 직접 무드보드를 생성하는 예시입니다.

![GPT-5.4가 일관된 비주얼 방향을 잡기 위해 생성한 무드보드 예시](https://cdn.openai.com/devhub/blog/codex_moodboard.png)

*NYC 커피 문화와 Y2K 미학에서 영감을 받아 Codex의 GPT-5.4가 만든 무드보드*

### 페이지를 하나의 내러티브로 구성하기

전형적인 마케팅 페이지 구조는 다음과 같습니다.

1. Hero: 정체성과 약속을 확립합니다.
2. Supporting imagery: 맥락이나 환경을 보여줍니다.
3. Product detail: 제공하는 내용을 설명합니다.
4. Social proof: 신뢰를 형성합니다.
5. Final CTA: 관심을 전환 행동으로 이어지게 합니다.

### 디자인 시스템 준수를 지시하기

모델이 빌드 초기에 명확한 디자인 시스템을 세우도록 유도하는 것이 좋습니다. `background`, `surface`, `primary text`, `muted text`, `accent` 같은 핵심 디자인 토큰과, `display`, `headline`, `body`, `caption` 같은 타이포그래피 역할을 정의해 두세요. 이렇게 구조를 잡아 주면 애플리케이션 전반에서 일관되고 확장 가능한 UI 패턴을 만들기 쉬워집니다.

대부분의 웹 프로젝트에서는 **React와 Tailwind** 같은 익숙한 스택으로 시작하는 것이 잘 맞습니다. GPT-5.4는 이런 도구들과 특히 잘 맞기 때문에 빠르게 반복하고 완성도 높은 결과에 도달하기가 수월합니다.

모션과 레이어형 UI 요소는 복잡성을 키울 수 있습니다. 특히 고정 요소나 플로팅 요소가 주요 콘텐츠와 상호작용할 때 더욱 그렇습니다. 애니메이션, 오버레이, 장식 레이어를 다룰 때는 안전한 레이아웃 동작을 유도하는 가이드를 포함하는 것이 좋습니다. 예를 들면 다음과 같습니다.

```text
Keep fixed or floating UI elements from overlapping text, buttons, or other key content across screen sizes. Place them in safe areas, behind primary content where appropriate, and maintain sufficient spacing.
```

### 추론 수준 낮추기

더 단순한 웹사이트에서는 추론을 많이 한다고 해서 항상 더 좋은 결과가 나오지는 않습니다. 실제로는 **low와 medium reasoning level이 더 강한 프런트엔드 결과로 이어지는 경우가 많습니다.** 모델이 빠르고 집중된 상태를 유지하고 과하게 생각하는 경향을 줄이면서도, 더 대담한 디자인이 필요할 때 추론 수준을 올릴 여지를 남겨 주기 때문입니다.

### 실제 콘텐츠에 디자인을 고정하기

실제 카피, 제품 맥락, 명확한 프로젝트 목표를 제공하는 것은 프런트엔드 결과를 개선하는 가장 간단한 방법 중 하나입니다. 이런 맥락이 있어야 모델이 적절한 사이트 구조를 고르고, 더 분명한 섹션 단위 내러티브를 만들고, 일반적인 플레이스홀더 패턴으로 돌아가지 않으면서 더 그럴듯한 메시지를 작성할 수 있습니다.

---

## Frontend Skill로 전체 흐름 묶기

일반적인 프런트엔드 작업에서 GPT-5.4를 더 잘 활용할 수 있도록, OpenAI는 전용 [`frontend-skill`](https://github.com/openai/skills/tree/main/skills/.curated/frontend-skill)도 준비했습니다. 이 스킬은 구조, 미감, 인터랙션 패턴에 대해 더 강한 가이드를 제공해, 별도 조정이 많지 않아도 더 세련되고 의도적이며 매력적인 디자인을 만들 수 있도록 돕습니다.

```text
---
name: frontend-skill
description: Use when the task asks for a visually strong landing page, website, app, prototype, demo, or game UI. This skill enforces restrained composition, image-led hierarchy, cohesive content structure, and tasteful motion while avoiding generic cards, weak branding, and UI clutter.
---

# Frontend skill

Use this skill when the quality of the work depends on art direction, hierarchy, restraint, imagery, and motion rather than component count.

Goal: ship interfaces that feel deliberate, premium, and current. Default toward award-level composition: one big idea, strong imagery, sparse copy, rigorous spacing, and a small number of memorable motions.

## Working Model

Before building, write three things:

- visual thesis: one sentence describing mood, material, and energy
- content plan: hero, support, detail, final CTA
- interaction thesis: 2-3 motion ideas that change the feel of the page

Each section gets one job, one dominant visual idea, and one primary takeaway or action.

## Beautiful Defaults

- Start with composition, not components.
- Prefer a full-bleed hero or full-canvas visual anchor.
- Make the brand or product name the loudest text.
- Keep copy short enough to scan in seconds.
- Use whitespace, alignment, scale, cropping, and contrast before adding chrome.
- Limit the system: two typefaces max, one accent color by default.
- Default to cardless layouts. Use sections, columns, dividers, lists, and media blocks instead.
- Treat the first viewport as a poster, not a document.

## Landing Pages

Default sequence:

1. Hero: brand or product, promise, CTA, and one dominant visual
2. Support: one concrete feature, offer, or proof point
3. Detail: atmosphere, workflow, product depth, or story
4. Final CTA: convert, start, visit, or contact

Hero rules:

- One composition only.
- Full-bleed image or dominant visual plane.
- Canonical full-bleed rule: on branded landing pages, the hero itself must run edge-to-edge with no inherited page gutters, framed container, or shared max-width; constrain only the inner text/action column.
- Brand first, headline second, body third, CTA fourth.
- No hero cards, stat strips, logo clouds, pill soup, or floating dashboards by default.
- Keep headlines to roughly 2-3 lines on desktop and readable in one glance on mobile.
- Keep the text column narrow and anchored to a calm area of the image.
- All text over imagery must maintain strong contrast and clear tap targets.

If the first viewport still works after removing the image, the image is too weak. If the brand disappears after hiding the nav, the hierarchy is too weak.

Viewport budget:

- If the first screen includes a sticky/fixed header, that header counts against the hero. The combined header + hero content must fit within the initial viewport at common desktop and mobile sizes.
- When using `100vh`/`100svh` heroes, subtract persistent UI chrome (`calc(100svh - header-height)`) or overlay the header instead of stacking it in normal flow.

## Apps

Default to Linear-style restraint:

- calm surface hierarchy
- strong typography and spacing
- few colors
- dense but readable information
- minimal chrome
- cards only when the card is the interaction

For app UI, organize around:

- primary workspace
- navigation
- secondary context or inspector
- one clear accent for action or state

Avoid:

- dashboard-card mosaics
- thick borders on every region
- decorative gradients behind routine product UI
- multiple competing accent colors
- ornamental icons that do not improve scanning

If a panel can become plain layout without losing meaning, remove the card treatment.

## Imagery

Imagery must do narrative work.

- Use at least one strong, real-looking image for brands, venues, editorial pages, and lifestyle products.
- Prefer in-situ photography over abstract gradients or fake 3D objects.
- Choose or crop images with a stable tonal area for text.
- Do not use images with embedded signage, logos, or typographic clutter fighting the UI.
- Do not generate images with built-in UI frames, splits, cards, or panels.
- If multiple moments are needed, use multiple images, not one collage.

The first viewport needs a real visual anchor. Decorative texture is not enough.

## Copy

- Write in product language, not design commentary.
- Let the headline carry the meaning.
- Supporting copy should usually be one short sentence.
- Cut repetition between sections.
- do not include prompt language or design commentary into the UI
- Give every section one responsibility: explain, prove, deepen, or convert.

If deleting 30 percent of the copy improves the page, keep deleting.

## Utility Copy For Product UI

When the work is a dashboard, app surface, admin tool, or operational workspace, default to utility copy over marketing copy.

- Prioritize orientation, status, and action over promise, mood, or brand voice.
- Start with the working surface itself: KPIs, charts, filters, tables, status, or task context. Do not introduce a hero section unless the user explicitly asks for one.
- Section headings should say what the area is or what the user can do there.
- Good: "Selected KPIs", "Plan status", "Search metrics", "Top segments", "Last sync".
- Avoid aspirational hero lines, metaphors, campaign-style language, and executive-summary banners on product surfaces unless specifically requested.
- Supporting text should explain scope, behavior, freshness, or decision value in one sentence.
- If a sentence could appear in a homepage hero or ad, rewrite it until it sounds like product UI.
- If a section does not help someone operate, monitor, or decide, remove it.
- Litmus check: if an operator scans only headings, labels, and numbers, can they understand the page immediately?

## Motion

Use motion to create presence and hierarchy, not noise.

Ship at least 2-3 intentional motions for visually led work:

- one entrance sequence in the hero
- one scroll-linked, sticky, or depth effect
- one hover, reveal, or layout transition that sharpens affordance

Prefer Framer Motion when available for:

- section reveals
- shared layout transitions
- scroll-linked opacity, translate, or scale shifts
- sticky storytelling
- carousels that advance narrative, not just fill space
- menus, drawers, and modal presence effects

Motion rules:

- noticeable in a quick recording
- smooth on mobile
- fast and restrained
- consistent across the page
- removed if ornamental only

## Hard Rules

- No cards by default.
- No hero cards by default.
- No boxed or center-column hero when the brief calls for full bleed.
- No more than one dominant idea per section.
- No section should need many tiny UI devices to explain itself.
- No headline should overpower the brand on branded pages.
- No filler copy.
- No split-screen hero unless text sits on a calm, unified side.
- No more than two typefaces without a clear reason.
- No more than one accent color unless the product already has a strong system.

## Reject These Failures

- Generic SaaS card grid as the first impression
- Beautiful image with weak brand presence
- Strong headline with no clear action
- Busy imagery behind text
- Sections that repeat the same mood statement
- Carousel with no narrative purpose
- App UI made of stacked cards instead of layout

## Litmus Checks

- Is the brand or product unmistakable in the first screen?
- Is there one strong visual anchor?
- Can the page be understood by scanning headlines only?
- Does each section have one job?
- Are cards actually necessary?
- Does motion improve hierarchy or atmosphere?
- Would the design still feel premium if all decorative shadows were removed?
```

Codex 앱 안에서는 다음 명령으로 `frontend-skill`을 설치할 수 있습니다.

```text
$skill-installer frontend-skill
```

Frontend Design skill의 도움으로 생성한 웹사이트 예시로는 Landing Pages, Games, Dashboards가 있습니다.

---

## 핵심 요약

GPT-5.4는 프롬프트에서 명확한 디자인 제약, 시각적 레퍼런스, 구조화된 내러티브, 정의된 디자인 시스템을 제공할 때 높은 품질의 프런트엔드 인터페이스를 생성할 수 있습니다.

이 기법들이 더 독창적이고 더 잘 설계된 앱을 만드는 데 도움이 되기를 바랍니다.

GPT-5.4와 [Codex](http://developers.openai.com/codex) 같은 코딩 에이전트로 전부 생성한 프로젝트를 공유하고 싶다면, 여러분의 앱을 [gallery](http://developers.openai.com/showcase)에 제출해 보세요.
