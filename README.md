# Device Mockups

Paste a URL and preview it live inside desktop (1440×900) and mobile (390×844) mockups.

Live: https://dclemares.github.io/device-mockups/

Share a preview: `?url=https://example.com` (optional `&view=desktop|mobile`).

Note: sites that send X-Frame-Options or a frame-ancestors CSP cannot be embedded.

## Linked navigation

Navigating in one device makes the other follow. Pages on `dclemares.github.io` are synced automatically (same origin). For any other site, add:

```html
<script src="https://dclemares.github.io/device-mockups/sync.js"></script>
```

### Sites you can't edit (e.g. guest.chekin.com)

Browsers don't let a page see where a frame from another domain navigates, so run the local proxy. It serves the site and this mockups page from the same localhost origin:

```bash
python3 proxy.py https://guest.chekin.com 7806
```

Then open `http://localhost:7806/__dm/` and paste any `https://guest.chekin.com/...` URL — it's routed through the proxy automatically and both devices navigate together.
