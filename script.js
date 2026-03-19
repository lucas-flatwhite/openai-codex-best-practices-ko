const storageKey = "ocbp-theme";
const root = document.documentElement;
const toggle = document.querySelector("[data-theme-toggle]");
const progressBar = document.querySelector(".progress-bar");
const backToTop = document.querySelector(".back-to-top");
const mobileNavToggle = document.querySelector(".mobile-nav-toggle");
const mobileNavOverlay = document.querySelector(".mobile-nav-overlay");
const mobileNavClose = document.querySelector(".mobile-nav-close");
const navLinks = Array.from(document.querySelectorAll(".side-nav a, .mobile-nav-drawer a"));
const sectionHeadings = Array.from(document.querySelectorAll(".doc-prose h2[id]")).filter(
  (heading) => heading.id !== "목차"
);
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
  if (saved === "light" || saved === "dark") {
    return saved;
  }

  return themeMedia.matches ? "dark" : "light";
}

function syncProgressBar() {
  if (!progressBar) return;

  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
  progressBar.style.width = `${Math.min(progress, 100)}%`;
}

function setMobileNavOpen(open) {
  if (!mobileNavOverlay) return;

  mobileNavOverlay.classList.toggle("is-open", open);
  mobileNavOverlay.setAttribute("aria-hidden", String(!open));
  mobileNavToggle?.setAttribute("aria-expanded", String(open));
  document.body.classList.toggle("nav-open", open);
}

function openMobileNav() {
  setMobileNavOpen(true);
}

function closeMobileNav() {
  setMobileNavOpen(false);
}

function activateNavLink(id) {
  const targetHash = `#${id}`;
  navLinks.forEach((link) => {
    link.classList.toggle("is-active", link.getAttribute("href") === targetHash);
  });
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
  if (!saved) {
    applyTheme(event.matches ? "dark" : "light");
  }
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

mobileNavToggle?.addEventListener("click", openMobileNav);
mobileNavClose?.addEventListener("click", closeMobileNav);

mobileNavOverlay?.addEventListener("click", (event) => {
  if (event.target === mobileNavOverlay) {
    closeMobileNav();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && mobileNavOverlay?.classList.contains("is-open")) {
    closeMobileNav();
  }
});

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    closeMobileNav();
  });
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 1100) {
    closeMobileNav();
  }
});

if (sectionHeadings.length > 0) {
  activateNavLink(sectionHeadings[0].id);

  const observer = new IntersectionObserver(
    (entries) => {
      const visibleEntries = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

      if (visibleEntries.length > 0) {
        activateNavLink(visibleEntries[0].target.id);
      }
    },
    {
      rootMargin: "-18% 0px -62% 0px",
      threshold: [0.15, 0.4, 0.75],
    }
  );

  sectionHeadings.forEach((heading) => observer.observe(heading));
}
