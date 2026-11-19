/* Device Mockups · linked navigation helper.
   Add to any site you preview:  <script src="https://dclemares.github.io/device-mockups/sync.js"></script>
   When the page runs inside a mockup frame it tells the mockup page its URL, so the other device follows. */
(function(){
  if (window.parent === window) return;
  var last = '';
  function post(){
    if (location.href === last) return;
    last = location.href;
    try { parent.postMessage({ type: 'dm:nav', href: location.href }, '*'); } catch (e) {}
  }
  ['pushState','replaceState'].forEach(function(m){
    var orig = history[m];
    history[m] = function(){ var r = orig.apply(this, arguments); setTimeout(post); return r; };
  });
  addEventListener('popstate', post);
  addEventListener('hashchange', post);
  // keep "new tab" links inside the mockup so both devices move together
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[target=_blank]');
    if (a && a.href && !e.defaultPrevented) { e.preventDefault(); location.href = a.href; }
  });
  post();
  setInterval(post, 500);
})();
