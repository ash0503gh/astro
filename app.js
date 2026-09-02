/* ================================================
   JYOTISH — Vedic Astrology App (Vanilla JS)
   ================================================ */

// ── Constants ──

const SIGN_SYMBOLS = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'];

const PLANET_COLORS = {
  Sun:'#d97706', Moon:'#475569', Mars:'#dc2626', Mercury:'#16a34a',
  Jupiter:'#ca8a04', Venus:'#db2777', Saturn:'#2563eb', Rahu:'#64748b', Ketu:'#7c3aed',
};

const DASHA_COLORS = {
  Ketu:'#7c3aed', Venus:'#db2777', Sun:'#d97706', Moon:'#64748b',
  Mars:'#dc2626', Rahu:'#475569', Jupiter:'#ca8a04', Saturn:'#2563eb', Mercury:'#16a34a',
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

// ── DOM ──

const $ = (sel) => document.querySelector(sel);
const show = (el) => el.classList.remove('hidden');
const hide = (el) => el.classList.add('hidden');

// ── API ──

async function apiChart(data) {
  const res = await fetch('/api/chart', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ name:data.name, birth_date:data.birthDate, birth_time:data.birthTime, birth_city:data.birthCity }),
  });
  if (!res.ok) { const e = await res.json().catch(()=>({detail:'Server error'})); throw new Error(e.detail||`HTTP ${res.status}`); }
  return res.json();
}

async function apiAIReading(data) {
  const res = await fetch('/api/ai-reading', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ name:data.name, birth_date:data.birthDate, birth_time:data.birthTime, birth_city:data.birthCity }),
  });
  if (!res.ok) throw new Error('AI reading request failed');
  return res.json();
}

// ── Event Handlers ──

async function handleSubmit(e) {
  e.preventDefault();
  const name=$('#inp-name').value.trim(), birthDate=$('#inp-date').value,
        birthTime=$('#inp-time').value, birthCity=$('#inp-city').value.trim();
  if (!name||!birthDate||!birthTime||!birthCity) return;
  birthInput = { name, birthDate, birthTime, birthCity };
  hide($('#section-form')); hide($('#section-error'));
  show($('#section-loading')); hide($('#section-results'));
  try {
    chartData = await apiChart(birthInput);
    activeTab='chart'; selectedDasha=null; aiReading=null; aiLoading=false;
    renderResults();
  } catch(err) { showError(err.message); }
}

function handleReset() {
  chartData=null; birthInput=null; aiReading=null;
  hide($('#section-loading')); hide($('#section-error'));
  hide($('#section-results')); show($('#section-form'));
  $('#btn-new-chart').style.display='none';
}

function handleTabClick(tabId) { activeTab=tabId; renderTabs(); renderTabContent(); }

function showError(msg) {
  hide($('#section-loading')); hide($('#section-form')); hide($('#section-results'));
  show($('#section-error')); $('#error-message').textContent=msg;
}

async function handleAIGenerate() {
  if (!birthInput||aiLoading) return;
  aiLoading=true; renderTabContent();
  try { const d = await apiAIReading(birthInput); aiReading=d.reading; }
  catch(err) { aiReading={error:err.message}; }
  finally { aiLoading=false; renderTabContent(); }
}

// ── Render ──

function renderResults() {
  hide($('#section-loading')); hide($('#section-form'));
  show($('#section-results')); $('#btn-new-chart').style.display='flex';
  renderResultsHeader(); renderTabs(); renderTabContent();
}

function renderResultsHeader() {
  const d=chartData, moon=d.planets.find(p=>p.name==='Moon');
  $('#results-header').innerHTML=`
    <h2>${esc(d.name)}'s Kundali</h2>
    <p class="meta">${d.birth_info.date} &middot; ${d.birth_info.time} &middot; ${esc(d.birth_info.city)}</p>
    <p class="meta-sub">Lagna: ${d.ascendant.sign} (${d.ascendant.sign_english}) &middot; Moon: ${moon?moon.sign:''} &middot; ${d.birth_info.timezone}</p>`;
}

function renderTabs() {
  $('#tabs-nav').innerHTML = TABS.map(t =>
    `<button class="tab-btn ${t.id===activeTab?'active':''}" onclick="handleTabClick('${t.id}')">${t.label}</button>`
  ).join('');
}

function renderTabContent() {
  const el=$('#tab-content');
  switch(activeTab) {
    case 'chart':   el.innerHTML=renderChartTab(); break;
    case 'planets': el.innerHTML=renderPlanetsTab(); break;
    case 'dasha':   el.innerHTML=renderDashaTab(); break;
    case 'yoga':    el.innerHTML=renderYogaDoshaTab(); break;
    case 'reading': el.innerHTML=renderReadingTab(); break;
    case 'ai':      el.innerHTML=renderAITab(); break;
  }
}

// ══════════════════════════════════════════
//  KUNDALI CHART — North Indian Diamond
// ══════════════════════════════════════════
//
//  Geometry: outer square + inner diamond
//  (connecting edge midpoints) + 2 diagonals.
//  Creates 12 regions. Houses are FIXED
//  counterclockwise from top = House 1 (Lagna).
//
//  House 1: top inner diamond (Lagna)
//  House 2: upper-left outer triangle
//  House 3: left-upper outer triangle
//  House 4: left inner diamond
//  House 5: lower-left outer triangle
//  House 6: bottom-left outer triangle
//  House 7: bottom inner diamond
//  House 8: bottom-right outer triangle
//  House 9: right-lower outer triangle
//  House 10: right inner diamond
//  House 11: upper-right outer triangle (right-upper)
//  House 12: top-right outer triangle

function renderChartTab() {
  const navRows = chartData.navamsa.map(n =>
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
        <div class="table-wrap"><table class="data-table">
          <thead><tr><th>Planet</th><th>Navamsa Sign</th></tr></thead>
          <tbody>${navRows}</tbody>
        </table></div>
      </div>
    </div>`;
}

function renderKundaliSVG() {
  const SIZE=400, PAD=10, S=SIZE-2*PAD;
  // Key points
  const TL=[PAD,PAD], TR=[PAD+S,PAD], BR=[PAD+S,PAD+S], BL=[PAD,PAD+S];
  const T=[200,PAD], R=[PAD+S,200], B=[200,PAD+S], L=[PAD,200], C=[200,200];
  // Where diagonals cross diamond sides
  const DLT=[105,105], DTR=[295,105], DRB=[295,295], DBL=[105,295];

  // House center positions (centroids of each region)
  const HC = {
    1:  [200,105],  // top inner diamond
    2:  [105,42],   // upper-left triangle
    3:  [42,105],   // left-upper triangle
    4:  [105,200],  // left inner diamond
    5:  [42,295],   // lower-left triangle
    6:  [105,358],  // bottom-left triangle
    7:  [200,295],  // bottom inner diamond
    8:  [295,358],  // bottom-right triangle
    9:  [358,295],  // right-lower triangle
    10: [295,200],  // right inner diamond
    11: [358,105],  // right-upper triangle
    12: [295,42],   // upper-right triangle
  };

  const cd = chartData.chart_data;

  // Draw chart lines
  const lines = `
    <!-- Outer square -->
    <rect x="${PAD}" y="${PAD}" width="${S}" height="${S}" fill="#fff" stroke="#1a1a2e" stroke-width="2.5" rx="2"/>
    <!-- Inner diamond -->
    <polygon points="${T} ${R} ${B} ${L}" fill="none" stroke="#1a1a2e" stroke-width="2"/>
    <!-- Diagonals -->
    <line x1="${TL[0]}" y1="${TL[1]}" x2="${BR[0]}" y2="${BR[1]}" stroke="#1a1a2e" stroke-width="1.2"/>
    <line x1="${TR[0]}" y1="${TR[1]}" x2="${BL[0]}" y2="${BL[1]}" stroke="#1a1a2e" stroke-width="1.2"/>
  `;

  // Render each house
  let houses = '';
  for (let h = 1; h <= 12; h++) {
    const [cx, cy] = HC[h];
    const sn = cd.house_signs[h];
    const sym = SIGN_SYMBOLS[sn-1] || '';
    const planets = cd.house_planets[h] || [];

    // Sign number (small, positioned above planets)
    const signY = planets.length > 0 ? cy - 6 : cy + 2;
    houses += `<text x="${cx}" y="${signY}" text-anchor="middle" font-size="11" fill="#8e8e9e" font-weight="500">${sn}</text>`;

    // Planets
    planets.forEach((p, i) => {
      const color = PLANET_COLORS[p.name] || '#1a1a2e';
      const retro = p.retro && p.name!=='Rahu' && p.name!=='Ketu' ? '(R)' : '';
      houses += `<text x="${cx}" y="${signY + 14 + i*14}" text-anchor="middle" font-size="12" font-weight="700" fill="${color}">${p.symbol}${retro}</text>`;
    });
  }

  return `<svg viewBox="0 0 ${SIZE} ${SIZE}" width="100%" style="max-width:400px" xmlns="http://www.w3.org/2000/svg">
    ${lines}${houses}
  </svg>`;
}

// ── Planets Tab ──

function renderPlanetsTab() {
  const rows = chartData.planets.map(p => {
    const color = PLANET_COLORS[p.name]||'#1a1a2e';
    const retro = p.retrograde && p.name!=='Rahu' && p.name!=='Ketu' ? '<span class="badge badge-retro">R</span>' : '';
    const dc = p.dignity==='exalted'?'badge-exalted':p.dignity==='own_sign'?'badge-own':p.dignity==='debilitated'?'badge-debil':'badge-neutral';
    const dl = p.dignity==='own_sign'?'Own Sign':p.dignity.charAt(0).toUpperCase()+p.dignity.slice(1);
    return `<tr>
      <td><span style="color:${color};font-weight:600;margin-right:6px">${p.symbol}</span>${p.vedic_name||p.name}${retro}</td>
      <td>${p.sign} <span style="color:#8e8e9e;font-size:0.78rem">(${p.sign_english})</span></td>
      <td style="font-weight:500">${p.house}</td><td>${p.degree_in_sign}°</td>
      <td>${p.nakshatra?.name||'-'}</td><td>${p.nakshatra?.pada||'-'}</td>
      <td><span class="badge ${dc}">${dl}</span></td><td>${p.navamsa?.sign||'-'}</td>
    </tr>`;
  }).join('');
  return `<div class="card"><div class="card-title">Planetary Positions</div>
    <div class="table-wrap"><table class="data-table">
      <thead><tr><th>Planet</th><th>Sign</th><th>House</th><th>Degree</th><th>Nakshatra</th><th>Pada</th><th>Dignity</th><th>Navamsa</th></tr></thead>
      <tbody>${rows}</tbody></table></div></div>`;
}

// ── Dasha Tab ──

function renderDashaTab() {
  const dashas=chartData.dashas, now=new Date().toISOString().slice(0,10);
  const currentIdx=dashas.findIndex(d=>d.start<=now&&d.end>=now);
  const totalYears=dashas.reduce((s,d)=>s+d.years,0);

  const bar = dashas.map((d,i) => {
    const w=Math.max((d.years/totalYears)*100,1.5);
    return `<div class="dasha-seg ${i===currentIdx?'current':''}" style="width:${w}%;background:${DASHA_COLORS[d.lord]}"
      title="${d.lord} — ${d.start} to ${d.end}" onclick="toggleDasha(${i})">${w>5?d.lord.slice(0,2):''}</div>`;
  }).join('');

  const legend = dashas.map((d,i) => {
    const curr=i===currentIdx?'<span class="dasha-current-badge">● NOW</span>':'';
    return `<span onclick="toggleDasha(${i})" style="opacity:${selectedDasha!==null&&selectedDasha!==i?0.4:1}">
      <span class="dot" style="background:${DASHA_COLORS[d.lord]}"></span>${d.lord} (${d.years.toFixed(1)}y)${curr}</span>`;
  }).join('');

  const rows = dashas.map((d,i) => {
    const status = i===currentIdx?'<span style="color:#b8860b;font-weight:600">Active</span>'
      :d.end<now?'<span style="color:#8e8e9e">Completed</span>':'<span style="color:#555566">Upcoming</span>';
    return `<tr style="cursor:pointer;${selectedDasha===i?'background:#f0ede6':''}" onclick="toggleDasha(${i})">
      <td><span style="color:${DASHA_COLORS[d.lord]};font-weight:600;margin-right:6px">●</span>${d.lord}
        <span style="color:#8e8e9e;font-size:0.78rem;margin-left:4px">(${d.total_years}y total)</span></td>
      <td>${d.years.toFixed(2)}</td><td>${d.start}</td><td>${d.end}</td><td>${status}</td></tr>`;
  }).join('');

  let antarPanel='';
  if (selectedDasha!==null && dashas[selectedDasha]?.antardashas) {
    const md=dashas[selectedDasha];
    const aRows=md.antardashas.map(a => {
      const isActive=a.start<=now&&a.end>=now;
      const ab=isActive?'<span style="color:#b8860b;margin-left:8px;font-size:0.72rem">● ACTIVE</span>':'';
      return `<tr><td><span style="color:${DASHA_COLORS[a.lord]};font-weight:600;margin-right:4px">●</span>${a.lord}${ab}</td>
        <td>${a.years.toFixed(2)}</td><td>${a.start}</td><td>${a.end}</td></tr>`;
    }).join('');
    antarPanel=`<div class="antar-panel"><h4>${md.lord} Mahadasha — Antardasha Periods</h4>
      <div class="table-wrap"><table class="data-table">
        <thead><tr><th>Antardasha Lord</th><th>Duration (Y)</th><th>Start</th><th>End</th></tr></thead>
        <tbody>${aRows}</tbody></table></div></div>`;
  }

  return `<div class="card"><div class="card-title">Vimshottari Dasha Periods</div>
    <p style="color:#555566;font-size:0.82rem;margin-bottom:16px">Click a period for Antardasha details.</p>
    <div class="dasha-bar">${bar}</div><div class="dasha-legend">${legend}</div>
    <div class="table-wrap"><table class="data-table">
      <thead><tr><th>Mahadasha</th><th>Period (Y)</th><th>Start</th><th>End</th><th>Status</th></tr></thead>
      <tbody>${rows}</tbody></table></div>${antarPanel}</div>`;
}

function toggleDasha(idx) { selectedDasha=selectedDasha===idx?null:idx; renderTabContent(); }

// ── Yogas & Doshas ──

function renderYogaDoshaTab() {
  const yc = chartData.yogas.length===0 ? '<p style="color:#8e8e9e">No major yogas detected.</p>'
    : chartData.yogas.map(y=>`<div class="yd-card yoga-card"><h4>${y.name}<span class="yd-type">${y.type}</span></h4>
      <p>${y.description}</p><p class="yd-meta">Planets: ${y.planets.join(', ')} &middot; Strength: ${y.strength}</p></div>`).join('');

  const dc = chartData.doshas.length===0 ? '<p style="color:#8e8e9e">No doshas analyzed.</p>'
    : chartData.doshas.map(d => {
      const cls=!d.present?'dosha-absent':d.severity==='cancelled'?'dosha-cancelled':'dosha-present';
      const sl=!d.present?'✓ Absent':d.severity==='cancelled'?'↩ Cancelled':`● ${d.severity}`;
      const eff=d.present&&d.effects?`<p style="margin-top:8px"><strong style="font-size:0.8rem">Effects:</strong> ${d.effects}</p>`:'';
      const can=d.cancellation?`<p class="cancellation">↩ ${d.cancellation}</p>`:'';
      const rem=d.present&&d.remedies?`<div class="remedies"><strong>Remedies:</strong><ul>${d.remedies.map(r=>`<li>${r}</li>`).join('')}</ul></div>`:'';
      return `<div class="yd-card ${cls}"><h4>${d.name}<span class="yd-type">${sl}</span></h4><p>${d.description}</p>${eff}${can}${rem}</div>`;
    }).join('');

  return `<div class="yd-grid">
    <div class="card"><div class="card-title"><span style="color:#16a34a">✦</span> Yogas Detected</div>${yc}</div>
    <div class="card"><div class="card-title"><span style="color:#dc2626">⚠</span> Doshas Analysis</div>${dc}</div></div>`;
}

// ── Reading ──

function renderReadingTab() {
  const r=chartData.basic_reading;
  if (!r) return '<div class="card"><p style="color:#8e8e9e">No reading available.</p></div>';
  const ps=(r.planets||[]).map(p=>`<div class="planet-reading"><h4>${p.placement}</h4><p>${p.reading||'Details in AI reading.'}</p></div>`).join('');
  const str=(r.key_strengths||[]).length>0?`<div class="reading-section"><h3><span>✦</span> Key Strengths</h3><ul class="reading-list strengths">${r.key_strengths.map(s=>`<li>${s}</li>`).join('')}</ul></div>`:'';
  const ch=(r.key_challenges||[]).length>0?`<div class="reading-section"><h3><span>🔥</span> Areas for Growth</h3><ul class="reading-list challenges">${r.key_challenges.map(c=>`<li>${c}</li>`).join('')}</ul></div>`:'';
  return `<div class="card"><div class="card-title">Chart Interpretation</div>
    <div class="reading-section"><h3><span>🌅</span> Personality & Ascendant</h3><p>${r.personality||''}</p></div>
    <div class="reading-section"><h3><span>🪐</span> Planetary Placements</h3>${ps}</div>
    ${r.career?`<div class="reading-section"><h3><span>💼</span> Career</h3><p>${r.career}</p></div>`:''}
    ${r.relationships?`<div class="reading-section"><h3><span>💑</span> Relationships</h3><p>${r.relationships}</p></div>`:''}
    ${str}${ch}
    ${r.summary?`<div class="reading-section"><h3><span>📋</span> Summary</h3><p>${r.summary}</p></div>`:''}</div>`;
}

// ── AI Reading ──

function renderAITab() {
  if (aiLoading) return `<div class="card loading-box" style="padding:50px 24px">
    <div class="orbit-spinner"><div class="orbit"></div><div class="orbit"></div><div class="orbit"></div></div>
    <p class="loading-title">Analyzing chart with AI…</p>
    <p class="loading-sub">This may take 15–30 seconds.</p></div>`;
  if (!aiReading) return `<div class="card ai-prompt"><h3>✦ AI-Powered Deep Reading</h3>
    <p>Comprehensive personalized interpretation covering personality, career, relationships, health, spirituality, and current planetary period.</p>
    <button class="btn btn-primary" onclick="handleAIGenerate()"><span>Generate AI Reading</span><span class="btn-icon">→</span></button>
    <p class="hint">Powered by Claude AI</p></div>`;
  if (aiReading.error) return `<div class="card"><div class="error-box" style="border:none;margin:0"><p>${aiReading.error}</p></div></div>`;
  const sections=aiReading.sections||{};
  let content='';
  if (Object.keys(sections).length>0) {
    content=Object.entries(sections).map(([k,t])=>{
      if(!t||t.trim().length<10) return '';
      const title=k.replace(/_/g,' ').replace(/and/g,'&').replace(/\b\w/g,c=>c.toUpperCase());
      return `<div class="ai-section"><h3>${title}</h3>${t.split('\n\n').map(p=>`<p>${esc(p)}</p>`).join('')}</div>`;
    }).join('');
  } else if (aiReading.full_text) { content=aiReading.full_text.split('\n\n').map(p=>`<p>${esc(p)}</p>`).join(''); }
  return `<div class="card"><div class="card-title">✦ AI-Powered Deep Reading</div>${content||'<p style="color:#8e8e9e">No content.</p>'}
    <div style="margin-top:24px;padding-top:16px;border-top:1px solid #e8e4de">
      <button class="btn btn-ghost" onclick="handleAIGenerate()">Regenerate Reading</button></div></div>`;
}

// ── Helpers ──
function esc(str) { const d=document.createElement('div'); d.textContent=str; return d.innerHTML; }
