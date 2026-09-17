// ── Translations (Full UI Localization: English & Hindi) ──

const TRANSLATIONS = {
  en: {
    logo_title: 'Jyotish',
    logo_tagline: 'Vedic Birth Chart & AI-Powered Readings',
    new_chart: '← New Chart',
    form_title: 'Enter Birth Details',
    form_subtitle: 'Accurate birth time is essential for precise Lagna and house calculations.',
    label_name: 'Full Name',
    placeholder_name: 'Enter your name',
    label_date: 'Date of Birth',
    label_time: 'Time of Birth',
    label_city: 'Birth City (India)',
    placeholder_city: 'Type Indian city to select (e.g. Jaipur, Bengaluru, Delhi)',
    city_hint: 'Select your Indian birth city from the dropdown list.',
    label_lang: 'Preferred Language / भाषा',
    lang_hint: 'Results will be generated in this language.',
    btn_generate: 'Generate Kundali',
    loading_calc_title: 'Computing planetary positions…',
    loading_calc_sub: 'Calculating sidereal longitudes with Lahiri Ayanamsa',
    cached_badge: (m) => `⚡ Cached (${m}m left)`,
    tabs: {
      chart: 'Kundali Chart',
      planets: 'Planets',
      dasha: 'Dasha',
      yoga: 'Yogas & Doshas',
      reading: 'Reading',
      ai: '✦ AI Reading',
    },
    chart_rashi_title: 'Rashi Chart (D1)',
    chart_navamsa_title: 'Navamsa Chart (D9)',
    table_planet: 'Planet',
    table_navamsa_sign: 'Navamsa Sign',
    table_sign: 'Sign',
    table_degree: 'Degree',
    table_nakshatra: 'Nakshatra',
    table_pada: 'Pada',
    table_house: 'House',
    table_status: 'Status',
    table_dignity: 'Dignity',
    dasha_title: 'Vimshottari Dasha Periods',
    dasha_hint: 'Click a period for Antardasha details.',
    dasha_current: 'Current Mahadasha & Antardasha',
    dasha_mahadasha: 'Mahadasha',
    dasha_antardasha: 'Antardasha',
    dasha_period: 'Period (Y)',
    dasha_start: 'Start',
    dasha_end: 'End',
    dasha_status: 'Status',
    dasha_active: 'Active',
    dasha_completed: 'Completed',
    dasha_upcoming: 'Upcoming',
    dasha_antar_title: (lord) => `${lord} Mahadasha — Antardasha Periods`,
    dasha_antar_lord: 'Antardasha Lord',
    dasha_duration: 'Duration (Y)',
    yoga_title: 'Yogas Detected',
    dosha_title: 'Doshas Analysis',
    reading_title: 'Chart Interpretation',
    reading_sec_personality: 'Personality & Ascendant',
    reading_sec_planets: 'Planetary Placements',
    reading_sec_career: 'Career',
    reading_sec_relationships: 'Relationships',
    reading_sec_strengths: 'Key Strengths',
    reading_sec_challenges: 'Areas for Growth',
    reading_sec_summary: 'Summary',
    ai_title: '✦ AI-Powered Deep Reading',
    ai_desc: 'Comprehensive personalized interpretation covering personality, career, relationships, health, spirituality, and current planetary period.',
    ai_btn: 'Generate AI Reading',
    ai_hint: 'Powered by Google Gemini',
    ai_loading_title: 'Analyzing chart with AI…',
    ai_loading_sub: 'This may take 15–30 seconds.',
    ai_regenerate: 'Regenerate Reading',
    ai_try_again: 'Try Again',
    ai_sections: {
      introduction: 'Introduction',
      personality_and_core_nature: 'Personality & Core Nature',
      mind_and_emotions: 'Mind & Emotions',
      career_and_profession: 'Career & Profession',
      wealth_and_finances: 'Wealth & Finances',
      relationships_and_marriage: 'Relationships & Marriage',
      health_and_vitality: 'Health & Vitality',
      spiritual_path: 'Spiritual Path',
      current_period_analysis: 'Current Period Analysis',
      key_recommendations: 'Key Recommendations',
    },
    dignities: {
      exalted: 'Exalted',
      own_sign: 'Own Sign',
      debilitated: 'Debilitated',
      neutral: 'Neutral',
    },
    footer_text: 'Jyotish — Vedic Astrology Engine &middot; Swiss Ephemeris &middot; Lahiri Ayanamsa &middot; Whole Sign Houses'
  },
  hi: {
    logo_title: 'ज्योतिष',
    logo_tagline: 'वैदिक जन्म कुण्डली एवं एआई फलादेश',
    new_chart: '← नया चार्ट',
    form_title: 'जन्म विवरण दर्ज करें',
    form_subtitle: 'सटीक लग्न एवं भाव गणना हेतु जन्म का सही समय आवश्यक है।',
    label_name: 'पूरा नाम',
    placeholder_name: 'अपना नाम दर्ज करें',
    label_date: 'जन्म तिथि',
    label_time: 'जन्म समय',
    label_city: 'जन्म स्थान (शहर)',
    placeholder_city: 'भारत का शहर खोजें (जैसे जयपुर, दिल्ली, मुम्बई)',
    city_hint: 'सूची में से अपने जन्म शहर का चयन करें।',
    label_lang: 'पसंदीदा भाषा / Preferred Language',
    lang_hint: 'समस्त परिणाम एवं फलादेश इस भाषा में तैयार होंगे।',
    btn_generate: 'कुण्डली बनाएं',
    loading_calc_title: 'ग्रहों की स्थिति की गणना जारी है…',
    loading_calc_sub: 'लाहिड़ी अयनांश द्वारा निरयण स्पष्ट गणना',
    cached_badge: (m) => `⚡ सुरक्षित (${m} मिनट शेष)`,
    tabs: {
      chart: 'कुण्डली चक्र',
      planets: 'ग्रह स्थिति',
      dasha: 'विंशोत्तरी दशा',
      yoga: 'योग एवं दोष',
      reading: 'फलादेश',
      ai: '✦ एआई फलादेश',
    },
    chart_rashi_title: 'लग्न राशि चक्र (D1)',
    chart_navamsa_title: 'नवांश चक्र (D9)',
    table_planet: 'ग्रह',
    table_navamsa_sign: 'नवांश राशि',
    table_sign: 'राशि',
    table_degree: 'अंश',
    table_nakshatra: 'नक्षत्र',
    table_pada: 'पाद',
    table_house: 'भाव',
    table_status: 'स्थिति',
    table_dignity: 'ग्रह बल',
    dasha_title: 'विंशोत्तरी महादशा कालक्रम',
    dasha_hint: 'अंतर्दशा विवरण देखने के लिए किसी दशा पर क्लिक करें।',
    dasha_current: 'वर्तमान महादशा एवं अंतर्दशा',
    dasha_mahadasha: 'महादशा',
    dasha_antardasha: 'अंतर्दशा',
    dasha_period: 'अवधि (वर्ष)',
    dasha_start: 'प्रारम्भ',
    dasha_end: 'समाप्ति',
    dasha_status: 'स्थिति',
    dasha_active: 'सक्रिय',
    dasha_completed: 'पूर्ण',
    dasha_upcoming: 'आगामी',
    dasha_antar_title: (lord) => `${lord} महादशा — अंतर्दशा कालखंड`,
    dasha_antar_lord: 'अंतर्दशा स्वामी',
    dasha_duration: 'अवधि (वर्ष)',
    yoga_title: 'कुण्डली में उपस्थित शुभ योग',
    dosha_title: 'दोष विश्लेषण एवं प्रभाव',
    reading_title: 'ग्रह स्थिति एवं सामान्य फलादेश',
    reading_sec_personality: 'व्यक्तित्व एवं लग्न फल',
    reading_sec_planets: 'ग्रहों का भाव फल',
    reading_sec_career: 'आजीविका एवं करियर',
    reading_sec_relationships: 'वैवाहिक जीवन एवं संबंध',
    reading_sec_strengths: 'मुख्य सकारात्मक योग',
    reading_sec_challenges: 'ध्यान देने योग्य बिंदु',
    reading_sec_summary: 'समग्र विश्लेषण',
    ai_title: '✦ एआई-संचालित वैदिक महाफलादेश',
    ai_desc: 'व्यक्तित्व, करियर, धन, वैवाहिक जीवन, स्वास्थ्य, आध्यात्म तथा वर्तमान दशा का प्रामाणिक व विस्तृत ज्योतिषीय विश्लेषण।',
    ai_btn: 'एआई फलादेश प्राप्त करें',
    ai_hint: 'गूगल जेमिनी (Google Gemini) द्वारा संचालित',
    ai_loading_title: 'ग्रहों एवं योगों का गहन विश्लेषण जारी है…',
    ai_loading_sub: 'कृपया 15–30 सेकंड की प्रतीक्षा करें।',
    ai_regenerate: 'पुनः फलादेश प्राप्त करें',
    ai_try_again: 'पुनः प्रयास करें',
    ai_sections: {
      introduction: 'परिचय एवं कुण्डली सार',
      personality_and_core_nature: 'व्यक्तित्व एवं स्वभाव',
      mind_and_emotions: 'मन, भावनाएं एवं मानसिक संतुलन',
      career_and_profession: 'करियर, आजीविका एवं कार्यक्षेत्र',
      wealth_and_finances: 'धन, संपत्ति एवं आर्थिक स्थिति',
      relationships_and_marriage: 'वैवाहिक जीवन एवं संबंध',
      health_and_vitality: 'स्वास्थ्य, आयु एवं जीवन ऊर्जा',
      spiritual_path: 'आध्यात्मिक मार्ग एवं धर्म',
      current_period_analysis: 'वर्तमान महादशा एवं दशा विश्लेषण',
      key_recommendations: 'प्रमुख वैदिक उपाय एवं समाधान',
    },
    dignities: {
      exalted: 'उच्च',
      own_sign: 'स्वराशि',
      debilitated: 'नीच',
      neutral: 'सम',
    },
    footer_text: 'ज्योतिष — वैदिक जन्म कुण्डली प्रणाली &middot; स्विस एफिमरिस &middot; लाहिड़ी अयनांश &middot; भाव गणना'
  }
};

let currentLanguage = 'en';
function t(k) { return TRANSLATIONS[currentLanguage]?.[k] || TRANSLATIONS.en[k]; }

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

const SIGNS_HI = {
  'Mesha': 'मेष', 'Vrishabha': 'वृषभ', 'Mithuna': 'मिथुन', 'Karka': 'कर्क',
  'Simha': 'सिंह', 'Kanya': 'कन्या', 'Tula': 'तुला', 'Vrishchika': 'वृश्चिक',
  'Dhanu': 'धनु', 'Makara': 'मकर', 'Kumbha': 'कुम्भ', 'Meena': 'मीन',
  'Aries': 'मेष', 'Taurus': 'वृषभ', 'Gemini': 'मिथुन', 'Cancer': 'कर्क',
  'Leo': 'सिंह', 'Virgo': 'कन्या', 'Libra': 'तुला', 'Scorpio': 'वृश्चिक',
  'Sagittarius': 'धनु', 'Capricorn': 'मकर', 'Aquarius': 'कुम्भ', 'Pisces': 'मीन'
};

const PLANETS_HI = {
  'Sun': 'सूर्य', 'Surya': 'सूर्य',
  'Moon': 'चन्द्र', 'Chandra': 'चन्द्र',
  'Mars': 'मंगल', 'Mangal': 'मंगल',
  'Mercury': 'बुध', 'Budha': 'बुध',
  'Jupiter': 'गुरु', 'Guru': 'गुरु',
  'Venus': 'शुक्र', 'Shukra': 'शुक्र',
  'Saturn': 'शनि', 'Shani': 'शनि',
  'Rahu': 'राहु',
  'Ketu': 'केतु'
};

const DASHA_LORDS_HI = {
  'Ketu': 'केतु', 'Venus': 'शुक्र', 'Sun': 'सूर्य', 'Moon': 'चन्द्र',
  'Mars': 'मंगल', 'Rahu': 'राहु', 'Jupiter': 'गुरु', 'Saturn': 'शनि', 'Mercury': 'बुध'
};

function localizeSign(s) {
  if (!s) return '';
  return currentLanguage === 'hi' ? (SIGNS_HI[s] || s) : s;
}

function localizePlanet(p) {
  if (!p) return '';
  return currentLanguage === 'hi' ? (PLANETS_HI[p] || p) : p;
}

function localizeDashaLord(lord) {
  if (!lord) return '';
  return currentLanguage === 'hi' ? (DASHA_LORDS_HI[lord] || lord) : lord;
}

const NAKSHATRAS_HI = {
  'Ashwini': 'अश्विनी', 'Bharani': 'भरणी', 'Krittika': 'कृत्तिका',
  'Rohini': 'रोहिणी', 'Mrigashira': 'मृगशिरा', 'Ardra': 'आर्द्रा',
  'Punarvasu': 'पुनर्वसु', 'Pushya': 'पुष्य', 'Ashlesha': 'आश्लेषा',
  'Magha': 'मघा', 'Purva Phalguni': 'पूर्वाफाल्गुनी', 'Uttara Phalguni': 'उत्तराफाल्गुनी',
  'Hasta': 'हस्त', 'Chitra': 'चित्रा', 'Swati': 'स्वाति',
  'Vishakha': 'विशाखा', 'Anuradha': 'अनुराधा', 'Jyeshtha': 'ज्येष्ठा',
  'Moola': 'मूल', 'Purva Ashadha': 'पूर्वाषाढ़ा', 'Uttara Ashadha': 'उत्तराषाढ़ा',
  'Shravana': 'श्रवण', 'Dhanishta': 'धनिष्ठा', 'Shatabhisha': 'शतभिषा',
  'Purva Bhadrapada': 'पूर्वाभाद्रपद', 'Uttara Bhadrapada': 'उत्तराभाद्रपद', 'Revati': 'रेवती'
};

function localizeNakshatra(n) {
  if (!n) return '-';
  return currentLanguage === 'hi' ? (NAKSHATRAS_HI[n] || n) : n;
}

// ── State ──

let chartData = null;
let birthInput = null;
let activeTab = 'chart';
let selectedDasha = null;
let aiReading = null;
let aiLoading = false;
let selectedCity = null;
let cityDebounceTimer = null;
let currentCityResults = [];
let activeCityIndex = -1;

// ── Browser Cache Configuration (1 Hour TTL) ──
const CACHE_KEY = 'jyotish_session_v4';
const CACHE_TTL_MS = 60 * 60 * 1000; // 1 hour = 3,600,000 ms
const citySearchCache = new Map();

// Purge any stale session cache from older versions
try {
  localStorage.removeItem('jyotish_session_v1');
  localStorage.removeItem('jyotish_session_v2');
  localStorage.removeItem('jyotish_session_cache');
} catch (e) {}

// ── DOM ──

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);
const show = (el) => el.classList.remove('hidden');
const hide = (el) => el.classList.add('hidden');

// ── Language Handler ──

function handleLanguageChange(lang, shouldReRender = true) {
  currentLanguage = lang || 'en';
  document.body.setAttribute('data-lang', currentLanguage);
  const langSelect = $('#inp-language');
  if (langSelect && langSelect.value !== currentLanguage) langSelect.value = currentLanguage;

  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;

  // Header
  const logoT = $('#logo-title'); if (logoT) logoT.textContent = tr.logo_title;
  const logoSub = $('#logo-tagline'); if (logoSub) logoSub.textContent = tr.logo_tagline;
  const btnNew = $('#btn-new-chart'); if (btnNew) btnNew.textContent = tr.new_chart;

  // Form labels & placeholders
  const formT = $('#form-title'); if (formT) formT.textContent = tr.form_title;
  const formSub = $('#form-sub'); if (formSub) formSub.textContent = tr.form_subtitle;
  const lblName = $('#lbl-name'); if (lblName) lblName.textContent = tr.label_name;
  const inpName = $('#inp-name'); if (inpName) inpName.placeholder = tr.placeholder_name;
  const lblDate = $('#lbl-date'); if (lblDate) lblDate.textContent = tr.label_date;
  const lblTime = $('#lbl-time'); if (lblTime) lblTime.textContent = tr.label_time;
  const lblCity = $('#lbl-city'); if (lblCity) lblCity.textContent = tr.label_city;
  const inpCity = $('#inp-city'); if (inpCity) inpCity.placeholder = tr.placeholder_city;
  const cityHint = $('#city-hint'); if (cityHint && !selectedCity) cityHint.textContent = tr.city_hint;
  const lblLang = $('#lbl-language'); if (lblLang) lblLang.textContent = tr.label_lang;
  const langHint = $('#lang-hint'); if (langHint) langHint.textContent = tr.lang_hint;
  const btnSubmitLbl = $('#btn-submit-label'); if (btnSubmitLbl) btnSubmitLbl.textContent = tr.btn_generate;

  // Loading box
  const loadTitle = $('#section-loading .loading-title'); if (loadTitle) loadTitle.textContent = tr.loading_calc_title;
  const loadSub = $('#section-loading .loading-sub'); if (loadSub) loadSub.textContent = tr.loading_calc_sub;

  // Footer
  const footerText = $('#footer-text'); if (footerText && tr.footer_text) footerText.innerHTML = tr.footer_text;

  if (shouldReRender && chartData && $('#section-results')?.style?.display !== 'none') {
    renderResultsHeader();
    renderTabs();
    renderTabContent();
  }
}

// ── API ──

async function apiChart(data) {
  const payload = {
    name: data.name,
    birth_date: data.birthDate,
    birth_time: data.birthTime,
    birth_city: data.birthCity,
    language: data.language || currentLanguage,
  };
  if (data.latitude && data.longitude) {
    payload.latitude = data.latitude;
    payload.longitude = data.longitude;
  }
  const res = await fetch('/api/chart', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify(payload),
  });
  if (!res.ok) { const e = await res.json().catch(()=>({detail:'Server error'})); throw new Error(e.detail||`HTTP ${res.status}`); }
  return res.json();
}

async function apiAIReading(data) {
  const res = await fetch('/api/ai-reading', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({
      name: data.name,
      birth_date: data.birthDate,
      birth_time: data.birthTime,
      birth_city: data.birthCity,
      latitude: chartData?.birth_info?.latitude,
      longitude: chartData?.birth_info?.longitude,
      language: data.language || currentLanguage,
    }),
  });
  if (!res.ok) {
    const e = await res.json().catch(()=>({detail:'AI reading request failed'}));
    throw new Error(e.detail || e.reading?.error || `HTTP ${res.status}`);
  }
  return res.json();
}

// ── Session Cache Helpers (1 Hour TTL) ──

function saveSessionToCache() {
  if (!chartData || !birthInput) return;
  try {
    const payload = {
      timestamp: Date.now(),
      language: currentLanguage,
      birthInput,
      selectedCity,
      chartData,
      aiReading,
      activeTab,
    };
    localStorage.setItem(CACHE_KEY, JSON.stringify(payload));
  } catch (err) {
    console.warn('Could not save session to cache:', err);
  }
}

function clearSessionCache() {
  try {
    localStorage.removeItem(CACHE_KEY);
  } catch (err) {}
}

function loadSessionFromCache() {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if (!raw) return false;
    const data = JSON.parse(raw);
    const now = Date.now();

    // Check if 1 hour has elapsed
    if (!data.timestamp || (now - data.timestamp > CACHE_TTL_MS)) {
      clearSessionCache();
      return false;
    }

    // Restore state from cache
    currentLanguage = data.language || 'en';
    handleLanguageChange(currentLanguage, false);

    birthInput = data.birthInput || null;
    selectedCity = data.selectedCity || null;
    chartData = data.chartData || null;
    aiReading = data.aiReading || null;
    activeTab = data.activeTab || 'chart';

    // Populate form fields so they match the cached chart
    if (birthInput) {
      const nameInp = $('#inp-name');
      if (nameInp) nameInp.value = birthInput.name || '';
      const dateInp = $('#inp-date');
      if (dateInp) dateInp.value = birthInput.birthDate || '';
      const timeInp = $('#inp-time');
      if (timeInp) timeInp.value = birthInput.birthTime || '';
    }
    if (selectedCity) {
      const cityInp = $('#inp-city');
      if (cityInp) cityInp.value = selectedCity.display || selectedCity.name || '';
      const latInp = $('#inp-city-lat');
      if (latInp) latInp.value = selectedCity.latitude || '';
      const lonInp = $('#inp-city-lon');
      if (lonInp) lonInp.value = selectedCity.longitude || '';
      const statusIcon = $('#city-status-icon');
      if (statusIcon) {
        statusIcon.className = 'city-status-icon active';
        statusIcon.innerHTML = '✓';
      }
      const hint = $('#city-hint');
      if (hint) {
        const selPrefix = currentLanguage === 'hi' ? '✓ चयनित:' : '✓ Selected:';
        hint.textContent = `${selPrefix} ${selectedCity.display}`;
        hint.style.color = '#16a34a';
      }
    }

    if (chartData) {
      renderResults();
      return true;
    }
  } catch (err) {
    console.warn('Could not restore session from cache:', err);
    clearSessionCache();
  }
  return false;
}

// ── Event Handlers ──

async function handleSubmit(e) {
  e.preventDefault();
  const name=$('#inp-name').value.trim(), birthDate=$('#inp-date').value,
        birthTime=$('#inp-time').value;

  if (!name||!birthDate||!birthTime) return;

  // Enforce selecting city from list
  if (!selectedCity) {
    const inp = $('#inp-city');
    inp.classList.add('field-error');
    inp.focus();
    const hint = $('#city-hint');
    if (hint) {
      const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
      hint.textContent = currentLanguage === 'hi' ? '⚠ कृपया सूची में से अपने जन्म शहर का चयन करें।' : '⚠ Please select an Indian city from the dropdown list.';
      hint.style.color = '#dc2626';
    }
    return;
  }

  birthInput = {
    name,
    birthDate,
    birthTime,
    birthCity: selectedCity.name,
    latitude: selectedCity.latitude,
    longitude: selectedCity.longitude,
    language: currentLanguage,
  };

  hide($('#section-form')); hide($('#section-error'));
  show($('#section-loading')); hide($('#section-results'));
  try {
    chartData = await apiChart(birthInput);
    activeTab='chart'; selectedDasha=null; aiReading=null; aiLoading=false;
    renderResults();
    saveSessionToCache();
  } catch(err) { showError(err.message); }
}

function handleReset() {
  clearSessionCache();
  chartData=null; birthInput=null; aiReading=null; selectedCity=null;
  const statusIcon = $('#city-status-icon');
  if (statusIcon) { statusIcon.className = 'city-status-icon'; statusIcon.innerHTML = ''; }
  const hint = $('#city-hint');
  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  if (hint) { hint.textContent = tr.city_hint; hint.style.color = ''; }
  const inp = $('#inp-city');
  if (inp) { inp.classList.remove('field-error'); inp.value = ''; }
  const latInp = $('#inp-city-lat');
  if (latInp) latInp.value = '';
  const lonInp = $('#inp-city-lon');
  if (lonInp) lonInp.value = '';
  const dropdown = $('#city-dropdown');
  if (dropdown) { dropdown.innerHTML = ''; hide(dropdown); }
  hide($('#section-loading')); hide($('#section-error'));
  hide($('#section-results')); show($('#section-form'));
  $('#btn-new-chart').style.display='none';
  handleLanguageChange(currentLanguage, false);
}

function handleTabClick(tabId) {
  activeTab=tabId;
  renderTabs();
  renderTabContent();
  saveSessionToCache();
}

function showError(msg) {
  hide($('#section-loading')); hide($('#section-form')); hide($('#section-results'));
  show($('#section-error')); $('#error-message').textContent=msg;
}

async function handleAIGenerate() {
  if (!birthInput||aiLoading) return;
  aiLoading=true; renderTabContent();
  try {
    const d = await apiAIReading(birthInput);
    aiReading=d.reading;
    saveSessionToCache();
  }
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
  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  let cacheNotice = '';
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      const remainingMin = Math.max(1, Math.round((CACHE_TTL_MS - (Date.now() - parsed.timestamp)) / 60000));
      const badgeText = typeof tr.cached_badge === 'function' ? tr.cached_badge(remainingMin) : `⚡ Cached (${remainingMin}m left)`;
      cacheNotice = `<span style="display:inline-flex;align-items:center;gap:4px;font-size:0.75rem;padding:2px 8px;border-radius:12px;background:#f0fdf4;color:#16a34a;border:1px solid #bbf7d0;font-weight:500;margin-left:8px;vertical-align:middle;">${badgeText}</span>`;
    }
  } catch (e) {}

  const isHi = currentLanguage === 'hi';
  const headerTitle = isHi ? `${esc(d.name)} की जन्म कुण्डली` : `${esc(d.name)}'s Kundali`;
  const lagnaLabel = isHi ? 'लग्न' : 'Lagna';
  const moonLabel = isHi ? 'चन्द्र राशि' : 'Moon';
  const ascSign = isHi ? localizeSign(d.ascendant.sign) : `${d.ascendant.sign} (${d.ascendant.sign_english})`;
  const moonSign = moon ? (isHi ? localizeSign(moon.sign) : moon.sign) : '';

  $('#results-header').innerHTML=`
    <h2>${headerTitle} ${cacheNotice}</h2>
    <p class="meta">${d.birth_info.date} &middot; ${d.birth_info.time} &middot; ${esc(d.birth_info.city)}</p>
    <p class="meta-sub">${lagnaLabel}: ${ascSign} &middot; ${moonLabel}: ${moonSign} &middot; ${d.birth_info.timezone}</p>`;
}

function renderTabs() {
  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  $('#tabs-nav').innerHTML = TABS.map(t => {
    const label = tr.tabs?.[t.id] || t.label;
    return `<button class="tab-btn ${t.id===activeTab?'active':''}" onclick="handleTabClick('${t.id}')">${label}</button>`;
  }).join('');
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
  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  const isHi = currentLanguage === 'hi';
  const navRows = chartData.navamsa.map(n => {
    const pName = isHi ? (PLANETS_HI[n.name] || n.vedic_name || n.name) : n.name;
    const signName = isHi ? (SIGNS_HI[n.navamsa_sign] || n.navamsa_sign) : n.navamsa_sign;
    return `<tr><td style="font-weight:500">${n.symbol} ${pName}</td><td>${signName}</td></tr>`;
  }).join('');
  return `
    <div class="chart-grid">
      <div class="card">
        <div class="card-title">${tr.chart_rashi_title}</div>
        <div class="chart-svg-wrap">${renderKundaliSVG()}</div>
      </div>
      <div class="card">
        <div class="card-title">${tr.chart_navamsa_title}</div>
        <div class="table-wrap"><table class="data-table">
          <thead><tr><th>${tr.table_planet}</th><th>${tr.table_navamsa_sign}</th></tr></thead>
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
  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  const isHi = currentLanguage === 'hi';
  const rows = chartData.planets.map(p => {
    const color = PLANET_COLORS[p.name]||'#1a1a2e';
    const retro = p.retrograde && p.name!=='Rahu' && p.name!=='Ketu' ? '<span class="badge badge-retro">R</span>' : '';
    const dc = p.dignity==='exalted'?'badge-exalted':p.dignity==='own_sign'?'badge-own':p.dignity==='debilitated'?'badge-debil':'badge-neutral';
    const dl = tr.dignities?.[p.dignity] || (p.dignity==='own_sign'?'Own Sign':p.dignity.charAt(0).toUpperCase()+p.dignity.slice(1));
    const pName = isHi ? (PLANETS_HI[p.name] || p.vedic_name || p.name) : (p.vedic_name || p.name);
    const signDisplay = isHi
      ? localizeSign(p.sign)
      : `${p.sign} <span style="color:#8e8e9e;font-size:0.78rem">(${p.sign_english})</span>`;
    const navSign = p.navamsa?.sign ? (isHi ? localizeSign(p.navamsa.sign) : p.navamsa.sign) : '-';
    const nakDisplay = isHi ? localizeNakshatra(p.nakshatra?.name) : (p.nakshatra?.name || '-');

    return `<tr>
      <td><span style="color:${color};font-weight:600;margin-right:6px">${p.symbol}</span>${pName}${retro}</td>
      <td>${signDisplay}</td>
      <td style="font-weight:500">${p.house}</td><td>${p.degree_in_sign}°</td>
      <td>${nakDisplay}</td><td>${p.nakshatra?.pada||'-'}</td>
      <td><span class="badge ${dc}">${dl}</span></td><td>${navSign}</td>
    </tr>`;
  }).join('');
  return `<div class="card"><div class="card-title">${isHi ? 'ग्रह स्थिति एवं बल' : 'Planetary Positions'}</div>
    <div class="table-wrap"><table class="data-table">
      <thead><tr><th>${tr.table_planet}</th><th>${tr.table_sign}</th><th>${tr.table_house}</th><th>${tr.table_degree}</th><th>${tr.table_nakshatra}</th><th>${tr.table_pada}</th><th>${tr.table_dignity}</th><th>${isHi ? 'नवांश' : 'Navamsa'}</th></tr></thead>
      <tbody>${rows}</tbody></table></div></div>`;
}

// ── Dasha Tab ──

function renderDashaTab() {
  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  const isHi = currentLanguage === 'hi';
  const dashas=chartData.dashas, now=new Date().toISOString().slice(0,10);
  const currentIdx=dashas.findIndex(d=>d.start<=now&&d.end>=now);
  const totalYears=dashas.reduce((s,d)=>s+d.years,0);

  const bar = dashas.map((d,i) => {
    const w=Math.max((d.years/totalYears)*100,1.5);
    const lordLabel = isHi ? localizeDashaLord(d.lord) : d.lord;
    return `<div class="dasha-seg ${i===currentIdx?'current':''}" style="width:${w}%;background:${DASHA_COLORS[d.lord]}"
      title="${lordLabel} — ${d.start} to ${d.end}" onclick="toggleDasha(${i})">${w>5?lordLabel.slice(0,2):''}</div>`;
  }).join('');

  const nowBadge = isHi ? '● वर्तमान' : '● NOW';
  const yUnit = isHi ? 'वर्ष' : 'y';
  const legend = dashas.map((d,i) => {
    const curr=i===currentIdx?`<span class="dasha-current-badge">${nowBadge}</span>`:'';
    const lordLabel = isHi ? localizeDashaLord(d.lord) : d.lord;
    return `<span onclick="toggleDasha(${i})" style="opacity:${selectedDasha!==null&&selectedDasha!==i?0.4:1}">
      <span class="dot" style="background:${DASHA_COLORS[d.lord]}"></span>${lordLabel} (${d.years.toFixed(1)}${yUnit})${curr}</span>`;
  }).join('');

  const rows = dashas.map((d,i) => {
    const status = i===currentIdx?`<span style="color:#b8860b;font-weight:600">${tr.dasha_active}</span>`
      :d.end<now?`<span style="color:#8e8e9e">${tr.dasha_completed}</span>`:`<span style="color:#555566">${tr.dasha_upcoming}</span>`;
    const lordLabel = isHi ? localizeDashaLord(d.lord) : d.lord;
    const totalYText = isHi ? `${d.total_years} वर्ष कुल` : `${d.total_years}y total`;
    return `<tr style="cursor:pointer;${selectedDasha===i?'background:#f0ede6':''}" onclick="toggleDasha(${i})">
      <td><span style="color:${DASHA_COLORS[d.lord]};font-weight:600;margin-right:6px">●</span>${lordLabel}
        <span style="color:#8e8e9e;font-size:0.78rem;margin-left:4px">(${totalYText})</span></td>
      <td>${d.years.toFixed(2)}</td><td>${d.start}</td><td>${d.end}</td><td>${status}</td></tr>`;
  }).join('');

  let antarPanel='';
  if (selectedDasha!==null && dashas[selectedDasha]?.antardashas) {
    const md=dashas[selectedDasha];
    const mdLordLabel = isHi ? localizeDashaLord(md.lord) : md.lord;
    const activeAntar = isHi ? '● सक्रिय' : '● ACTIVE';
    const aRows=md.antardashas.map(a => {
      const isActive=a.start<=now&&a.end>=now;
      const ab=isActive?`<span style="color:#b8860b;margin-left:8px;font-size:0.72rem">${activeAntar}</span>`:'';
      const aLordLabel = isHi ? localizeDashaLord(a.lord) : a.lord;
      return `<tr><td><span style="color:${DASHA_COLORS[a.lord]};font-weight:600;margin-right:4px">●</span>${aLordLabel}${ab}</td>
        <td>${a.years.toFixed(2)}</td><td>${a.start}</td><td>${a.end}</td></tr>`;
    }).join('');
    antarPanel=`<div class="antar-panel"><h4>${typeof tr.dasha_antar_title === 'function' ? tr.dasha_antar_title(mdLordLabel) : `${mdLordLabel} Mahadasha — Antardasha Periods`}</h4>
      <div class="table-wrap"><table class="data-table">
        <thead><tr><th>${tr.dasha_antar_lord}</th><th>${tr.dasha_duration}</th><th>${tr.dasha_start}</th><th>${tr.dasha_end}</th></tr></thead>
        <tbody>${aRows}</tbody></table></div></div>`;
  }

  return `<div class="card"><div class="card-title">${tr.dasha_title}</div>
    <p style="color:#555566;font-size:0.82rem;margin-bottom:16px">${tr.dasha_hint}</p>
    <div class="dasha-bar">${bar}</div><div class="dasha-legend">${legend}</div>
    <div class="table-wrap"><table class="data-table">
      <thead><tr><th>${tr.dasha_mahadasha}</th><th>${tr.dasha_period}</th><th>${tr.dasha_start}</th><th>${tr.dasha_end}</th><th>${tr.dasha_status}</th></tr></thead>
      <tbody>${rows}</tbody></table></div>${antarPanel}</div>`;
}

function toggleDasha(idx) { selectedDasha=selectedDasha===idx?null:idx; renderTabContent(); }

// ── Yogas & Doshas ──

function renderYogaDoshaTab() {
  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  const isHi = currentLanguage === 'hi';
  const noYogaText = isHi ? 'कुण्डली में कोई प्रमुख योग उपस्थित नहीं है।' : 'No major yogas detected.';
  const noDoshaText = isHi ? 'कोई प्रमुख दोष उपस्थित नहीं है।' : 'No doshas analyzed.';
  const planetsLabel = isHi ? 'संबंधित ग्रह' : 'Planets';
  const strengthLabel = isHi ? 'प्रभाव' : 'Strength';
  const effectsLabel = isHi ? 'प्रभाव:' : 'Effects:';
  const remediesLabel = isHi ? 'वैदिक उपाय:' : 'Remedies:';

  const yc = chartData.yogas.length===0 ? `<p style="color:#8e8e9e">${noYogaText}</p>`
    : chartData.yogas.map(y => {
      const pList = isHi ? y.planets.map(p => localizePlanet(p)).join(', ') : y.planets.join(', ');
      const yName = isHi && y.name_hi ? y.name_hi : y.name;
      const yType = isHi && y.type_hi ? y.type_hi : y.type;
      const yDesc = isHi && y.description_hi ? y.description_hi : y.description;
      const yStr = isHi && y.strength_hi ? y.strength_hi : y.strength;
      return `<div class="yd-card yoga-card"><h4>${yName}<span class="yd-type">${yType}</span></h4>
      <p>${yDesc}</p><p class="yd-meta">${planetsLabel}: ${pList} &middot; ${strengthLabel}: ${yStr}</p></div>`;
    }).join('');

  const dc = chartData.doshas.length===0 ? `<p style="color:#8e8e9e">${noDoshaText}</p>`
    : chartData.doshas.map(d => {
      const cls=!d.present?'dosha-absent':d.severity==='cancelled'?'dosha-cancelled':'dosha-present';
      const sl=!d.present?(isHi ? '✓ अनुपस्थित' : '✓ Absent')
        :d.severity==='cancelled'?(isHi ? '↩ भंग / निष्फल' : '↩ Cancelled')
        :`● ${isHi ? (d.severity==='high'?'तीव्र प्रभाव':d.severity==='moderate'?'मध्यम प्रभाव':'सामान्य'):d.severity}`;
      const dName = isHi && d.name_hi ? d.name_hi : d.name;
      const dDesc = isHi && d.description_hi ? d.description_hi : d.description;
      const dEff = isHi && d.effects_hi ? d.effects_hi : d.effects;
      const dRem = isHi && d.remedies_hi ? d.remedies_hi : d.remedies;
      const dCan = isHi && d.cancellation_hi ? d.cancellation_hi : d.cancellation;
      const eff=d.present&&dEff?`<p style="margin-top:8px"><strong style="font-size:0.8rem">${effectsLabel}</strong> ${dEff}</p>`:'';
      const can=dCan?`<p class="cancellation">↩ ${dCan}</p>`:'';
      const rem=d.present&&dRem?`<div class="remedies"><strong>${remediesLabel}</strong><ul>${dRem.map(r=>`<li>${r}</li>`).join('')}</ul></div>`:'';
      return `<div class="yd-card ${cls}"><h4>${dName}<span class="yd-type">${sl}</span></h4><p>${dDesc}</p>${eff}${can}${rem}</div>`;
    }).join('');

  return `<div class="yd-grid">
    <div class="card"><div class="card-title"><span style="color:#16a34a">✦</span> ${tr.yoga_title}</div>${yc}</div>
    <div class="card"><div class="card-title"><span style="color:#dc2626">⚠</span> ${tr.dosha_title}</div>${dc}</div></div>`;
}

// ── Reading ──

function renderReadingTab() {
  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  const isHi = currentLanguage === 'hi';
  const r=chartData.basic_reading;
  if (!r) return `<div class="card"><p style="color:#8e8e9e">${isHi ? 'कोई फलादेश उपलब्ध नहीं है।' : 'No reading available.'}</p></div>`;
  const defaultPlanetNote = isHi ? 'विस्तृत विश्लेषण एआई फलादेश में देखें।' : 'Details in AI reading.';
  const ps=(r.planets||[]).map(p=>`<div class="planet-reading"><h4>${p.placement}</h4><p>${p.reading||defaultPlanetNote}</p></div>`).join('');
  const str=(r.key_strengths||[]).length>0?`<div class="reading-section"><h3><span>✦</span> ${tr.reading_sec_strengths}</h3><ul class="reading-list strengths">${r.key_strengths.map(s=>`<li>${s}</li>`).join('')}</ul></div>`:'';
  const ch=(r.key_challenges||[]).length>0?`<div class="reading-section"><h3><span>🔥</span> ${tr.reading_sec_challenges}</h3><ul class="reading-list challenges">${r.key_challenges.map(c=>`<li>${c}</li>`).join('')}</ul></div>`:'';
  return `<div class="card"><div class="card-title">${tr.reading_title}</div>
    <div class="reading-section"><h3><span>🌅</span> ${tr.reading_sec_personality}</h3><p>${r.personality||''}</p></div>
    <div class="reading-section"><h3><span>🪐</span> ${tr.reading_sec_planets}</h3>${ps}</div>
    ${r.career?`<div class="reading-section"><h3><span>💼</span> ${tr.reading_sec_career}</h3><p>${r.career}</p></div>`:''}
    ${r.relationships?`<div class="reading-section"><h3><span>💑</span> ${tr.reading_sec_relationships}</h3><p>${r.relationships}</p></div>`:''}
    ${str}${ch}
    ${r.summary?`<div class="reading-section"><h3><span>📋</span> ${tr.reading_sec_summary}</h3><p>${r.summary}</p></div>`:''}</div>`;
}

// ── AI Reading ──

function renderAITab() {
  const tr = TRANSLATIONS[currentLanguage] || TRANSLATIONS.en;
  const isHi = currentLanguage === 'hi';
  if (aiLoading) return `<div class="card loading-box" style="padding:50px 24px">
    <div class="orbit-spinner"><div class="orbit"></div><div class="orbit"></div><div class="orbit"></div></div>
    <p class="loading-title">${tr.ai_loading_title}</p>
    <p class="loading-sub">${tr.ai_loading_sub}</p></div>`;
  if (!aiReading) return `<div class="card ai-prompt"><h3>${tr.ai_title}</h3>
    <p>${tr.ai_desc}</p>
    <button class="btn btn-primary" onclick="handleAIGenerate()"><span>${tr.ai_btn}</span><span class="btn-icon">→</span></button>
    <p class="hint">${tr.ai_hint}</p></div>`;
  if (aiReading.error) return `<div class="card">
    <div class="card-title">${tr.ai_title}</div>
    <div class="error-box" style="border:none;margin:0 0 16px 0"><p>${esc(aiReading.error)}</p></div>
    <button class="btn btn-primary" onclick="handleAIGenerate()"><span>${tr.ai_try_again}</span><span class="btn-icon">→</span></button>
  </div>`;
  const sections=aiReading.sections||{};
  let content='';
  if (Object.keys(sections).length>0) {
    content=Object.entries(sections).map(([k,t])=>{
      if(!t||t.trim().length<10) return '';
      const localizedTitle = tr.ai_sections?.[k] || k.replace(/_/g,' ').replace(/and/g,'&').replace(/\b\w/g,c=>c.toUpperCase());
      return `<div class="ai-section"><h3>${localizedTitle}</h3>${formatAIContent(t)}</div>`;
    }).join('');
  } else if (aiReading.full_text) { content=`<div class="ai-section">${formatAIContent(aiReading.full_text)}</div>`; }
  return `<div class="card"><div class="card-title">${tr.ai_title}</div>${content||`<p style="color:#8e8e9e">${isHi ? 'कोई सामग्री उपलब्ध नहीं है।' : 'No content.'}</p>`}
    <div style="margin-top:24px;padding-top:16px;border-top:1px solid #e8e4de">
      <button class="btn btn-ghost" onclick="handleAIGenerate()">${tr.ai_regenerate}</button></div></div>`;
}

// ── Helpers ──
function esc(str) { const d=document.createElement('div'); d.textContent=str; return d.innerHTML; }

function formatAIContent(rawText) {
  if (!rawText) return '';

  let text = rawText.replace(/\r\n/g, '\n');

  // Split standalone inline bullets (e.g. "Title:** * Sub" or "text. * **Sub:**")
  // Must require whitespace before AND after bullet marker so bold markdown (**) is never broken
  text = text.replace(/\s+[\*\-•]\s+/g, '\n* ');

  const lines = text.split('\n');
  const htmlBlocks = [];
  let currentBullets = [];

  function flushBullets() {
    if (currentBullets.length > 0) {
      htmlBlocks.push(`<ul class="ai-bullet-list">${currentBullets.map(it => `<li>${formatInline(it)}</li>`).join('')}</ul>`);
      currentBullets = [];
    }
  }

  function formatInline(str) {
    if (!str) return '';
    let s = str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Triple asterisks: ***bold italic***
    s = s.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    // Bold: **text**
    s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic: *text* or _text_
    s = s.replace(/(^|[^*])\*([^*\n]+?)\*([^*]|$)/g, '$1<em>$2</em>$3');
    s = s.replace(/(^|[^_])_([^_]+?)_([^_]|$)/g, '$1<em>$2</em>$3');
    // Strip any remaining asterisks (unmatched **, stray *, etc.) so none ever show
    s = s.replace(/\*/g, '');
    return s.trim();
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) {
      flushBullets();
      continue;
    }

    // Subheadings: ##, ###, ####
    const hMatch = line.match(/^#{2,4}\s+(.+)$/);
    if (hMatch) {
      flushBullets();
      htmlBlocks.push(`<h4 class="ai-subheading">${formatInline(hMatch[1])}</h4>`);
      continue;
    }

    // Bullet item: * or - or •
    const bulletMatch = line.match(/^[\*\-•]\s+(.+)$/);
    if (bulletMatch) {
      currentBullets.push(bulletMatch[1]);
      continue;
    }

    // Non-bullet line: flush collected bullets first
    flushBullets();

    // Numbered item: e.g. "1. **Title:** text"
    const numMatch = line.match(/^(\d+)[\.\)]\s+(.+)$/);
    if (numMatch) {
      const num = numMatch[1];
      const rest = numMatch[2];
      htmlBlocks.push(`
        <div class="ai-numbered-item">
          <span class="ai-num-badge">${num}</span>
          <div class="ai-item-body">${formatInline(rest)}</div>
        </div>
      `);
      continue;
    }

    // Sign-off / closing remarks
    if (/^(with deepest regards|with warm regards|warm regards|namaste|blessings)/i.test(line)) {
      htmlBlocks.push(`<p class="ai-signoff">${formatInline(line)}</p>`);
      continue;
    }

    // Normal paragraph
    htmlBlocks.push(`<p class="ai-paragraph">${formatInline(line)}</p>`);
  }

  flushBullets();
  return htmlBlocks.join('');
}

// ── City Autocomplete ──

function initCityAutocomplete() {
  const inp = $('#inp-city');
  const dropdown = $('#city-dropdown');
  const statusIcon = $('#city-status-icon');
  const hint = $('#city-hint');

  if (!inp || !dropdown) return;

  inp.addEventListener('input', (e) => {
    const val = e.target.value.trim();
    selectedCity = null;
    const latInp = $('#inp-city-lat');
    if (latInp) latInp.value = '';
    const lonInp = $('#inp-city-lon');
    if (lonInp) lonInp.value = '';

    statusIcon.className = 'city-status-icon';
    statusIcon.innerHTML = '';
    inp.classList.remove('field-error');
    if (hint) {
      hint.textContent = 'Select your Indian birth city from the dropdown list.';
      hint.style.color = '';
    }

    clearTimeout(cityDebounceTimer);
    if (val.length < 2) {
      dropdown.innerHTML = '';
      hide(dropdown);
      currentCityResults = [];
      activeCityIndex = -1;
      return;
    }

    statusIcon.className = 'city-status-icon loading';
    cityDebounceTimer = setTimeout(async () => {
      try {
        const cacheKey = val.toLowerCase();
        const cached = citySearchCache.get(cacheKey);
        if (cached && (Date.now() - cached.timestamp < CACHE_TTL_MS)) {
          currentCityResults = cached.data;
          renderCityDropdown(currentCityResults);
          return;
        }

        const res = await fetch(`/api/cities?q=${encodeURIComponent(val)}`);
        if (!res.ok) throw new Error();
        const data = await res.json();
        currentCityResults = data.cities || [];
        citySearchCache.set(cacheKey, { timestamp: Date.now(), data: currentCityResults });
        renderCityDropdown(currentCityResults);
      } catch (err) {
        currentCityResults = [];
        renderCityDropdown([]);
      } finally {
        if (!selectedCity) {
          statusIcon.className = 'city-status-icon';
        }
      }
    }, 180);
  });

  inp.addEventListener('keydown', (e) => {
    if (dropdown.classList.contains('hidden') || currentCityResults.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      activeCityIndex = (activeCityIndex + 1) % currentCityResults.length;
      updateDropdownHighlight();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      activeCityIndex = (activeCityIndex - 1 + currentCityResults.length) % currentCityResults.length;
      updateDropdownHighlight();
    } else if (e.key === 'Enter') {
      if (activeCityIndex >= 0 && activeCityIndex < currentCityResults.length) {
        e.preventDefault();
        selectCity(currentCityResults[activeCityIndex]);
      }
    } else if (e.key === 'Escape') {
      hide(dropdown);
    }
  });

  document.addEventListener('click', (e) => {
    if (!inp.contains(e.target) && !dropdown.contains(e.target)) {
      hide(dropdown);
      if (inp.value.trim() && !selectedCity) {
        const exact = currentCityResults.find(
          c => c.name.toLowerCase() === inp.value.trim().toLowerCase() ||
               c.display.toLowerCase() === inp.value.trim().toLowerCase()
        );
        if (exact) {
          selectCity(exact);
        } else {
          inp.classList.add('field-error');
          if (hint) {
            hint.textContent = currentLanguage === 'hi' ? '⚠ कृपया सूची में से अपने जन्म शहर का चयन करें।' : '⚠ Please select an Indian city from the dropdown list.';
            hint.style.color = '#dc2626';
          }
        }
      }
    }
  });
}

function renderCityDropdown(cities) {
  const dropdown = $('#city-dropdown');
  activeCityIndex = -1;
  if (!cities || cities.length === 0) {
    const noCityMsg = currentLanguage === 'hi' ? 'कोई भारतीय शहर नहीं मिला। कृपया वर्तनी जांचें या निकटतम शहर दर्ज करें।' : 'No Indian cities found. Check spelling or enter a nearby city.';
    dropdown.innerHTML = `<div class="city-item no-results">${noCityMsg}</div>`;
    show(dropdown);
    return;
  }

  const selectBtnText = currentLanguage === 'hi' ? 'चयन करें ↵' : 'Select ↵';
  dropdown.innerHTML = cities.map((c, i) => `
    <div class="city-item" data-index="${i}" onclick="window.handleCitySelect(${i})">
      <div>
        <strong>${esc(c.name)}</strong>
        <span class="city-sub">${esc(c.display.replace(c.name + ', ', ''))}</span>
      </div>
      <span style="font-size:0.75rem;color:#8e8e9e">${selectBtnText}</span>
    </div>
  `).join('');
  show(dropdown);
}

function updateDropdownHighlight() {
  const items = $$('#city-dropdown .city-item');
  items.forEach((item, i) => {
    if (i === activeCityIndex) {
      item.classList.add('active');
      item.scrollIntoView({ block: 'nearest' });
    } else {
      item.classList.remove('active');
    }
  });
}

window.handleCitySelect = function(index) {
  if (currentCityResults[index]) {
    selectCity(currentCityResults[index]);
  }
};

function selectCity(city) {
  selectedCity = city;
  const inp = $('#inp-city');
  inp.value = city.display;
  inp.classList.remove('field-error');
  const latInp = $('#inp-city-lat');
  if (latInp) latInp.value = city.latitude;
  const lonInp = $('#inp-city-lon');
  if (lonInp) lonInp.value = city.longitude;

  const statusIcon = $('#city-status-icon');
  if (statusIcon) {
    statusIcon.className = 'city-status-icon active';
    statusIcon.innerHTML = '✓';
  }
  const hint = $('#city-hint');
  if (hint) {
    const selPrefix = currentLanguage === 'hi' ? '✓ चयनित:' : '✓ Selected:';
    hint.textContent = `${selPrefix} ${city.display}`;
    hint.style.color = '#16a34a';
  }
  hide($('#city-dropdown'));
}

// ── Startup ──

function initApp() {
  initCityAutocomplete();
  const cached = loadSessionFromCache();
  if (!cached) {
    handleLanguageChange(currentLanguage, false);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
