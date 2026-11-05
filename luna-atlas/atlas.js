/* Luna Atlas catalog browser: search, filters, master/detail, deep links.  No dependencies.
   Data: catalog.json next to this page (refreshed on deploy), or the repo's copy on GitHub. */
(() => {
  'use strict';
  const root = document.getElementById('atlas');
  if (!root) return;

  const SOURCES = ['/luna-atlas/catalog.json', 'https://raw.githubusercontent.com/ohmybahgosh/WEBOS-LUNA-SEND-ATLAS/main/web/catalog.json'];
  const ROW = 58;
  const $ = (s, r = root) => r.querySelector(s);
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmt = (n) => Number(n).toLocaleString('en-US');
  const ACCESS = ['public', 'private', 'ssap', 'root', 'unknown'];
  const CONF = ['documented', 'inferred', 'stub'];
  const NOTE_M = 'Description inferred from the method name; parameters not publicly documented.';
  const NOTE_S = 'Service description inferred; this service is not publicly documented.';
  const NOTE_STUB = 'Found on a TV, but nothing is documented about it yet.';

  const el = {
    q: $('#atlas-q'), cat: $('#atlas-cat'), acc: $('#atlas-acc'), conf: $('#atlas-conf'), dz: $('#atlas-dz'),
    dzw: $('#atlas-dzw'), count: $('#atlas-count'), clear: $('#atlas-clear'), side: $('#atlas-side'),
    svcHead: $('#atlas-svchead'), list: $('#atlas-list'), listTitle: $('#atlas-listtitle'), detail: $('#atlas-detail'),
    body: $('#atlas-body'), loading: $('#atlas-loading'), seg: root.querySelectorAll('[data-side]'),
  };

  let S = [];          // services
  let M = [];          // every method, flattened
  let byName = {};     // service name -> index
  let list = [];       // indexes into M for the method list
  let svcCount = [];   // matches per service for the current filters
  let catCount = {};   // matches per category for the current filters
  const st = { q: '', cat: '', acc: '', conf: '', danger: false, svc: -1, sel: -1, side: 'services' };

  /* ---------- load ---------- */
  async function load() {
    for (const src of SOURCES) {
      try {
        const r = await fetch(src, { cache: 'no-cache' });
        if (!r.ok) continue;
        const j = await r.json();
        if (j && Array.isArray(j.services)) return init(j);
      } catch (e) { /* try the next source */ }
    }
    el.loading.innerHTML = 'The catalog didn\'t load.  <a class="c-gr" href="https://github.com/ohmybahgosh/WEBOS-LUNA-SEND-ATLAS">Browse it on GitHub ↗</a>';
  }

  function init(j) {
    S = j.services.map((s, i) => ({ name: s.service, sd: s.sd || '', sdc: s.sdc || 'inferred', n: (s.methods || []).length, i }));
    S.forEach((s) => { byName[s.name] = s.i; });
    j.services.forEach((s, si) => (s.methods || []).forEach((m) => {
      M.push({
        m: m.m || '', u: m.u, c: m.c || 'misc', a: m.a || 'unknown', s: !!m.s, d: !!m.d, dc: m.dc || 'inferred',
        desc: m.desc || '', p: m.p || {}, si,
        hay: (m.m + ' ' + s.service + ' ' + m.u + ' ' + (m.desc || '') + ' ' + m.c).toLowerCase(),
      });
    }));
    const c = j.counts || {};
    fill('methods', c.methods || M.length);
    fill('services', c.services || S.length);
    const bd = c.by_doc || {};
    fill('documented', bd.documented || 0);
    fill('inferred', bd.inferred || 0);
    fill('dangerous', M.filter((m) => m.d).length);
    fill('categories', Object.keys(c.by_category || {}).length);

    const cats = Object.entries(c.by_category || {}).sort((a, b) => b[1] - a[1]);
    el.cat.innerHTML = '<option value="">every category</option>' + cats.map(([k, n]) => `<option value="${esc(k)}">${esc(k)} (${fmt(n)})</option>`).join('');
    const ba = c.by_access || {};
    el.acc.innerHTML = '<option value="">any access</option>' + ACCESS.filter((a) => ba[a]).map((a) => `<option value="${a}">${a} (${fmt(ba[a])})</option>`).join('');
    el.conf.innerHTML = '<option value="">any confidence</option>' + CONF.filter((k) => bd[k]).map((k) => `<option value="${k}">${k} (${fmt(bd[k])})</option>`).join('');

    el.loading.hidden = true;
    el.body.hidden = false;
    root.dataset.view = 'list';
    applyHash(true);
    render();
  }
  function fill(key, v) { document.querySelectorAll(`[data-atlas-count="${key}"]`).forEach((n) => { n.textContent = fmt(v); }); }

  /* ---------- filtering ---------- */
  function compute() {
    const toks = st.q.toLowerCase().split(/\s+/).filter(Boolean);
    svcCount = new Array(S.length).fill(0);
    catCount = {};
    list = [];
    for (let i = 0; i < M.length; i++) {
      const m = M[i];
      if (st.acc && m.a !== st.acc) continue;
      if (st.conf && m.dc !== st.conf) continue;
      if (st.danger && !m.d) continue;
      if (toks.length && !toks.every((t) => m.hay.includes(t))) continue;
      catCount[m.c] = (catCount[m.c] || 0) + 1;
      if (st.cat && m.c !== st.cat) continue;
      svcCount[m.si]++;
      if (st.svc >= 0 && m.si !== st.svc) continue;
      list.push(i);
    }
    if (toks.length) {
      // name matches first, then shorter names
      const q = toks.join(' ');
      const score = (m) => (m.m.toLowerCase() === q ? 0 : m.m.toLowerCase().startsWith(toks[0]) ? 1 : m.m.toLowerCase().includes(toks[0]) ? 2 : 3);
      list.sort((a, b) => score(M[a]) - score(M[b]) || M[a].m.length - M[b].m.length);
    }
  }
  const filtering = () => !!(st.q || st.cat || st.acc || st.conf || st.danger);

  /* ---------- render ---------- */
  function render() {
    compute();
    // a filter or search that leaves the chosen service empty widens back to every service
    if (st.svc >= 0 && filtering() && svcCount[st.svc] === 0) { st.svc = -1; compute(); }
    renderSide();
    renderSvcHead();
    renderList(true);
    renderDetail();
    el.count.innerHTML = `<b>${fmt(list.length)}</b> of ${fmt(M.length)} methods`;
    el.clear.hidden = !filtering() && st.svc < 0;
    el.dzw.classList.toggle('on', st.danger);
  }

  function renderSide() {
    el.seg.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.side === st.side)));
    let h = '';
    if (st.side === 'services') {
      const tot = svcCount.reduce((a, b) => a + b, 0);
      h += `<button class="row" type="button" data-svc="-1" aria-current="${st.svc < 0}"><span class="nm">all services</span><span class="n">${fmt(tot)}</span></button>`;
      const show = S.filter((s) => !filtering() || svcCount[s.i] > 0 || s.i === st.svc);
      h += show.map((s) => `<button class="row" type="button" data-svc="${s.i}" aria-current="${s.i === st.svc}" title="${esc(s.name)}"><span class="nm">${esc(s.name)}</span><span class="n">${fmt(filtering() ? svcCount[s.i] : s.n)}</span></button>`).join('');
      if (!show.length) h += '<div class="atlas-empty">No services match.</div>';
    } else {
      const cats = Object.entries(catCount).sort((a, b) => b[1] - a[1]);
      const tot = cats.reduce((a, [, n]) => a + n, 0);
      h += `<button class="row" type="button" data-cat="" aria-current="${!st.cat}"><span class="nm">every category</span><span class="n">${fmt(tot)}</span></button>`;
      h += cats.map(([k, n]) => `<button class="row" type="button" data-cat="${esc(k)}" aria-current="${k === st.cat}"><span class="nm">${esc(k)}</span><span class="n">${fmt(n)}</span></button>`).join('');
    }
    el.side.innerHTML = h;
  }

  function renderSvcHead() {
    if (st.svc < 0) { el.svcHead.hidden = true; el.listTitle.textContent = st.cat ? st.cat : 'methods'; return; }
    const s = S[st.svc];
    el.listTitle.textContent = 'service';
    el.svcHead.hidden = false;
    el.svcHead.innerHTML = `<h3>${esc(s.name)} <span class="ab sm c-${esc(s.sdc)}">${esc(s.sdc)}</span></h3>` +
      (s.sd ? `<p>${esc(s.sd)}</p>` : '') + (s.sdc === 'inferred' ? `<p class="note">${NOTE_S}</p>` : '') +
      `<p class="note" style="font-style:normal">${fmt(s.n)} methods${filtering() ? `, ${fmt(svcCount[s.i])} matching` : ''}</p>`;
  }

  let vTop = -1;
  function renderList(reset) {
    const box = el.list;
    if (reset) { box.scrollTop = 0; vTop = -1; }
    if (!list.length) { box.innerHTML = '<div class="atlas-empty">No methods match.  Try fewer words, or clear the filters.</div>'; return; }
    const h = box.clientHeight || 600;
    const start = Math.max(0, Math.floor(box.scrollTop / ROW) - 6);
    if (!reset && start === vTop) return;
    vTop = start;
    const end = Math.min(list.length, start + Math.ceil(h / ROW) + 14);
    let rows = '';
    for (let k = start; k < end; k++) {
      const i = list[k], m = M[i], s = S[m.si];
      const cur = i === st.sel;
      rows += `<a class="vrow" style="top:${k * ROW}px" href="${esc(link(s.name, m.m))}" aria-current="${cur}" data-i="${i}">` +
        `<span class="l1"><span class="cdot c-${esc(m.dc)}" title="${esc(m.dc)}"></span><span class="mn">${esc(m.m || '(service root)')}</span>` +
        `<span class="bd">${m.d ? '<span class="ab sm danger" title="dangerous">⚠</span>' : ''}${m.s ? '<span class="ab sm sub" title="subscribe">sub</span>' : ''}<span class="ab sm a-${esc(m.a)}">${esc(m.a)}</span></span></span>` +
        `<span class="l2">${esc(st.svc >= 0 ? (m.desc || m.c) : s.name)}</span></a>`;
    }
    box.innerHTML = `<div style="height:${list.length * ROW}px;position:relative">${rows}</div>`;
  }

  function renderDetail() {
    if (st.sel < 0) {
      el.detail.innerHTML = `<div class="atlas-blank"><b>Pick a method</b> to see its URI, access level, parameters and a ready-to-run <code>luna-send</code> command.<br><br>Every view has its own link, so you can share any service or method.</div>`;
      return;
    }
    const m = M[st.sel], s = S[m.si];
    const cmd = `luna-send -n 1 -f ${m.u} '{}'`;
    const params = Object.entries(m.p);
    let ph = '';
    if (params.length) {
      ph = '<div class="tblw"><table class="tbl"><thead><tr><th>param</th><th>type and notes</th></tr></thead><tbody>' +
        params.map(([k, v]) => `<tr><td><code>${esc(k)}</code></td><td>${esc(typeof v === 'string' ? v : JSON.stringify(v))}</td></tr>`).join('') + '</tbody></table></div>';
    } else {
      ph = `<p class="note">${m.dc === 'documented' ? 'No parameters documented.' : m.dc === 'stub' ? NOTE_STUB : 'Not publicly documented.'}</p>`;
    }
    el.detail.innerHTML =
      `<h3>${esc(m.m || '(service root)')}</h3>` +
      `<button class="svcl" type="button" data-goto="${esc(s.name)}">${esc(s.name)} ↗</button>` +
      `<div class="badges"><span class="ab a-${esc(m.a)}">${esc(m.a)}</span>${m.d ? '<span class="ab danger">⚠ dangerous</span>' : ''}${m.s ? '<span class="ab sub">subscribe</span>' : ''}<span class="ab c-${esc(m.dc)}">${esc(m.dc)}</span><span class="ab a-unknown">${esc(m.c)}</span></div>` +
      `<p class="uri">${esc(m.u)}</p>` +
      `<p class="desc">${esc(m.desc)}</p>` +
      (m.dc === 'inferred' ? `<p class="note">${NOTE_M}</p>` : m.dc === 'stub' ? `<p class="note">${NOTE_STUB}</p>` : '') +
      (m.d ? '<div class="warn">Flagged dangerous: it can change, reset or break things on the TV.  Know what it does before you run it.  <a class="c-pk" href="https://github.com/ohmybahgosh/WEBOS-LUNA-SEND-ATLAS/blob/main/docs/dangerous.md" target="_blank" rel="noopener">dangerous.md ↗</a></div>' : '') +
      `<h4>parameters</h4>${ph}` +
      `<h4>run it</h4><div class="code"><pre><span class="pr">$ </span>${esc(cmd)}</pre><button class="copy" type="button" data-copy="${esc(cmd)}">copy</button></div>` +
      (m.s ? '<p class="note" style="margin-top:8px">Supports subscriptions: add <code>"subscribe": true</code> and drop <code>-n 1</code> to keep listening.</p>' : '') +
      `<p class="share">link: <button type="button" data-copy="${esc(location.origin + location.pathname + link(s.name, m.m))}">copy link to this method</button></p>`;
  }

  /* ---------- deep links: #/service or #/service/method ---------- */
  function link(svc, m) { return '#/' + encodeURI(svc) + (m != null ? '/' + encodeURI(m) : ''); }
  let keepScope = false;   // set by a click in the list: show the method, keep the list as it is
  function applyHash(first) {
    const h = location.hash;
    if (!h.startsWith('#/')) return;
    let path;
    try { path = decodeURI(h.slice(2)); } catch (e) { return; }
    const cut = path.indexOf('/');
    const svc = cut < 0 ? path : path.slice(0, cut);
    const meth = cut < 0 ? null : path.slice(cut + 1);
    const si = byName[svc];
    if (si == null) return;
    const keep = keepScope && meth != null;
    keepScope = false;
    if (!keep) st.svc = si;
    st.sel = -1;
    if (meth != null) {
      const idx = M.findIndex((m) => m.si === si && m.m === meth);
      if (idx >= 0) st.sel = idx;
    }
    root.dataset.view = st.sel >= 0 ? 'detail' : 'list';
    if (first) setTimeout(() => root.scrollIntoView({ block: 'start' }), 50);
  }
  window.addEventListener('hashchange', () => {
    if (!M.length) return;
    const keep = keepScope;
    applyHash(false);
    if (keep) { renderList(false); renderDetail(); highlight(); } else { render(); scrollToSel(); }
    el.detail.parentElement.scrollTop = 0;
  });
  function scrollToSel() {
    const k = list.indexOf(st.sel);
    if (k < 0) return;
    const box = el.list;
    if (k * ROW < box.scrollTop || k * ROW > box.scrollTop + box.clientHeight - ROW) box.scrollTop = Math.max(0, k * ROW - ROW * 2);
    renderList(false);
  }
  function setHash(h) {
    if (location.hash === h) return;
    if (h) location.hash = h;
    else history.pushState(null, '', location.pathname + location.search);
  }

  /* ---------- events ---------- */
  let qt;
  el.q.addEventListener('input', () => { clearTimeout(qt); qt = setTimeout(() => { st.q = el.q.value.trim(); render(); }, 60); });
  el.cat.addEventListener('change', () => { st.cat = el.cat.value; render(); });
  el.acc.addEventListener('change', () => { st.acc = el.acc.value; render(); });
  el.conf.addEventListener('change', () => { st.conf = el.conf.value; render(); });
  el.dz.addEventListener('change', () => { st.danger = el.dz.checked; render(); });
  el.clear.addEventListener('click', () => {
    Object.assign(st, { q: '', cat: '', acc: '', conf: '', danger: false, svc: -1, sel: -1 });
    el.q.value = ''; el.cat.value = ''; el.acc.value = ''; el.conf.value = ''; el.dz.checked = false;
    setHash('');
    render();
  });
  el.seg.forEach((b) => b.addEventListener('click', () => { st.side = b.dataset.side; renderSide(); }));
  el.side.addEventListener('click', (e) => {
    const b = e.target.closest('button.row');
    if (!b) return;
    if (b.dataset.svc != null) {
      const si = Number(b.dataset.svc);
      st.svc = si; st.sel = -1;
      setHash(si >= 0 ? link(S[si].name) : '');
    } else {
      st.cat = b.dataset.cat; el.cat.value = st.cat; st.svc = -1; st.sel = -1;
    }
    root.dataset.view = 'list';
    render();
  });
  el.list.addEventListener('scroll', () => requestAnimationFrame(() => renderList(false)), { passive: true });
  el.list.addEventListener('click', (e) => {
    const r = e.target.closest('.vrow');
    if (!r) return;
    keepScope = r.getAttribute('href') !== location.hash;   // same link: no hashchange will follow
    root.dataset.view = 'detail';
  });
  function highlight() { el.list.querySelectorAll('.vrow').forEach((r) => r.setAttribute('aria-current', String(Number(r.dataset.i) === st.sel))); }
  root.addEventListener('click', (e) => {
    const g = e.target.closest('[data-goto]');
    if (g) { setHash(link(g.dataset.goto)); return; }
    const back = e.target.closest('[data-back]');
    if (back) { root.dataset.view = back.dataset.back; return; }
    const c = e.target.closest('[data-copy]');
    if (c) copy(c.dataset.copy, c);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && !/input|textarea|select/i.test(document.activeElement.tagName) && !e.metaKey && !e.ctrlKey) {
      e.preventDefault(); el.q.focus();
    }
  });
  window.addEventListener('resize', () => renderList(false));

  function copy(t, btn) {
    const done = () => { const o = btn.textContent; btn.textContent = 'copied'; setTimeout(() => { btn.textContent = o; }, 1400); };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(t).then(done, () => legacy(t) && done());
    else if (legacy(t)) done();
  }
  function legacy(t) {
    const a = document.createElement('textarea');
    a.value = t; a.style.position = 'fixed'; a.style.opacity = '0';
    document.body.appendChild(a); a.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    a.remove();
    return ok;
  }

  // load when the browser is near the screen, or straight away for a deep link
  if (location.hash.startsWith('#/') || !('IntersectionObserver' in window)) load();
  else {
    const io = new IntersectionObserver((es) => { if (es.some((x) => x.isIntersecting)) { io.disconnect(); load(); } }, { rootMargin: '600px' });
    io.observe(root);
  }
})();
