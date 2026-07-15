# -*- coding: utf-8 -*-
import json
from pathlib import Path

BASE = Path(__file__).parent
productos = json.loads((BASE / "productos.json").read_text(encoding="utf-8"))
divisores = json.loads((BASE / "divisores.json").read_text(encoding="utf-8"))

data_json = json.dumps(productos, ensure_ascii=False)

HTML = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Catálogo — Revisión</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<style>
  :root {
    --cream: #f5f1ea;
    --ink: #17140f;
    --terracotta: #a8492c;
    --muted: #948c7d;
    --line-soft: rgba(23,20,15,.09);
  }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0;
    font-family: "Inter", sans-serif;
    background: var(--cream);
    color: var(--ink);
    -webkit-font-smoothing: antialiased;
  }
  .serif { font-family: "Cormorant Garamond", serif; }

  header.util {
    position: sticky; top: 0; z-index: 30;
    background: rgba(245,241,234,.94); backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--line-soft);
    padding: 20px 40px;
    display: flex; align-items: center; gap: 24px;
  }
  header.util .label {
    font-family: "Cormorant Garamond", serif; font-style: italic; font-weight: 500;
    font-size: 22px; letter-spacing: .01em; color: var(--ink);
    cursor: pointer;
  }
  header.util .stats {
    margin-left: auto; font-size: 11px; color: var(--muted);
    display: flex; align-items: center; gap: 18px; letter-spacing: .04em;
  }
  header.util .chk {
    display: flex; align-items: center; gap: 6px; cursor: pointer; user-select: none;
  }
  header.util .chk input { accent-color: var(--ink); cursor: pointer; }
  header.util button {
    background: var(--ink); color: var(--cream); border: 1px solid var(--ink);
    font-family: "Inter", sans-serif; padding: 11px 24px; border-radius: 100px; font-size: 11px;
    letter-spacing: .08em; text-transform: uppercase; cursor: pointer;
    transition: all .2s ease;
  }
  header.util button:hover { background: var(--terracotta); border-color: var(--terracotta); }

  nav.catnav {
    position: sticky; top: 65px; z-index: 25;
    background: var(--cream);
    border-bottom: 1px solid var(--line-soft);
    padding: 16px 32px; display: flex; gap: 40px; overflow-x: auto;
    font-size: 11px; letter-spacing: .16em; text-transform: uppercase;
    justify-content: center;
  }
  nav.catnav a {
    color: var(--muted); text-decoration: none; white-space: nowrap; padding-bottom: 4px;
    border-bottom: 1px solid transparent; cursor: pointer; transition: all .2s ease;
  }
  nav.catnav a:hover { color: var(--ink); border-color: var(--terracotta); }

  #homeView.hidden, #categoryView.hidden { display: none; }

  /* ---------- Portada: secciones grandes tipo catálogo (foto + texto encima) ---------- */
  .home-hero {
    max-width: 1440px; margin: 0 auto; padding: 48px 40px 100px;
    display: grid; grid-template-columns: 2fr 1fr; grid-auto-rows: 200px; gap: 20px;
  }
  .home-hero a.hero-tile {
    position: relative; display: block; border-radius: 3px; overflow: hidden; cursor: pointer;
    text-decoration: none; color: #fff; background: #cabfa9;
  }
  .home-hero a.hero-tile.big { grid-row: 1 / span 3; }
  .home-hero a.hero-tile img {
    position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block;
    transition: transform .7s cubic-bezier(.2,.7,.3,1);
  }
  .home-hero a.hero-tile:hover img { transform: scale(1.045); }
  .home-hero a.hero-tile .scrim {
    position: absolute; inset: 0; background: linear-gradient(to top, rgba(15,13,10,.62) 0%, rgba(15,13,10,0) 58%);
  }
  .home-hero a.hero-tile .label {
    position: absolute; left: 26px; bottom: 22px; right: 26px; z-index: 1;
    font-family: "Cormorant Garamond", serif; font-weight: 500; font-style: italic;
    font-size: 24px; letter-spacing: .03em;
  }
  .home-hero a.hero-tile.big .label { font-size: 44px; }
  @media (max-width: 800px) {
    .home-hero { grid-template-columns: 1fr; grid-auto-rows: 240px; }
    .home-hero a.hero-tile.big { grid-row: auto; }
  }

  .homegrid {
    max-width: 1440px; margin: 0 auto; padding: 20px 40px 100px;
    display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 84px 48px;
  }
  .homegrid a.tile { text-decoration: none; color: inherit; display: block; cursor: pointer; }
  .homegrid .tile img {
    width: 100%; height: 300px; object-fit: contain; display: block;
    filter: drop-shadow(0 22px 32px rgba(23,20,15,.13));
    transition: transform .5s cubic-bezier(.2,.7,.3,1);
  }
  .homegrid a.tile:hover img { transform: translateY(-6px); }
  .homegrid .tile .cap { text-align: center; margin-top: 28px; }
  .homegrid .tile .cap .t1 {
    font-family: "Cormorant Garamond", serif; font-weight: 500; font-size: 27px;
    letter-spacing: .08em; text-transform: uppercase;
  }
  .homegrid .tile .cap .t2 {
    font-size: 11px; color: var(--muted); margin-top: 6px; min-height: 14px;
    letter-spacing: .18em; text-transform: uppercase;
  }

  .breadcrumb {
    position: sticky; top: 114px; z-index: 20;
    background: var(--cream); margin: 0 auto; padding: 16px 32px;
    font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted);
    display: flex; align-items: center; gap: 10px; justify-content: center;
    border-bottom: 1px solid var(--line-soft);
  }
  .breadcrumb a { color: var(--muted); text-decoration: none; cursor: pointer; transition: color .15s ease; }
  .breadcrumb a:hover { color: var(--terracotta); }
  .breadcrumb .sep { color: var(--line-soft); }
  .breadcrumb .current { color: var(--ink); }
  .breadcrumb .back-arrow {
    cursor: pointer; color: var(--ink); font-size: 15px; margin-right: 2px;
    transition: transform .15s ease;
  }
  .breadcrumb .back-arrow:hover { transform: translateX(-3px); color: var(--terracotta); }

  #categoryContent { padding: 0 32px 60px; max-width: 1360px; margin: 0 auto; }

  .section-actions {
    max-width: 1360px; margin: 0 auto; padding: 20px 32px 0; display: flex; justify-content: center;
  }
  .section-actions button {
    background: none; color: var(--muted); border: 1px solid var(--line-soft);
    font-family: "Inter", sans-serif; padding: 9px 20px; border-radius: 100px; font-size: 11px;
    letter-spacing: .06em; text-transform: uppercase; cursor: pointer; transition: all .15s ease;
  }
  .section-actions button:hover { background: var(--ink); color: var(--cream); border-color: var(--ink); }

  @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
  .fade-in { animation: fadeIn .4s ease; }

  .pdf-overlay {
    display: none; position: fixed; inset: 0; background: rgba(23,20,15,.9); z-index: 200;
    align-items: center; justify-content: center; flex-direction: column; gap: 18px; color: #fff;
  }
  .pdf-overlay.open { display: flex; }
  .pdf-overlay .pct {
    font-family: "Cormorant Garamond", serif; font-size: 48px; font-weight: 500; letter-spacing: .02em;
  }
  .pdf-overlay .bar-track {
    width: 220px; height: 2px; background: rgba(255,255,255,.2); border-radius: 2px; overflow: hidden;
  }
  .pdf-overlay .bar-fill {
    height: 100%; width: 0%; background: var(--terracotta); transition: width .2s ease;
  }
  .pdf-overlay .txt { font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: rgba(255,255,255,.6); }
  .pdf-overlay .cancel {
    margin-top: 8px; background: none; border: 1px solid rgba(255,255,255,.35); color: #fff;
    font-family: "Inter", sans-serif; padding: 8px 22px; border-radius: 100px; font-size: 11px;
    letter-spacing: .08em; text-transform: uppercase; cursor: pointer; transition: all .15s ease;
  }
  .pdf-overlay .cancel:hover { background: #fff; color: var(--ink); border-color: #fff; }

  .cat-section { padding-top: 64px; }
  .cat-heading { text-align: center; }
  .cat-heading h2 {
    font-family: "Cormorant Garamond", serif; font-weight: 500; font-style: italic;
    font-size: 46px; margin: 0; letter-spacing: .01em;
  }
  .cat-heading .count { font-size: 11px; color: var(--muted); margin-top: 8px; letter-spacing: .16em; text-transform: uppercase; }

  .subcat-heading {
    font-size: 11px; letter-spacing: .22em; text-transform: uppercase; color: var(--terracotta);
    margin: 72px 0 40px; font-weight: 500; text-align: center;
  }

  /* ---------- Grilla principal: mismo tamaño para todas las fotos, recorte centrado parejo ---------- */
  .grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 56px 44px; margin-top: 50px;
  }
  .card { cursor: pointer; }
  .card .frame { aspect-ratio: 3 / 2; overflow: hidden; }
  .card .frame img.photo {
    width: 100%; height: 100%; object-fit: cover; object-position: center;
    display: block; transition: transform .6s cubic-bezier(.2,.7,.3,1);
  }
  .card:hover .frame img.photo { transform: scale(1.04); }
  .card .name {
    font-family: "Cormorant Garamond", serif; font-size: 21px; font-weight: 500;
    text-align: center; margin-top: 20px; letter-spacing: .06em; text-transform: uppercase;
  }

  /* ---------- Modal de detalle: lightbox limpio, sin caja ni marco ---------- */
  .modal-backdrop {
    display: none; position: fixed; inset: 0; background: rgba(23,20,15,.92);
    z-index: 100; padding: 60px 20px; overflow-y: auto;
  }
  .modal-backdrop.open { display: flex; align-items: center; justify-content: center; }
  .modal {
    max-width: 88vw; max-height: 84vh; position: relative;
    display: flex; align-items: center; justify-content: center;
  }
  .modal .close {
    position: fixed; top: 24px; right: 28px; width: 38px; height: 38px; border-radius: 50%;
    background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.25); cursor: pointer;
    display: flex; align-items: center; justify-content: center; font-size: 16px; z-index: 2; color: #fff;
    transition: background .15s ease;
  }
  .modal .close:hover { background: rgba(255,255,255,.18); }
  .modal .m-photo { position: relative; display: flex; align-items: center; justify-content: center; }
  .modal .m-photo img.main { max-width: 88vw; max-height: 84vh; width: auto; height: auto; display: block; box-shadow: 0 30px 80px rgba(0,0,0,.4); }
  .modal .m-photo .stamp {
    position: absolute; top: 16px; left: 16px; width: 32px; height: 32px; border-radius: 50%;
    background: rgba(255,255,255,.9); border: 1px solid var(--line-soft); display: flex;
    align-items: center; justify-content: center; cursor: pointer; font-size: 15px; color: #c9c2b4;
  }
  .modal .m-photo .stamp.on { background: var(--terracotta); color: #fff; border-color: var(--terracotta); }
  .modal .nav-arrow {
    position: fixed; top: 50%; transform: translateY(-50%); width: 46px; height: 46px; border-radius: 50%;
    background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.25); cursor: pointer;
    display: flex; align-items: center; justify-content: center; font-size: 18px; z-index: 2; color: #fff;
    transition: background .15s ease;
  }
  .modal .nav-arrow:hover { background: rgba(255,255,255,.18); }
  .modal .nav-arrow.prev { left: 28px; }
  .modal .nav-arrow.next { right: 28px; }
  .modal .nav-arrow.hidden { display: none; }
  .modal .dots { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; z-index: 2; }
  .modal .dots .dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,.35); cursor: pointer; }
  .modal .dots .dot.on { background: #fff; }
  footer.pagefoot {
    text-align: center; padding: 50px 20px 60px; color: var(--muted); font-size: 10px;
    opacity: .55; max-width: 560px; margin: 0 auto; line-height: 1.6;
  }
  footer.pagefoot .doc-label {
    display: block; font-size: 9px; letter-spacing: .18em; text-transform: uppercase;
    margin-bottom: 8px; color: var(--muted);
  }
</style>
</head>
<body>
<header class="util">
  <span class="label" id="homeLink">Catálogo</span>
  <div class="stats">
    <label class="chk"><input type="checkbox" id="incluirNombres" checked> Incluir nombres</label>
    <button id="downloadPdfBtn">Descargar catálogo (PDF)</button>
  </div>
</header>
<nav class="catnav" id="catnav"></nav>

<div id="homeView">
  <div class="home-hero" id="homeHero"></div>
</div>

<div id="categoryView" class="hidden">
  <div class="breadcrumb" id="breadcrumb"></div>
  <div class="section-actions"><button id="downloadSectionPdfBtn">Descargar esta sección (PDF)</button></div>
  <div id="categoryContent"></div>
</div>

<footer class="pagefoot">
  <span class="doc-label">Documentación</span>
  Las imágenes son representaciones ilustrativas de cada modelo. Colores, texturas y medidas
  pueden presentar variaciones respecto del producto fabricado.
</footer>

<div class="modal-backdrop" id="modalBackdrop">
  <div class="nav-arrow prev hidden" id="mPrev">‹</div>
  <div class="modal" id="modal">
    <div class="close" id="modalClose">✕</div>
    <div class="m-photo">
      <img class="main" id="mPhoto">
      <div class="stamp" id="mStamp" title="Marcar como aprobado">✓</div>
    </div>
  </div>
  <div class="nav-arrow next hidden" id="mNext">›</div>
  <div class="dots" id="mDots"></div>
</div>

<div class="pdf-overlay" id="pdfOverlay">
  <div class="pct" id="pdfPct">0%</div>
  <div class="bar-track"><div class="bar-fill" id="pdfBarFill"></div></div>
  <div class="txt" id="pdfOverlayText">Generando catálogo en PDF</div>
  <button class="cancel" id="pdfCancelBtn">Cancelar</button>
</div>

<script>
const productos = __DATA__;

function slugify(s) {
  return (s || "")
    .normalize("NFKD").replace(/[\\u0300-\\u036f]/g, "")
    .toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}
function titleCase(s) {
  return (s || "").toLowerCase().replace(/(^|\\s)\\S/g, c => c.toUpperCase());
}

const homeHero = document.getElementById("homeHero");
const catnav = document.getElementById("catnav");
const homeView = document.getElementById("homeView");
const categoryView = document.getElementById("categoryView");
const categoryContent = document.getElementById("categoryContent");

// ---- Secciones grandes del catálogo (agrupan una o más categorías) ----
const SECCIONES = [
  { id: "sofas", nombre: "Sofás", categorias: ["SOFÁS"], grande: true },
  { id: "sillas-banquetas", nombre: "Sillas y Banquetas", categorias: ["SILLAS", "BANQUETAS"], grande: false },
  { id: "complementos", nombre: "Complementos", categorias: ["COMPLEMENTOS"], grande: false },
  { id: "respaldos", nombre: "Respaldos", categorias: ["RESPALDOS"], grande: false },
];

const grupos = [];
const idx = new Map();
productos.forEach(p => {
  const key = p.categoria + "||" + p.subcategoria;
  if (!idx.has(key)) {
    idx.set(key, { categoria: p.categoria, subcategoria: p.subcategoria, items: [] });
    grupos.push(idx.get(key));
  }
  idx.get(key).items.push(p);
});

const state = {};
let activeCardId = null;
let currentCategoryItems = [];

function groupSlug(categoria, subcategoria) {
  return slugify(categoria) + (subcategoria ? "-" + slugify(subcategoria) : "");
}

function seccionItems(sec) {
  return productos.filter(p => sec.categorias.includes(p.categoria));
}

function seccionSubtiles(sec) {
  const seen = new Set();
  const tiles = [];
  seccionItems(sec).forEach(p => {
    const key = p.categoria + "||" + p.subcategoria;
    if (seen.has(key)) return;
    seen.add(key);
    tiles.push({ categoria: p.categoria, subcategoria: p.subcategoria });
  });
  return tiles;
}

function seccionEsFlat(sec) {
  const tiles = seccionSubtiles(sec);
  return tiles.length <= 1;
}

function findSeccionForCategoria(categoria) {
  return SECCIONES.find(s => s.categorias.includes(categoria)) || null;
}

// ---- Portada: una tile grande + tiles chicas, con texto sobre la foto ----
SECCIONES.forEach(sec => {
  const items = seccionItems(sec);
  if (!items.length) return;
  const rep = items[0];
  const a = document.createElement("a");
  a.className = "hero-tile" + (sec.grande ? " big" : "");
  a.innerHTML = `
    <img src="${rep.foto_ambientacion}" loading="lazy" alt="${sec.nombre}">
    <div class="scrim"></div>
    <div class="label">${sec.nombre}</div>
  `;
  a.addEventListener("click", (e) => { e.preventDefault(); enterSeccion(sec); });
  homeHero.appendChild(a);
});

// ---- Nav superior: una por sección ----
SECCIONES.forEach(sec => {
  const a = document.createElement("a");
  a.textContent = sec.nombre;
  a.addEventListener("click", () => enterSeccion(sec));
  catnav.appendChild(a);
});

function goHome(pushHistory = true) {
  categoryView.classList.add("hidden");
  homeView.classList.remove("hidden");
  homeView.classList.remove("fade-in"); void homeView.offsetWidth; homeView.classList.add("fade-in");
  window.scrollTo(0, 0);
  if (pushHistory) history.pushState({ home: true }, "", location.pathname);
}
document.getElementById("homeLink").addEventListener("click", () => goHome());

function renderBreadcrumb(sec, categoria, subcategoria) {
  const bc = document.getElementById("breadcrumb");
  bc.innerHTML = "";

  const back = document.createElement("span");
  back.className = "back-arrow";
  back.textContent = "←";
  back.title = "Volver";
  back.addEventListener("click", () => {
    if (categoria != null && sec && !seccionEsFlat(sec)) enterSeccion(sec);
    else goHome();
  });
  bc.appendChild(back);

  const home = document.createElement("a");
  home.textContent = "Catálogo";
  home.addEventListener("click", () => goHome());
  bc.appendChild(home);

  const addSep = () => {
    const s = document.createElement("span");
    s.className = "sep"; s.textContent = "/";
    bc.appendChild(s);
  };

  if (categoria == null) {
    addSep();
    const cur = document.createElement("span");
    cur.className = "current"; cur.textContent = sec.nombre;
    bc.appendChild(cur);
    return;
  }

  if (sec && !seccionEsFlat(sec)) {
    addSep();
    const secLink = document.createElement("a");
    secLink.textContent = sec.nombre;
    secLink.addEventListener("click", () => enterSeccion(sec));
    bc.appendChild(secLink);
  }
  addSep();
  const cur = document.createElement("span");
  cur.className = "current";
  cur.textContent = subcategoria ? titleCase(subcategoria) : titleCase(categoria);
  bc.appendChild(cur);
}

function enterSeccion(sec, pushHistory = true) {
  const subtiles = seccionSubtiles(sec);
  if (subtiles.length <= 1) {
    const only = subtiles[0];
    enterCategory(only ? only.categoria : sec.categorias[0], only ? (only.subcategoria || null) : null, pushHistory, sec);
    return;
  }

  currentCategoryItems = seccionItems(sec);
  renderBreadcrumb(sec, null, null);

  categoryContent.innerHTML = "";
  const section = document.createElement("section");
  section.className = "cat-section";
  section.innerHTML = `
    <div class="cat-heading"><h2 class="serif">${sec.nombre}</h2><div class="count">${currentCategoryItems.length} productos</div></div>
  `;
  categoryContent.appendChild(section);

  const grid = document.createElement("div");
  grid.className = "homegrid";
  grid.style.padding = "0";
  section.appendChild(grid);

  subtiles.forEach(t => {
    const groupItems = seccionItems(sec).filter(p => p.categoria === t.categoria && p.subcategoria === t.subcategoria);
    const rep = groupItems[0];
    const title = t.subcategoria ? titleCase(t.subcategoria) : titleCase(t.categoria);
    const a = document.createElement("a");
    a.className = "tile";
    a.innerHTML = `<img src="${rep.foto_ambientacion}" loading="lazy" alt="${title}"><div class="cap"><div class="t1">${title}</div></div>`;
    a.addEventListener("click", (e) => { e.preventDefault(); enterCategory(t.categoria, t.subcategoria || null, true, sec); });
    grid.appendChild(a);
  });

  if (pushHistory) history.pushState({ seccionId: sec.id }, "", "#" + sec.id);

  homeView.classList.add("hidden");
  categoryView.classList.remove("hidden");
  categoryView.classList.remove("fade-in"); void categoryView.offsetWidth; categoryView.classList.add("fade-in");
  window.scrollTo(0, 0);
}

function enterCategory(categoria, subcategoria, pushHistory = true, sec = null) {
  if (!sec) sec = findSeccionForCategoria(categoria);
  const catGroups = grupos.filter(g => g.categoria === categoria && (subcategoria == null || g.subcategoria === subcategoria));
  const total = catGroups.reduce((n, g) => n + g.items.length, 0);
  currentCategoryItems = catGroups.flatMap(g => g.items);

  renderBreadcrumb(sec, categoria, subcategoria);

  categoryContent.innerHTML = "";
  const section = document.createElement("section");
  section.className = "cat-section";
  section.innerHTML = `
    <div class="cat-heading"><h2 class="serif">${titleCase(subcategoria || categoria)}</h2><div class="count">${total} productos</div></div>
  `;
  categoryContent.appendChild(section);

  if (pushHistory) {
    history.pushState({ categoria, subcategoria, seccionId: sec ? sec.id : null }, "", "#" + groupSlug(categoria, subcategoria));
  }

  catGroups.forEach(g => {
    if (subcategoria == null && g.subcategoria) {
      const sh = document.createElement("div");
      sh.className = "subcat-heading";
      sh.textContent = g.subcategoria;
      section.appendChild(sh);
    }
    const grid = document.createElement("div");
    grid.className = "grid";
    section.appendChild(grid);

    g.items.forEach(p => {
      const cardId = "card_" + slugify(p.id);
      if (!state[cardId]) {
        state[cardId] = Object.assign({}, p, { revisado: false, fotos_adicionales: (p.fotos_adicionales || []).slice() });
      }
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <div class="frame"><img class="photo" src="${p.foto_ambientacion}" loading="lazy" alt="${(p.nombre||"").replace(/"/g,'&quot;')}"></div>
        <div class="name" id="${cardId}_name">${state[cardId].nombre || ""}</div>
      `;
      card.addEventListener("click", () => openModal(cardId));
      grid.appendChild(card);
    });
  });

  homeView.classList.add("hidden");
  categoryView.classList.remove("hidden");
  categoryView.classList.remove("fade-in"); void categoryView.offsetWidth; categoryView.classList.add("fade-in");
  window.scrollTo(0, 0);
}

window.addEventListener("popstate", (e) => {
  const st = e.state;
  if (!st || st.home) { goHome(false); return; }
  if (st.seccionId && !st.categoria) {
    const sec = SECCIONES.find(s => s.id === st.seccionId);
    if (sec) enterSeccion(sec, false);
    return;
  }
  const sec = st.seccionId ? SECCIONES.find(s => s.id === st.seccionId) : null;
  enterCategory(st.categoria, st.subcategoria, false, sec);
});

(function initFromHash() {
  const hash = location.hash.replace(/^#/, "");
  if (!hash) return;
  const sec = SECCIONES.find(s => s.id === hash);
  if (sec) { enterSeccion(sec, false); return; }
  for (const g of grupos) {
    if (groupSlug(g.categoria, g.subcategoria) === hash) {
      enterCategory(g.categoria, g.subcategoria, false);
      return;
    }
  }
})();

let modalFotos = [];
let modalFotoIndex = 0;

function renderModalFoto() {
  document.getElementById("mPhoto").src = modalFotos[modalFotoIndex];
  const prev = document.getElementById("mPrev");
  const next = document.getElementById("mNext");
  const multi = modalFotos.length > 1;
  prev.classList.toggle("hidden", !multi);
  next.classList.toggle("hidden", !multi);
  const dots = document.getElementById("mDots");
  dots.innerHTML = "";
  if (multi) {
    modalFotos.forEach((_, i) => {
      const d = document.createElement("div");
      d.className = "dot" + (i === modalFotoIndex ? " on" : "");
      d.addEventListener("click", () => { modalFotoIndex = i; renderModalFoto(); });
      dots.appendChild(d);
    });
  }
}

function openModal(cardId) {
  activeCardId = cardId;
  const s = state[cardId];
  modalFotos = [s.foto_ambientacion, ...(s.fotos_adicionales || [])];
  modalFotoIndex = 0;
  renderModalFoto();
  const stamp = document.getElementById("mStamp");
  stamp.classList.toggle("on", !!s.revisado);
  document.getElementById("modalBackdrop").classList.add("open");
}
function closeModal() {
  document.getElementById("modalBackdrop").classList.remove("open");
  activeCardId = null;
}
function modalPrev() {
  if (!modalFotos.length) return;
  modalFotoIndex = (modalFotoIndex - 1 + modalFotos.length) % modalFotos.length;
  renderModalFoto();
}
function modalNext() {
  if (!modalFotos.length) return;
  modalFotoIndex = (modalFotoIndex + 1) % modalFotos.length;
  renderModalFoto();
}
document.getElementById("mPrev").addEventListener("click", modalPrev);
document.getElementById("mNext").addEventListener("click", modalNext);
document.getElementById("modalClose").addEventListener("click", closeModal);
document.getElementById("modalBackdrop").addEventListener("click", (e) => {
  if (e.target.id === "modalBackdrop") closeModal();
});
document.addEventListener("keydown", (e) => {
  if (!document.getElementById("modalBackdrop").classList.contains("open")) return;
  if (e.key === "Escape") closeModal();
  if (e.key === "ArrowLeft") modalPrev();
  if (e.key === "ArrowRight") modalNext();
});

document.getElementById("mStamp").addEventListener("click", () => {
  if (!activeCardId) return;
  state[activeCardId].revisado = !state[activeCardId].revisado;
  document.getElementById("mStamp").classList.toggle("on", state[activeCardId].revisado);
});

// ---- Descarga del catálogo en PDF (liviano: cada foto se reescala antes de incrustarla) ----
// A prueba de fallos: cualquier error (imagen que no carga, canvas bloqueado por el
// navegador al abrir el archivo con doble clic, CDN caído, etc.) corta la generación
// y cierra el overlay en vez de dejarlo colgado para siempre.
function cargarImagenViaCanvas(url, maxDim, quality) {
  return new Promise((resolve, reject) => {
    const timeoutId = setTimeout(() => reject(new Error("timeout cargando " + url)), 12000);
    const img = new Image();
    img.onload = () => {
      clearTimeout(timeoutId);
      try {
        let w = img.naturalWidth, h = img.naturalHeight;
        const scale = Math.min(1, maxDim / Math.max(w, h));
        w = Math.round(w * scale); h = Math.round(h * scale);
        const canvas = document.createElement("canvas");
        canvas.width = w; canvas.height = h;
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, w, h);
        ctx.drawImage(img, 0, 0, w, h);
        const dataUrl = canvas.toDataURL("image/jpeg", quality);
        resolve({ dataUrl, w, h });
      } catch (err) {
        reject(err);
      }
    };
    img.onerror = () => { clearTimeout(timeoutId); reject(new Error("no se pudo cargar " + url)); };
    img.src = url;
  });
}

// Algunos navegadores bloquean la lectura de imágenes locales dentro de un <canvas>
// cuando la página se abrió con doble clic (file://). Si eso falla, probamos leer el
// archivo directamente como blob (funciona en más casos al servir desde file://).
function cargarImagenViaBlob(url) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.responseType = "blob";
    xhr.onload = () => {
      if (xhr.status !== 0 && xhr.status !== 200) { reject(new Error("status " + xhr.status)); return; }
      const reader = new FileReader();
      reader.onload = () => {
        const img = new Image();
        img.onload = () => resolve({ dataUrl: reader.result, w: img.naturalWidth, h: img.naturalHeight });
        img.onerror = () => reject(new Error("blob no es una imagen válida"));
        img.src = reader.result;
      };
      reader.onerror = () => reject(new Error("no se pudo leer el blob"));
      reader.readAsDataURL(xhr.response);
    };
    xhr.onerror = () => reject(new Error("xhr falló para " + url));
    xhr.send();
  });
}

async function cargarImagenComoJPEG(url, maxDim, quality) {
  try {
    return await cargarImagenViaCanvas(url, maxDim, quality);
  } catch (err) {
    return await cargarImagenViaBlob(url);
  }
}

let pdfCancelado = false;
let pdfEnCurso = false;

function actualizarProgresoPDF(i, total) {
  const pct = Math.round(((i + 1) / total) * 100);
  document.getElementById("pdfPct").textContent = pct + "%";
  document.getElementById("pdfBarFill").style.width = pct + "%";
  document.getElementById("pdfOverlayText").textContent = `Página ${i + 1} de ${total}`;
}

function cerrarOverlayPDF() {
  document.getElementById("pdfOverlay").classList.remove("open");
  pdfEnCurso = false;
}

async function generarPDF(lista, filename, titulo) {
  if (pdfEnCurso) return;
  if (typeof window.jspdf === "undefined") {
    alert("No se pudo cargar el generador de PDF (revisá tu conexión a internet e intentá de nuevo).");
    return;
  }
  pdfEnCurso = true;
  pdfCancelado = false;
  const overlay = document.getElementById("pdfOverlay");
  document.getElementById("pdfPct").textContent = "0%";
  document.getElementById("pdfBarFill").style.width = "0%";
  document.getElementById("pdfOverlayText").textContent = "Preparando…";
  overlay.classList.add("open");

  try {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({ orientation: "landscape", unit: "mm", format: "a4" });
    const pageW = doc.internal.pageSize.getWidth();
    const pageH = doc.internal.pageSize.getHeight();

    doc.setFillColor(245, 241, 234);
    doc.rect(0, 0, pageW, pageH, "F");
    doc.setTextColor(23, 20, 15);
    doc.setFont("times", "italic");
    doc.setFontSize(36);
    doc.text(titulo, pageW / 2, pageH / 2, { align: "center" });

    const incluirNombres = document.getElementById("incluirNombres").checked;

    for (let i = 0; i < lista.length; i++) {
      if (pdfCancelado) { cerrarOverlayPDF(); return; }
      const p = lista[i];
      actualizarProgresoPDF(i, lista.length);
      doc.addPage();
      doc.setFillColor(245, 241, 234);
      doc.rect(0, 0, pageW, pageH, "F");

      // texto arriba de la foto (si "incluir nombres" está tildado)
      let topMargin = 16;
      if (incluirNombres) {
        let yText = 24;
        if (p.subcategoria || p.categoria) {
          doc.setFont("helvetica", "normal");
          doc.setFontSize(9);
          doc.setTextColor(154, 146, 132);
          doc.text((p.subcategoria || p.categoria).toUpperCase(), pageW / 2, yText, { align: "center" });
          yText += 9;
        }
        doc.setFont("times", "bold");
        doc.setFontSize(19);
        doc.setTextColor(23, 20, 15);
        doc.text((p.nombre || "").toUpperCase(), pageW / 2, yText, { align: "center" });
        topMargin = yText + 10;
      }

      try {
        const { dataUrl, w, h } = await cargarImagenComoJPEG(p.foto_ambientacion, 1500, 0.82);
        if (pdfCancelado) { cerrarOverlayPDF(); return; }
        const maxW = pageW - 50, maxH = pageH - topMargin - 16;
        const scale = Math.min(maxW / w, maxH / h);
        const finalW = w * scale, finalH = h * scale;
        const x = (pageW - finalW) / 2;
        const y = topMargin + (maxH - finalH) / 2;
        const formato = /^data:image\\/png/i.test(dataUrl) ? "PNG" : "JPEG";
        doc.addImage(dataUrl, formato, x, y, finalW, finalH);
      } catch (e) {
        // si una foto puntual falla (o tarda demasiado), seguimos con el resto del catálogo
      }
    }

    if (pdfCancelado) { cerrarOverlayPDF(); return; }
    doc.save(filename);
  } catch (err) {
    alert("Hubo un problema generando el PDF. Si abriste este archivo con doble clic, probá abrirlo desde un servidor local o subido a la web — algunos navegadores bloquean la lectura de imágenes locales.");
  } finally {
    cerrarOverlayPDF();
  }
}

document.getElementById("pdfCancelBtn").addEventListener("click", () => {
  pdfCancelado = true;
  cerrarOverlayPDF();
});

document.getElementById("downloadPdfBtn").addEventListener("click", () => {
  generarPDF(productos, "catalogo.pdf", "Catálogo");
});
document.getElementById("downloadSectionPdfBtn").addEventListener("click", () => {
  const heading = document.querySelector(".cat-heading h2");
  const titulo = heading ? heading.textContent : "Catálogo";
  generarPDF(currentCategoryItems, `catalogo-${slugify(titulo)}.pdf`, titulo);
});
</script>
</body>
</html>
"""

HTML = HTML.replace("__DATA__", data_json)
(BASE / "index.html").write_text(HTML, encoding="utf-8")
print("index.html generado con", len(productos), "productos y", len({(p['categoria'],p['subcategoria']) for p in productos}), "grupos")
