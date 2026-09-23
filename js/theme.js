/* CLUG theme toggle: light / dark / auto (follows OS).
 * Preference is stored only in this browser (localStorage "clug-theme").
 * No tracking, no network requests. */
(function () {
  'use strict';

  var STORAGE_KEY = 'clug-theme';
  var MODES = ['auto', 'light', 'dark'];
  var ICONS = { auto: 'fa-adjust', light: 'fa-sun-o', dark: 'fa-moon-o' };
  var LABELS = { auto: 'Auto', light: 'Light', dark: 'Dark' };
  var META_COLORS = { light: '#3fb1a3', dark: '#14171b' };

  var mediaQuery = null;
  try {
    mediaQuery = window.matchMedia
      ? window.matchMedia('(prefers-color-scheme: dark)')
      : null;
  } catch (e) {
    mediaQuery = null;
  }

  function getStoredMode() {
    try {
      var v = window.localStorage.getItem(STORAGE_KEY);
      return MODES.indexOf(v) !== -1 ? v : 'auto';
    } catch (e) {
      return 'auto';
    }
  }

  function resolveEffective(mode) {
    if (mode === 'light') return 'light';
    if (mode === 'dark') return 'dark';
    if (mediaQuery && typeof mediaQuery.matches === 'boolean') {
      return mediaQuery.matches ? 'dark' : 'light';
    }
    return 'light';
  }

  function nextMode(mode) {
    var i = MODES.indexOf(mode);
    return MODES[(i + 1) % MODES.length];
  }

  function updateMeta(effective) {
    try {
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta && META_COLORS[effective]) {
        meta.setAttribute('content', META_COLORS[effective]);
      }
    } catch (e) { /* ignore */ }
  }

  function updateButtons(mode) {
    var buttons = document.querySelectorAll('.theme-toggle');
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      var icon = btn.querySelector('.fa');
      var label = btn.querySelector('.theme-toggle-text');
      if (icon) {
        icon.className = 'fa ' + ICONS[mode];
        icon.setAttribute('aria-hidden', 'true');
      }
      if (label) {
        label.textContent = ' ' + LABELS[mode];
      }
      btn.setAttribute('title', 'Theme: ' + LABELS[mode] + ' (click for ' + LABELS[nextMode(mode)] + ')');
      btn.setAttribute('aria-label', 'Color theme: ' + LABELS[mode] + '. Activate to switch to ' + LABELS[nextMode(mode)] + ' theme.');
    }
  }

  function apply(mode, animate) {
    var effective = resolveEffective(mode);
    var root = document.documentElement;
    if (animate) {
      root.classList.add('theme-anim');
      window.setTimeout(function () {
        root.classList.remove('theme-anim');
      }, 300);
    }
    root.setAttribute('data-theme', effective);
    root.setAttribute('data-theme-mode', mode);
    updateMeta(effective);
    updateButtons(mode);
    return effective;
  }

  var currentMode = getStoredMode();
  apply(currentMode, false);

  // Small popup confirming which mode was just activated.
  var toast = null;
  var toastTimer = null;
  function showToast(mode) {
    try {
      if (!toast) {
        toast = document.createElement('div');
        toast.className = 'theme-toast';
        toast.setAttribute('role', 'status');
        toast.setAttribute('aria-live', 'polite');
        document.body.appendChild(toast);
      }
      var names = { auto: 'Auto (follows system)', light: 'Light', dark: 'Dark' };
      toast.textContent = 'Theme: ' + (names[mode] || mode);
      toast.classList.add('show');
      if (toastTimer) window.clearTimeout(toastTimer);
      toastTimer = window.setTimeout(function () {
        toast.classList.remove('show');
      }, 1600);
    } catch (e) { /* ignore */ }
  }

  function setMode(mode, animate, silent) {
    currentMode = mode;
    try {
      window.localStorage.setItem(STORAGE_KEY, mode);
    } catch (e) { /* private mode: keep in-memory only */ }
    apply(mode, animate !== false);
    if (!silent) showToast(mode);
  }

  function cycle() {
    setMode(nextMode(currentMode), true);
  }

  // Follow OS changes while in Auto.
  if (mediaQuery) {
    var onSystemChange = function () {
      if (currentMode === 'auto') {
        apply('auto', false);
      }
    };
    if (typeof mediaQuery.addEventListener === 'function') {
      mediaQuery.addEventListener('change', onSystemChange);
    } else if (typeof mediaQuery.addListener === 'function') {
      mediaQuery.addListener(onSystemChange);
    }
  }

  // Bind every toggle (header clones into mobile panels duplicate markup,
  // so bind by class after DOM is ready and watch for late clones).
  function bindAll() {
    var buttons = document.querySelectorAll('.theme-toggle');
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      if (!btn.getAttribute('data-theme-bound')) {
        btn.setAttribute('data-theme-bound', '1');
        btn.addEventListener('click', function (e) {
          e.preventDefault();
          cycle();
        });
      }
    }
    updateButtons(currentMode);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindAll);
  } else {
    bindAll();
  }
  // Skel clones #nav into panels slightly after load — re-scan briefly.
  var scans = 0;
  var scanTimer = window.setInterval(function () {
    bindAll();
    scans += 1;
    if (scans >= 10) {
      window.clearInterval(scanTimer);
    }
  }, 500);

  // Debug / reuse hook.
  window.CLUGTheme = {
    get: function () { return currentMode; },
    set: setMode,
    cycle: cycle
  };
})();
