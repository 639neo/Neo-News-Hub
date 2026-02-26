// ── Mobile Nav Toggle ──────────────────────────────────────
const toggle = document.getElementById('navToggle');
const mobileNav = document.getElementById('mobileNav');
if (toggle && mobileNav) {
  toggle.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
    const bars = toggle.querySelectorAll('span');
    toggle.classList.toggle('active');
  });
  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!toggle.contains(e.target) && !mobileNav.contains(e.target)) {
      mobileNav.classList.remove('open');
    }
  });
}

// ── Live Date in Top Bar ───────────────────────────────────
const dateEl = document.getElementById('live-date');
if (dateEl) {
  const fmt = new Intl.DateTimeFormat('en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });
  dateEl.textContent = fmt.format(new Date());
}
