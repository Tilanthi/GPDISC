#!/usr/bin/env python3
"""
GPDISC standalone app launcher (2026-09-04).

Runs the consultation front door as a resident local process: one
interpreter, one pre-warmed ConsultationPipeline, a private web UI in
the browser. No LLM anywhere at runtime — every answer is produced by
the deterministic clinical reasoning core on this machine, offline.

Designed to be bundled with PyInstaller (see build_mac.sh) but runs
plain from the repo too:   python3 app/gpdisc_app.py

Privacy: the server binds 127.0.0.1 only. Nothing is transmitted off
this machine. Session history lives in the browser tab's memory and is
gone when the tab closes.
"""
import json
import logging
import os
import signal
import socket
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PORTS = [8790, 8791, 8792, 8793, 8794]  # first free port wins
HOST = "127.0.0.1"                       # local-only, never 0.0.0.0

# Plain-run mode: make the repo root importable (the PyInstaller bundle
# already carries gpdisc_core, so skip when frozen).
if not getattr(sys, "frozen", False):
    sys.path.insert(0, str(APP_DIR.parent))

# --- logging: windowed .app builds have no console, so log to file ---
LOG_DIR = Path.home() / "Library" / "Logs" / "GPDISC"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "app.log"),
              logging.StreamHandler(sys.stderr)],
)
log = logging.getLogger("gpdisc.app")

# Set by the UI quit button and SIGTERM; the main loop exits when it is.
# (server.shutdown() alone only stops serving — the process used to
# linger as a zombie, squatting on nothing while the next launch took
# the next port.)
SHUTDOWN = threading.Event()


# --- the engine: ONE pipeline for the app's lifetime (pre-warm) -----
_PIPELINE = None


def pipeline():
    """Lazy singleton. The first consultation pays the import + table
    build; every later one is milliseconds. The interaction checker is
    itself a lazy singleton inside the pipeline (2026-09-04 fix)."""
    global _PIPELINE
    if _PIPELINE is None:
        from gpdisc_core.clinical_reasoning import ConsultationPipeline
        _PIPELINE = ConsultationPipeline()
    return _PIPELINE


def run_consultation(presentation: str) -> dict:
    """Run one consultation. Local only; no external calls of any kind."""
    rec = pipeline().run(presentation, {})
    return {
        "presenting_complaint": rec.presenting_complaint,
        "escalation": rec.escalation,
        "summary": rec.summary(),
        "ranked_differential": rec.ranked_differential,
        "dangerous_alternatives": rec.dangerous_alternatives,
        "discriminating_questions": getattr(
            rec, "discriminating_questions", []),
        "investigations": rec.investigation_strategy,
        "treatment": rec.treatment,
        "referral": rec.referral,
        "safety_net": rec.safety_net,
        "uncertainty": rec.uncertainty,
        "outside_scope": rec.outside_scope,
        "validation_passed": (rec.validation.passed
                              if rec.validation is not None else None),
        "ruleset": getattr(rec, "ruleset", ""),
    }


class GPDISCAppHandler(SimpleHTTPRequestHandler):
    """Serves the consultation UI and the local JSON API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    # -- API ----------------------------------------------------------
    def do_POST(self):
        if self.path == "/api/consult":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length) or b"{}")
                presentation = str(body.get("presentation", ""))[:2000]
                if not presentation.strip():
                    payload, status = {"error": "presentation required"}, 400
                else:
                    payload, status = run_consultation(presentation), 200
            except Exception as exc:  # never crash the server on input
                payload, status = {"error": f"consultation failed: {exc}"}, 500
            self._json(payload, status)
            return

        if self.path == "/api/quit":
            self._json({"bye": True}, 200)
            log.info("quit requested from the UI — shutting down")
            SHUTDOWN.set()
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return

        self._json({"error": "not found"}, 404)

    def do_GET(self):
        if self.path == "/api/status":
            from gpdisc_core.clinical_reasoning.knowledge import CONDITIONS
            self._json({
                "engine": "GPDISC clinical reasoning core",
                "conditions": len(CONDITIONS),
                "status": "running",
                "local_only": True,
            }, 200)
            return
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def _json(self, payload, status):
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        log.info("%s", fmt % args)


def first_free_port() -> int:
    for port in PORTS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((HOST, port)) != 0:   # nothing listening
                return port
    raise SystemExit("No free port in " + str(PORTS))


def main() -> int:
    # Pre-warm FIRST, single-threaded, before the server can accept a
    # request: two threads importing the package simultaneously can
    # deadlock on the module locks, and the first question must be as
    # fast as every other one.
    pipeline()
    log.info("pipeline warm")

    port = first_free_port()
    server = ThreadingHTTPServer((HOST, port), GPDISCAppHandler)
    url = f"http://{HOST}:{port}/"

    def _stop(*_):
        SHUTDOWN.set()
        threading.Thread(target=server.shutdown, daemon=True).start()

    # SIGTERM (Dock quit / logout) shuts down cleanly AND exits
    signal.signal(signal.SIGTERM, _stop)

    threading.Thread(target=server.serve_forever, daemon=True).start()
    log.info("GPDISC app listening on %s", url)

    webbrowser.open(url)
    try:
        while not SHUTDOWN.wait(3600):
            pass
    except (KeyboardInterrupt, OSError):
        pass
    finally:
        server.shutdown()
        server.server_close()
        log.info("GPDISC app stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
