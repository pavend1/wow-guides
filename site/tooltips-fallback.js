/**
 * Wowhead tooltips via nether API (works on GitHub Pages; no zamimg.com / power.js).
 * Links: https://www.wowhead.com/ru/spell=12345
 */
(function () {
  "use strict";

  var LOCALE = 7;
  var cache = Object.create(null);
  var tipEl = null;
  var activeLink = null;
  var hideTimer = null;

  function parseWowheadLink(href) {
    if (!href || href.indexOf("wowhead.com") === -1) return null;
    var m = href.match(/wowhead\.com\/(?:[a-z]{2}\/)?(spell|item|achievement|npc|zone|quest)=(\d+)/i);
    if (!m) return null;
    return { kind: m[1].toLowerCase(), id: m[2] };
  }

  function ensureTipEl() {
    if (tipEl) return tipEl;
    tipEl = document.createElement("div");
    tipEl.id = "wh-fallback-tooltip";
    tipEl.className = "wh-fallback-tooltip";
    tipEl.setAttribute("role", "tooltip");
    document.body.appendChild(tipEl);
    return tipEl;
  }

  function hideTip() {
    if (hideTimer) {
      clearTimeout(hideTimer);
      hideTimer = null;
    }
    if (tipEl) tipEl.style.display = "none";
    activeLink = null;
  }

  function positionTip(ev) {
    if (!tipEl) return;
    var pad = 12;
    var x = ev.clientX + pad;
    var y = ev.clientY + pad;
    var rect = tipEl.getBoundingClientRect();
    if (x + rect.width > window.innerWidth - pad) {
      x = ev.clientX - rect.width - pad;
    }
    if (y + rect.height > window.innerHeight - pad) {
      y = ev.clientY - rect.height - pad;
    }
    tipEl.style.left = Math.max(pad, x) + "px";
    tipEl.style.top = Math.max(pad, y) + "px";
  }

  function fetchTooltip(kind, id) {
    var key = kind + ":" + id;
    if (cache[key]) return Promise.resolve(cache[key]);
    var url =
      "https://nether.wowhead.com/tooltip/" +
      encodeURIComponent(kind) +
      "/" +
      encodeURIComponent(id) +
      "?locale=" +
      LOCALE;
    return fetch(url, { credentials: "omit", mode: "cors" })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then(function (data) {
        var html = data.tooltip || data.tooltip2 || "";
        cache[key] = html;
        return html;
      });
  }

  function showTip(link, html, ev) {
    var el = ensureTipEl();
    el.innerHTML = html;
    el.style.display = "block";
    activeLink = link;
    positionTip(ev);
  }

  document.addEventListener(
    "mouseover",
    function (ev) {
      var link = ev.target.closest && ev.target.closest('a[href*="wowhead.com"]');
      if (!link || link === activeLink) return;
      var parsed = parseWowheadLink(link.href);
      if (!parsed) return;

      if (hideTimer) {
        clearTimeout(hideTimer);
        hideTimer = null;
      }

      fetchTooltip(parsed.kind, parsed.id)
        .then(function (html) {
          if (!html || link !== ev.target.closest('a[href*="wowhead.com"]')) return;
          showTip(link, html, ev);
        })
        .catch(function () {
          /* CDN/API blocked — silent */
        });
    },
    true
  );

  document.addEventListener(
    "mousemove",
    function (ev) {
      if (!tipEl || tipEl.style.display === "none") return;
      var link = ev.target.closest && ev.target.closest('a[href*="wowhead.com"]');
      if (link && link === activeLink) positionTip(ev);
    },
    true
  );

  document.addEventListener(
    "mouseout",
    function (ev) {
      var link = ev.target.closest && ev.target.closest('a[href*="wowhead.com"]');
      if (!link || link !== activeLink) return;
      var rel = ev.relatedTarget;
      if (rel && (link.contains(rel) || (tipEl && tipEl.contains(rel)))) return;
      hideTimer = setTimeout(hideTip, 80);
    },
    true
  );
})();
