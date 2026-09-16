(function () {
  'use strict';
  const pages = Array.from(document.querySelectorAll('.page'));
  const links = Array.from(document.querySelectorAll(
    'a[data-slot="sidebar-menu-button"], a[data-slot="sidebar-menu-sub-button"]'));
  const app = document.querySelector('.app');
  const menu = document.querySelector('.menutog');
  const nav = document.getElementById('nav');
  let pendingScroll;

  function setMenu(open) {
    nav.classList.toggle('open', open);
    menu.setAttribute('aria-expanded', String(open));
  }

  function setGroup(group, open) {
    group.dataset.state = open ? 'open' : 'closed';
    group.querySelector('[data-slot="sidebar-group-label"]').setAttribute('aria-expanded', String(open));
  }

  function saveGroups() {
    const closed = Array.from(document.querySelectorAll('[data-slot="sidebar-group"]'))
      .map((group, index) => group.dataset.state === 'closed' ? index : null)
      .filter(index => index !== null);
    try { localStorage.setItem('cr-groups', JSON.stringify(closed)); } catch (_) { /* Groups still toggle. */ }
  }

  function setSidebar(collapsed, persist) {
    app.dataset.sidebar = collapsed ? 'collapsed' : 'expanded';
    document.querySelector('[data-slot="sidebar"]').dataset.state = collapsed ? 'collapsed' : 'expanded';
    if (persist) {
      try { localStorage.setItem('cr-sidebar', collapsed ? 'collapsed' : 'expanded'); } catch (_) { /* Toggle still works. */ }
    }
  }

  function readRoute() {
    const [rawId, query = ''] = location.hash.slice(1).split('?');
    let id;
    try { id = decodeURIComponent(rawId || 'home'); } catch (_) { id = 'home'; }
    return { id, params: new URLSearchParams(query) };
  }

  function applyFilter(page) {
    const input = page.querySelector('input[type=search]');
    if (!input) return;
    const query = input.value.trim().toLowerCase();
    const filter = page.querySelector('[data-filter="serious"]');
    const serious = filter && filter.getAttribute('aria-pressed') === 'true';
    const items = Array.from(page.querySelectorAll('[data-find]'));
    let count = 0;
    items.forEach(item => {
      const visible = (!query || item.dataset.find.includes(query)) &&
        (!serious || item.dataset.bite === 'serious');
      item.classList.toggle('hide', !visible);
      if (visible) count++;
    });
    page.querySelector('.tcount').textContent = count + ' / ' + items.length;
    page.querySelector('.empty').classList.toggle('hide', count > 0);
  }

  function show() {
    const { id, params } = readRoute();
    const direct = document.getElementById('p-' + id);
    const anchor = direct ? null : document.getElementById(id);
    const page = direct || (anchor && anchor.closest('.page')) || document.getElementById('p-home');
    setMenu(false);
    pages.forEach(item => item.classList.toggle('hide', item !== page));
    links.forEach(link => {
      const current = link.getAttribute('href') === '#' + page.id.slice(2);
      if (current) {
        link.setAttribute('aria-current', 'page');
        link.setAttribute('data-active', 'true');
        // an active item inside a collapsed group would be invisible, so open it
        const group = link.closest('[data-slot="sidebar-group"]');
        if (group && group.dataset.state === 'closed') setGroup(group, true);
      } else {
        link.removeAttribute('aria-current');
        link.removeAttribute('data-active');
      }
    });
    const input = page.querySelector('input[type=search]');
    if (input) {
      input.value = anchor ? '' : params.get('q') || '';
      const filter = page.querySelector('[data-filter="serious"]');
      if (filter) filter.setAttribute('aria-pressed', String(!anchor && params.get('serious') === '1'));
      applyFilter(page);
    }
    const heading = page.querySelector('h1');
    document.title = (heading ? heading.textContent + ' — ' : '') + 'Cloud Rosetta';
    const destination = anchor && page.contains(anchor) ? anchor : heading;
    // Close navigation and settle page layout before positioning. Focus must move
    // out of the previous page so keyboard/browser focus cannot pull scrolling back.
    cancelAnimationFrame(pendingScroll);
    pendingScroll = requestAnimationFrame(() => {
      if (destination) {
        destination.setAttribute('tabindex', '-1');
        destination.focus({ preventScroll: true });
      }
      window.scrollTo({ top: anchor && destination ? destination.getBoundingClientRect().top + window.scrollY - 16 : 0, behavior: 'instant' });
    });
  }

  function navigate(hash) {
    if (location.hash !== hash) history.pushState(null, '', hash);
    show();
  }

  function saveFilters(page, push) {
    const params = new URLSearchParams();
    const value = page.querySelector('input[type=search]').value;
    if (value) params.set('q', value);
    const filter = page.querySelector('[data-filter="serious"]');
    if (filter && filter.getAttribute('aria-pressed') === 'true') params.set('serious', '1');
    const hash = '#' + page.id.slice(2) + (params.size ? '?' + params.toString() : '');
    if (hash !== location.hash) history[push ? 'pushState' : 'replaceState'](null, '', hash);
    applyFilter(page);
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (link) {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      navigate(link.getAttribute('href'));
      return;
    }
    const button = event.target.closest('button');
    if (!button) return;
    if (button.matches('.menutog')) { setMenu(!nav.classList.contains('open')); return; }
    if (button.matches('[data-slot="sidebar-group-label"]')) {
      const group = button.closest('[data-slot="sidebar-group"]');
      setGroup(group, group.dataset.state === 'closed');
      saveGroups();
      return;
    }
    if (button.matches('[data-slot="sidebar-trigger"]')) {
      setSidebar(app.dataset.sidebar !== 'collapsed', true);
      return;
    }
    if (button.matches('.themetog')) {
      const current = document.documentElement.getAttribute('data-theme');
      const dark = current ? current === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
      const next = dark ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('cr-theme', next); } catch (_) { /* Theme still works without storage. */ }
      return;
    }
    const page = button.closest('.page');
    if (button.matches('[data-filter="serious"]')) {
      button.setAttribute('aria-pressed', String(button.getAttribute('aria-pressed') !== 'true'));
      saveFilters(page, true);
    } else if (button.matches('[data-clear]')) {
      page.querySelector('input[type=search]').value = '';
      const filter = page.querySelector('[data-filter="serious"]');
      if (filter) filter.setAttribute('aria-pressed', 'false');
      saveFilters(page, true);
      page.querySelector('input[type=search]').focus();
    }
  });
  document.addEventListener('input', event => {
    if (event.target.matches('input[type=search]')) saveFilters(event.target.closest('.page'), false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); menu.focus(); }
    const typing = event.target.matches && event.target.matches('input, textarea, [contenteditable="true"]');
    if (!typing && (event.ctrlKey || event.metaKey) && !event.altKey && !event.shiftKey && event.key.toLowerCase() === 'b') {
      event.preventDefault();
      setSidebar(app.dataset.sidebar !== 'collapsed', true);
    }
  });
  window.addEventListener('hashchange', show);
  window.addEventListener('popstate', show);
  try { history.scrollRestoration = 'manual'; } catch (_) { /* Older embedded browsers use their default. */ }
  try {
    const theme = localStorage.getItem('cr-theme');
    if (theme === 'dark' || theme === 'light') document.documentElement.setAttribute('data-theme', theme);
  } catch (_) { /* The system theme remains available. */ }
  try {
    if (localStorage.getItem('cr-sidebar') === 'collapsed') setSidebar(true, false);
    const closed = JSON.parse(localStorage.getItem('cr-groups') || '[]');
    const groups = document.querySelectorAll('[data-slot="sidebar-group"]');
    closed.forEach(index => { if (groups[index]) setGroup(groups[index], false); });
  } catch (_) { /* Everything starts expanded without storage. */ }
  pages.forEach(applyFilter);
  show();
})();
