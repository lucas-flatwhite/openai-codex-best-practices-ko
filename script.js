const storageKey = "ocbp-theme";
const root = document.documentElement;
const toggle = document.querySelector("[data-theme-toggle]");
const navLinks = [...document.querySelectorAll(".side-nav a")];
const sections = [...document.querySelectorAll(".doc-prose h2[id]")];

/* ── Theme ── */
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

applyTheme(preferredTheme());

toggle?.addEventListener("click", () => {
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  window.localStorage.setItem(storageKey, nextTheme);
  applyTheme(nextTheme);
});

/* ── Active nav tracking ── */
function setActiveNav(id) {
  navLinks.forEach((link) => {
    const active = link.getAttribute("href") === `#${id}`;
    link.classList.toggle("is-active", active);
  });

  // Also update mobile nav links
  document.querySelectorAll(".mobile-nav-drawer a").forEach((link) => {
    const active = link.getAttribute("href") === `#${id}`;
    link.classList.toggle("is-active", active);
  });
}

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

/* ── Reading progress bar ── */
const progressBar = document.querySelector(".progress-bar");

if (progressBar) {
  window.addEventListener(
    "scroll",
    () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = `${Math.min(progress, 100)}%`;
    },
    { passive: true }
  );
}

/* ── Back to top ── */
const backToTop = document.querySelector(".back-to-top");

if (backToTop) {
  window.addEventListener(
    "scroll",
    () => {
      backToTop.classList.toggle("is-visible", window.scrollY > 400);
    },
    { passive: true }
  );

  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/* ── Mobile nav drawer ── */
const mobileNavToggle = document.querySelector(".mobile-nav-toggle");
const mobileNavOverlay = document.querySelector(".mobile-nav-overlay");
const mobileNavClose = document.querySelector(".mobile-nav-close");

function openMobileNav() {
  if (!mobileNavOverlay) return;
  mobileNavOverlay.style.pointerEvents = "auto";
  requestAnimationFrame(() => {
    mobileNavOverlay.classList.add("is-open");
  });
  document.body.style.overflow = "hidden";
}

function closeMobileNav() {
  if (!mobileNavOverlay) return;
  mobileNavOverlay.classList.remove("is-open");
  document.body.style.overflow = "";
  setTimeout(() => {
    mobileNavOverlay.style.pointerEvents = "";
  }, 300);
}

mobileNavToggle?.addEventListener("click", openMobileNav);
mobileNavClose?.addEventListener("click", closeMobileNav);

mobileNavOverlay?.addEventListener("click", (e) => {
  if (e.target === mobileNavOverlay) {
    closeMobileNav();
  }
});

document.querySelectorAll(".mobile-nav-drawer a").forEach((link) => {
  link.addEventListener("click", closeMobileNav);
});
