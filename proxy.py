#!/usr/bin/env python3
"""Local proxy so cross-origin sites get linked navigation in Device Mockups.

    python3 proxy.py                      # proxies https://guest.chekin.com on :7806
    python3 proxy.py https://site.com 7807

It serves the target site from http://localhost:<port>, removes the headers that
block framing and injects sync.js into every HTML page.
Open http://localhost:<port>/__dm/ (the mockups page served by the proxy, so both
devices share its origin) and paste any URL of the target site.
"""
import http.server, socketserver, sys, urllib.request, urllib.error, os, ssl

TARGET = (sys.argv[1] if len(sys.argv) > 1 else "https://guest.chekin.com").rstrip("/")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 7806
HERE = os.path.dirname(os.path.abspath(__file__))
SYNC = open(os.path.join(HERE, "sync.js"), "rb").read()
TAG = b'<script src="/__dm/sync.js"></script>'
DROP = {"content-security-policy", "x-frame-options", "content-length", "content-encoding",
        "transfer-encoding", "connection", "strict-transport-security", "alt-svc"}
CTX = ssl.create_default_context()


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _proxy(self):
        if self.path == "/__dm" or self.path.startswith(("/__dm/?", "/__dm/index.html")) or self.path == "/__dm/":
            page = open(os.path.join(HERE, "index.html"), "rb").read()
            page = page.replace(b"</head>", b'<script>window.DM_PROXY_TARGET=' + repr(TARGET).encode() + b';</script></head>', 1)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(page)
            return
        if self.path == "/__dm/sync.js":
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(SYNC)
            return
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else None
        hdrs = {k: v for k, v in self.headers.items()
                if k.lower() not in ("host", "accept-encoding", "origin", "referer", "connection")}
        hdrs["Accept-Encoding"] = "identity"
        req = urllib.request.Request(TARGET + self.path, data=body, headers=hdrs, method=self.command)
        try:
            r = urllib.request.urlopen(req, context=CTX, timeout=30)
        except urllib.error.HTTPError as e:
            r = e
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
        if "text/html" in ctype:
            low = data.lower()
            i = low.find(b"</head>")
            data = data[:i] + TAG + data[i:] if i >= 0 else TAG + data
        self.send_response(r.status if hasattr(r, "status") else r.code)
        for k, v in r.headers.items():
            if k.lower() not in DROP:
                self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        if "text/html" in ctype:
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = _proxy


class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    print(f"Proxying {TARGET} on http://localhost:{PORT}")
    print(f"Open: http://localhost:{PORT}/__dm/  and paste any {TARGET} URL")
    S(("127.0.0.1", PORT), H).serve_forever()
