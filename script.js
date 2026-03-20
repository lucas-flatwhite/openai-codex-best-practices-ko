const storageKey = "ocbp-theme";
const root = document.documentElement;
const toggle = document.querySelector("[data-theme-toggle]");
const progressBar = document.querySelector(".progress-bar");
const backToTop = document.querySelector(".back-to-top");
const themeMedia = window.matchMedia("(prefers-color-scheme: dark)");

function applyTheme(theme) {
  root.dataset.theme = theme;

  if (!toggle) return;

  const dark = theme === "dark";
  const nextLabel = dark ? "라이트 모드로 전환" : "다크 모드로 전환";
  toggle.setAttribute("aria-pressed", String(dark));
  toggle.setAttribute("aria-label", nextLabel);
  toggle.setAttribute("title", nextLabel);
}

function preferredTheme() {
  const saved = window.localStorage.getItem(storageKey);
  if (saved === "light" || saved === "dark") return saved;
  return themeMedia.matches ? "dark" : "light";
}

function syncProgressBar() {
  if (!progressBar) return;
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
  progressBar.style.width = `${Math.min(progress, 100)}%`;
}

applyTheme(preferredTheme());
syncProgressBar();

toggle?.addEventListener("click", () => {
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  window.localStorage.setItem(storageKey, nextTheme);
  applyTheme(nextTheme);
});

themeMedia.addEventListener("change", (event) => {
  const saved = window.localStorage.getItem(storageKey);
  if (!saved) applyTheme(event.matches ? "dark" : "light");
});

window.addEventListener("scroll", syncProgressBar, { passive: true });

if (backToTop) {
  window.addEventListener(
    "scroll",
    () => {
      backToTop.classList.toggle("is-visible", window.scrollY > 420);
    },
    { passive: true }
  );

  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}
