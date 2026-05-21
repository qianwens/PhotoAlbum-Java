#!/usr/bin/env python3
"""
Generates report.html from report.json (Java/.NET) or js-assessment-report.md (JS/TS).

Usage:
    python generate_report_html.py /path/to/.github/modernize/assessment/reports/report-{id}
"""

import json
import math
import os
import re
import sys
from html import escape
from pathlib import Path

# ── CSS (exact copy from reference) ──────────────────────────────────────────
CSS = r""":root {
  --bg-primary: #ffffff;
  --bg-card: #f8f9fa;
  --bg-page: #f0f1f3;
  --text-primary: #24292f;
  --text-secondary: #57606a;
  --text-muted: #6b7280;
  --border-color: #d0d7de;
  --border-light: #e1e4e8;
  --link-color: #2563eb;
  --color-mandatory: #E3008C;
  --color-potential: #637CEF;
  --color-optional: #A19F9D;
  --font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
  --font-mono: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-family); font-size: 13px; color: var(--text-primary); background: var(--bg-primary); line-height: 1.5; margin: 0; padding: 0; }
a { color: var(--link-color); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ── Page layout ───────────────────────────────────────────── */
.main { margin: 0; padding: 24px 32px; background: var(--bg-primary); }
.back-link { color: var(--text-muted); font-size: 13px; margin-bottom: 16px; display: block; }
h1 { font-weight: 600; font-size: 20px; color: var(--text-primary); margin-bottom: 20px; }

/* ── Report cards (matches VS Code .vscode-report-card) ──── */
.report-card { background: var(--bg-card); border: 1px solid var(--border-light); border-radius: 4px; padding: 12px; margin-bottom: 20px; }
.report-card h2 { font-size: 14px; font-weight: 600; margin: 0; color: var(--text-primary); }
.report-card-body { margin-top: 16px; }

/* ── Application Information (two-column) ────────────────── */
.app-info-container { display: flex; gap: 8px; flex-wrap: wrap; }
.app-info-column { flex: 1; min-width: 200px; display: flex; flex-direction: column; gap: 8px; }
.app-info-row { display: flex; align-items: baseline; }
.app-info-label { width: 136px; flex-shrink: 0; font-weight: 600; color: var(--text-primary); }
.app-info-value { flex: 1; color: var(--text-primary); }

/* ── Issue Summary (pie charts + legend) ─────────────────── */
.cards-container { display: flex; align-items: stretch; gap: 20px; flex-wrap: wrap; }
.issue-summary-card { flex: 2; }
.domain-summary-container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-around; }
.domain-summary-item { flex: 1; min-width: 120px; text-align: center; padding: 0 16px; border-right: 1px solid var(--border-light); }
.domain-summary-item:last-child { border-right: none; }
.domain-summary-item h3 { font-size: 13px; font-weight: 600; color: var(--text-primary); margin-top: 8px; }
.domain-summary-item .count { font-size: 12px; color: var(--text-secondary); }
.criticality-legend { display: flex; flex-wrap: wrap; gap: 15px; padding-top: 12px; justify-content: center; }
.criticality-legend .legend-item { display: flex; align-items: center; gap: 4px; font-size: 12px; color: var(--text-secondary); }
.legend-swatch { display: inline-block; width: 1em; height: 1em; border-radius: 2px; }

/* ── Issue list tables ───────────────────────────────────── */
.issue-section { margin-top: 20px; }
.issue-section h2 { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
.issue-table { width: 100%; border-collapse: collapse; table-layout: fixed; min-width: 600px; }
.issue-table th { text-align: left; text-transform: uppercase; font-weight: 600; font-size: calc(13px * 0.875); padding: 6px 8px; background: var(--bg-card); border-bottom: 1px solid var(--border-color); color: var(--text-secondary); position: sticky; top: 0; z-index: 1; }
.issue-table td { padding: 12px 8px; border-bottom: 1px solid var(--border-light); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; vertical-align: middle; }
.col-issue { width: 55%; }
.col-criticality { width: 25%; }
.col-storypoint { width: 20%; }

/* ── Target dropdown ─────────────────────────────────────── */
.target-select-container { margin: 4px 0 16px 0; display: flex; align-items: center; gap: 8px; }
.target-select-container label { font-weight: 600; color: var(--text-primary); font-size: 14px; }
.target-select-container select { font-family: var(--font-family); font-size: 13px; padding: 4px 8px; border: 1px solid var(--border-color); border-radius: 4px; background: var(--bg-primary); color: var(--text-primary); cursor: pointer; }

/* ── Filter bar ──────────────────────────────────────────── */
.filter-bar { display: flex; flex-wrap: wrap; gap: 16px; margin: 16px 0 8px 0; align-items: center; }
.multi-select { position: relative; display: inline-block; min-width: 140px; }
.multi-select-btn { font-family: var(--font-family); font-size: 13px; padding: 4px 24px 4px 8px; border: 1px solid var(--border-color); border-radius: 4px; background: var(--bg-primary); color: var(--text-primary); cursor: pointer; width: 100%; text-align: left; position: relative; white-space: nowrap; }
.multi-select-btn::after { content: '\25BE'; position: absolute; right: 8px; top: 50%; transform: translateY(-50%); font-size: 11px; color: var(--text-secondary); }
.multi-select-dropdown { display: none; position: absolute; top: 100%; left: 0; min-width: 100%; background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); z-index: 100; margin-top: 2px; }
.multi-select.open .multi-select-dropdown { display: block; }
.multi-select-option { display: flex; align-items: center; gap: 6px; padding: 5px 10px; cursor: pointer; font-size: 13px; white-space: nowrap; }
.multi-select-option:hover { background: var(--bg-secondary); }
.multi-select-option input[type=checkbox] { margin: 0; cursor: pointer; }
.clear-filters { font-size: 12px; color: var(--link-color); cursor: pointer; margin-left: 4px; }

/* ── Criticality labels (colored square + text) ──────────── */
.crit-label { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; white-space: nowrap; }
.crit-square { display: inline-block; width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }
.crit-square-mandatory { background: var(--color-mandatory); }
.crit-square-potential { background: var(--color-potential); }
.crit-square-optional { background: var(--color-optional); }

/* ── Expandable rows ─────────────────────────────────────── */
.expand-btn { background: none; border: none; cursor: pointer; width: 20px; height: 20px; display: inline-flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 11px; transition: transform 0.15s; padding: 0; vertical-align: middle; flex-shrink: 0; }
.expand-btn.open { transform: rotate(90deg); }
.issue-title-cell { display: flex; align-items: center; gap: 4px; }
.detail-row td { padding: 0; border-bottom: 1px solid var(--border-light); white-space: normal; overflow: visible; text-overflow: clip; }
.detail-content { display: flex; gap: 0; padding: 8px 8px 8px 32px; min-width: 0; }
.file-list { flex: 0 0 50%; min-width: 0; overflow: hidden; }
.file-list table { width: 100%; border-collapse: collapse; }
.file-list th { font-size: calc(13px * 0.875); text-transform: uppercase; font-weight: 600; color: var(--text-secondary); padding: 6px 8px; border-bottom: 1px solid var(--border-color); text-align: left; height: 32px; }
.file-list td { font-size: 13px; padding: 6px 8px; border-bottom: 1px solid var(--border-light); color: var(--text-primary); }
.file-list .file-path { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 300px; display: block; }
.file-list .position { font-family: var(--font-mono); font-size: 12px; color: var(--text-secondary); }
.explanation-panel { flex: 1; padding-left: 16px; min-width: 0; overflow-wrap: break-word; word-wrap: break-word; }
.explanation-panel h4 { font-size: calc(13px * 0.875); text-transform: uppercase; font-weight: 600; color: var(--text-secondary); padding: 6px 0; border-bottom: 1px solid var(--border-color); height: 32px; margin: 0; }
.explanation-panel p { font-size: 13px; padding: 8px 0; color: var(--text-primary); line-height: 1.6; white-space: normal; word-break: break-word; }

/* ── Experimental badge ──────────────────────────────────── */
.badge-experimental { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; background: #fef9c3; color: #854d0e; vertical-align: middle; margin-left: 8px; cursor: default; }

/* ── Footer ──────────────────────────────────────────────── */
.footer { text-align: center; margin-top: 24px; color: var(--text-muted); font-size: 13px; }

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 800px) {
  .main { padding: 16px; }
  .app-info-container { flex-direction: column; }
  .domain-summary-container { flex-direction: column; }
  .domain-summary-item { border-right: none; border-bottom: 1px solid var(--border-light); padding-bottom: 12px; }
  .detail-content { flex-direction: column; }
  .file-list { flex: none; width: 100%; }
  .explanation-panel { padding-left: 0; padding-top: 8px; }
}
/* ── Tab navigation ──────────────────────────────────────── */
.tab-nav { display: flex; gap: 0; border-bottom: 1px solid var(--border-color); margin-bottom: 28px; flex-wrap: wrap; }
.tab-btn { background: none; border: none; border-bottom: 2px solid transparent; padding: 10px 18px; font-size: 13px; font-family: var(--font-family); color: var(--text-secondary); cursor: pointer; margin-bottom: -1px; white-space: nowrap; position: relative; }
.tab-btn:hover { color: var(--text-primary); }
.tab-btn.active { color: var(--link-color); border-bottom-color: var(--link-color); font-weight: 600; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }

/* ── Tooltip on tab ──────────────────────────────────────── */
.tab-btn[data-tooltip]::after { content: attr(data-tooltip); position: absolute; bottom: calc(100% + 8px); left: 50%; transform: translateX(-50%); background: #24292f; color: #ffffff; font-size: 12px; font-weight: 400; padding: 6px 10px; border-radius: 4px; white-space: normal; width: max-content; max-width: 260px; text-align: center; pointer-events: none; opacity: 0; transition: opacity 0.15s; z-index: 100; }
.tab-btn[data-tooltip]:hover::after { opacity: 1; }

/* ── Fact content — prose column ─────────────────────────── */
.fact-content { max-width: 860px; margin: 0 auto; line-height: 1.75; color: var(--text-primary); font-size: 14px; }
.fact-content h1 { font-size: 22px; font-weight: 700; margin: 0 0 6px 0; color: var(--text-primary); letter-spacing: -0.01em; }
.fact-content h1 + p { margin-top: 6px; color: var(--text-secondary); font-size: 14px; margin-bottom: 24px; }
.fact-content h2 { font-size: 17px; font-weight: 700; margin: 36px 0 12px 0; padding-bottom: 6px; border-bottom: 1px solid var(--border-color); color: var(--text-primary); letter-spacing: -0.01em; }
.fact-content h3 { font-size: 14px; font-weight: 700; margin: 24px 0 8px 0; color: var(--text-primary); text-transform: uppercase; letter-spacing: 0.04em; font-size: 12px; color: var(--text-secondary); }
.fact-content p { margin: 10px 0; color: var(--text-primary); }
.fact-content ul, .fact-content ol { margin: 10px 0 10px 22px; }
.fact-content li { margin: 5px 0; }
.fact-content a { color: var(--link-color); }
.fact-content a:hover { text-decoration: underline; }

/* ── Fact tables ─────────────────────────────────────────── */
.table-wrap { overflow-x: auto; margin: 16px 0; }
.fact-content table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 13px; border-radius: 6px; overflow: hidden; border: 1px solid var(--border-color); }
.fact-content thead { background: var(--bg-card); }
.fact-content th { text-align: left; font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; padding: 8px 14px; border-bottom: 1px solid var(--border-color); color: var(--text-secondary); }
.fact-content td { padding: 9px 14px; border-bottom: 1px solid var(--border-light); vertical-align: top; color: var(--text-primary); }
.fact-content tr:last-child td { border-bottom: none; }
.fact-content tbody tr:hover { background: #f6f8fa; }

/* ── Fact code ───────────────────────────────────────────── */
.fact-content code { font-family: var(--font-mono); font-size: 12px; background: #f0f1f3; padding: 2px 6px; border-radius: 4px; color: #c7254e; }
.fact-content pre { background: #f6f8fa; border: 1px solid var(--border-light); border-radius: 6px; padding: 14px 16px; overflow-x: auto; margin: 14px 0; }
.fact-content pre code { background: none; color: var(--text-primary); padding: 0; border-radius: 0; }
.fact-content hr { border: none; border-top: 1px solid var(--border-light); margin: 28px 0; }
.fact-content strong { font-weight: 600; }
.fact-content em { font-style: italic; }
.fact-content blockquote { border-left: 3px solid var(--border-color); margin: 12px 0; padding: 4px 16px; color: var(--text-secondary); }
.fact-unavailable { padding: 32px 0; }
.fact-unavailable h3 { font-size: 16px; font-weight: 600; color: var(--text-primary); text-transform: none; letter-spacing: 0; margin: 0 0 12px 0; }
.fact-unavailable p { margin: 0 0 8px 0; color: var(--text-secondary); }
.fact-unavailable ol, .fact-unavailable ul { margin: 0 0 0 22px; color: var(--text-primary); }
.fact-unavailable li { margin: 6px 0; }

/* ── Mermaid diagram card ─────────────────────────────────── */
.mermaid { background: var(--bg-card); border: 1px solid var(--border-light); border-radius: 8px; padding: 24px 16px; margin: 20px 0; overflow-x: auto; text-align: center; cursor: pointer; position: relative; }
.mermaid:hover { border-color: var(--border-color); }
.mermaid svg { max-width: 100%; height: auto !important; display: inline-block; }
.mermaid-zoom-hint { position: absolute; top: 8px; right: 10px; font-size: 11px; color: var(--text-muted); opacity: 0; transition: opacity 0.15s; pointer-events: none; }
.mermaid:hover .mermaid-zoom-hint { opacity: 1; }

/* ── Diagram lightbox ────────────────────────────────────── */
.diagram-lightbox { display: none; position: fixed; inset: 0; z-index: 1000; background: rgba(0,0,0,0.7); backdrop-filter: blur(2px); align-items: center; justify-content: center; cursor: zoom-out; padding: 48px 32px; }
.diagram-lightbox.open { display: flex; }
.diagram-lightbox-inner { background: #ffffff; border-radius: 10px; padding: 32px; width: 88vw; max-height: 88vh; overflow: hidden; cursor: default; box-shadow: 0 24px 64px rgba(0,0,0,0.35); display: flex; align-items: center; justify-content: center; }
.diagram-lightbox-inner svg { width: 100% !important; height: auto !important; max-height: 76vh; display: block; }
.diagram-lightbox-close { position: fixed; top: 20px; right: 24px; background: #ffffff; border: none; border-radius: 50%; width: 36px; height: 36px; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; color: var(--text-primary); box-shadow: 0 2px 8px rgba(0,0,0,0.2); z-index: 1001; }
.diagram-lightbox-close:hover { background: var(--bg-card); }
.diagram-lightbox-hint { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.55); color: #ffffff; font-size: 12px; padding: 6px 14px; border-radius: 20px; pointer-events: none; white-space: nowrap; z-index: 1001; }"""

# ── Mermaid head script ──────────────────────────────────────────────────────
MERMAID_HEAD_SCRIPT = """<script>
window.__mermaidPending = [];
window.__mermaidReady = false;
window.__renderMermaidIn = function(container) {
  if (container) { window.__mermaidPending.push(container); }
};
</script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: false, theme: 'default', flowchart: { useMaxWidth: true }, sequence: { useMaxWidth: true } });

window.__renderMermaidIn = function(container) {
  var nodes = container ? container.querySelectorAll('.mermaid:not([data-processed])') : [];
  if (nodes.length > 0) {
    mermaid.run({ nodes: Array.from(nodes) }).then(function() {
      nodes.forEach(function(node) {
        if (!node.querySelector('.mermaid-zoom-hint')) {
          var hint = document.createElement('span');
          hint.className = 'mermaid-zoom-hint';
          hint.textContent = 'Click to expand';
          node.appendChild(hint);
        }
      });
    });
  }
};

var drained = new Set();
(window.__mermaidPending || []).forEach(function(c) {
  if (!drained.has(c)) { drained.add(c); window.__renderMermaidIn(c); }
});
window.__mermaidPending = [];
window.__mermaidReady = true;

function renderActivePanels() {
  document.querySelectorAll('.tab-panel.active').forEach(function(p) {
    if (!drained.has(p)) { drained.add(p); window.__renderMermaidIn(p); }
  });
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', renderActivePanels);
} else {
  renderActivePanels();
}
</script>"""

# ── JavaScript ───────────────────────────────────────────────────────────────
MAIN_SCRIPT = r"""function toggleRow(rowId, triggerRow) {
  var detail = document.getElementById(rowId);
  var btn = document.getElementById('btn-' + rowId);
  if (!detail) return;
  var visible = detail.style.display !== 'none';
  detail.style.display = visible ? 'none' : 'table-row';
  if (btn) btn.classList.toggle('open', !visible);
}
(function() {
  var nav = document.querySelector('.tab-nav');
  if (!nav) return;
  nav.addEventListener('click', function(e) {
    var btn = e.target.closest('.tab-btn');
    if (!btn) return;
    var targetId = btn.getAttribute('data-tab');
    document.querySelectorAll('.tab-btn').forEach(function(b) { b.classList.remove('active'); });
    document.querySelectorAll('.tab-panel').forEach(function(p) { p.classList.remove('active'); });
    btn.classList.add('active');
    var panel = document.getElementById(targetId);
    if (panel) {
      panel.classList.add('active');
      if (window.__mermaidReady) { window.__renderMermaidIn(panel); }
    }
  });
})();

// ── Diagram lightbox ────────────────────────────────────────
(function() {
  var lightbox = document.getElementById('diagram-lightbox');
  var inner = document.getElementById('diagram-lightbox-inner');
  var closeBtn = document.getElementById('diagram-lightbox-close');
  if (!lightbox || !inner || !closeBtn) return;

  var scale = 1;
  var translateX = 0;
  var translateY = 0;
  var isDragging = false;
  var dragStartX = 0;
  var dragStartY = 0;

  function applyTransform() {
    var svg = inner.querySelector('svg');
    if (svg) {
      svg.style.transform = 'translate(' + translateX + 'px, ' + translateY + 'px) scale(' + scale + ')';
      svg.style.transformOrigin = 'center center';
      svg.style.transition = 'none';
    }
  }

  function resetTransform() {
    scale = 1; translateX = 0; translateY = 0;
    applyTransform();
  }

  function openLightbox(svgEl) {
    inner.innerHTML = svgEl.outerHTML;
    var injected = inner.querySelector('svg');
    if (injected) {
      injected.removeAttribute('width');
      injected.removeAttribute('height');
      injected.style.cursor = 'grab';
    }
    resetTransform();
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    inner.innerHTML = '';
    document.body.style.overflow = '';
    resetTransform();
  }

  inner.addEventListener('wheel', function(e) {
    e.preventDefault();
    var delta = e.deltaY > 0 ? 0.9 : 1.1;
    scale = Math.min(Math.max(scale * delta, 0.3), 8);
    applyTransform();
  }, { passive: false });

  inner.addEventListener('mousedown', function(e) {
    if (e.button !== 0) return;
    isDragging = true;
    dragStartX = e.clientX - translateX;
    dragStartY = e.clientY - translateY;
    var svg = inner.querySelector('svg');
    if (svg) { svg.style.cursor = 'grabbing'; }
    e.preventDefault();
  });

  document.addEventListener('mousemove', function(e) {
    if (!isDragging) return;
    translateX = e.clientX - dragStartX;
    translateY = e.clientY - dragStartY;
    applyTransform();
  });

  document.addEventListener('mouseup', function() {
    if (!isDragging) return;
    isDragging = false;
    var svg = inner.querySelector('svg');
    if (svg) { svg.style.cursor = 'grab'; }
  });

  inner.addEventListener('dblclick', function() { resetTransform(); });

  document.addEventListener('click', function(e) {
    var card = e.target.closest('.mermaid');
    if (!card) return;
    if (e.target.closest('.diagram-lightbox-close')) return;
    var svg = card.querySelector('svg');
    if (svg) { openLightbox(svg); }
  });

  closeBtn.addEventListener('click', closeLightbox);

  lightbox.addEventListener('click', function(e) {
    if (e.target === lightbox) { closeLightbox(); }
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') { closeLightbox(); }
  });
})();

var _currentTarget = '';

function toggleMultiSelect(id) {
  var el = document.getElementById(id);
  if (!el) return;
  document.querySelectorAll('.multi-select.open').forEach(function(ms) { if (ms.id !== id) ms.classList.remove('open'); });
  el.classList.toggle('open');
}

document.addEventListener('click', function(e) {
  if (!e.target.closest('.multi-select')) {
    document.querySelectorAll('.multi-select.open').forEach(function(ms) { ms.classList.remove('open'); });
  }
});

function getMultiSelectValues(msId) {
  var el = document.getElementById(msId);
  if (!el) return [];
  var checked = el.querySelectorAll('input[type=checkbox]:checked');
  var vals = [];
  for (var i = 0; i < checked.length; i++) vals.push(checked[i].value);
  return vals;
}

function onMultiSelectChange(msId, label) {
  var el = document.getElementById(msId);
  if (!el) return;
  var vals = getMultiSelectValues(msId);
  var total = el.querySelectorAll('input[type=checkbox]').length;
  var btn = el.querySelector('.multi-select-btn');
  if (btn) {
    btn.textContent = vals.length > 0 && vals.length < total ? label + ' (' + vals.length + ')' : label;
  }
  applyFilters();
}

function applyFilters() {
  var selectedDomains = getMultiSelectValues('domain-ms');
  var selectedCrits = getMultiSelectValues('criticality-ms');

  var sections = document.querySelectorAll('.issue-section');
  for (var i = 0; i < sections.length; i++) {
    var domain = sections[i].getAttribute('data-domain');
    sections[i].style.display = (selectedDomains.length === 0 || selectedDomains.indexOf(domain) >= 0) ? '' : 'none';
  }

  var rows = document.querySelectorAll('.issue-row');
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var section = row.closest('.issue-section');
    if (section && section.style.display === 'none') {
      row.style.display = 'none';
      var next = row.nextElementSibling;
      if (next && next.classList.contains('detail-row')) next.style.display = 'none';
      continue;
    }

    var show = true;
    if (_currentTarget && row.hasAttribute('data-targets')) {
      var targetsStr = row.getAttribute('data-targets');
      if (targetsStr && targetsStr !== '{}') {
        try {
          var targets = JSON.parse(targetsStr);
          if (Object.keys(targets).length > 0 && !targets[_currentTarget]) {
            show = false;
          }
        } catch(e) {}
      }
    }

    if (show && selectedCrits.length > 0) {
      var crit = row.getAttribute('data-criticality');
      if (selectedCrits.indexOf(crit) < 0) show = false;
    }

    row.style.display = show ? '' : 'none';
    var nextRow = row.nextElementSibling;
    if (nextRow && nextRow.classList.contains('detail-row')) {
      if (!show) nextRow.style.display = 'none';
    }
  }
}

function clearAllFilters() {
  document.querySelectorAll('.multi-select input[type=checkbox]').forEach(function(cb) { cb.checked = false; });
  var domainBtn = document.querySelector('#domain-ms .multi-select-btn');
  if (domainBtn) domainBtn.textContent = 'Domain';
  var critBtn = document.querySelector('#criticality-ms .multi-select-btn');
  if (critBtn) critBtn.textContent = 'Criticality';
  applyFilters();
}

function onTargetChange(targetId) {
  _currentTarget = targetId;
  var rows = document.querySelectorAll('.issue-row[data-targets]');
  var totalEffort = 0;
  var domainCrits = {};

  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var targets = JSON.parse(row.getAttribute('data-targets'));
    var section = row.closest('.issue-section');
    var domain = section ? section.getAttribute('data-domain') : '';

    if (!targets || Object.keys(targets).length === 0) {
      var sp = parseFloat(row.querySelector('.sp-cell').textContent) || 0;
      totalEffort += sp;
      if (!domainCrits[domain]) domainCrits[domain] = {mandatory:0,potential:0,optional:0};
      var crit = row.getAttribute('data-criticality') || 'optional';
      domainCrits[domain][crit] = (domainCrits[domain][crit] || 0) + 1;
      continue;
    }

    var override = targets[targetId];
    if (!override) {
      continue;
    }

    var newSeverity = (override.severity || row.getAttribute('data-default-severity') || '').toLowerCase();
    row.setAttribute('data-criticality', newSeverity);
    var critCell = row.querySelector('.crit-cell');
    if (critCell) {
      var critText = newSeverity === 'mandatory' ? 'Mandatory' : newSeverity === 'potential' ? 'Potential' : 'Optional';
      var cssClass = newSeverity === 'mandatory' ? 'crit-square-mandatory' : newSeverity === 'potential' ? 'crit-square-potential' : 'crit-square-optional';
      critCell.innerHTML = '<span class="crit-label"><span class="crit-square ' + cssClass + '"></span>' + critText + '</span>';
    }

    var newEffort = override.effort !== undefined ? override.effort : parseFloat(row.getAttribute('data-default-effort')) || 0;
    var spCell = row.querySelector('.sp-cell');
    if (spCell) spCell.textContent = newEffort;
    totalEffort += newEffort;

    if (!domainCrits[domain]) domainCrits[domain] = {mandatory:0,potential:0,optional:0};
    domainCrits[domain][newSeverity] = (domainCrits[domain][newSeverity] || 0) + 1;
  }

  var secSection = document.querySelector('.issue-section[data-domain="security"]');
  if (secSection) {
    var secRows = secSection.querySelectorAll('.issue-row');
    for (var j = 0; j < secRows.length; j++) {
      if (!secRows[j].hasAttribute('data-targets') || secRows[j].getAttribute('data-targets') === '') {
        var sp = parseFloat(secRows[j].querySelector('.sp-cell').textContent) || 0;
        totalEffort += sp;
        if (!domainCrits['security']) domainCrits['security'] = {mandatory:0,potential:0,optional:0};
        var sc = secRows[j].getAttribute('data-criticality') || 'optional';
        domainCrits['security'][sc] = (domainCrits['security'][sc] || 0) + 1;
      }
    }
  }

  var label = totalEffort < 20 ? 'S' : totalEffort < 50 ? 'M' : totalEffort < 100 ? 'L' : 'XL';
  var effortEl = document.getElementById('effort-display');
  if (effortEl) effortEl.textContent = label + ' (total story points: ' + totalEffort + ')';

  updateDonuts(domainCrits);
  applyFilters();
}

function updateDonuts(domainCrits) {
  var container = document.getElementById('donut-container');
  if (!container) return;
  container.innerHTML = '';
  var domainNames = {'cloud-readiness':'Cloud Readiness','java-upgrade':'Java Upgrade','security':'Security'};
  var domainOrder = ['cloud-readiness','java-upgrade','security'];
  for (var d = 0; d < domainOrder.length; d++) {
    var key = domainOrder[d];
    var c = domainCrits[key];
    if (!c || (c.mandatory + c.potential + c.optional) === 0) continue;
    var total = c.mandatory + c.potential + c.optional;
    var div = document.createElement('div');
    div.className = 'domain-summary-item';
    div.innerHTML = buildDonutSvg(c.mandatory, c.potential, c.optional) +
      '<h3>' + domainNames[key] + '</h3>' +
      '<div class="count">' + total + ' issue' + (total !== 1 ? 's' : '') + '</div>';
    container.appendChild(div);
  }
}

function buildDonutSvg(m, p, o) {
  var total = m + p + o;
  if (total === 0) return '<svg viewBox="0 0 100 100" width="100" height="100" style="display:block;margin:0 auto;"><circle cx="50" cy="50" r="35" fill="none" stroke="#d0d7de" stroke-width="15" opacity="0.5"/></svg>';
  var r = 35, circ = 2 * Math.PI * r, offset = 0;
  var svg = '<svg viewBox="0 0 100 100" width="100" height="100" style="display:block;margin:0 auto;transform:rotate(-90deg);">';
  var segs = [{c:m,color:'var(--color-mandatory)'},{c:p,color:'var(--color-potential)'},{c:o,color:'var(--color-optional)'}];
  for (var i = 0; i < segs.length; i++) {
    if (segs[i].c === 0) continue;
    var segLen = (segs[i].c / total) * circ;
    var gap = total > segs[i].c ? 1.5 : 0;
    var drawLen = Math.max(segLen - gap, 0.5);
    svg += '<circle cx="50" cy="50" r="' + r + '" fill="none" stroke="' + segs[i].color + '" stroke-width="15" stroke-dasharray="' + drawLen.toFixed(2) + ' ' + circ.toFixed(2) + '" stroke-dashoffset="' + (-offset).toFixed(2) + '"/>';
    offset += segLen;
  }
  svg += '</svg>';
  return svg;
}"""


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_severity_rank(severity):
    if not severity:
        return 99
    s = severity.strip().lower()
    return {"mandatory": 0, "potential": 1, "optional": 2}.get(s, 99)


def build_donut_svg(mandatory, potential, optional):
    total = mandatory + potential + optional
    if total == 0:
        return ('<svg viewBox="0 0 100 100" width="100" height="100" style="display:block;margin:0 auto;">'
                '<circle cx="50" cy="50" r="35" fill="none" stroke="#d0d7de" stroke-width="15" opacity="0.5"/>'
                '</svg>\n')
    r = 35
    circ = 2 * math.pi * r
    segments = [
        (mandatory, "var(--color-mandatory)"),
        (potential, "var(--color-potential)"),
        (optional, "var(--color-optional)"),
    ]
    svg = '<svg viewBox="0 0 100 100" width="100" height="100" style="display:block;margin:0 auto;transform:rotate(-90deg);">\n'
    offset = 0.0
    for count, color in segments:
        if count == 0:
            continue
        seg_len = (count / total) * circ
        gap = 1.5 if total > count else 0
        draw_len = max(seg_len - gap, 0.5)
        svg += (f'  <circle cx="50" cy="50" r="{r}" fill="none" stroke="{color}" '
                f'stroke-width="15" stroke-dasharray="{draw_len:.2f} {circ:.2f}" '
                f'stroke-dashoffset="{-offset:.2f}"/>\n')
        offset += seg_len
    svg += '</svg>\n'
    return svg


def simple_markdown_to_html(md):
    """Convert rule description markdown to inline HTML."""
    if not md:
        return ""
    html = escape(md)
    # Code blocks
    html = re.sub(r'```\w*\r?\n([\s\S]*?)```', r'<pre><code>\1</code></pre>', html)
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Links
    def replace_link(m):
        text, url = m.group(1), m.group(2)
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, html)

    def apply_italic(text):
        return re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # Process line-by-line for block structures
    lines = re.split(r'\r?\n', html)
    result = []
    in_list = False
    in_paragraph = False

    for line in lines:
        # List item
        list_match = re.match(r'^[\-\*]\s+(.+)', line)
        if list_match:
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            if not in_list:
                result.append('<ul>')
                in_list = True
            content = apply_italic(list_match.group(1))
            result.append(f'<li>{content}</li>')
            continue

        # End list if needed
        if in_list:
            result.append('</ul>')
            in_list = False

        # Blank line
        if not line.strip():
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            continue

        # Regular text
        text_content = apply_italic(line)
        if not in_paragraph:
            result.append('<p>')
            in_paragraph = True
        else:
            result.append('<br/>')
        result.append(text_content)

    if in_list:
        result.append('</ul>')
    if in_paragraph:
        result.append('</p>')

    return ''.join(result)


def markdown_to_fact_html(md):
    """Convert a fact .md file to HTML for the fact-content div."""
    if not md:
        return ""
    lines = md.split('\n')
    out = []
    i = 0
    in_list = None  # 'ul' or 'ol'
    in_table = False
    table_lines = []

    def flush_table():
        nonlocal in_table, table_lines
        if not table_lines:
            return
        # Parse markdown table
        header = table_lines[0]
        # table_lines[1] is the separator
        rows = table_lines[2:] if len(table_lines) > 2 else []
        cols = [c.strip() for c in header.strip('|').split('|')]
        out.append('<div class="table-wrap"><table><thead><tr>')
        out.append(''.join(f'<th>{inline_md(c)}</th>' for c in cols))
        out.append('</tr></thead><tbody>')
        for row in rows:
            cells = [c.strip() for c in row.strip('|').split('|')]
            out.append('<tr>' + ''.join(f'<td>{inline_md(c)}</td>' for c in cells) + '</tr>')
        out.append('</tbody></table></div>')
        table_lines = []
        in_table = False

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append(f'</{in_list}>')
            in_list = None

    def inline_md(text):
        """Convert inline markdown."""
        t = text
        t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
        t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
        return t

    while i < len(lines):
        line = lines[i]

        # Mermaid code block
        if line.strip().startswith('```mermaid'):
            flush_list()
            flush_table()
            i += 1
            mermaid_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                mermaid_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            out.append('<div class="mermaid">')
            out.append('\n'.join(mermaid_lines))
            out.append('</div>')
            continue

        # Regular code block
        if line.strip().startswith('```'):
            flush_list()
            flush_table()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(escape(lines[i]))
                i += 1
            i += 1
            out.append('<pre><code>')
            out.append('\n'.join(code_lines))
            out.append('</code></pre>')
            continue

        # Table detection
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?[\s\-:|]+\|', lines[i + 1]):
            flush_list()
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            i += 1
            continue
        if in_table and '|' in line:
            table_lines.append(line)
            i += 1
            continue
        if in_table:
            flush_table()

        # Headers
        m = re.match(r'^(#{1,3})\s+(.+)', line)
        if m:
            flush_list()
            level = len(m.group(1))
            text = m.group(2).strip()
            tag = f'h{level}'
            hid = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
            out.append(f'<{tag} id="{hid}">{inline_md(text)}</{tag}>')
            i += 1
            continue

        # Unordered list
        m = re.match(r'^[\-\*]\s+(.+)', line)
        if m:
            flush_table()
            if in_list != 'ul':
                flush_list()
                in_list = 'ul'
                out.append('<ul>')
            out.append(f'<li>{inline_md(m.group(1))}</li>')
            i += 1
            continue

        # Ordered list
        m = re.match(r'^\d+\.\s+(.+)', line)
        if m:
            flush_table()
            if in_list != 'ol':
                flush_list()
                in_list = 'ol'
                out.append('<ol>')
            out.append(f'<li>{inline_md(m.group(1))}</li>')
            i += 1
            continue

        # Blank line
        if not line.strip():
            flush_list()
            i += 1
            continue

        # Paragraph
        flush_list()
        out.append(f'<p>{inline_md(line)}</p>')
        i += 1

    flush_list()
    flush_table()
    return '\n'.join(out)


def is_dotnet_component(language):
    if not language or language.strip().upper() == "N/A":
        return True
    return ".net" in language.lower() or "c#" in language.lower()


# ── Fact tabs catalog ────────────────────────────────────────────────────────
FACT_TABS = [
    ("tab-arch", "Architecture", "How the app's layers connect — from UI to data.", "architecture-diagram.md"),
    ("tab-api", "API Contracts", "Endpoints exposed by this app and how services communicate.", "api-service-contracts.md"),
    ("tab-config", "Configuration", "Environment settings, runtime profiles, and deployment manifests.", "configuration-inventory.md"),
    ("tab-workflows", "Business Workflows", "Domain entities and the core flows users move through.", "business-workflows.md"),
    ("tab-deps", "Dependencies", "Libraries and frameworks this app depends on, grouped by category.", "dependency-map.md"),
    ("tab-data", "Data Model", "Database schema, entity relationships, and persistence behavior.", "data-architecture.md"),
]


# ── Main generation logic ────────────────────────────────────────────────────

def generate_from_report_json(report_dir):
    """Generate report.html from report.json (Java/.NET)."""
    report_json_path = os.path.join(report_dir, "report.json")
    if not os.path.isfile(report_json_path):
        print(f"Error: report.json not found at {report_json_path}", file=sys.stderr)
        sys.exit(1)

    with open(report_json_path, 'r', encoding='utf-8') as f:
        root = json.load(f)

    # Parse metadata
    metadata = root.get("metadata", {})
    target_display_names = metadata.get("targetDisplayNames", [])
    target_ids = metadata.get("targetIds", [])

    # Parse rules
    rules = root.get("rules", {})

    # Parse projects/incidents
    projects = root.get("projects", [])
    # Merge all projects into one component view
    component_name = ""
    component_display_name = ""
    language = "N/A"
    frameworks = "N/A"
    build_tools = "N/A"
    jdk_version = ""
    all_incidents = []

    for proj in projects:
        props = proj.get("properties", {})
        if not component_name:
            component_name = props.get("repo", "") or props.get("appName", "Application")
            component_display_name = props.get("appName", "") or component_name
        lang = props.get("languages")
        if lang:
            language = ", ".join(lang) if isinstance(lang, list) else str(lang)
        fw = props.get("frameworks")
        if fw:
            frameworks = ", ".join(fw) if isinstance(fw, list) else str(fw)
        tools = props.get("tools")
        if tools:
            build_tools = ", ".join(tools) if isinstance(tools, list) else str(tools)
        if not jdk_version:
            jdk_version = props.get("jdkVersion", "")

        for incident in proj.get("incidents", []):
            rule_id = incident.get("ruleId", "")
            if rule_id and rule_id in rules:
                all_incidents.append(incident)

    # Parse security findings
    security_findings = root.get("security", [])
    # Parse rearchitect findings
    rearchitect_findings = root.get("rearchitect", [])

    is_dotnet = is_dotnet_component(language)

    # Group incidents by rule
    incidents_by_rule = {}
    for inc in all_incidents:
        rid = inc.get("ruleId", "")
        if rid not in incidents_by_rule:
            incidents_by_rule[rid] = []
        incidents_by_rule[rid].append(inc)

    # Classify into cloud/upgrade domains
    cloud_groups = []  # list of (rule_id, incidents_list)
    upgrade_groups = []
    upgrade_domain_name = "Upgrade"

    for rule_id, incs in incidents_by_rule.items():
        rule_obj = rules.get(rule_id, {})
        labels = rule_obj.get("labels", [])
        has_domain = any(l.startswith("domain=") for l in labels)
        is_cloud = any(l == "domain=cloud-readiness" for l in labels)
        is_upgrade = any(l.endswith("-upgrade") for l in labels)

        if not has_domain and is_dotnet:
            is_cloud = True

        if is_cloud:
            cloud_groups.append((rule_id, incs))
        if is_upgrade:
            upgrade_groups.append((rule_id, incs))
            upgrade_label = next((l for l in labels if l.endswith("-upgrade") and l.startswith("domain=")), None)
            if upgrade_label:
                domain_val = upgrade_label[len("domain="):]
                upgrade_domain_name = " ".join(w.capitalize() for w in domain_val.split("-"))

    # Count criticalities per domain
    def count_crits(groups):
        m, p, o = 0, 0, 0
        for rid, _ in groups:
            sev = rules.get(rid, {}).get("severity", "").strip().lower()
            if sev == "mandatory": m += 1
            elif sev == "potential": p += 1
            else: o += 1
        return m, p, o

    cloud_crit = count_crits(cloud_groups)
    upgrade_crit = count_crits(upgrade_groups)

    # Add rearchitect to upgrade optional count
    if rearchitect_findings:
        upgrade_crit = (upgrade_crit[0], upgrade_crit[1], upgrade_crit[2] + len(rearchitect_findings))

    sec_mandatory = sum(1 for f in security_findings if f.get("severity", "").strip().lower() == "mandatory")
    sec_potential = sum(1 for f in security_findings if f.get("severity", "").strip().lower() == "potential")
    sec_optional = len(security_findings) - sec_mandatory - sec_potential
    security_crit = (sec_mandatory, sec_potential, sec_optional)

    # Compute total effort
    # For each unique rule, take aksEffort from first incident
    total_effort = 0.0
    seen_rules = set()
    for inc in all_incidents:
        rid = inc.get("ruleId", "")
        if rid in seen_rules:
            continue
        seen_rules.add(rid)
        # Get AKS effort
        aks_effort = 0
        targets = inc.get("targets", {})
        for tid, tdata in targets.items():
            if "aks" in tid.lower() or "kubernetes" in tid.lower():
                aks_effort = tdata.get("effort", 0)
                break
        if aks_effort == 0:
            aks_effort = rules.get(rid, {}).get("effort", 0) or 0
        total_effort += aks_effort

    total_effort += sum(f.get("storyPoint", 0) for f in security_findings)
    total_effort += len(rearchitect_findings) * 10

    if total_effort < 20:
        effort_label = "S"
    elif total_effort < 50:
        effort_label = "M"
    elif total_effort < 100:
        effort_label = "L"
    else:
        effort_label = "XL"
    effort_display = f"{effort_label} (total story points: {int(total_effort)})"

    # Load fact tabs
    facts_dir = os.path.join(report_dir, "facts")
    # Fallback: if facts/ doesn't have the files, try engines/ directory
    engines_dir = os.path.join(os.path.dirname(os.path.dirname(report_dir)), "engines")
    fact_tab_data = []  # (tab_id, label, tooltip, html_content)
    for tab_id, label, tooltip, filename in FACT_TABS:
        fpath = os.path.join(facts_dir, filename)
        if not os.path.isfile(fpath):
            # Try engines/ as fallback
            fpath = os.path.join(engines_dir, filename)
        if os.path.isfile(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                md_content = f.read()
            html_content = markdown_to_fact_html(md_content)
            fact_tab_data.append((tab_id, label, tooltip, html_content))

    # ── Build HTML ───────────────────────────────────────────────────────────
    html = []
    html.append('<!DOCTYPE html>')
    html.append('<html><head><meta charset="utf-8" />')
    html.append('<meta name="viewport" content="width=device-width, initial-scale=1" />')
    html.append(f'<title>Assessment - {escape(component_display_name or component_name)}</title>')
    html.append('<style>')
    html.append(CSS)
    html.append('</style>')
    html.append(MERMAID_HEAD_SCRIPT)
    html.append('</head><body>')

    # Lightbox
    html.append('<div id="diagram-lightbox" class="diagram-lightbox" role="dialog" aria-modal="true">')
    html.append('  <button class="diagram-lightbox-close" id="diagram-lightbox-close" aria-label="Close">&#x2715;</button>')
    html.append('  <div class="diagram-lightbox-hint">Scroll to zoom &nbsp;&middot;&nbsp; Drag to pan &nbsp;&middot;&nbsp; Double-click to reset</div>')
    html.append('  <div class="diagram-lightbox-inner" id="diagram-lightbox-inner"></div>')
    html.append('</div>')

    html.append('<div class="main">')
    html.append(f'<h1>{escape(component_display_name or component_name)}</h1>')

    # App info card
    html.append('<div class="report-card">')
    html.append('  <h2>Application Information</h2>')
    html.append('  <div class="report-card-body">')
    html.append('    <div class="app-info-container">')
    html.append('      <div class="app-info-column">')
    html.append(f'        <div class="app-info-row"><span class="app-info-label">Application Name</span><span class="app-info-value">{escape(component_display_name or component_name)}</span></div>')
    if jdk_version:
        html.append(f'        <div class="app-info-row"><span class="app-info-label">Java Version</span><span class="app-info-value">{escape(jdk_version)}</span></div>')
    html.append(f'        <div class="app-info-row"><span class="app-info-label">Effort</span><span class="app-info-value" id="effort-display">{escape(effort_display)}</span></div>')
    html.append('      </div>')
    html.append('      <div class="app-info-column">')
    html.append(f'        <div class="app-info-row"><span class="app-info-label">Build Tools</span><span class="app-info-value">{escape(build_tools)}</span></div>')
    html.append(f'        <div class="app-info-row"><span class="app-info-label">Frameworks</span><span class="app-info-value">{escape(frameworks)}</span></div>')
    html.append('      </div>')
    html.append('    </div>')
    html.append('  </div>')
    html.append('</div>')

    # Tab navigation
    html.append('<nav class="tab-nav">')
    html.append('  <button class="tab-btn active" data-tab="tab-issues" data-tooltip="Issues detected in the source code">Issues</button>')
    for tab_id, label, tooltip, _ in fact_tab_data:
        html.append(f'  <button class="tab-btn" data-tab="{tab_id}" data-tooltip="{escape(tooltip)}">{escape(label)}</button>')
    html.append('</nav>')

    # Issues tab panel
    html.append('<div id="tab-issues" class="tab-panel active">')

    # Target dropdown
    if target_display_names and target_ids:
        html.append('<div class="target-select-container">')
        html.append('  <label for="target-select">Target Compute Service:</label>')
        html.append('  <select id="target-select" onchange="onTargetChange(this.value)">')
        count = min(len(target_display_names), len(target_ids))
        for idx in range(count):
            html.append(f'    <option value="{escape(target_ids[idx])}">{escape(target_display_names[idx])}</option>')
        html.append('  </select>')
        html.append('</div>')

    # Issue Summary card
    html.append('<div class="report-card">')
    html.append('  <h2>Issue Summary</h2>')
    html.append('  <div class="report-card-body">')
    html.append('    <div class="domain-summary-container" id="donut-container">')

    def render_domain_donut(title, m, p, o):
        total = m + p + o
        html.append('      <div class="domain-summary-item">')
        html.append(build_donut_svg(m, p, o))
        html.append(f'        <h3>{escape(title)}</h3>')
        html.append(f'        <div class="count">{total} issue{"s" if total != 1 else ""}</div>')
        html.append('      </div>')

    if cloud_groups:
        render_domain_donut("Cloud Readiness", *cloud_crit)
    if upgrade_groups or rearchitect_findings:
        render_domain_donut(upgrade_domain_name, *upgrade_crit)
    if security_findings:
        render_domain_donut("Security", *security_crit)

    html.append('    </div>')
    html.append('    <div class="criticality-legend">')
    html.append('      <div class="legend-item"><span class="legend-swatch" style="background:var(--color-mandatory)"></span>Mandatory</div>')
    html.append('      <div class="legend-item"><span class="legend-swatch" style="background:var(--color-potential)"></span>Potential</div>')
    html.append('      <div class="legend-item"><span class="legend-swatch" style="background:var(--color-optional)"></span>Optional</div>')
    html.append('    </div>')
    html.append('  </div>')
    html.append('</div>')

    # Filter bar
    available_domains = []
    if cloud_groups:
        available_domains.append(("cloud-readiness", "Cloud Readiness"))
    if upgrade_groups:
        available_domains.append(("java-upgrade", upgrade_domain_name))
    if security_findings:
        available_domains.append(("security", "Security"))

    available_crits = set()
    for rid, _ in cloud_groups + upgrade_groups:
        sev = rules.get(rid, {}).get("severity", "optional").strip().lower()
        available_crits.add(sev)
    for f in security_findings:
        available_crits.add(f.get("severity", "optional").strip().lower() or "optional")

    html.append('<div class="filter-bar" id="filter-bar">')
    if len(available_domains) > 1:
        html.append('  <div class="multi-select" id="domain-ms">')
        html.append('    <button class="multi-select-btn" onclick="toggleMultiSelect(\'domain-ms\')">Domain</button>')
        html.append('    <div class="multi-select-dropdown">')
        for did, dlabel in available_domains:
            html.append(f'      <label class="multi-select-option"><input type="checkbox" value="{escape(did)}" onchange="onMultiSelectChange(\'domain-ms\',\'Domain\')"/> {escape(dlabel)}</label>')
        html.append('    </div>')
        html.append('  </div>')
    if len(available_crits) > 1:
        html.append('  <div class="multi-select" id="criticality-ms">')
        html.append('    <button class="multi-select-btn" onclick="toggleMultiSelect(\'criticality-ms\')">Criticality</button>')
        html.append('    <div class="multi-select-dropdown">')
        for c in ["mandatory", "potential", "optional"]:
            if c in available_crits:
                html.append(f'      <label class="multi-select-option"><input type="checkbox" value="{c}" onchange="onMultiSelectChange(\'criticality-ms\',\'Criticality\')"/> {c.capitalize()}</label>')
        html.append('    </div>')
        html.append('  </div>')
    html.append('  <a class="clear-filters" href="javascript:void(0)" onclick="clearAllFilters()">Clear all</a>')
    html.append('</div>')

    # Issue sections
    def render_issue_section(section_title, groups, domain_id, badge_html=None, extra_rearchitect=None):
        if not groups and not extra_rearchitect:
            return
        html.append(f'<div class="issue-section" data-domain="{domain_id}">')
        badge = badge_html or ""
        html.append(f'  <h2>{escape(section_title)}{badge}</h2>')
        html.append('  <table class="issue-table">')
        html.append('    <colgroup><col class="col-issue"/><col class="col-criticality"/><col class="col-storypoint"/></colgroup>')
        html.append('    <thead><tr><th>Issue Category</th><th>Criticality</th><th>Story Point</th></tr></thead>')
        html.append('    <tbody>')

        # Sort by severity rank then count desc
        ordered = sorted(groups, key=lambda g: (get_severity_rank(rules.get(g[0], {}).get("severity", "")), -len(g[1])))

        section_no_spaces = section_title.replace(" ", "").lower()
        for gi, (rule_id, incs) in enumerate(ordered):
            rule_obj = rules.get(rule_id, {})
            title = rule_obj.get("title", rule_id)
            severity = rule_obj.get("severity", "").strip().lower()
            first_inc = incs[0]

            # Get AKS effort from first incident
            story_point = 0
            targets_data = first_inc.get("targets", {})
            for tid, tdata in targets_data.items():
                if "aks" in tid.lower() or "kubernetes" in tid.lower():
                    story_point = tdata.get("effort", 0)
                    break
            if story_point == 0:
                story_point = rule_obj.get("effort", 0) or 0

            row_id = f"row-{section_no_spaces}-{gi}"

            if severity == "mandatory":
                crit_text, crit_css = "Mandatory", "crit-square-mandatory"
            elif severity == "potential":
                crit_text, crit_css = "Potential", "crit-square-potential"
            else:
                crit_text, crit_css = "Optional", "crit-square-optional"

            # Build targets JSON
            targets_json_obj = {}
            for tid, tdata in targets_data.items():
                targets_json_obj[tid] = {"effort": tdata.get("effort", 0), "severity": tdata.get("severity")}
            targets_json_str = json.dumps(targets_json_obj, separators=(',', ':'))

            html.append(f"    <tr class=\"issue-row\" data-criticality=\"{severity}\" data-targets='{escape(targets_json_str)}' data-default-effort=\"{story_point}\" data-default-severity=\"{severity}\" data-rule=\"{escape(rule_id)}\" onclick=\"toggleRow('{row_id}', this)\" style=\"cursor:pointer;\">")
            html.append(f'      <td style="white-space:normal;"><div class="issue-title-cell"><button class="expand-btn" id="btn-{row_id}">&#x276F;</button> {escape(title)}</div></td>')
            html.append(f'      <td class="crit-cell"><span class="crit-label"><span class="crit-square {crit_css}"></span>{crit_text}</span></td>')
            html.append(f'      <td class="sp-cell">{story_point}</td>')
            html.append('    </tr>')

            # Detail row
            incidents_with_loc = [inc for inc in incs if inc.get("location")]
            html.append(f'    <tr class="detail-row" id="{row_id}" style="display:none;">')
            html.append('      <td colspan="3">')
            html.append('        <div class="detail-content">')
            html.append('          <div class="file-list">')
            html.append('            <table><colgroup><col style="width:70%"/><col style="width:30%"/></colgroup>')
            html.append('            <thead><tr><th>File</th><th>Position</th></tr></thead><tbody>')
            for inc in incidents_with_loc:
                fp = inc.get("location", "")
                line = inc.get("line")
                line_text = f"Line {line}" if line else ""
                html.append(f'            <tr><td><span class="file-path" title="{escape(fp)}">{escape(fp)}</span></td><td><span class="position">{line_text}</span></td></tr>')
            html.append('            </tbody></table>')
            html.append('          </div>')

            description = rule_obj.get("description", "")
            if description:
                html.append('          <div class="explanation-panel">')
                html.append('            <h4>Explanation</h4>')
                html.append(f'            <div>{simple_markdown_to_html(description)}</div>')
                html.append('          </div>')

            html.append('        </div>')
            html.append('      </td>')
            html.append('    </tr>')

        # Rearchitect findings
        if extra_rearchitect:
            for ri, finding in enumerate(extra_rearchitect):
                row_id = f"row-{section_no_spaces}-rearch-{ri}"
                old_val = finding.get("old", "")
                explanation = finding.get("explanation", "")
                detected_in = finding.get("detectedIn", {})
                all_files = (detected_in.get("configFiles") or []) + (detected_in.get("sourceFiles") or [])

                html.append(f'    <tr class="issue-row" data-criticality="optional" data-targets=\'{{}}\' onclick="toggleRow(\'{row_id}\', this)" style="cursor:pointer;">')
                html.append(f'      <td style="white-space:normal;"><div class="issue-title-cell"><button class="expand-btn" id="btn-{row_id}">&#x276F;</button> Framework obsoletion ({escape(old_val)})</div></td>')
                html.append(f'      <td><span class="crit-label"><span class="crit-square crit-square-optional"></span>Optional</span></td>')
                html.append(f'      <td class="sp-cell">10</td>')
                html.append('    </tr>')
                html.append(f'    <tr class="detail-row" id="{row_id}" style="display:none;">')
                html.append('      <td colspan="3">')
                html.append('        <div class="detail-content">')
                if all_files:
                    html.append('          <div class="file-list">')
                    html.append('            <table><colgroup><col style="width:70%"/><col style="width:30%"/></colgroup>')
                    html.append('            <thead><tr><th>File</th><th>Position</th></tr></thead><tbody>')
                    for fp in all_files:
                        html.append(f'            <tr><td><span class="file-path" title="{escape(fp)}">{escape(fp)}</span></td><td></td></tr>')
                    html.append('            </tbody></table>')
                    html.append('          </div>')
                if explanation:
                    html.append('          <div class="explanation-panel">')
                    html.append('            <h4>Explanation</h4>')
                    html.append(f'            <p>{escape(explanation)}</p>')
                    html.append('          </div>')
                html.append('        </div>')
                html.append('      </td>')
                html.append('    </tr>')

        html.append('    </tbody>')
        html.append('  </table>')
        html.append('</div>')

    render_issue_section("Cloud Readiness", cloud_groups, "cloud-readiness")
    render_issue_section(upgrade_domain_name, upgrade_groups, "java-upgrade", extra_rearchitect=rearchitect_findings)

    # Security section
    if security_findings:
        html.append('<div class="issue-section" data-domain="security">')
        html.append('  <h2>Security <span class="badge-experimental" title="These issues were generated by AI and may contain inaccuracies or incomplete information. Please review carefully.">Experimental</span></h2>')
        html.append('  <table class="issue-table">')
        html.append('    <colgroup><col class="col-issue"/><col class="col-criticality"/><col class="col-storypoint"/></colgroup>')
        html.append('    <thead><tr><th>Issue Category</th><th>Criticality</th><th>Story Point</th></tr></thead>')
        html.append('    <tbody>')

        ordered_sec = sorted(security_findings, key=lambda f: (get_severity_rank(f.get("severity", "")), -f.get("storyPoint", 0)))
        for fi, finding in enumerate(ordered_sec):
            row_id = f"row-security-{fi}"
            sev = finding.get("severity", "").strip().lower()
            if sev == "mandatory":
                crit_text, crit_css = "Mandatory", "crit-square-mandatory"
            elif sev == "potential":
                crit_text, crit_css = "Potential", "crit-square-potential"
            else:
                crit_text, crit_css = "Optional", "crit-square-optional"

            fid = finding.get("id", "")
            ftitle = finding.get("title", "")
            display_name = f"{fid}: {ftitle}" if ftitle else fid
            sp = finding.get("storyPoint", 0)

            html.append(f'    <tr class="issue-row" data-criticality="{sev}" onclick="toggleRow(\'{row_id}\', this)" style="cursor:pointer;">')
            html.append(f'      <td style="white-space:normal;"><div class="issue-title-cell"><button class="expand-btn" id="btn-{row_id}">&#x276F;</button> {escape(display_name)}</div></td>')
            html.append(f'      <td class="crit-cell"><span class="crit-label"><span class="crit-square {crit_css}"></span>{crit_text}</span></td>')
            html.append(f'      <td class="sp-cell">{sp}</td>')
            html.append('    </tr>')

            html.append(f'    <tr class="detail-row" id="{row_id}" style="display:none;">')
            html.append('      <td colspan="3">')
            html.append('        <div class="detail-content">')
            html.append('          <div class="file-list">')
            html.append('            <table><thead><tr><th>File</th></tr></thead><tbody>')
            evidence = finding.get("evidence", {})
            files = evidence.get("files", []) if isinstance(evidence, dict) else []
            for fp in files:
                html.append(f'            <tr><td><span class="file-path" title="{escape(fp)}">{escape(fp)}</span></td></tr>')
            html.append('            </tbody></table>')
            html.append('          </div>')
            desc = finding.get("description", "")
            if desc:
                html.append('          <div class="explanation-panel">')
                html.append('            <h4>Explanation</h4>')
                html.append(f'            <div>{simple_markdown_to_html(desc)}</div>')
                html.append('          </div>')
            html.append('        </div>')
            html.append('      </td>')
            html.append('    </tr>')

        html.append('    </tbody>')
        html.append('  </table>')
        html.append('</div>')

    html.append('</div><!-- #tab-issues -->')

    # Fact tab panels
    for tab_id, _, _, content in fact_tab_data:
        html.append(f'<div id="{tab_id}" class="tab-panel">')
        html.append(f'  <div class="fact-content">{content}</div>')
        html.append('</div>')

    # Footer
    html.append('<p class="footer">Your feedback is invaluable &mdash; <a href="https://aka.ms/ghcp-appmod/feedback">Share feedback</a></p>')

    # Script
    html.append('<script>')
    html.append(MAIN_SCRIPT)
    html.append('</script>')

    # Initial target change
    if target_ids:
        html.append(f"<script>document.addEventListener('DOMContentLoaded', function() {{ onTargetChange('{escape(target_ids[0])}'); }});</script>")

    html.append('</div></body></html>')

    return '\n'.join(html)


def generate_from_js_markdown(report_dir):
    """Generate report.html from js-assessment-report.md (JS/TS)."""
    # Look for js-assessment-report.md in report_dir or parent directories
    md_path = None
    search_dir = report_dir
    for _ in range(5):
        candidate = os.path.join(search_dir, "js-assessment-report.md")
        if os.path.isfile(candidate):
            md_path = candidate
            break
        search_dir = os.path.dirname(search_dir)

    if not md_path:
        print("Error: js-assessment-report.md not found", file=sys.stderr)
        sys.exit(1)

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract title from first heading
    title_match = re.match(r'^#\s+(.+)', md_content)
    title = title_match.group(1) if title_match else "Assessment Report"

    fact_html = markdown_to_fact_html(md_content)

    html = []
    html.append('<!DOCTYPE html>')
    html.append('<html><head><meta charset="utf-8" />')
    html.append('<meta name="viewport" content="width=device-width, initial-scale=1" />')
    html.append(f'<title>Assessment - {escape(title)}</title>')
    html.append('<style>')
    html.append(CSS)
    html.append('</style>')
    html.append(MERMAID_HEAD_SCRIPT)
    html.append('</head><body>')
    html.append('<div id="diagram-lightbox" class="diagram-lightbox" role="dialog" aria-modal="true">')
    html.append('  <button class="diagram-lightbox-close" id="diagram-lightbox-close" aria-label="Close">&#x2715;</button>')
    html.append('  <div class="diagram-lightbox-hint">Scroll to zoom &nbsp;&middot;&nbsp; Drag to pan &nbsp;&middot;&nbsp; Double-click to reset</div>')
    html.append('  <div class="diagram-lightbox-inner" id="diagram-lightbox-inner"></div>')
    html.append('</div>')
    html.append('<div class="main">')
    html.append(f'<h1>{escape(title)}</h1>')
    html.append(f'<div class="fact-content">{fact_html}</div>')
    html.append('<p class="footer">Your feedback is invaluable &mdash; <a href="https://aka.ms/ghcp-appmod/feedback">Share feedback</a></p>')
    html.append('<script>')
    html.append(MAIN_SCRIPT)
    html.append('</script>')
    html.append('</div></body></html>')

    return '\n'.join(html)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report_html.py /path/to/report-directory", file=sys.stderr)
        sys.exit(1)

    report_dir = sys.argv[1]
    if not os.path.isdir(report_dir):
        print(f"Error: Directory not found: {report_dir}", file=sys.stderr)
        sys.exit(1)

    report_json_path = os.path.join(report_dir, "report.json")

    if os.path.isfile(report_json_path):
        output = generate_from_report_json(report_dir)
    else:
        # Look for JS/TS markdown
        output = generate_from_js_markdown(report_dir)

    output_path = os.path.join(report_dir, "report.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
