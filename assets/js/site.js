/* ohmybahgosh.dev :: shared behavior.  No dependencies. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ROOT = document.documentElement.dataset.root || '/';

  const REPOS = [
    { name: 'TiviBro', slug: 'tivibro', desc: 'The IPTV player LG TVs never got' },
    { name: 'LG-USB-2-ETH0', slug: 'lg-usb-2-eth0', desc: 'USB Ethernet becomes the TV\'s eth0' },
    { name: 'WEBOS-ENTWARE-INSTALLER', slug: 'webos-entware-installer', desc: 'Entware for rooted webOS: TV app, packages, add-ons' },
    { name: 'LG-WEBOS-SSH-DOCTOR', slug: 'ssh-doctor', desc: 'Check and fix SSH on a rooted LG TV, pair a key' },
    { name: 'WEBOS-LUNA-SEND-ATLAS', slug: 'luna-atlas', desc: 'Every LG webOS luna-send command, documented' },
    { name: 'pipseek', slug: 'pipseek', desc: 'Search PyPI from your terminal', tool: true },
  ];

  /* ---------- typed terminals ---------- */
  const esc = (t) => t.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  async function runTerm(el) {
    const src = $('script[type="text/x-term"]', el);
    if (!src) return;
    const d = await Promise.race([gh(), sleep(1500).then(() => null)]);
    const lines = JSON.parse(fillTokens(src.textContent, d));
    const scr = $('.scr', el);
    const prompt = el.dataset.prompt || '<span class="c-gr">root@lgtv</span>:<span class="c-cy">~</span># ';
    const loop = el.dataset.loop !== 'false';
    const render = () => {
      scr.innerHTML = lines.filter((l) => l[0] !== 'p' && l[0] !== 'clr')
        .map((l) => `<span class="ln">${l[0] === '$' ? prompt + esc(l[1]) : l[1]}</span>`).join('') +
        `<span class="ln">${prompt}<span class="caret"></span></span>`;
    };
    if (reduce) return render();

    let seen = false;
    await new Promise((res) => {
      const io = new IntersectionObserver((e) => { if (e[0].isIntersecting && !seen) { seen = true; io.disconnect(); res(); } }, { threshold: .25 });
      io.observe(el);
    });

    do {
      scr.innerHTML = '';
      for (const [kind, text] of lines) {
        if (kind === 'p') { await sleep(text); continue; }
        if (kind === 'clr') { await sleep(1200); scr.innerHTML = ''; continue; }
        const ln = document.createElement('span');
        ln.className = 'ln';
        scr.appendChild(ln);
        if (kind === '$') {
          ln.innerHTML = prompt + '<span class="t"></span><span class="caret"></span>';
          const t = $('.t', ln);
          await sleep(350);
          for (const ch of text) { t.textContent += ch; await sleep(18 + Math.random() * 38); }
          await sleep(260);
          $('.caret', ln).remove();
        } else {
          ln.innerHTML = text;
          await sleep(kind === 'o!' ? 380 : 70);
        }
      }
      const end = document.createElement('span');
      end.className = 'ln';
      end.innerHTML = prompt + '<span class="caret"></span>';
      scr.appendChild(end);
      if (loop) await sleep(5200);
    } while (loop);
  }

  /* ---------- live GitHub stats ---------- */
  const KEY = 'omb-gh-v2';
  const ago = (iso) => {
    const s = (Date.now() - new Date(iso)) / 1000;
    if (s < 3600) return 'just now';
    if (s < 86400) return Math.floor(s / 3600) + 'h ago';
    const d = Math.floor(s / 86400);
    if (d < 2) return 'yesterday';
    if (d < 45) return d + 'd ago';
    if (d < 400) return Math.floor(d / 30) + 'mo ago';
    return Math.floor(d / 365) + 'y ago';
  };
  // Site data: /data/repos.json is rebuilt from GitHub on every deploy and every few hours,
  // so pages stay current with no edits.  The live API is only a fallback (local previews).
  let ghPromise = null;
  const gh = () => ghPromise || (ghPromise = (async () => {
    try {
      const r = await fetch(ROOT + 'data/repos.json', { cache: 'no-cache' });
      if (r.ok) {
        const j = await r.json();
        const d = {};
        Object.values(j.repos || {}).forEach((x) => { d[x.name] = { ...x, release: x.tag, releases: (x.releases || []).map((y) => ({ ...y, body: y.notes })) }; });
        if (Object.keys(d).length) return d;
      }
    } catch (e) {}
    let cache = null;
    try { cache = JSON.parse(localStorage.getItem(KEY)); } catch (e) {}
    if (cache && Date.now() - cache.t < 30 * 60e3) return cache.d;
    const d = {};
    const get = (u) => fetch('https://api.github.com/repos/ohmybahgosh/' + u).then((x) => x.ok ? x.json() : null).catch(() => null);
    await Promise.all(REPOS.map(async (r) => {
      const [a, rel0, com] = await Promise.all([get(r.name), get(r.name + '/releases?per_page=20'), get(r.name + '/commits?per_page=4')]);
      if (!a) return;
      // GitHub doesn't list releases newest first (alpha.99 above alpha.101): by when they were published.
      const at = (x) => x.published_at || x.created_at || '';
      const rel = rel0 && rel0.filter((x) => !x.draft).sort((x, y) => (at(y) > at(x) ? 1 : at(y) < at(x) ? -1 : 0)).slice(0, 6);
      const tag = rel && rel[0] ? rel[0].tag_name : null;
      d[r.name] = {
        stars: a.stargazers_count, forks: a.forks_count, issues: a.open_issues_count, pushed: a.pushed_at,
        release: tag, tag, version: tag && tag.replace(/^v/, ''), version_name: rel && rel[0] ? rel[0].name : null,
        downloads: (rel || []).reduce((n, x) => n + (x.assets || []).reduce((m, y) => m + y.download_count, 0), 0),
        releases: (rel || []).map((x) => ({ tag: x.tag_name, name: x.name || x.tag_name, pre: x.prerelease, at: x.published_at || x.created_at, url: x.html_url, body: (x.body || '').slice(0, 600) })),
        commits: (com || []).map((x) => ({ msg: x.commit.message.split('\n')[0], at: x.commit.author.date, url: x.html_url, sha: x.sha.slice(0, 7) })),
      };
    }));
    if (Object.keys(d).length) { try { localStorage.setItem(KEY, JSON.stringify({ t: Date.now(), d })); } catch (e) {} }
    return d;
  })());
  // {{Repo:field|fallback}} tokens inside terminal demos and placeholders
  const fillTokens = (text, d) => text.replace(/\{\{([\w.-]+):(\w+)(?:\|([^}]*))?\}\}/g, (m, repo, f, fb) => {
    const v = d && d[repo] && d[repo][f];
    return v != null && v !== '' ? String(v) : (fb || '');
  });
  window.ombData = gh;
  window.ombFill = fillTokens;
  $$('.term[data-typed]').forEach(runTerm);
  const plain = (md) => md.replace(/```[\s\S]*?```/g, ' ').replace(/!\[[^\]]*\]\([^)]*\)/g, '').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/<[^>]+>/g, '').replace(/^#+\s*/gm, '').replace(/[*_`>|]/g, '').replace(/^\s*[-+]\s+/gm, '• ').replace(/\s+/g, ' ').trim();
  const COLORS = { 'TiviBro': '#33e1ff', 'LG-USB-2-ETH0': '#3ddc97', 'WEBOS-ENTWARE-INSTALLER': '#ff3ea5', 'pipseek': '#4c9eff', 'WEBOS-LUNA-SEND-ATLAS': '#3ddc97', 'LG-WEBOS-SSH-DOCTOR': '#3ddc97' };
  const SHORT = { 'TiviBro': 'TiviBro', 'LG-USB-2-ETH0': 'USB-2-ETH0', 'WEBOS-ENTWARE-INSTALLER': 'Entware', 'pipseek': 'pipseek', 'WEBOS-LUNA-SEND-ATLAS': 'Luna Atlas', 'LG-WEBOS-SSH-DOCTOR': 'SSH Doctor' };

  gh().then((d) => {
    let total = 0, all = 0;
    const webos = REPOS.filter((r) => !r.tool).map((r) => r.name);
    Object.entries(d).forEach(([k, r]) => { all += r.stars || 0; if (webos.includes(k)) total += r.stars || 0; });
    $$('[data-gh]').forEach((el) => {
      const [repo, f] = el.dataset.gh.split(':');
      if (repo === 'total') { if (total) el.textContent = total.toLocaleString(); return; }
      if (repo === 'all') { if (all) el.textContent = all.toLocaleString(); return; }
      const r = d[repo];
      if (!r || r[f] == null) return;
      el.textContent = (f === 'pushed' || f === 'released') ? ago(r[f]) : typeof r[f] === 'number' ? r[f].toLocaleString() : r[f];
    });

    // Recent activity across the showcased repos
    const feed = $('#feed');
    if (feed) {
      const items = [];
      Object.entries(d).forEach(([repo, r]) => {
        (r.releases || []).slice(0, 2).forEach((x) => items.push({ repo, kind: 'release', text: x.name, url: x.url, at: x.at }));
        (r.commits || []).forEach((x) => items.push({ repo, kind: 'commit', text: x.msg, url: x.url, at: x.at }));
      });
      items.sort((a, b) => new Date(b.at) - new Date(a.at));
      feed.innerHTML = items.length ? items.slice(0, 8).map((x) => `<li><span class="k" style="--kc:${COLORS[x.repo]}">${x.kind === 'release' ? '▲ release' : '● commit'}</span><a href="${x.url}" target="_blank" rel="noopener"><small>${SHORT[x.repo]}</small>${esc(x.text)}</a><time datetime="${x.at}">${ago(x.at)}</time></li>`).join('')
        : '<li><span class="empty">GitHub is rate-limiting this browser.  <a href="https://github.com/ohmybahgosh" target="_blank" rel="noopener">See the activity on GitHub ↗</a></span></li>';
    }

    // Release timeline on a project page
    const tl = $('#timeline');
    if (tl) {
      const r = d[tl.dataset.repo];
      const rels = r && r.releases || [];
      if (r && (tl.dataset.mode === 'commits' || !rels.length) && (r.commits || []).length) {
        tl.innerHTML = r.commits.map((x) => `<div class="rel"><div class="card"><h3><a href="${x.url}" target="_blank" rel="noopener">${esc(x.msg)}</a></h3><div class="when">${x.sha} · ${new Date(x.at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })} · ${ago(x.at)}</div></div></div>`).join('');
        return;
      }
      tl.innerHTML = rels.length ? rels.map((x) => `<div class="rel"><div class="card"><h3><a href="${x.url}" target="_blank" rel="noopener">${esc(x.name)}</a>${x.pre ? '<span class="pill" style="--ca:var(--amber)">pre-release</span>' : '<span class="pill">stable</span>'}</h3><div class="when">${esc(x.tag)} · ${new Date(x.at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })} · ${ago(x.at)}</div><p>${esc(plain(x.body)) || 'No notes for this release.'}</p></div></div>`).join('')
        : `<p class="muted">Couldn't load releases right now.  <a class="c-cy" href="https://github.com/ohmybahgosh/${tl.dataset.repo}/releases" target="_blank" rel="noopener">See them on GitHub ↗</a></p>`;
    }
  });

  /* ---------- theme toggle ---------- */
  const setTheme = (t) => {
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem('omb-theme', t); } catch (e) {}
    const m = $('meta[name="theme-color"]');
    if (m) m.content = t === 'light' ? '#f5f7fc' : '#05070d';
  };
  $$('[data-theme-toggle]').forEach((b) => b.onclick = () => setTheme(document.documentElement.dataset.theme === 'light' ? 'dark' : 'light'));
  if (document.documentElement.dataset.theme === 'light') setTheme('light');

  /* ---------- copy buttons ---------- */
  $$('.code').forEach((c) => {
    const b = document.createElement('button');
    b.className = 'copy';
    b.type = 'button';
    b.textContent = 'copy';
    b.setAttribute('aria-label', 'Copy command');
    b.onclick = async () => {
      const txt = $('pre', c).innerText.split('\n').filter((l) => !l.trim().startsWith('#')).map((l) => l.replace(/^\$ /, '')).join('\n').trim();
      try { await navigator.clipboard.writeText(txt); } catch (e) {
        const ta = document.createElement('textarea'); ta.value = txt; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
      }
      b.textContent = 'copied'; b.classList.add('ok');
      setTimeout(() => { b.textContent = 'copy'; b.classList.remove('ok'); }, 1600);
    };
    c.appendChild(b);
  });

  /* ---------- tabs ---------- */
  $$('[data-tabs]').forEach((w) => {
    const btns = $$('.tabs button', w);
    btns.forEach((b) => b.onclick = () => {
      btns.forEach((x) => x.setAttribute('aria-selected', x === b));
      $$('.tabpanel', w).forEach((p) => p.hidden = p.id !== b.dataset.for);
    });
  });

  /* ---------- card spotlight ---------- */
  $$('.card').forEach((c) => c.addEventListener('pointermove', (e) => {
    const r = c.getBoundingClientRect();
    c.style.setProperty('--mx', e.clientX - r.left + 'px');
    c.style.setProperty('--my', e.clientY - r.top + 'px');
  }));

  /* ---------- reveal on scroll ---------- */
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    $$('.rv').forEach((el) => io.observe(el));
  } else $$('.rv').forEach((el) => el.classList.add('in'));

  /* ---------- lightbox ---------- */
  $$('.gallery figure').forEach((f) => f.addEventListener('click', () => {
    const img = $('img', f);
    const lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.innerHTML = `<div><img src="${img.src}" alt="${img.alt}"><p>${esc(img.alt)}</p></div>`;
    lb.onclick = () => lb.remove();
    document.addEventListener('keydown', function k(e) { if (e.key === 'Escape') { lb.remove(); document.removeEventListener('keydown', k); } });
    document.body.appendChild(lb);
  }));

  /* ---------- projects menu: hover on desktop, tap on touch ---------- */
  $$('[data-menu]').forEach((m) => {
    const b = $('.mbtn', m);
    const set = (on) => { m.classList.toggle('open', on); b.setAttribute('aria-expanded', on); };
    b.addEventListener('click', (e) => { e.stopPropagation(); set(!m.classList.contains('open')); });
    document.addEventListener('click', (e) => { if (!m.contains(e.target)) set(false); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && m.classList.contains('open')) { set(false); b.focus(); } });
    $$('a', m).forEach((a) => a.addEventListener('click', () => set(false)));
  });

  /* ---------- command palette ---------- */
  const items = [
    { i: '~', t: 'cd ~', s: 'home', u: ROOT },
    ...REPOS.map((r) => ({ i: '▸', t: `cd ${r.slug}`, s: r.desc, u: ROOT + r.slug + '/' })),
    ...REPOS.map((r) => ({ i: '↗', t: `open github/${r.name}`, s: 'GitHub', u: `https://github.com/ohmybahgosh/${r.name}` })),
    { i: '↗', t: 'open tivibro.app', s: 'TiviBro website', u: 'https://tivibro.app/?utm_source=ohmybahgosh.dev&utm_medium=referral&utm_campaign=ohmybahgosh&utm_content=command_palette' },
    { i: '↗', t: 'open github/ohmybahgosh', s: 'all repos', u: 'https://github.com/ohmybahgosh' },
    { i: '▸', t: 'cd install', s: 'install guide: root, Homebrew Channel, repo', u: ROOT + 'install/' },
    { i: '▸', t: 'cd guides', s: 'how-tos for rooted LG TVs', u: ROOT + 'guides/' },
    { i: '▶', t: 'play tour', s: 'the 2-minute video tour', u: ROOT + 'tour/' },
    ...[['lg-tv-ethernet-100mbps', 'LG TV Ethernet stuck at 100 Mbps'], ['usb-ethernet-adapter-lg-tv', 'which USB Ethernet adapter'], ['ssh-into-lg-tv', 'SSH into a rooted LG TV'], ['homebrew-channel-repository', 'add a Homebrew Channel repo'], ['iptv-player-lg-tv', 'an IPTV player for LG TVs'], ['root-lg-tv-2026', 'rooting an LG TV in 2026'], ['lg-tv-wake-on-lan', 'turn on an LG TV over the network (Wake on LAN)'], ['block-lg-tv-updates', 'block LG TV firmware updates'], ['tailscale-lg-tv', 'Tailscale on an LG TV'], ['lg-tv-file-sharing-samba', 'Samba and file sharing on an LG TV']]
      .map(([g, d]) => ({ i: '▸', t: `cat guides/${g}`, s: d, u: ROOT + 'guides/' + g + '/' })),
    ...REPOS.filter((r) => !r.tool).map((r) => ({ i: '?', t: `man ${r.slug}`, s: r.name + ' FAQ', u: ROOT + r.slug + '/faq/' })),
    { i: '▸', t: 'cd luna-atlas/examples', s: 'common luna-send commands', u: ROOT + 'luna-atlas/examples/' },
    { i: '▸', t: 'cd luna-atlas/categories', s: 'luna-send commands by category', u: ROOT + 'luna-atlas/categories/' },
    { i: '?', t: 'whoami', s: 'about OhMyBahGosh', u: ROOT + 'about/' },
    { i: '@', t: 'mail hello', s: 'contact and templates', u: ROOT + 'contact/' },
    { i: '◐', t: 'theme toggle', s: 'light / dark', u: '#theme' },
    ...$$('section[id][data-pal]').map((s) => ({ i: '#', t: 'goto ' + s.id, s: s.dataset.pal, u: '#' + s.id })),
  ];
  const pal = document.createElement('div');
  pal.className = 'pal';
  pal.hidden = true;
  pal.innerHTML = `<div class="box" role="dialog" aria-label="Command palette"><input type="text" placeholder="type a command or repo..." aria-label="Search"><ul></ul><div class="hint"><span>↑↓ move</span><span>↵ open</span><span>esc close</span></div></div>`;
  document.body.appendChild(pal);
  const inp = $('input', pal), ul = $('ul', pal);
  let sel = 0, list = items;
  const draw = () => {
    ul.innerHTML = list.map((x, n) => `<li><a href="${x.u}" class="${n === sel ? 'on' : ''}" ${x.u.startsWith('http') ? 'target="_blank" rel="noopener"' : ''}><i>${x.i}</i>${esc(x.t)}<small>${esc(x.s)}</small></a></li>`).join('') || '<li><a class="on"><i>!</i>command not found</a></li>';
  };
  const open = () => { pal.hidden = false; inp.value = ''; list = items; sel = 0; draw(); setTimeout(() => inp.focus(), 10); };
  const close = () => { pal.hidden = true; };
  inp.oninput = () => {
    const q = inp.value.toLowerCase().trim();
    list = items.filter((x) => (x.t + ' ' + x.s).toLowerCase().includes(q));
    sel = 0; draw();
  };
  inp.onkeydown = (e) => {
    if (e.key === 'ArrowDown') { sel = Math.min(sel + 1, list.length - 1); draw(); e.preventDefault(); }
    if (e.key === 'ArrowUp') { sel = Math.max(sel - 1, 0); draw(); e.preventDefault(); }
    if (e.key === 'Enter') { const a = $$('a', ul)[sel]; if (a) { close(); a.click(); } }
  };
  pal.onclick = (e) => {
    if (e.target === pal) close();
    const l = e.target.closest('a');
    if (l) { close(); if (l.getAttribute('href') === '#theme') { e.preventDefault(); setTheme(document.documentElement.dataset.theme === 'light' ? 'dark' : 'light'); } }
  };
  document.addEventListener('keydown', (e) => {
    if ((e.key === 'k' && (e.metaKey || e.ctrlKey)) || (e.key === '/' && !/input|textarea/i.test(document.activeElement.tagName))) { e.preventDefault(); pal.hidden ? open() : close(); }
    if (e.key === 'Escape' && !pal.hidden) close();
  });
  $$('[data-pal-open]').forEach((b) => b.onclick = open);
  const mac = /Mac|iPhone|iPad/.test(navigator.platform);
  $$('.kbtn kbd').forEach((k) => k.textContent = mac ? '⌘K' : 'Ctrl K');

  /* ---------- email links (built here to keep the address from simple scrapers) ---------- */
  const MAIL = ['hello', 'ohmybahgosh.dev'].join('@');
  $$('[data-mail]').forEach((a) => { if (!a.getAttribute('href') || a.getAttribute('href') === '#' || a.dataset.mail === 'text') a.href = 'mailto:' + MAIL; if (a.dataset.mail === 'text') a.textContent = MAIL; });

  /* ---------- year ---------- */
  $$('[data-year]').forEach((y) => y.textContent = new Date().getFullYear());
})();
