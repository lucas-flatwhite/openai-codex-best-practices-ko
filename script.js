const storageKey = "ocbp-theme";
const root = document.documentElement;
const toggle = document.querySelector("[data-theme-toggle]");
const navLinks = [...document.querySelectorAll(".side-nav a")];
const sections = [...document.querySelectorAll(".doc-prose h2[id]")];

function applyTheme(theme) {
  root.dataset.theme = theme;
  const dark = theme === "dark";
  if (toggle) {
    toggle.setAttribute("aria-pressed", String(dark));
    const nextLabel = dark ? "라이트 모드로 전환" : "다크 모드로 전환";
    toggle.setAttribute("aria-label", nextLabel);
    toggle.setAttribute("title", nextLabel);
  }
}

function preferredTheme() {
  const saved = window.localStorage.getItem(storageKey);
  if (saved === "light" || saved === "dark") {
    return saved;
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function setActiveNav(id) {
  navLinks.forEach((link) => {
    const active = link.getAttribute("href") === `#${id}`;
    link.classList.toggle("is-active", active);
  });
}

applyTheme(preferredTheme());

toggle?.addEventListener("click", () => {
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  window.localStorage.setItem(storageKey, nextTheme);
  applyTheme(nextTheme);
});

if (sections.length && "IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (visible?.target?.id) {
        setActiveNav(visible.target.id);
      }
    },
    {
      rootMargin: "-24% 0px -60% 0px",
      threshold: [0.2, 0.45, 0.7],
    }
  );

  sections.forEach((section) => observer.observe(section));
  setActiveNav(sections[0].id);
}
