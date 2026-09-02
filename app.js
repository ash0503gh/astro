/* ================================================
   JYOTISH — Vedic Astrology App (Vanilla JS)
   ================================================ */

// ── Constants ──

const SIGN_SYMBOLS = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'];

const PLANET_COLORS = {
  Sun:'#f59e0b', Moon:'#e2e8f0', Mars:'#ef4444', Mercury:'#34d399',
  Jupiter:'#eab308', Venus:'#ec4899', Saturn:'#3b82f6', Rahu:'#94a3b8', Ketu:'#a78bfa',
};

const DASHA_COLORS = {
  Ketu:'#a78bfa', Venus:'#ec4899', Sun:'#f59e0b', Moon:'#e2e8f0',
  Mars:'#ef4444', Rahu:'#94a3b8', Jupiter:'#eab308', Saturn:'#3b82f6', Mercury:'#34d399',
};

const TABS = [
  { id:'chart',   label:'Kundali Chart' },
  { id:'planets', label:'Planets' },
  { id:'dasha',   label:'Dasha' },
  { id:'yoga',    label:'Yogas & Doshas' },
  { id:'reading', label:'Reading' },
  { id:'ai',      label:'✦ AI Reading' },
];

// ── State ──

let chartData = null;
let birthInput = null;
let activeTab = 'chart';
let selectedDasha = null;
let aiReading = null;
let aiLoading = false;

// ── DOM Helpers ──

const $ = (sel) => document.querySelector(sel);
const show = (el) => el.classList.remove('hidden');
const hide = (el) => el.classList.add('hidden');

// ── API ──

async function apiChart(data) {
  const res = await fetch('/api/chart', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: data.name, birth_date: data.birthDate,
      birth_time: data.birthTime, birth_city: data.birthCity,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Server error' }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

async function apiAIReading(data) {
  const res = await fetch('/api/ai-reading', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: data.name, birth_date: data.birthDate,
      birth_time: data.birthTime, birth_city: data.birthCity,
    }),
  });
  if (!res.ok) throw new Error('AI reading request failed');
  return res.json();
}

// ── Event Handlers ──

async function handleSubmit(e) {
  e.preventDefault();
  const name = $('#inp-name').value.trim();
  const birthDate = $('#inp-date').value;
  const birthTime = $('#inp-time').value;
  const birthCity = $('#inp-city').value.trim();
  if (!name || !birthDate || !birthTime || !birthCity) return;

  birthInput = { name, birthDate, birthTime, birthCity };
  hide($('#section-form'));
  hide($('#section-error'));
  show($('#section-loading'));
  hide($('#section-results'));

  try {
    chartData = await apiChart(birthInput);
    activeTab = 'chart';
    selectedDasha = null;
    aiReading = null;
    aiLoading = false;
    renderResults();
  } catch (err) {
    showError(err.message);
  }
}

function handleReset() {
  chartData = null;
  birthInput = null;
  aiReading = null;
  hide($('#section-loading'));
  hide($('#section-error'));
  hide($('#section-results'));
  show($('#section-form'));
  $('#btn-new-chart').style.display = 'none';
}

function handleTabClick(tabId) {
  activeTab = tabId;
  renderTabs();
  renderTabContent();
}

function showError(msg) {
  hide($('#section-loading'));
  hide($('#section-form'));
  hide($('#section-results'));
  show($('#section-error'));
  $('#error-message').textContent = msg;
}

async function handleAIGenerate() {
  if (!birthInput || aiLoading) return;
  aiLoading = true;
  renderTabContent();
  try {
    const data = await apiAIReading(birthInput);
    aiReading = data.reading;
  } catch (err) {
    aiReading = { error: err.message };
  } finally {
    aiLoading = false;
    renderTabContent();
  }
}

// ── Renderers ──

function renderResults() {
  hide($('#section-loading'));
  hide($('#section-form'));
  show($('#section-results'));
  $('#btn-new-chart').style.display = 'flex';

  renderResultsHeader();
  renderTabs();
  renderTabContent();
}

function renderResultsHeader() {
  const d = chartData;
  const moon = d.planets.find(p => p.name === 'Moon');
  $('#results-header').innerHTML = `
    <h2>${esc(d.name)}'s Kundali</h2>
    <p class="meta">${d.birth_info.date} &middot; ${d.birth_info.time} &middot; ${esc(d.birth_info.city)}</p>
    <p class="meta-sub">
      Lagna: ${d.ascendant.sign} (${d.ascendant.sign_english}) &middot;
      Moon: ${moon ? moon.sign : ''} &middot;
      ${d.birth_info.timezone}
    </p>
  `;
}

function renderTabs() {
  const nav = $('#tabs-nav');
  nav.innerHTML = TABS.map(t =>
    `<button class="tab-btn ${t.id === activeTab ? 'active' : ''}"
             onclick="handleTabClick('${t.id}')">${t.label}</button>`
  ).join('');
}

function renderTabContent() {
  const el = $('#tab-content');
  switch (activeTab) {
    case 'chart':   el.innerHTML = renderChartTab(); break;
    case 'planets': el.innerHTML = renderPlanetsTab(); break;
    case 'dasha':   el.innerHTML = renderDashaTab(); break;
    case 'yoga':    el.innerHTML = renderYogaDoshaTab(); break;
    case 'reading': el.innerHTML = renderReadingTab(); break;
    case 'ai':      el.innerHTML = renderAITab(); break;
  }
}

// ── Chart Tab ──

function renderChartTab() {
  const navamsaHTML = chartData.navamsa.map(n =>
    `<tr><td style="font-weight:500">${n.symbol} ${n.name}</td><td>${n.navamsa_sign}</td></tr>`
  ).join('');

  return `
    <div class="chart-grid">
      <div class="card">
        <div class="card-title">Rashi Chart (D1)</div>
        <div class="chart-svg-wrap">${renderKundaliSVG()}</div>
      </div>
      <div class="card">
        <div class="card-title">Navamsa Chart (D9)</div>
        <div class="table-wrap">
          <table class="data-table">
            <thead><tr><th>Planet</th><th>Navamsa Sign</th></tr></thead>
            <tbody>${navamsaHTML}</tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

function renderKundaliSVG() {
  const S = 380, PAD = 10, SIZE = 400, CX = 200, CY = 200;
  const cd = chartData.chart_data;

  // House center positions
  const HC = {
    1:[CX, PAD+S*0.13], 2:[PAD+S*0.82, PAD+S*0.18],
    3:[PAD+S*0.87, CY],  4:[PAD+S*0.82, PAD+S*0.82],
    5:[CX, PAD+S*0.87],  6:[PAD+S*0.18, PAD+S*0.82],
    7:[PAD+S*0.13, CY],  8:[PAD+S*0.18, PAD+S*0.18],
    9:[PAD+S*0.35, PAD+S*0.35],  10:[PAD+S*0.35, PAD+S*0.65],
    11:[PAD+S*0.65, PAD+S*0.65], 12:[PAD+S*0.65, PAD+S*0.35],
  };

  let houses = '';
  for (let h = 1; h <= 12; h++) {
    const [cx, cy] = HC[h];
    const sn = cd.house_signs[h];
    const sym = SIGN_SYMBOLS[sn - 1] || '';
    const planets = cd.house_planets[h] || [];

    // ASC label for house 1
    const ascLabel = h === 1
      ? `<text x="${cx}" y="${cy-22}" text-anchor="middle" font-size="9" fill="#d4a520" font-weight="700">ASC</text>`
      : '';

    // Sign label
    const signLabel = `<text x="${cx}" y="${cy-8}" text-anchor="middle" font-size="11" fill="#5e5e80" font-weight="500">${sym} ${sn}</text>`;

    // Planets
    const planetLabels = planets.map((p, i) => {
      const color = PLANET_COLORS[p.name] || '#e8e8f4';
      const retro = p.retro && p.name !== 'Rahu' && p.name !== 'Ketu' ? '(R)' : '';
      return `<text x="${cx}" y="${cy+8+i*14}" text-anchor="middle" font-size="12" font-weight="600" fill="${color}">${p.symbol}${retro}</text>`;
    }).join('');

    houses += ascLabel + signLabel + planetLabels;
  }

  return `
    <svg viewBox="0 0 ${SIZE} ${SIZE}" width="100%" style="max-width:380px" xmlns="http://www.w3.org/2000/svg">
      <rect x="${PAD}" y="${PAD}" width="${S}" height="${S}" fill="#060612" rx="4" stroke="#1e1e44" stroke-width="1"/>
      <line x1="${PAD}" y1="${PAD}" x2="${PAD+S}" y2="${PAD+S}" stroke="#a07c15" stroke-width="0.8" opacity="0.5"/>
      <line x1="${PAD+S}" y1="${PAD}" x2="${PAD}" y2="${PAD+S}" stroke="#a07c15" stroke-width="0.8" opacity="0.5"/>
      <line x1="${PAD}" y1="${CY}" x2="${PAD+S}" y2="${CY}" stroke="#a07c15" stroke-width="0.8" opacity="0.5"/>
      <line x1="${CX}" y1="${PAD}" x2="${CX}" y2="${PAD+S}" stroke="#a07c15" stroke-width="0.8" opacity="0.5"/>
      <rect x="${PAD}" y="${PAD}" width="${S}" height="${S}" fill="none" stroke="#a07c15" stroke-width="1.5" rx="4"/>
      <text x="${CX}" y="${CY-3}" text-anchor="middle" font-size="10" fill="#5e5e80" font-weight="500">RASHI</text>
      <text x="${CX}" y="${CY+11}" text-anchor="middle" font-size="9" fill="#5e5e80">D1</text>
      ${houses}
    </svg>
  `;
}

// ── Planets Tab ──

function renderPlanetsTab() {
  const rows = chartData.planets.map(p => {
    const color = PLANET_COLORS[p.name] || '#e8e8f4';
    const retroBadge = p.retrograde && p.name !== 'Rahu' && p.name !== 'Ketu'
      ? '<span class="badge badge-retro">R</span>' : '';
    const digClass = p.dignity === 'exalted' ? 'badge-exalted'
      : p.dignity === 'own_sign' ? 'badge-own'
      : p.dignity === 'debilitated' ? 'badge-debil' : 'badge-neutral';
    const digLabel = p.dignity === 'own_sign' ? 'Own Sign'
      : p.dignity.charAt(0).toUpperCase() + p.dignity.slice(1);
    return `<tr>
      <td><span style="color:${color};font-weight:600;margin-right:6px">${p.symbol}</span>${p.vedic_name || p.name}${retroBadge}</td>
      <td>${p.sign} <span style="color:#5e5e80;font-size:0.78rem">(${p.sign_english})</span></td>
      <td style="font-weight:500">${p.house}</td>
      <td>${p.degree_in_sign}°</td>
      <td>${p.nakshatra?.name || '-'}</td>
      <td>${p.nakshatra?.pada || '-'}</td>
      <td><span class="badge ${digClass}">${digLabel}</span></td>
      <td>${p.navamsa?.sign || '-'}</td>
    </tr>`;
  }).join('');

  return `<div class="card"><div class="card-title">Planetary Positions</div>
    <div class="table-wrap"><table class="data-table">
      <thead><tr><th>Planet</th><th>Sign</th><th>House</th><th>Degree</th><th>Nakshatra</th><th>Pada</th><th>Dignity</th><th>Navamsa</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div></div>`;
}

// ── Dasha Tab ──

function renderDashaTab() {
  const dashas = chartData.dashas;
  const now = new Date().toISOString().slice(0, 10);
  const currentIdx = dashas.findIndex(d => d.start <= now && d.end >= now);
  const totalYears = dashas.reduce((s, d) => s + d.years, 0);

  // Bar
  const bar = dashas.map((d, i) => {
    const w = Math.max((d.years / totalYears) * 100, 1.5);
    const cls = i === currentIdx ? 'current' : '';
    return `<div class="dasha-seg ${cls}" style="width:${w}%;background:${DASHA_COLORS[d.lord]}"
                 title="${d.lord} — ${d.start} to ${d.end}"
                 onclick="toggleDasha(${i})">${w > 5 ? d.lord.slice(0,2) : ''}</div>`;
  }).join('');

  // Legend
  const legend = dashas.map((d, i) => {
    const curr = i === currentIdx ? '<span class="dasha-current-badge">● NOW</span>' : '';
    return `<span onclick="toggleDasha(${i})" style="opacity:${selectedDasha !== null && selectedDasha !== i ? 0.4 : 1}">
      <span class="dot" style="background:${DASHA_COLORS[d.lord]}"></span>${d.lord} (${d.years.toFixed(1)}y)${curr}
    </span>`;
  }).join('');

  // Table
  const rows = dashas.map((d, i) => {
    const status = i === currentIdx ? '<span style="color:#d4a520;font-weight:600">Active</span>'
      : d.end < now ? '<span style="color:#5e5e80">Completed</span>'
      : '<span style="color:#9898bb">Upcoming</span>';
    return `<tr style="cursor:pointer;${selectedDasha===i?'background:#1e1e50':''}" onclick="toggleDasha(${i})">
      <td><span style="color:${DASHA_COLORS[d.lord]};font-weight:600;margin-right:6px">●</span>${d.lord}
        <span style="color:#5e5e80;font-size:0.78rem;margin-left:4px">(${d.total_years}y total)</span></td>
      <td>${d.years.toFixed(2)}</td><td>${d.start}</td><td>${d.end}</td><td>${status}</td>
    </tr>`;
  }).join('');

  // Antardasha panel
  let antarPanel = '';
  if (selectedDasha !== null && dashas[selectedDasha]?.antardashas) {
    const md = dashas[selectedDasha];
    const aRows = md.antardashas.map(a => {
      const isActive = a.start <= now && a.end >= now;
      const activeBadge = isActive ? '<span style="color:#d4a520;margin-left:8px;font-size:0.72rem">● ACTIVE</span>' : '';
      return `<tr>
        <td><span style="color:${DASHA_COLORS[a.lord]};font-weight:600;margin-right:4px">●</span>${a.lord}${activeBadge}</td>
        <td>${a.years.toFixed(2)}</td><td>${a.start}</td><td>${a.end}</td>
      </tr>`;
    }).join('');
    antarPanel = `<div class="antar-panel">
      <h4>${md.lord} Mahadasha — Antardasha Periods</h4>
      <div class="table-wrap"><table class="data-table">
        <thead><tr><th>Antardasha Lord</th><th>Duration (Years)</th><th>Start</th><th>End</th></tr></thead>
        <tbody>${aRows}</tbody>
      </table></div></div>`;
  }

  return `<div class="card">
    <div class="card-title">Vimshottari Dasha Periods</div>
    <p style="color:#9898bb;font-size:0.82rem;margin-bottom:16px">Click a period for Antardasha details.</p>
    <div class="dasha-bar">${bar}</div>
    <div class="dasha-legend">${legend}</div>
    <div class="table-wrap"><table class="data-table">
      <thead><tr><th>Mahadasha</th><th>Period (Y)</th><th>Start</th><th>End</th><th>Status</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
    ${antarPanel}
  </div>`;
}

function toggleDasha(idx) {
  selectedDasha = selectedDasha === idx ? null : idx;
  renderTabContent();
}

// ── Yogas & Doshas Tab ──

function renderYogaDoshaTab() {
  // Yogas
  const yogaCards = chartData.yogas.length === 0
    ? '<p style="color:#5e5e80">No major yogas detected.</p>'
    : chartData.yogas.map(y => `
      <div class="yd-card yoga-card">
        <h4>${y.name}<span class="yd-type">${y.type}</span></h4>
        <p>${y.description}</p>
        <p class="yd-meta">Planets: ${y.planets.join(', ')} &middot; Strength: ${y.strength}</p>
      </div>`).join('');

  // Doshas
  const doshaCards = chartData.doshas.length === 0
    ? '<p style="color:#5e5e80">No doshas analyzed.</p>'
    : chartData.doshas.map(d => {
      const cls = !d.present ? 'dosha-absent'
        : d.severity === 'cancelled' ? 'dosha-cancelled' : 'dosha-present';
      const statusLabel = !d.present ? '✓ Absent'
        : d.severity === 'cancelled' ? '↩ Cancelled' : `● ${d.severity}`;
      const effects = d.present && d.effects ? `<p style="margin-top:8px"><strong style="color:#e8e8f4;font-size:0.8rem">Effects:</strong> ${d.effects}</p>` : '';
      const cancel = d.cancellation ? `<p class="cancellation">↩ ${d.cancellation}</p>` : '';
      const remedies = d.present && d.remedies ? `<div class="remedies"><strong>Remedies:</strong><ul>${d.remedies.map(r => `<li>${r}</li>`).join('')}</ul></div>` : '';
      return `<div class="yd-card ${cls}">
        <h4>${d.name}<span class="yd-type">${statusLabel}</span></h4>
        <p>${d.description}</p>${effects}${cancel}${remedies}
      </div>`;
    }).join('');

  return `
    <div class="yd-grid">
      <div class="card">
        <div class="card-title"><span style="color:#34d399">✦</span> Yogas Detected</div>
        ${yogaCards}
      </div>
      <div class="card">
        <div class="card-title"><span style="color:#f87171">⚠</span> Doshas Analysis</div>
        ${doshaCards}
      </div>
    </div>`;
}

// ── Reading Tab ──

function renderReadingTab() {
  const r = chartData.basic_reading;
  if (!r) return '<div class="card"><p style="color:#5e5e80">No reading available.</p></div>';

  const planetSections = (r.planets || []).map(p => `
    <div class="planet-reading">
      <h4>${p.placement}</h4>
      <p>${p.reading || 'Details available in AI reading.'}</p>
    </div>`).join('');

  const strengths = (r.key_strengths || []).length > 0 ? `
    <div class="reading-section">
      <h3><span>✦</span> Key Strengths</h3>
      <ul class="reading-list strengths">${r.key_strengths.map(s => `<li>${s}</li>`).join('')}</ul>
    </div>` : '';

  const challenges = (r.key_challenges || []).length > 0 ? `
    <div class="reading-section">
      <h3><span>🔥</span> Areas for Growth</h3>
      <ul class="reading-list challenges">${r.key_challenges.map(c => `<li>${c}</li>`).join('')}</ul>
    </div>` : '';

  return `<div class="card"><div class="card-title">Chart Interpretation</div>
    <div class="reading-section"><h3><span>🌅</span> Personality & Ascendant</h3><p>${r.personality || ''}</p></div>
    <div class="reading-section"><h3><span>🪐</span> Planetary Placements</h3>${planetSections}</div>
    ${r.career ? `<div class="reading-section"><h3><span>💼</span> Career</h3><p>${r.career}</p></div>` : ''}
    ${r.relationships ? `<div class="reading-section"><h3><span>💑</span> Relationships</h3><p>${r.relationships}</p></div>` : ''}
    ${strengths}${challenges}
    ${r.summary ? `<div class="reading-section"><h3><span>📋</span> Summary</h3><p>${r.summary}</p></div>` : ''}
  </div>`;
}

// ── AI Reading Tab ──

function renderAITab() {
  if (aiLoading) {
    return `<div class="card loading-box" style="padding:50px 24px">
      <div class="orbit-spinner"><div class="orbit"></div><div class="orbit"></div><div class="orbit"></div></div>
      <p class="loading-title">Analyzing chart with AI…</p>
      <p class="loading-sub">This may take 15–30 seconds for a thorough reading.</p>
    </div>`;
  }

  if (!aiReading) {
    return `<div class="card ai-prompt">
      <h3>✦ AI-Powered Deep Reading</h3>
      <p>Get a comprehensive, personalized interpretation covering personality, career, relationships, health, spirituality, and current planetary period.</p>
      <button class="btn btn-primary" onclick="handleAIGenerate()">
        <span class="btn-label">Generate AI Reading</span><span class="btn-icon">→</span>
      </button>
      <p class="hint">Powered by Claude AI &middot; Requires ANTHROPIC_API_KEY on backend</p>
    </div>`;
  }

  if (aiReading.error) {
    return `<div class="card"><div class="error-box" style="border:none;margin:0"><p>${aiReading.error}</p></div></div>`;
  }

  const sections = aiReading.sections || {};
  let content = '';
  if (Object.keys(sections).length > 0) {
    content = Object.entries(sections).map(([key, text]) => {
      if (!text || text.trim().length < 10) return '';
      const title = key.replace(/_/g, ' ').replace(/and/g, '&').replace(/\b\w/g, c => c.toUpperCase());
      const paras = text.split('\n\n').map(p => `<p>${esc(p)}</p>`).join('');
      return `<div class="ai-section"><h3>${title}</h3>${paras}</div>`;
    }).join('');
  } else if (aiReading.full_text) {
    content = aiReading.full_text.split('\n\n').map(p => `<p>${esc(p)}</p>`).join('');
  }

  return `<div class="card">
    <div class="card-title">✦ AI-Powered Deep Reading</div>
    ${content || '<p style="color:#5e5e80">No content received.</p>'}
    <div style="margin-top:24px;padding-top:16px;border-top:1px solid #1e1e44">
      <button class="btn btn-ghost" onclick="handleAIGenerate()">Regenerate Reading</button>
    </div>
  </div>`;
}

// ── Helpers ──

function esc(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}
