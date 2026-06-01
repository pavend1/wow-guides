/**
 * Fallback Wowhead tooltips (nether API + universal.css) when power.js CDN is blocked.
 */
(function () {
  "use strict";

  var LOCALE = 7;
  var CSS_CDN = "https://wow.zamimg.com/css/universal.css?19";
  var cache = Object.create(null);
  var tipEl = null;
  var activeLink = null;
  var hideTimer = null;
  var enabled = false;

  function powerReady() {
    return typeof window.WH !== "undefined";
  }

  function parseWowheadLink(href) {
    if (!href || href.indexOf("wowhead.com") === -1) return null;
    var m = href.match(/wowhead\.com\/(?:[a-z]{2}\/)?(spell|item|achievement|npc|zone|quest)=(\d+)/i);
    if (!m) return null;
    return { kind: m[1].toLowerCase(), id: m[2] };
  }

  function fixTooltipHtml(html) {
    return html
      .replace(/src=(["'])\/\/wow\.zamimg\.com/gi, "src=$1https://wow.zamimg.com")
      .replace(/url\(\s*\/\/wow\.zamimg\.com/gi, "url(https://wow.zamimg.com");
  }

  function ensureWowheadCss() {
    if (document.getElementById("wowhead-universal-css")) return;
    var link = document.createElement("link");
    link.id = "wowhead-universal-css";
    link.rel = "stylesheet";
    link.href = CSS_CDN;
    document.head.appendChild(link);
  }

  function ensureTipEl() {
    if (tipEl) return tipEl;
    tipEl = document.createElement("div");
    tipEl.id = "wowhead-fallback-tip";
    tipEl.className = "wowhead-tooltip";
    tipEl.setAttribute("role", "tooltip");
    tipEl.style.position = "fixed";
    tipEl.style.visibility = "visible";
    tipEl.style.pointerEvents = "none";
    tipEl.style.zIndex = "2147483647";
    document.body.appendChild(tipEl);
    return tipEl;
  }

  function hideTip() {
    if (hideTimer) {
      clearTimeout(hideTimer);
      hideTimer = null;
    }
    if (tipEl) {
      tipEl.style.display = "none";
      tipEl.innerHTML = "";
    }
    activeLink = null;
  }

  function positionTip(ev) {
    if (!tipEl) return;
    var pad = 14;
    var x = ev.clientX + pad;
    var y = ev.clientY + pad;
    tipEl.style.display = "block";
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
        var html = fixTooltipHtml(data.tooltip || data.tooltip2 || "");
        cache[key] = html;
        return html;
      });
  }

  function showTip(link, html, ev) {
    ensureWowheadCss();
    var el = ensureTipEl();
    el.innerHTML = html;
    el.style.display = "block";
    activeLink = link;
    positionTip(ev);
  }

  function enable() {
    if (enabled || powerReady()) return;
    enabled = true;
  }

  document.addEventListener(
    "mouseover",
    function (ev) {
      if (!enabled || powerReady()) return;
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
          if (!enabled || powerReady() || !html) return;
          var still = ev.target.closest && ev.target.closest('a[href*="wowhead.com"]');
          if (still !== link) return;
          showTip(link, html, ev);
        })
        .catch(function () {});
    },
    true
  );

  document.addEventListener(
    "mousemove",
    function (ev) {
      if (!enabled || !tipEl || tipEl.style.display === "none") return;
      var link = ev.target.closest && ev.target.closest('a[href*="wowhead.com"]');
      if (link && link === activeLink) positionTip(ev);
    },
    true
  );

  document.addEventListener(
    "mouseout",
    function (ev) {
      if (!enabled) return;
      var link = ev.target.closest && ev.target.closest('a[href*="wowhead.com"]');
      if (!link || link !== activeLink) return;
      var rel = ev.relatedTarget;
      if (rel && (link.contains(rel) || (tipEl && tipEl.contains(rel)))) return;
      hideTimer = setTimeout(hideTip, 80);
    },
    true
  );

  function tryEnableFallback() {
    if (!powerReady()) enable();
  }

  window.setTimeout(tryEnableFallback, 2000);
})();
