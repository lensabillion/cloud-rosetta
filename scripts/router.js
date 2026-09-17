(function () {
  'use strict';
  const root = document.documentElement;
  const body = document.body;
  const pages = Array.from(document.querySelectorAll('.page'));
  const trees = Array.from(document.querySelectorAll('.tree'));
  const outlines = Array.from(document.querySelectorAll('.page-toc'));
  const header = document.querySelector('.topnav');
  const side = document.getElementById('side');
  const menuButton = document.querySelector('.menu-button');
  const dialog = document.querySelector('dialog.search');
  const field = dialog.querySelector('.search-input');
  const results = dialog.querySelector('.search-results');
  const note = dialog.querySelector('.search-note');
  const desktop = matchMedia('(min-width: {{bp-lg}})');
  let pendingScroll, ticking = false, index = null, selected = -1;

  const routeOf = page => page.id.slice(2);

  function setMenu(open) {
    body.dataset.menu = open ? 'open' : '';
    menuButton.setAttribute('aria-expanded', String(open));
  }

  function readRoute() {
    const [rawId, query = ''] = location.hash.slice(1).split('?');
    let id;
    try { id = decodeURIComponent(rawId || 'home'); } catch (_) { id = 'home'; }
    return { id, params: new URLSearchParams(query) };
  }

  function applyFilter(page) {
    const input = page.querySelector('input[data-scope]');
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

  function markNavigation(page) {
    const id = routeOf(page);
    const section = page.dataset.section || 'home';
    // The home page has no sidebar, but its menu still opens on a small screen,
    // so the first section's tree is the one it shows.
    const shown = section === 'home' ? trees[0].dataset.tree : section;
    trees.forEach(tree => tree.classList.toggle('hide', tree.dataset.tree !== shown));
    document.querySelectorAll('.tree-link').forEach(link => {
      if (link.getAttribute('href') === '#' + id) {
        link.setAttribute('aria-current', 'page');
        link.dataset.active = 'true';
      } else {
        link.removeAttribute('aria-current');
        delete link.dataset.active;
      }
    });
    document.querySelectorAll('.tree-parent').forEach(parent => {
      parent.dataset.expanded = String(!!parent.querySelector('.tree-link[data-active="true"]'));
    });
    document.querySelectorAll('[data-tab]').forEach(tab => {
      if (tab.dataset.tab === section) tab.dataset.active = 'true';
      else delete tab.dataset.active;
    });
    outlines.forEach(outline => outline.classList.toggle('hide', outline.dataset.for !== id));
    keepActiveLinkInView();
  }

  function keepActiveLinkInView() {
    const link = side.querySelector('.tree:not(.hide) .tree-link[data-active="true"]');
    if (!link || side.scrollHeight <= side.clientHeight) return;
    const box = side.getBoundingClientRect(), item = link.getBoundingClientRect();
    if (item.top < box.top || item.bottom > box.bottom) {
      side.scrollTop += item.top - box.top - box.height / 3;
    }
  }

  function updateOutline() {
    const outline = outlines.find(item => !item.classList.contains('hide'));
    if (!outline || !outline.offsetParent) return;
    const items = Array.from(outline.querySelectorAll('li'));
    const limit = header.offsetHeight + 24;
    let current = 0;
    items.forEach((item, i) => {
      const link = item.querySelector('a');
      const target = link && document.getElementById(link.getAttribute('href').slice(1));
      if (target && target.getBoundingClientRect().top <= limit) current = i;
    });
    items.forEach((item, i) => {
      if (i === current) item.dataset.active = 'true';
      else delete item.dataset.active;
    });
  }

  // `moved` is true when the reader navigated. Focus follows them to the new
  // page so a screen reader announces it, but the first paint leaves focus
  // alone: nobody asked for it, and it would ring the title on arrival.
  function show(moved) {
    const { id, params } = readRoute();
    const direct = document.getElementById('p-' + id);
    const anchor = direct ? null : document.getElementById(id);
    const page = direct || (anchor && anchor.closest('.page')) || document.getElementById('p-home');
    setMenu(false);
    if (dialog.open) dialog.close();
    pages.forEach(item => item.classList.toggle('hide', item !== page));
    body.dataset.section = page.dataset.section || 'home';
    markNavigation(page);
    const input = page.querySelector('input[data-scope]');
    if (input) {
      input.value = anchor ? '' : params.get('q') || '';
      const filter = page.querySelector('[data-filter="serious"]');
      if (filter) filter.setAttribute('aria-pressed', String(!anchor && params.get('serious') === '1'));
      applyFilter(page);
    }
    const heading = page.querySelector('h1');
    document.title = (heading ? heading.textContent.trim() + ' — ' : '') + 'Cloud Rosetta';
    const destination = anchor && page.contains(anchor) ? anchor : heading;
    // Close navigation and settle page layout before positioning. Focus must move
    // out of the previous page so keyboard/browser focus cannot pull scrolling back.
    cancelAnimationFrame(pendingScroll);
    pendingScroll = requestAnimationFrame(() => {
      if (destination && moved) {
        destination.setAttribute('tabindex', '-1');
        destination.focus({ preventScroll: true });
      }
      const offset = header.offsetHeight + 20;
      window.scrollTo({
        top: anchor && destination ? destination.getBoundingClientRect().top + window.scrollY - offset : 0,
        behavior: 'instant',
      });
      updateOutline();
    });
  }

  function navigate(hash) {
    if (location.hash !== hash) history.pushState(null, '', hash);
    show(true);
  }

  function saveFilters(page, push) {
    const params = new URLSearchParams();
    const value = page.querySelector('input[data-scope]').value;
    if (value) params.set('q', value);
    const filter = page.querySelector('[data-filter="serious"]');
    if (filter && filter.getAttribute('aria-pressed') === 'true') params.set('serious', '1');
    const hash = '#' + routeOf(page) + (params.size ? '?' + params.toString() : '');
    if (hash !== location.hash) history[push ? 'pushState' : 'replaceState'](null, '', hash);
    applyFilter(page);
  }

  // ---------------------------------------------------------------- search
  function buildIndex() {
    const entries = [];
    const label = section => {
      const tab = document.querySelector('.topnav [data-tab="' + section + '"]');
      return tab ? tab.textContent.trim() : '';
    };
    pages.forEach(page => {
      if ((page.dataset.section || 'home') === 'home') return;
      const heading = page.querySelector('h1');
      const title = heading ? heading.textContent.trim() : '';
      let current = { href: '#' + routeOf(page), title: title, context: label(page.dataset.section),
        hay: title.toLowerCase(), rank: 3 };
      entries.push(current);
      Array.from(page.children).forEach(node => {
        if ((node.tagName === 'H2' || node.tagName === 'H3') && node.id) {
          current = { href: '#' + node.id, title: node.textContent.trim(), context: title,
            hay: node.textContent.toLowerCase(), rank: 2 };
          entries.push(current);
        } else if (node.matches('p, ul, ol, blockquote, .tw, figure')) {
          current.hay += ' ' + node.textContent.toLowerCase();
        }
      });
      // A mapping row and a decoder term are what most searches are looking for.
      page.querySelectorAll('article[id][data-find]').forEach(item => {
        const name = item.querySelector('h3');
        entries.push({ href: '#' + item.id, title: name ? name.textContent.trim() : '', context: title,
          hay: item.dataset.find, rank: 4 });
      });
    });
    return entries;
  }

  function search(query) {
    const words = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    if (!index) index = buildIndex();
    const found = [];
    index.forEach((entry, order) => {
      const title = entry.title.toLowerCase();
      const inTitle = words.every(word => title.includes(word));
      if (!inTitle && !words.every(word => entry.hay.includes(word))) return;
      found.push({ entry: entry, order: order,
        score: entry.rank + (inTitle ? 10 : 0) + (title.startsWith(words[0]) ? 5 : 0) });
    });
    found.sort((a, b) => b.score - a.score || a.order - b.order);
    return found.slice(0, 20).map(hit => hit.entry);
  }

  function renderResults() {
    const query = field.value.trim();
    const found = search(query);
    results.replaceChildren(...found.map((entry, i) => {
      const option = document.createElement('li');
      option.id = 'search-result-' + i;
      option.setAttribute('role', 'option');
      option.setAttribute('aria-selected', String(i === 0));
      const link = document.createElement('a');
      link.href = entry.href;
      link.tabIndex = -1;
      const title = document.createElement('span');
      title.className = 'result-title';
      title.textContent = entry.title;
      const context = document.createElement('span');
      context.className = 'result-context';
      context.textContent = entry.context;
      link.append(title, context);
      option.append(link);
      return option;
    }));
    selected = found.length ? 0 : -1;
    field.setAttribute('aria-activedescendant', selected >= 0 ? 'search-result-0' : '');
    note.textContent = !query
      ? 'Search chapters, service equivalents and terms'
      : found.length
        ? found.length + (found.length === 1 ? ' result' : ' results')
        : 'Nothing matches ' + query;
  }

  function openSearch() {
    setMenu(false);
    if (!dialog.open) dialog.showModal();
    field.select();
    renderResults();
  }

  function moveSelection(step) {
    const options = Array.from(results.children);
    if (!options.length) return;
    selected = (selected + step + options.length) % options.length;
    options.forEach((option, i) => option.setAttribute('aria-selected', String(i === selected)));
    field.setAttribute('aria-activedescendant', options[selected].id);
    options[selected].scrollIntoView({ block: 'nearest' });
  }

  field.addEventListener('input', renderResults);
  field.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      moveSelection(event.key === 'ArrowDown' ? 1 : -1);
    } else if (event.key === 'Enter') {
      event.preventDefault();
      const option = results.children[selected];
      if (option) navigate(option.querySelector('a').getAttribute('href'));
    }
  });
  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });

  // ---------------------------------------------------------------- events
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (link) {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      if (link.hasAttribute('data-skip')) {
        const page = pages.find(item => !item.classList.contains('hide'));
        const target = page && (page.querySelector('h1') || page);
        if (target) { target.setAttribute('tabindex', '-1'); target.focus(); }
        return;
      }
      navigate(link.getAttribute('href'));
      return;
    }
    const button = event.target.closest('button');
    if (!button) return;
    if (button.matches('.menu-button')) { setMenu(body.dataset.menu !== 'open'); return; }
    if (button.hasAttribute('data-search-open')) { openSearch(); return; }
    if (button.hasAttribute('data-search-close')) { dialog.close(); return; }
    if (button.matches('.themetog')) {
      const current = root.getAttribute('data-theme');
      const dark = current ? current === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
      const next = dark ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('cr-theme', next); } catch (_) { /* Theme still works without storage. */ }
      return;
    }
    const page = button.closest('.page');
    if (!page) return;
    if (button.matches('[data-filter="serious"]')) {
      button.setAttribute('aria-pressed', String(button.getAttribute('aria-pressed') !== 'true'));
      saveFilters(page, true);
    } else if (button.matches('[data-clear]')) {
      page.querySelector('input[data-scope]').value = '';
      const filter = page.querySelector('[data-filter="serious"]');
      if (filter) filter.setAttribute('aria-pressed', 'false');
      saveFilters(page, true);
      page.querySelector('input[data-scope]').focus();
    }
  });
  document.addEventListener('input', event => {
    if (event.target.matches('input[data-scope]')) saveFilters(event.target.closest('.page'), false);
  });
  document.addEventListener('keydown', event => {
    const typing = event.target.closest && event.target.closest('input, textarea, [contenteditable="true"]');
    if ((event.metaKey || event.ctrlKey) && !event.altKey && !event.shiftKey && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      if (dialog.open) dialog.close(); else openSearch();
      return;
    }
    if (event.key === '/' && !typing && !dialog.open) { event.preventDefault(); openSearch(); return; }
    if (event.key === 'Escape' && body.dataset.menu === 'open') { setMenu(false); menuButton.focus(); }
  });
  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      header.dataset.scrolled = String(window.scrollY > 0);
      updateOutline();
    });
  }, { passive: true });
  desktop.addEventListener('change', () => { if (desktop.matches) setMenu(false); });
  window.addEventListener('hashchange', () => show(true));
  window.addEventListener('popstate', () => show(true));
  try { history.scrollRestoration = 'manual'; } catch (_) { /* Older embedded browsers use their default. */ }
  try {
    const theme = localStorage.getItem('cr-theme');
    if (theme === 'dark' || theme === 'light') root.setAttribute('data-theme', theme);
  } catch (_) { /* The system theme remains available. */ }
  const platform = (navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || '';
  root.dataset.platform = /mac|iphone|ipad|ipod/i.test(platform) ? 'mac' : 'win';
  pages.forEach(applyFilter);
  show(false);
})();
