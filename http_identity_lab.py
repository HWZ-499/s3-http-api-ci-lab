from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json

# 实验用 Token 映射表
TOKENS = {
    "token-alice": "alice",
    "token-bob": "bob",
    "token-admin": "admin",
}

DOCUMENT_OWNERS = {
    "42": "alice",
    "43": "bob",
    "44": "admin",
}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):

        has_auth = "Authorization" in self.headers

        print(
            f"has_authorization_header={has_auth}",
            flush=True
        )

        auth = self.headers.get("Authorization", "")

        if auth.startswith("Bearer "):
            token = auth.removeprefix("Bearer ")
        else:
            token = None

        user = TOKENS.get(token)

        if user is None:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"unauthorized\n")
            return

        if not self.path.startswith("/documents/"):
            self.send_response(404)
            self.end_headers()
            return

        document_id = self.path.removeprefix("/documents/")

        document_owner = DOCUMENT_OWNERS.get(document_id)

        if user == "admin":
            if document_owner is None:
                self.send_response(404)
                self.end_headers()
                return
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"admin access granted\n")
            return

        if document_owner is None:
            self.send_response(404)
            self.end_headers()
            return

        if user != document_owner:
            self.send_response(404)
            self.end_headers()
            return

        claimed_user = self.headers.get(
            "X-User-ID", "anonymous"
        )

        response = (
            f"authenticated_user={user}\n"
            f"claimed_user={claimed_user}\n"
        )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))


# Read effective runtime binding from local service configuration.
settings = json.loads(
    Path(__file__).with_name("service_settings.json").read_text(encoding="utf-8")
)
HTTPServer((settings["bind_host"], settings["bind_port"]), Handler).serve_forever()
