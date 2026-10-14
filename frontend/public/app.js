'use strict';

const app = document.getElementById('app');
const PAGE_SIZE = 10;

// ---------- helpers ----------

function h(tag, props = {}, ...children) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (key === 'class') el.className = value;
    else if (key.startsWith('on')) el.addEventListener(key.slice(2), value);
    else if (value !== false && value != null) el.setAttribute(key, value);
  }
  for (const child of children.flat()) {
    if (child == null || child === false) continue;
    el.append(child instanceof Node ? child : String(child));
  }
  return el;
}

let toastTimer;
function toast(message, isError = false) {
  const el = document.getElementById('toast');
  el.textContent = message;
  el.className = isError ? 'show error' : 'show';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.className = ''; }, 3500);
}

const STATUS_TEXT = { 400: 'Invalid input', 404: 'Not found', 409: 'Already exists' };

async function api(path, { method = 'GET', body } = {}) {
  const res = await fetch('/api' + path, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`${STATUS_TEXT[res.status] || 'Request failed'} (${res.status})`);
  if (res.status === 204) return null;
  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

async function run(fn) {
  try {
    await fn();
  } catch (e) {
    toast(e.message, true);
  }
}

const query = (params) => new URLSearchParams(params).toString();
const fmt = (iso) => (iso ? new Date(iso).toLocaleString() : '');
const truncate = (s, n) => (s && s.length > n ? s.slice(0, n) + '...' : s || '');

function lengthError(label, value, min, max) {
  if (value.length < min || value.length > max) {
    return `${label} must be between ${min} and ${max} characters`;
  }
  return null;
}

// ---------- shared components ----------

function tagChips(tags) {
  return (tags || []).map((t) => h('a', { class: 'chip', href: `#/tag/${encodeURIComponent(t)}` }, t));
}

function questionCard(q) {
  return h('article', { class: 'card' },
    h('h3', {}, h('a', { href: `#/q/${q.id}` }, q.title)),
    h('p', { class: 'excerpt' }, truncate(q.content, 200)),
    h('div', { class: 'meta' },
      tagChips(q.tags),
      q.views != null ? `${q.views} views` : null,
      fmt(q.createdAt)));
}

function likeBar(targetId, targetType) {
  const likeBtn = h('button', { class: 'link' }, 'Like (0)');
  const dislikeBtn = h('button', { class: 'link' }, 'Dislike (0)');

  async function refresh() {
    const c = await api(`/likes/count?${query({ targetId, targetType })}`);
    likeBtn.textContent = `Like (${c.likes})`;
    dislikeBtn.textContent = `Dislike (${c.dislikes})`;
  }
  const vote = (isLike) => run(async () => {
    await api('/likes', { method: 'POST', body: { targetId, targetType, isLike } });
    await refresh();
  });

  likeBtn.addEventListener('click', () => vote(true));
  dislikeBtn.addEventListener('click', () => vote(false));
  refresh().catch(() => {});

  return h('span', {}, likeBtn, dislikeBtn);
}

function commentItem(c, refresh) {
  const edit = h('button', { class: 'link' }, 'Edit');
  edit.addEventListener('click', () => run(async () => {
    const content = prompt('Edit comment', c.content);
    if (content == null) return;
    const trimmed = content.trim();
    if (!trimmed || trimmed.length > 500) throw new Error('Comment must be 1 to 500 characters');
    await api(`/comments/${c.id}`, {
      method: 'PUT',
      body: { content: trimmed, targetId: c.targetId, targetType: c.targetType },
    });
    await refresh();
  }));

  const del = h('button', { class: 'link' }, 'Delete');
  del.addEventListener('click', () => run(async () => {
    if (!confirm('Delete this comment and its replies?')) return;
    await api(`/comments/${c.id}`, { method: 'DELETE' });
    await refresh();
  }));

  return h('div', { class: 'comment' },
    h('p', {}, c.content),
    h('div', { class: 'meta' }, fmt(c.createdAt)),
    h('div', { class: 'actions' }, likeBar(c.id, 'COMMENT'), edit, del),
    commentSection(c.id, 'COMMENT'));
}

// comments hang off an answer, replies hang off a comment
function commentSection(targetId, targetType) {
  const label = targetType === 'ANSWER' ? 'Comments' : 'Replies';
  const toggle = h('button', { class: 'link' }, label);
  const list = h('div');
  const input = h('input', {
    placeholder: targetType === 'ANSWER' ? 'Add a comment' : 'Add a reply',
    maxlength: 500,
  });

  async function load() {
    const items = await api(`/comments?${query({ targetId, targetType })}`);
    list.replaceChildren(...items.map((c) => commentItem(c, load)));
    toggle.textContent = `${label} (${items.length})`;
  }

  const form = h('form', {
    class: 'inline',
    onsubmit: (e) => {
      e.preventDefault();
      run(async () => {
        const content = input.value.trim();
        if (!content) return;
        await api('/comments', { method: 'POST', body: { content, targetId, targetType } });
        input.value = '';
        await load();
      });
    },
  }, input, h('button', {}, 'Post'));

  const body = h('div', { class: 'comments', hidden: true }, list, form);

  let loaded = false;
  toggle.addEventListener('click', () => {
    body.hidden = !body.hidden;
    if (!body.hidden && !loaded) {
      loaded = true;
      run(load);
    }
  });
  api(`/comments/count?${query({ targetId, targetType })}`)
    .then((n) => { toggle.textContent = `${label} (${n})`; })
    .catch(() => {});

  return h('div', {}, toggle, body);
}

function answerItem(a, refresh) {
  const edit = h('button', { class: 'link' }, 'Edit');
  edit.addEventListener('click', () => run(async () => {
    const content = prompt('Edit answer', a.content);
    if (content == null) return;
    const trimmed = content.trim();
    const err = lengthError('Answer', trimmed, 10, 1000);
    if (err) throw new Error(err);
    await api(`/answers/${a.id}`, { method: 'PUT', body: { content: trimmed, questionId: a.questionId } });
    await refresh();
  }));

  const del = h('button', { class: 'link' }, 'Delete');
  del.addEventListener('click', () => run(async () => {
    if (!confirm('Delete this answer?')) return;
    await api(`/answers/${a.id}`, { method: 'DELETE' });
    await refresh();
  }));

  return h('article', { class: 'card' },
    h('p', { class: 'content' }, a.content),
    h('div', { class: 'meta' }, fmt(a.createdAt)),
    h('div', { class: 'actions' }, likeBar(a.id, 'ANSWER'), edit, del),
    commentSection(a.id, 'ANSWER'));
}

// ---------- pages ----------

function askForm() {
  const title = h('input', { placeholder: 'Question title (10 to 100 characters)', maxlength: 100 });
  const content = h('textarea', { placeholder: 'Details (10 to 1000 characters)', rows: 4, maxlength: 1000 });
  const tags = h('input', { placeholder: 'Tags, comma separated (max 5)' });

  return h('form', {
    class: 'card form',
    onsubmit: (e) => {
      e.preventDefault();
      run(async () => {
        const t = title.value.trim();
        const c = content.value.trim();
        const tagList = tags.value.split(',').map((s) => s.trim()).filter(Boolean);
        const err = lengthError('Title', t, 10, 100) || lengthError('Details', c, 10, 1000);
        if (err) throw new Error(err);
        if (tagList.length > 5) throw new Error('At most 5 tags are allowed');
        if (tagList.some((s) => s.length > 30)) throw new Error('A tag must be at most 30 characters');

        const created = await api('/questions', { method: 'POST', body: { title: t, content: c, tags: tagList } });
        location.hash = `#/q/${created.id}`;
      });
    },
  }, h('strong', {}, 'Ask a question'), title, content, tags, h('button', {}, 'Post question'));
}

async function feedPage() {
  const list = h('div');
  const empty = h('p', { class: 'muted' }, 'No questions yet. Ask the first one above.');
  const more = h('button', { class: 'secondary', hidden: true }, 'Load more');
  let cursor = null;
  let total = 0;

  async function load() {
    const params = { size: PAGE_SIZE };
    if (cursor) params.cursor = cursor;
    const items = await api(`/questions?${query(params)}`);
    items.forEach((q) => list.append(questionCard(q)));
    if (items.length) cursor = items[items.length - 1].createdAt;
    total += items.length;
    empty.hidden = total > 0;
    more.hidden = items.length < PAGE_SIZE;
  }

  more.addEventListener('click', () => run(load));
  app.replaceChildren(askForm(), h('h2', {}, 'Questions'), list, empty, more);
  await load();
}

async function questionPage(id) {
  const q = await api(`/questions/${id}`);
  if (!q) throw new Error('Question not found');

  const answersBox = h('div');
  const answerCount = h('h2');

  async function loadAnswers() {
    const answers = await api(`/answers/question/${id}/latest`);
    answerCount.textContent = `${answers.length} answer${answers.length === 1 ? '' : 's'}`;
    answersBox.replaceChildren(...answers.map((a) => answerItem(a, loadAnswers)));
    if (!answers.length) answersBox.append(h('p', { class: 'muted' }, 'No answers yet.'));
  }

  const answerInput = h('textarea', { placeholder: 'Write an answer (10 to 1000 characters)', rows: 4, maxlength: 1000 });
  const answerForm = h('form', {
    class: 'card form',
    onsubmit: (e) => {
      e.preventDefault();
      run(async () => {
        const content = answerInput.value.trim();
        const err = lengthError('Answer', content, 10, 1000);
        if (err) throw new Error(err);
        await api('/answers', { method: 'POST', body: { content, questionId: id } });
        answerInput.value = '';
        await loadAnswers();
      });
    },
  }, answerInput, h('button', {}, 'Post answer'));

  app.replaceChildren(
    h('article', { class: 'card' },
      h('h2', { style: 'margin-top:0' }, q.title),
      h('p', { class: 'content' }, q.content),
      h('div', { class: 'meta' }, tagChips(q.tags), q.views != null ? `${q.views} views` : null, fmt(q.createdAt)),
      h('div', { class: 'actions' }, likeBar(q.id, 'QUESTION'))),
    answerCount,
    answerForm,
    answersBox);
  await loadAnswers();
}

async function pagedQuestions(heading, fetchPage) {
  let page = 0;
  const list = h('div');
  const prev = h('button', { class: 'secondary' }, 'Previous');
  const next = h('button', { class: 'secondary' }, 'Next');
  const label = h('span', { class: 'muted' });

  async function show() {
    const items = await fetchPage(page);
    list.replaceChildren(...items.map(questionCard));
    if (!items.length) list.append(h('p', { class: 'muted' }, 'No questions found.'));
    prev.disabled = page === 0;
    next.disabled = items.length < PAGE_SIZE;
    label.textContent = `Page ${page + 1}`;
  }

  prev.addEventListener('click', () => { page--; run(show); });
  next.addEventListener('click', () => { page++; run(show); });

  app.replaceChildren(h('h2', {}, heading), list, h('div', { class: 'pager' }, prev, label, next));
  await show();
}

function tagPage(encodedTag) {
  const tag = decodeURIComponent(encodedTag);
  return pagedQuestions(`Tagged "${tag}"`, (page) =>
    api(`/questions/tag/${encodeURIComponent(tag)}?${query({ page, size: PAGE_SIZE })}`));
}

async function searchPage(qs) {
  const text = new URLSearchParams(qs).get('q') || '';
  const items = await api(`/questions/elasticsearch?${query({ query: text })}`);
  app.replaceChildren(
    h('h2', {}, `Results for "${text}"`),
    ...(items.length ? items.map(questionCard) : [h('p', { class: 'muted' }, 'No questions found.')]));
}

async function tagsPage() {
  const chips = h('div', { class: 'meta' });
  const input = h('input', { placeholder: 'New tag name', maxlength: 30 });

  async function load() {
    const tags = await api('/tags');
    chips.replaceChildren(...tags.map((t) =>
      h('a', { class: 'chip', href: `#/tag/${encodeURIComponent(t.name)}` }, t.name)));
    if (!tags.length) chips.append(h('span', { class: 'muted' }, 'No tags yet.'));
  }

  const form = h('form', {
    class: 'card inline',
    onsubmit: (e) => {
      e.preventDefault();
      run(async () => {
        const name = input.value.trim();
        if (!name) return;
        await api('/tags', { method: 'POST', body: { name } });
        input.value = '';
        toast('Tag created');
        await load();
      });
    },
  }, input, h('button', {}, 'Create tag'));

  app.replaceChildren(h('h2', {}, 'Tags'), form, h('div', { class: 'card' }, chips));
  await load();
}

async function usersPage() {
  const tbody = h('tbody');
  const username = h('input', { placeholder: 'Username (3 to 50)', maxlength: 50 });
  const email = h('input', { type: 'email', placeholder: 'Email' });
  const displayName = h('input', { placeholder: 'Display name (optional)', maxlength: 100 });

  async function load() {
    const users = await api('/users');
    tbody.replaceChildren(...users.map((u) =>
      h('tr', {}, h('td', {}, u.id), h('td', {}, u.username), h('td', {}, u.email),
        h('td', {}, u.displayName || ''), h('td', {}, fmt(u.createdAt)))));
  }

  const form = h('form', {
    class: 'card form',
    onsubmit: (e) => {
      e.preventDefault();
      run(async () => {
        const name = username.value.trim();
        const err = lengthError('Username', name, 3, 50);
        if (err) throw new Error(err);
        await api('/users', {
          method: 'POST',
          body: { username: name, email: email.value.trim(), displayName: displayName.value.trim() || null },
        });
        username.value = email.value = displayName.value = '';
        toast('User registered');
        await load();
      });
    },
  }, h('strong', {}, 'Register a user'), username, email, displayName, h('button', {}, 'Register'));

  app.replaceChildren(
    h('h2', {}, 'Users'),
    form,
    h('table', {},
      h('thead', {}, h('tr', {}, ['ID', 'Username', 'Email', 'Display name', 'Joined'].map((t) => h('th', {}, t)))),
      tbody));
  await load();
}

// ---------- routing ----------

const routes = [
  [/^#\/?$/, feedPage],
  [/^#\/q\/([\w-]+)$/, questionPage],
  [/^#\/tag\/(.+)$/, tagPage],
  [/^#\/tags$/, tagsPage],
  [/^#\/users$/, usersPage],
  [/^#\/search\?(.*)$/, searchPage],
];

async function route() {
  const hash = location.hash || '#/';
  for (const [pattern, page] of routes) {
    const match = hash.match(pattern);
    if (!match) continue;
    app.replaceChildren(h('p', { class: 'muted' }, 'Loading...'));
    try {
      await page(...match.slice(1));
    } catch (e) {
      app.replaceChildren(h('p', { class: 'error' }, e.message));
    }
    return;
  }
  app.replaceChildren(h('p', {}, 'Page not found.'));
}

document.getElementById('search-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const q = document.getElementById('search-input').value.trim();
  if (q) location.hash = `#/search?${query({ q })}`;
});

window.addEventListener('hashchange', route);
route();
