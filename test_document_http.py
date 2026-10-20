import os
import unittest
from http.client import HTTPConnection


def request_status(token, document_id):
    headers = {}

    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    conn = HTTPConnection(
        "127.0.0.1",
        int(os.getenv("API_PORT", "18080")),
        timeout=3
    )

    try:
        conn.request(
            "GET",
            f"/documents/{document_id}",
            headers=headers
        )


        response = conn.getresponse()
        return response.status

    finally:
        conn.close()


class TestDocumentAPI(unittest.TestCase):

    def test_bob_reads_own_document(self):
        actual = request_status("token-bob", "43")
        self.assertEqual(actual, 200)

    def test_bob_cannot_read_alice_document(self):
        actual = request_status("token-bob", "42")
        self.assertEqual(actual, 404)

    def test_missing_authorization_header(self):
        actual = request_status(None, "42")
        self.assertEqual(actual, 401)

    def test_invalid_token_and_missing_document(self):
        actual = request_status("fake-token", "999")
        self.assertEqual(actual, 401)

    def test_admin_can_read_alice_document(self):
        actual = request_status("token-admin", "42")
        self.assertEqual(actual, 200)

    def test_admin_can_read_bob_document(self):
        actual = request_status("token-admin", "43")
        self.assertEqual(actual, 200)

    def test_admin_can_read_admin_document(self):
        actual = request_status("token-admin", "44")
        self.assertEqual(actual, 200)

    def test_admin_cannot_read_missing_document(self):
        actual = request_status("token-admin", "999")
        self.assertEqual(actual, 404)

    
if __name__ == "__main__":
    unittest.main()
