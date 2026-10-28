"""The real (HTTP) backend, tested against a stub OpenAI-compatible server on 127.0.0.1."""
import json
import os
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import _util  # noqa: F401
from lab import llm

SEEN = []


class Stub(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        SEEN.append((self.path, self.headers.get("Authorization"), body))
        msg = {"role": "assistant", "content": None, "tool_calls": [
            {"id": "c1", "type": "function",
             "function": {"name": "search_docs", "arguments": '{"query": "kettle"}'}}]}
        if body["messages"][-1]["role"] == "tool":
            msg = {"role": "assistant", "content": "Use vinegar."}
        data = json.dumps({"choices": [{"message": msg}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class HttpBackendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), Stub)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        SEEN.clear()
        self.old = dict(os.environ)
        os.environ["LLM_BASE_URL"] = f"http://127.0.0.1:{self.srv.server_port}/v1"
        os.environ["LLM_API_KEY"] = "test-key"
        os.environ["LLM_MODEL"] = "stub-model"

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old)

    def test_request_and_normalised_tool_call(self):
        m = llm.chat([{"role": "user", "content": "hi"}], tools=[{"type": "function"}],
                     temperature=0.7, max_tokens=50)
        path, auth, body = SEEN[0]
        self.assertEqual(path, "/v1/chat/completions")
        self.assertEqual(auth, "Bearer test-key")
        self.assertEqual((body["model"], body["temperature"], body["max_tokens"]),
                         ("stub-model", 0.7, 50))
        self.assertEqual(m["content"], "")                    # None -> ""
        self.assertEqual(m["tool_calls"][0]["function"]["name"], "search_docs")
        self.assertEqual(llm.model_label(), "stub-model")

    def test_full_sieve_loop_over_http(self):
        from lab.setup_lab import setup
        from lab.target import Sieve
        setup()
        t = Sieve().ask("How do I descale a kettle?")
        self.assertEqual(t.tool_calls[0]["name"], "search_docs")
        self.assertIn("kettle-descaling.md", t.tool_calls[0]["result"])
        self.assertEqual(t.output, "Use vinegar.")
        sent = SEEN[-1][2]["messages"]
        self.assertEqual(sent[-1]["role"], "tool")
        self.assertEqual(sent[-1]["tool_call_id"], "c1")

    def test_unreachable_server_raises_llmerror(self):
        os.environ["LLM_BASE_URL"] = "http://127.0.0.1:9/v1"
        with self.assertRaises(llm.LLMError):
            llm.chat([{"role": "user", "content": "hi"}])


if __name__ == "__main__":
    unittest.main()
