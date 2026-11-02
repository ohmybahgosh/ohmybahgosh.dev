/* ohmybahgosh.dev :: shared behavior.  No dependencies. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ROOT = document.documentElement.dataset.root || '/';

  const REPOS = [
    { name: 'TiviBro', slug: 'tivibro', desc: 'The IPTV player LG TVs never got' },
    { name: 'LG-USB-2-ETH0', slug: 'lg-usb-2-eth0', desc: 'USB Ethernet becomes the TV\'s eth0' },
    { name: 'WEBOS-ENTWARE-INSTALLER', slug: 'webos-entware-installer', desc: 'One-line Entware for rooted webOS' },
  ];

  /* ---------- typed terminals ---------- */
  const esc = (t) => t.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  async function runTerm(el) {
    const src = $('script[type="text/x-term"]', el);
    if (!src) return;
    const lines = JSON.parse(src.textContent);
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
  $$('.term[data-typed]').forEach(runTerm);

  /* ---------- live GitHub stats ---------- */
  const KEY = 'omb-gh-v1';
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
  async function gh() {
    let cache = null;
    try { cache = JSON.parse(localStorage.getItem(KEY)); } catch (e) {}
    if (cache && Date.now() - cache.t < 30 * 60e3) return cache.d;
    const d = {};
    await Promise.all(REPOS.map(async (r) => {
      try {
        const [a, b] = await Promise.all([
          fetch(`https://api.github.com/repos/ohmybahgosh/${r.name}`).then((x) => x.ok ? x.json() : null),
          fetch(`https://api.github.com/repos/ohmybahgosh/${r.name}/releases?per_page=1`).then((x) => x.ok ? x.json() : null),
        ]);
        if (a) d[r.name] = { stars: a.stargazers_count, forks: a.forks_count, issues: a.open_issues_count, pushed: a.pushed_at, release: b && b[0] ? b[0].tag_name : null };
      } catch (e) {}
    }));
    if (Object.keys(d).length) { try { localStorage.setItem(KEY, JSON.stringify({ t: Date.now(), d })); } catch (e) {} }
    return d;
  }
  if ($('[data-gh]')) gh().then((d) => {
    let total = 0;
    Object.values(d).forEach((r) => total += r.stars || 0);
    $$('[data-gh]').forEach((el) => {
      const [repo, f] = el.dataset.gh.split(':');
      if (repo === 'total') { if (total) el.textContent = total.toLocaleString(); return; }
      const r = d[repo];
      if (!r || r[f] == null) return;
      el.textContent = f === 'pushed' ? ago(r[f]) : typeof r[f] === 'number' ? r[f].toLocaleString() : r[f];
    });
  });

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

  /* ---------- command palette ---------- */
  const items = [
    { i: '~', t: 'cd ~', s: 'home', u: ROOT },
    ...REPOS.map((r) => ({ i: '▸', t: `cd ${r.slug}`, s: r.desc, u: ROOT + r.slug + '/' })),
    ...REPOS.map((r) => ({ i: '↗', t: `open github/${r.name}`, s: 'GitHub', u: `https://github.com/ohmybahgosh/${r.name}` })),
    { i: '↗', t: 'open tivibro.app', s: 'TiviBro website', u: 'https://tivibro.app' },
    { i: '↗', t: 'open github/ohmybahgosh', s: 'all repos', u: 'https://github.com/ohmybahgosh' },
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
  pal.onclick = (e) => { if (e.target === pal) close(); if (e.target.closest('a')) close(); };
  document.addEventListener('keydown', (e) => {
    if ((e.key === 'k' && (e.metaKey || e.ctrlKey)) || (e.key === '/' && !/input|textarea/i.test(document.activeElement.tagName))) { e.preventDefault(); pal.hidden ? open() : close(); }
    if (e.key === 'Escape' && !pal.hidden) close();
  });
  $$('[data-pal-open]').forEach((b) => b.onclick = open);
  const mac = /Mac|iPhone|iPad/.test(navigator.platform);
  $$('.kbtn kbd').forEach((k) => k.textContent = mac ? '⌘K' : 'Ctrl K');

  /* ---------- year ---------- */
  $$('[data-year]').forEach((y) => y.textContent = new Date().getFullYear());
})();
