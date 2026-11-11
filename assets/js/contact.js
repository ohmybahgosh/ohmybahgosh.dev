/* ohmybahgosh.dev :: contact page.
   Each template either prefills a GitHub issue form (by field id), opens a GitHub Discussion,
   or opens an email to hello@ohmybahgosh.dev.  Nothing is sent anywhere until the visitor clicks. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const MAIL = ['hello', 'ohmybahgosh.dev'].join('@');
  const GH = 'https://github.com/ohmybahgosh/';

  const f = {
    title: (ph) => ({ id: 'title', label: 'Short summary', type: 'input', req: true, ph }),
    tv: { id: 'tv', label: 'TV model and webOS version', type: 'input', req: true, ph: 'OLED65C2PUA, webOS 25 (10.3.1)' },
    tbver: { id: 'version', label: 'TiviBro version', type: 'input', req: true, ph: '{{TiviBro:version|0.6.0-alpha.105}}  (Settings > Updates and about)' },
  };

  // kind: issue (GitHub issue form), discussion, blank (plain GitHub issue), mail
  const T = [
    { key: 'tb-bug', group: 'TiviBro', icon: '🐞', name: 'App bug', desc: 'Something in TiviBro breaks or acts wrong.', kind: 'issue', repo: 'TiviBro', template: '1-bug.yml', prefix: '[Bug]: ',
      fields: [f.title('The guide jumps to the top after a refresh'), { id: 'what', label: 'What happened?', type: 'textarea', req: true }, { id: 'steps', label: 'How do you get there?', type: 'textarea', req: true, ph: '1. Open the guide\n2. …' }, { id: 'expected', label: 'What did you expect?', type: 'textarea', req: true }, f.tbver, f.tv] },
    { key: 'tb-playback', group: 'TiviBro', icon: '📺', name: 'Playback problem', desc: 'A channel won’t start, freezes or has no sound.', kind: 'issue', repo: 'TiviBro', template: '2-playback.yml', prefix: '[Playback]: ',
      fields: [f.title('Sports channels buffer every few seconds'), { id: 'details', label: 'What happens?', type: 'textarea', req: true }, { id: 'tried', label: 'What did you try?', type: 'textarea' }, f.tbver, f.tv],
      note: 'Never paste your playlist URL, username or password.  GitHub issues are public.' },
    { key: 'tb-install', group: 'TiviBro', icon: '📦', name: 'Install or update', desc: 'Installing or updating TiviBro fails.', kind: 'issue', repo: 'TiviBro', template: '3-install.yml', prefix: '[Install]: ',
      fields: [f.title('Homebrew Channel says install failed'), { id: 'what', label: 'What happened?', type: 'textarea', req: true }, f.tv, { id: 'version', label: 'Version you’re installing, and the one installed now', type: 'input' }] },
    { key: 'tb-question', group: 'TiviBro', icon: '❓', name: 'Question', desc: 'How do I…?  Is it possible to…?', kind: 'issue', repo: 'TiviBro', template: '5-question.yml', prefix: '[Question]: ',
      fields: [f.title('Can I use two playlists at once?'), { id: 'question', label: 'Your question', type: 'textarea', req: true }, { id: 'version', label: 'TiviBro version and TV, if it matters', type: 'input' }] },
    { key: 'tb-idea', group: 'TiviBro', icon: '💡', name: 'Idea', desc: 'A feature you’d love to see.', kind: 'discussion', url: GH + 'TiviBro/discussions/new?category=ideas',
      fields: [f.title('Recording to a USB drive'), { id: 'idea', label: 'The idea', type: 'textarea', req: true }, { id: 'why', label: 'Why it would help you', type: 'textarea' }] },

    { key: 'eth-bug', group: 'LG-USB-2-ETH0', icon: '🐞', name: 'Bug', desc: 'The script errors or the swap misbehaves.', kind: 'issue', repo: 'LG-USB-2-ETH0', template: 'bug-report.yml', prefix: '[Bug] ',
      fields: [f.title('Adapter goes back to eth1 after a reboot'), { id: 'what', label: 'What happened', type: 'textarea', req: true }, { id: 'version', label: 'Script version', type: 'input', req: true, ph: 'v{{LG-USB-2-ETH0:version|2.11.7}}' }, { id: 'report', label: 'Output of  sh LG-USB-2-ETH0.sh report', type: 'textarea', req: true, mono: true }] },
    { key: 'eth-compat', group: 'LG-USB-2-ETH0', icon: '🔌', name: 'Compatibility report', desc: 'Tell everyone whether your TV + adapter worked.', kind: 'issue', repo: 'LG-USB-2-ETH0', template: 'compatibility-report.yml',
      title: (v) => `[Compat] ${v.model || '<TV model>'} + ${v.adapter || '<adapter>'}`,
      fields: [{ id: 'model', label: 'TV model', type: 'input', req: true, ph: 'OLED65C2PUA' }, { id: 'webos', label: 'webOS version and firmware', type: 'input', req: true, ph: 'webOS 25 (10.3.1), 33.31.68' }, { id: 'adapter', label: 'Adapter (brand, model, chip)', type: 'input', req: true, ph: 'UGREEN 2.5G, RTL8156' }, { id: 'speed', label: 'Measured speed (optional)', type: 'input', ph: '290 Mbit/s' }, { id: 'report', label: 'Output of  sh LG-USB-2-ETH0.sh report', type: 'textarea', req: true, mono: true }, { id: 'notes', label: 'Anything else', type: 'textarea' }],
      note: 'You’ll pick the result (works, problems, not detected) on GitHub.' },
    { key: 'eth-idea', group: 'LG-USB-2-ETH0', icon: '💡', name: 'Idea', desc: 'Something the script should do.', kind: 'blank', repo: 'LG-USB-2-ETH0', prefix: '[Idea] ',
      fields: [f.title('Option to prefer Wi-Fi when no cable is in'), { id: 'idea', label: 'The idea', type: 'textarea', req: true }, { id: 'why', label: 'Why it would help', type: 'textarea' }] },

    { key: 'ent-bug', group: 'Entware Installer', icon: '🐞', name: 'Bug', desc: 'Install, repair, the TV app or a command went wrong.', kind: 'issue', repo: 'WEBOS-ENTWARE-INSTALLER', template: 'bug-report.yml', prefix: '[Bug] ',
      fields: [f.title('opkg not found after reboot'), { id: 'what', label: 'What happened', type: 'textarea', req: true }, { id: 'steps', label: 'What you ran', type: 'textarea', mono: true, ph: 'sh /tmp/webos-entware-installer.sh install' }, f.tv, { id: 'version', label: 'Installer version', type: 'input', req: true, ph: '{{WEBOS-ENTWARE-INSTALLER:version|2.15.1}}  (top of the TV app, or webos-entware --help)' }, { id: 'doctor', label: 'Output of  webos-entware doctor', type: 'textarea', mono: true }] },
    { key: 'ent-compat', group: 'Entware Installer', icon: '📺', name: 'Compatibility report', desc: 'Tell everyone how Entware works on your TV, good or bad.', kind: 'issue', repo: 'WEBOS-ENTWARE-INSTALLER', template: 'compatibility-report.yml',
      title: (v) => `[Compat] ${v.tv || '<TV model and webOS version>'}`,
      fields: [f.tv, { id: 'version', label: 'Installer version', type: 'input', req: true, ph: '{{WEBOS-ENTWARE-INSTALLER:version|2.15.1}}  (top of the TV app, or webos-entware --help)' }, { id: 'uses', label: 'What you use it for (optional)', type: 'input', ph: 'git, Python, htop' }, { id: 'doctor', label: 'Output of  webos-entware doctor', type: 'textarea', req: true, mono: true }, { id: 'notes', label: 'Anything else', type: 'textarea' }],
      note: 'You’ll pick the result, the build, how you installed it and where Entware lives on GitHub.  Report for GitHub in the TV app fills all of this in for you.' },
    { key: 'ent-idea', group: 'Entware Installer', icon: '💡', name: 'Idea', desc: 'A helper, package or option to add.', kind: 'issue', repo: 'WEBOS-ENTWARE-INSTALLER', template: 'feature-request.yml', prefix: '[Idea] ',
      fields: [f.title('Add a helper to mount a USB drive at /opt'), { id: 'idea', label: 'The idea', type: 'textarea', req: true }, { id: 'why', label: 'Why it would help', type: 'textarea' }] },

    { key: 'sd-bug', group: 'SSH Doctor', icon: '🐞', name: 'Bug', desc: 'A check, repair, setting or the pairing page went wrong.', kind: 'issue', repo: 'LG-WEBOS-SSH-DOCTOR', template: 'bug-report.yml', prefix: '[Bug] ',
      fields: [f.title('Settings don\u2019t come back after a restart'), { id: 'what', label: 'What happened', type: 'textarea', req: true }, f.tv, { id: 'report', label: 'The report (More tools, Report for getting help)', type: 'textarea', req: true, mono: true }],
      note: 'You\u2019ll pick where it happened (TV app, pairing page, telnet, after a restart) on GitHub.' },
    { key: 'sd-tv', group: 'SSH Doctor', icon: '📺', name: 'How it went on my TV', desc: 'Tell everyone whether SSH Doctor sorted out your TV.', kind: 'issue', repo: 'LG-WEBOS-SSH-DOCTOR', template: 'tv-report.yml',
      title: (v) => `[TV] ${v.tv || '<TV model>, webOS <version>'}`,
      fields: [{ id: 'tv', label: 'TV model', type: 'input', req: true, ph: 'OLED65C2PUA' }, { id: 'webos', label: 'webOS version and firmware', type: 'input', req: true, ph: 'webOS 25 (10.3.1), 33.31.68' }, { id: 'rooted', label: 'How the TV was rooted', type: 'input', ph: 'RootMyTV, faultmanager-autoroot' }, { id: 'report', label: 'The report (More tools, Report for getting help)', type: 'textarea', mono: true }, { id: 'notes', label: 'Anything else', type: 'textarea' }],
      note: 'You\u2019ll tick what you used and pick the result on GitHub.' },

    { key: 'mail-hello', group: 'Email me', icon: '✉️', name: 'Say hello', desc: 'Questions, thanks, or anything else.', kind: 'mail', subject: (v) => v.title || 'Hello from ohmybahgosh.dev',
      fields: [{ id: 'name', label: 'Your name', type: 'input' }, f.title('Loving TiviBro'), { id: 'message', label: 'Message', type: 'textarea', req: true }] },
    { key: 'mail-collab', group: 'Email me', icon: '🤝', name: 'Collaborate', desc: 'Contribute, partner or build something together.', kind: 'mail', subject: (v) => 'Collaboration: ' + (v.title || 'idea'),
      fields: [{ id: 'name', label: 'Your name', type: 'input', req: true }, { id: 'link', label: 'GitHub or website', type: 'input', ph: 'https://github.com/you' }, f.title('Porting TiviBro to Tizen'), { id: 'message', label: 'What you have in mind', type: 'textarea', req: true }] },
    { key: 'mail-press', group: 'Email me', icon: '📰', name: 'Press or review', desc: 'Writing about or reviewing a project.', kind: 'mail', subject: (v) => 'Press: ' + (v.title || 'story'),
      fields: [{ id: 'name', label: 'Your name', type: 'input', req: true }, { id: 'outlet', label: 'Publication or channel', type: 'input', req: true }, { id: 'project', label: 'Which project', type: 'select', options: ['TiviBro', 'LG-USB-2-ETH0', 'Entware Installer', 'SSH Doctor', 'All of them'] }, f.title('Review of TiviBro 0.6'), { id: 'deadline', label: 'Deadline, if any', type: 'input' }, { id: 'message', label: 'Questions or details', type: 'textarea', req: true }] },
    { key: 'mail-private', group: 'Email me', icon: '🔒', name: 'Private or security', desc: 'Anything that shouldn’t be public.', kind: 'mail', subject: (v) => 'Private: ' + (v.title || 'report'),
      fields: [{ id: 'project', label: 'Which project', type: 'select', options: ['TiviBro', 'LG-USB-2-ETH0', 'Entware Installer', 'SSH Doctor', 'The website', 'Something else'] }, f.title('Security issue in the web editor'), { id: 'message', label: 'Details', type: 'textarea', req: true }],
      note: 'Email stays private.  Use this for security issues instead of a public GitHub issue.' },
  ];

  const ICON_KIND = { issue: 'GitHub issue', blank: 'GitHub issue', discussion: 'GitHub discussion', mail: 'email' };
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ---- picker ---- */
  const picker = $('#picker');
  const groups = [...new Set(T.map((t) => t.group))];
  picker.innerHTML = groups.map((g) => `<div class="pgroup"><h3>${esc(g)}</h3><div class="pgrid">${T.filter((t) => t.group === g).map((t) =>
    `<button type="button" class="pick" data-key="${t.key}" aria-pressed="false"><span class="pi">${t.icon}</span><span><b>${esc(t.name)}</b><small>${esc(t.desc)}</small></span><em>${ICON_KIND[t.kind]}</em></button>`).join('')}</div></div>`).join('');

  /* ---- form ---- */
  const form = $('#cform'), fieldsEl = $('#fields'), head = $('#fhead'), out = $('#preview'), go = $('#go'), copy = $('#copy'), hint = $('#hint');
  let cur = null;
  let DATA = null;
  const fill = (t) => window.ombFill ? window.ombFill(t, DATA) : t.replace(/\{\{[^|}]+\|?([^}]*)\}\}/g, '$1');
  const DKEY = (k) => 'omb-contact-' + k;
  const vals = () => Object.fromEntries($$('[name]', fieldsEl).map((i) => [i.name, i.value.trim()]));

  function select(key, push = true) {
    cur = T.find((t) => t.key === key) || null;
    $$('.pick', picker).forEach((b) => b.setAttribute('aria-pressed', b.dataset.key === key));
    if (!cur) { form.hidden = true; return; }
    let draft = {};
    try { draft = JSON.parse(localStorage.getItem(DKEY(key))) || {}; } catch (e) {}
    head.innerHTML = `<span class="pi">${cur.icon}</span><div><div class="eyebrow">${esc(cur.group)}</div><h2 class="h2" style="font-size:30px;margin-top:6px">${esc(cur.name)}</h2></div>`;
    fieldsEl.innerHTML = cur.fields.map((x) => {
      const v = esc(draft[x.id] || '');
      const ph = x.ph ? ` placeholder="${esc(fill(x.ph))}"` : '';
      const req = x.req ? ' required' : '';
      const lab = `<label for="f-${x.id}">${esc(x.label)}${x.req ? ' <i>*</i>' : ''}</label>`;
      if (x.type === 'textarea') return `<div class="fld">${lab}<textarea id="f-${x.id}" name="${x.id}" rows="${x.mono ? 6 : 4}"${ph}${req}${x.mono ? ' class="mono" spellcheck="false"' : ''}>${v}</textarea></div>`;
      if (x.type === 'select') return `<div class="fld">${lab}<select id="f-${x.id}" name="${x.id}">${x.options.map((o) => `<option${o === draft[x.id] ? ' selected' : ''}>${esc(o)}</option>`).join('')}</select></div>`;
      return `<div class="fld">${lab}<input id="f-${x.id}" name="${x.id}" type="text" value="${v}"${ph}${req}></div>`;
    }).join('') + (cur.note ? `<p class="callout" style="margin:4px 0 0">${esc(cur.note)}</p>` : '');
    go.textContent = cur.kind === 'mail' ? 'Open in your email app ↗' : cur.kind === 'discussion' ? 'Open the discussion on GitHub ↗' : 'Open the issue on GitHub ↗';
    hint.textContent = cur.kind === 'mail' ? `Sends to ${MAIL} from your own email app.  Nothing is sent until you hit send there.`
      : 'Opens GitHub with everything filled in.  Review it there and submit.  Issues are public, so leave out passwords and playlist links.';
    form.hidden = false;
    render();
    if (push) { history.replaceState(null, '', '?t=' + key); form.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' }); }
  }

  function build() {
    const v = vals();
    const title = cur.title ? cur.title(v) : (cur.prefix || '') + (v.title || '');
    const parts = cur.fields.filter((x) => x.id !== 'title' && v[x.id]).map((x) => `### ${x.label.replace(/\s+/g, ' ').trim()}\n\n${x.mono ? '```\n' + v[x.id] + '\n```' : v[x.id]}`);
    const footer = '\n\n---\nSent from https://ohmybahgosh.dev/contact/';
    let url, body;
    if (cur.kind === 'mail') {
      const subject = cur.subject(v);
      body = cur.fields.filter((x) => x.id !== 'title' && v[x.id]).map((x) => x.id === 'message' ? v[x.id] : `${x.label.replace(/\s+/g, ' ').trim()}: ${v[x.id]}`).join('\n\n') + footer;
      url = `mailto:${MAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      return { url, preview: `To: ${MAIL}\nSubject: ${subject}\n\n${body}`, copyText: body, long: url.length > 1900 };
    }
    if (cur.kind === 'issue') {
      const q = new URLSearchParams({ template: cur.template, title });
      cur.fields.forEach((x) => { if (x.id !== 'title' && v[x.id]) q.set(x.id, v[x.id]); });
      url = `${GH}${cur.repo}/issues/new?${q}`;
      body = parts.join('\n\n');
    } else {
      body = parts.join('\n\n') + footer;
      const base = cur.kind === 'discussion' ? cur.url + '&' : `${GH}${cur.repo}/issues/new?`;
      url = base + new URLSearchParams({ title, body });
    }
    return { url, preview: `${title}\n${'─'.repeat(Math.min(48, Math.max(12, title.length)))}\n\n${body.replace(footer, '')}`, copyText: `${title}\n\n${body}`, long: url.length > 7500 };
  }

  function render() {
    const b = build();
    out.textContent = b.preview;
    const missing = cur.fields.filter((x) => x.req && !vals()[x.id]).map((x) => x.label);
    go.disabled = missing.length > 0;
    go.title = missing.length ? 'Fill in: ' + missing.join(', ') : '';
    $('#warn').hidden = !b.long;
  }

  fieldsEl.addEventListener('input', () => {
    try { localStorage.setItem(DKEY(cur.key), JSON.stringify(vals())); } catch (e) {}
    render();
  });
  picker.addEventListener('click', (e) => { const b = e.target.closest('.pick'); if (b) select(b.dataset.key); });

  const toClip = async (t) => {
    try { await navigator.clipboard.writeText(t); return true; } catch (e) {
      const ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select();
      const ok = document.execCommand('copy'); ta.remove(); return ok;
    }
  };
  const flash = (btn, txt) => { const o = btn.textContent; btn.textContent = txt; setTimeout(() => btn.textContent = o, 1800); };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const b = build();
    if (b.long) {
      // Too long for a URL: open with the short fields, put the full text on the clipboard.
      await toClip(b.copyText);
      alertBox('Your message was too long for a link, so the full text is on your clipboard.  Paste it into the page that opens.');
      const short = cur.kind === 'mail' ? `mailto:${MAIL}?subject=${encodeURIComponent(cur.subject(vals()))}` : b.url.split('&').filter((p) => !/^(report|doctor|log|body)=/.test(p)).join('&');
      window.open(short, cur.kind === 'mail' ? '_self' : '_blank', 'noopener');
      return;
    }
    window.open(b.url, cur.kind === 'mail' ? '_self' : '_blank', 'noopener');
  });
  copy.addEventListener('click', async () => { if (cur && await toClip(build().copyText)) flash(copy, 'copied'); });
  $('#clear').addEventListener('click', () => {
    if (!cur) return;
    try { localStorage.removeItem(DKEY(cur.key)); } catch (e) {}
    select(cur.key, false);
  });
  function alertBox(msg) { const w = $('#warn'); w.hidden = false; w.textContent = msg; }

  // Email links assembled in the browser to keep the address away from simple scrapers
  $$('[data-mail]').forEach((a) => { a.href = 'mailto:' + MAIL; if (!a.textContent.trim() || a.dataset.mail === 'text') a.textContent = MAIL; });

  // Live versions for placeholders once site.js has loaded the site data
  window.addEventListener('DOMContentLoaded', () => { if (window.ombData) window.ombData().then((d) => { DATA = d; if (cur) $$('[placeholder]', fieldsEl).forEach((el) => { const x = cur.fields.find((y) => y.id === el.name); if (x && x.ph) el.placeholder = fill(x.ph); }); }); });

  const want = new URLSearchParams(location.search).get('t');
  if (want && T.some((t) => t.key === want)) select(want, false);
})();
