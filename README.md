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
