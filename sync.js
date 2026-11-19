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
  post();
  setInterval(post, 500);
})();
