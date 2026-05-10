// Lazy-load Strudel REPL iframes when "Spielen" is clicked.
// Each .snippet has data-code-b64 with UTF-8 base64 of the code.
(function () {
  document.querySelectorAll('.snippet-play').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var snippet = btn.closest('.snippet');
      if (!snippet || snippet.classList.contains('playing')) return;
      var b64 = snippet.getAttribute('data-code-b64');
      if (!b64) return;
      var src = 'https://strudel.cc/#' + encodeURIComponent(b64);
      var iframe = document.createElement('iframe');
      iframe.setAttribute('src', src);
      iframe.setAttribute('title', 'Strudel REPL');
      iframe.setAttribute('allow', 'autoplay');
      iframe.setAttribute('loading', 'lazy');
      snippet.appendChild(iframe);
      snippet.classList.add('playing');
    });
  });
})();
