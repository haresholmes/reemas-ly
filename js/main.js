/**
 * AL REEMAS CENTER — Advanced Luxury Experience & Interactive Trading Engine
 * Live Bullion Rates, Wholesale Calculator, 3D Bullion Inspector, Bilingual Engine
 */

(function () {
  'use strict';

  // --- Base Market Benchmarks (Simulated Tripoli & London Spot Fix) ---
  const MARKET = {
    goldOunceUsd: 2625.50,
    usdLydRate: 4.88,
    karats: {
      "24k": { purity: 0.9999, nameAr: "سبائك عيار 24", nameEn: "24K Pure Bullion", hallmark: "999.9" },
      "22k": { purity: 0.9166, nameAr: "مشغولات عيار 22", nameEn: "22K Gulf Jewelry", hallmark: "916" },
      "21k": { purity: 0.8750, nameAr: "مشغولات عيار 21", nameEn: "21K Libyan Market", hallmark: "875" },
      "18k": { purity: 0.7500, nameAr: "مجوهرات عيار 18", nameEn: "18K Fine Jewelry", hallmark: "750" }
    }
  };

  // --- Translation Dictionary ---
  const translations = {
    en: {
      "page.title": "Al Reemas Center | Official Gold & Jewelry Importer — Tripoli, Libya",
      "nav.about": "About Us",
      "nav.products": "Bullion & Karats",
      "nav.calculator": "Wholesale Calculator",
      "nav.pipeline": "Import Pipeline",
      "nav.credentials": "Credentials",
      "nav.contact": "Contact",
      "nav.quote": "Request Wholesale Quote",

      "hero.badge": "Official Gold Importer · Tripoli, Libya · Est. 2013",
      "hero.title": "Imported Gold & Pure Bullion for Libya's Goldsmiths",
      "hero.lead": "Al Reemas Center is a licensed wholesale importer connecting local jewellery workshops and gold merchants with accredited international refineries. Guaranteed assayed purity, customs documentation, and registered commercial invoices.",
      "hero.cta_quote": "Request Wholesale Pricing",
      "hero.cta_products": "Inspect 24K Bullion",

      "ticker.live": "Live Global Bullion Spot | Tripoli Market Benchmark",
      "ticker.refresh": "Refresh Spot",
      "ticker.24k": "24K Bullion (999.9)",
      "ticker.22k": "22K Jewelry (916)",
      "ticker.21k": "21K Market (875)",
      "ticker.18k": "18K Fine (750)",

      "cred.cr": "Commercial Registry",
      "cred.lic": "Import License",
      "cred.tax": "Tax Identification",
      "cred.est": "Founded Year",
      "cred.copied": "Copied!",

      "showcase.label": "Refinery Minted Bullion",
      "showcase.title": "Certified Investment Bullion Bars",
      "showcase.subtitle": "LBMA-grade assayed bullion imported directly from top-tier Swiss and international refineries.",
      "bar.weight_1000": "1000g (1 kg)",
      "bar.weight_100": "100g Minted",
      "bar.weight_oz": "1 Ounce (31.1g)",

      "calc.label": "Wholesale Estimator",
      "calc.title": "Interactive Order & Volume Calculator",
      "calc.subtitle": "Calculate gold content and estimated wholesale spot volume for your jewelry shop orders.",
      "calc.select_karat": "Select Gold Karat",
      "calc.select_weight": "Order Weight (Grams)",
      "calc.pure_content": "Pure Gold Content (Fine Gold)",
      "calc.fineness": "Assayed Hallmark Fineness",
      "calc.est_lyd": "Estimated Value (LYD)",
      "calc.est_usd": "Estimated Value (USD)",
      "calc.order_btn": "Order this Batch via WhatsApp",

      "pipe.label": "Supply Chain Security",
      "pipe.title": "From Global Refineries to Tripoli",
      "pipe.subtitle": "A fully insured, legally compliant import pipeline handled by our registered team.",
      "pipe.s1_t": "Direct Refinery Acquisition",
      "pipe.s1_d": "Contracted directly with LBMA-audited refineries at spot market rates.",
      "pipe.s2_t": "Insured High-Security Transit",
      "pipe.s2_d": "Armored transit and specialized air cargo fully insured to Tripoli International Airport.",
      "pipe.s3_t": "Official Customs Clearance",
      "pipe.s3_d": "Regulatory compliance, commercial registry verification, and statutory tax payment.",
      "pipe.s4_t": "Assay Testing & Delivery",
      "pipe.s4_d": "Batch assay verification in Tripoli and handover with formal registered tax invoices.",

      "contact.label": "Trading Inquiries",
      "contact.title": "Request Today's Quote or Schedule a Visit",
      "contact.info_title": "Direct B2B Desk",
      "contact.info_desc": "Our Tripoli wholesale desk welcomes gold merchants, workshop owners, and jewelry retailers.",
      "contact.addr_label": "Headquarters",
      "contact.addr_val": "Tripoli, Libya",
      "contact.hours_label": "Trading Hours",
      "contact.hours_val": "Saturday – Thursday: 9:00 AM – 6:00 PM",
      "contact.phone_label": "Wholesale Desk",
      "contact.phone_val": "+218 (0) 91 000 0000",
      "contact.email_label": "Official Email",
      "contact.email_val": "orders@alreemas-center.ly",

      "form.name_label": "Shop or Merchant Name",
      "form.name_placeholder": "e.g., Al-Baraka Jewelry",
      "form.city_label": "City",
      "form.city_placeholder": "Tripoli, Benghazi, Misrata...",
      "form.phone_label": "Phone / WhatsApp",
      "form.phone_placeholder": "+218 9X XXXXXXX",
      "form.type_label": "Order Category",
      "form.type_opt1": "24K Bullion (999.9)",
      "form.type_opt2": "21K Jewelry (875)",
      "form.type_opt3": "18K Fine Jewelry (750)",
      "form.type_opt4": "Special Import Contract",
      "form.weight_label": "Estimated Weight / Quantity",
      "form.weight_placeholder": "e.g., 500g, 1kg, 50 sets",
      "form.msg_label": "Special Specifications",
      "form.msg_placeholder": "Provide any custom requirements...",
      "form.submit": "Submit Wholesale Request",
      "form.success_msg": "Thank you! Your wholesale inquiry has been submitted. Our commercial representative will contact you immediately.",

      "assets.label": "Official Brand Assets",
      "assets.title": "Corporate Medallion & Official Seal Package",
      "assets.subtitle": "Download vector SVGs and ultra-high-resolution transparent PNG files for print, stamps, and invoices.",
      "asset.seal_badge": "Imperial Medallion Seal (Dark)",
      "asset.seal_duo": "Official Seal (Navy & Gold)",
      "asset.seal_gold": "Official Seal (Royal Gold)",
      "asset.logo_prim": "Circular Brand Logo",
      "asset.download_svg": "Download SVG",
      "asset.download_png": "Download 2K PNG",

      "foot.desc": "Al Reemas Center for Gold & Jewelry Import is a registered Libyan wholesale company operating in Tripoli under Commercial Registry 45069.",
      "foot.quick_links": "Quick Links",
      "foot.legal": "Legal Credentials",
      "foot.copy": "© 2013–2026 Al Reemas Center for Gold & Jewelry Import. All Rights Reserved."
    }
  };

  // --- Element Caches ---
  const htmlEl = document.documentElement;
  const langBtn = document.getElementById('langToggle');
  const themeBtn = document.getElementById('themeToggle');
  const navToggle = document.getElementById('navToggle');
  const mainNav = document.getElementById('mainNav');
  const quoteForm = document.getElementById('quoteForm');
  const formFeedback = document.getElementById('formFeedback');

  // Cache initial Arabic texts
  const arabicDictionary = {};
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    arabicDictionary[el.getAttribute('data-i18n')] = el.innerHTML;
  });

  const arabicPlaceholders = {};
  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    arabicPlaceholders[el.getAttribute('data-i18n-placeholder')] = el.getAttribute('placeholder');
  });

  // --- Language Switching Engine ---
  function setLanguage(lang) {
    const isEn = lang === 'en';
    htmlEl.lang = isEn ? 'en' : 'ar';
    htmlEl.dir = isEn ? 'ltr' : 'rtl';

    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      if (isEn && translations.en[key]) {
        el.innerHTML = translations.en[key];
      } else if (!isEn && arabicDictionary[key]) {
        el.innerHTML = arabicDictionary[key];
      }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
      const key = el.getAttribute('data-i18n-placeholder');
      if (isEn && translations.en[key]) {
        el.setAttribute('placeholder', translations.en[key]);
      } else if (!isEn && arabicPlaceholders[key]) {
        el.setAttribute('placeholder', arabicPlaceholders[key]);
      }
    });

    document.title = isEn ? translations.en["page.title"] : "مركز الريماس | لاستيراد الذهب والمجوهرات — طرابلس، ليبيا";

    if (langBtn) {
      langBtn.innerHTML = isEn 
        ? '<span class="lang-text">العربية</span> <span style="font-size:0.8rem">🇱🇾</span>' 
        : '<span class="lang-text">English</span> <span style="font-size:0.8rem">🌐</span>';
    }

    try {
      localStorage.setItem('reemas_lang', lang);
    } catch (e) {}
    
    updateCalculator();
  }

  if (langBtn) {
    langBtn.addEventListener('click', () => {
      setLanguage(htmlEl.lang === 'en' ? 'ar' : 'en');
    });
  }

  // Restore saved language
  try {
    if (localStorage.getItem('reemas_lang') === 'en') {
      setLanguage('en');
    }
  } catch (e) {}

  // --- Theme Toggle Engine (Imperial Dark / Ivory Light) ---
  function setTheme(theme) {
    htmlEl.setAttribute('data-theme', theme);
    if (themeBtn) {
      themeBtn.innerHTML = theme === 'light' 
        ? '<span>🌙</span> <span class="theme-label">' + (htmlEl.lang === 'en' ? 'Dark Luxury' : 'الوضع الملكي') + '</span>'
        : '<span>☀️</span> <span class="theme-label">' + (htmlEl.lang === 'en' ? 'Ivory Light' : 'الوضع الفاتح') + '</span>';
    }
    try {
      localStorage.setItem('reemas_theme', theme);
    } catch (e) {}
  }

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = htmlEl.getAttribute('data-theme') || 'dark';
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  try {
    const savedTheme = localStorage.getItem('reemas_theme');
    if (savedTheme) setTheme(savedTheme);
  } catch (e) {}

  // --- Mobile Menu Toggle ---
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', () => {
      mainNav.classList.toggle('open');
    });
    mainNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => mainNav.classList.remove('open'));
    });
  }

  // --- Live Gold Spot Ticker Simulator ---
  function updateGoldSpot(jitter = false) {
    if (jitter) {
      // Simulate realistic slight spot market fluctuation (±0.25%)
      const delta = (Math.random() - 0.48) * 4.5;
      MARKET.goldOunceUsd = Math.max(2580, Math.min(2680, MARKET.goldOunceUsd + delta));
    }

    const gram24Usd = MARKET.goldOunceUsd / 31.1034768;

    Object.keys(MARKET.karats).forEach((k) => {
      const data = MARKET.karats[k];
      const usdPrice = gram24Usd * data.purity;
      const lydPrice = usdPrice * MARKET.usdLydRate;

      const lydEl = document.getElementById(`price-lyd-${k}`);
      const usdEl = document.getElementById(`price-usd-${k}`);

      if (lydEl) lydEl.innerText = `${lydPrice.toFixed(2)} LYD`;
      if (usdEl) usdEl.innerText = `$${usdPrice.toFixed(2)} / g`;
    });
  }

  updateGoldSpot(false);

  const refreshBtn = document.getElementById('refreshSpotBtn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      refreshBtn.style.transform = 'rotate(180deg)';
      setTimeout(() => { refreshBtn.style.transform = 'none'; }, 400);
      updateGoldSpot(true);
      updateCalculator();
    });
  }

  // --- Interactive Wholesale Order Calculator ---
  let selectedKarat = '24k';
  let orderGrams = 500;

  const karatButtons = document.querySelectorAll('.calc-radio-btn');
  const weightInput = document.getElementById('calcWeight');
  const weightSlider = document.getElementById('calcWeightSlider');
  const pureContentEl = document.getElementById('calcPureContent');
  const finenessEl = document.getElementById('calcFineness');
  const estLydEl = document.getElementById('calcEstLyd');
  const estUsdEl = document.getElementById('calcEstUsd');
  const whatsappBtn = document.getElementById('calcWhatsappBtn');

  function updateCalculator() {
    const kData = MARKET.karats[selectedKarat];
    const pureGrams = orderGrams * kData.purity;
    const gram24Usd = MARKET.goldOunceUsd / 31.1034768;
    const usdPrice = gram24Usd * kData.purity;
    const totalUsd = usdPrice * orderGrams;
    const totalLyd = totalUsd * MARKET.usdLydRate;

    if (pureContentEl) pureContentEl.innerText = `${pureGrams.toFixed(1)} g`;
    if (finenessEl) finenessEl.innerText = `${kData.hallmark} (${(kData.purity * 100).toFixed(1)}%)`;
    if (estLydEl) estLydEl.innerText = `${totalLyd.toLocaleString('en-US', { maximumFractionDigits: 0 })} LYD`;
    if (estUsdEl) estUsdEl.innerText = `$${totalUsd.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;

    if (whatsappBtn) {
      const isEn = htmlEl.lang === 'en';
      const msg = isEn
        ? `Hello Al Reemas Center, I would like to request an official wholesale invoice quote for ${orderGrams}g of ${kData.nameEn} (${kData.hallmark}).`
        : `السلام عليكم مركز الريماس، أرغب في طلب عرض أسعار رسمي لشحنة جملة: ${orderGrams} جرام من ${kData.nameAr} (دمغة ${kData.hallmark}).`;
      whatsappBtn.href = `https://wa.me/218910000000?text=${encodeURIComponent(msg)}`;
    }
  }

  karatButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      karatButtons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      selectedKarat = btn.getAttribute('data-karat');
      updateCalculator();
    });
  });

  if (weightInput) {
    weightInput.addEventListener('input', (e) => {
      orderGrams = Math.max(10, Math.min(10000, Number(e.target.value) || 10));
      if (weightSlider) weightSlider.value = orderGrams;
      updateCalculator();
    });
  }

  if (weightSlider) {
    weightSlider.addEventListener('input', (e) => {
      orderGrams = Number(e.target.value);
      if (weightInput) weightInput.value = orderGrams;
      updateCalculator();
    });
  }

  updateCalculator();

  // --- 3D Bullion Bar Weight Switcher ---
  const barWeightPills = document.querySelectorAll('.bar-weight-pill');
  const barWeightDisplay = document.getElementById('barWeightDisplay');
  const barSerialDisplay = document.getElementById('barSerialDisplay');

  barWeightPills.forEach((pill) => {
    pill.addEventListener('click', () => {
      barWeightPills.forEach((p) => p.classList.remove('active'));
      pill.classList.add('active');
      const w = pill.getAttribute('data-weight');
      if (barWeightDisplay) barWeightDisplay.innerText = w;
      if (barSerialDisplay) {
        barSerialDisplay.innerText = w.includes('1000') ? 'AR-2013-45069' : (w.includes('100') ? 'AR-2013-10088' : 'AR-2013-OZ99');
      }
    });
  });

  // --- Copy to Clipboard on Credential Cards ---
  document.querySelectorAll('.credential-item').forEach((item) => {
    item.addEventListener('click', async () => {
      const val = item.getAttribute('data-copy');
      if (!val) return;

      try {
        await navigator.clipboard.writeText(val);
      } catch (err) {
        const temp = document.createElement('textarea');
        temp.value = val;
        document.body.appendChild(temp);
        temp.select();
        document.execCommand('copy');
        document.body.removeChild(temp);
      }

      const toast = item.querySelector('.copied-toast');
      if (toast) {
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 1800);
      }
    });
  });

  // --- Quote Form Handling ---
  if (quoteForm) {
    quoteForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = quoteForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = htmlEl.lang === 'en' ? 'Registering Order...' : 'جاري تسجيل الطلب...';
      }

      setTimeout(() => {
        if (formFeedback) {
          formFeedback.classList.add('success');
          formFeedback.hidden = false;
        }
        quoteForm.reset();
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerText = htmlEl.lang === 'en' ? 'Submit Wholesale Request' : 'إرسال طلب التسعيرة';
        }
        formFeedback.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 700);
    });
  }
})();
