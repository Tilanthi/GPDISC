#!/usr/bin/env python3
"""
GPDISC Dashboard Server
Serves the GPDISC Medical Consultation dashboard on port 8790

🚨 CRITICAL PRIVACY WARNING 🚨
YOU ARE ABSOLPUTELY FORBIDDEN FROM PUSHING ANY CODE, DATA, OR COMMITS TO GLENN'S GITHUB REPOSITORY.
THIS SYSTEM HANDLES SENSITIVE PATIENT MEDICAL DATA AND MUST REMAIN LOCAL-ONLY.
NO EXCEPTIONS WITHOUT EXPLICIT INSTRUCTION FROM GLENN.
"""

import http.server
import socketserver
import os
import json
import threading
import time
from pathlib import Path

# Configuration
PORT = 8790
DASHBOARD_DIR = Path(__file__).parent


def _clinical_corpus_stats():
    """Real corpus stats from the clinical reasoning core (never mock)."""
    try:
        from gpdisc_core.clinical_reasoning.knowledge import CONDITIONS
        cats = {}
        for c in CONDITIONS:
            cats[c.category] = cats.get(c.category, 0) + 1
        return {
            'total_conditions': len(CONDITIONS),
            'categories': len(cats),
            'category_counts': cats,
        }
    except Exception:
        return {'total_conditions': 0, 'categories': 0, 'category_counts': {}}


def _run_consultation(presentation):
    """Run the consultation pipeline — local only, no external calls."""
    from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
    rec = ConsultationPipeline().run(presentation, {})
    return {
        'presenting_complaint': rec.presenting_complaint,
        'escalation': rec.escalation,
        'summary': rec.summary(),
        'ranked_differential': rec.ranked_differential,
        'dangerous_alternatives': rec.dangerous_alternatives,
        'discriminating_questions': rec.discriminating_questions,
        'safety_net': rec.safety_net,
        'referral': rec.referral,
        'uncertainty': rec.uncertainty,
        'outside_scope': rec.outside_scope,
        'validation_passed': (rec.validation.passed
                              if rec.validation is not None else None),
    }


class GPDISCDashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for GPDISC medical consultation dashboard"""

    # GPDISC state
    cycle_count = 0
    discoveries = []
    corpus_stats = {
        'total_papers': 1300,
        'domains': 10,
        'arxiv_papers': 800,
        'openalex_papers': 500
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def do_POST(self):
        """POST /api/consult {"presentation": "..."} — the consultation
        endpoint. Runs entirely locally; nothing leaves this machine."""
        if self.path == '/api/consult':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(length) or b'{}')
                presentation = str(body.get('presentation', ''))[:2000]
                if not presentation.strip():
                    payload = {'error': 'presentation required'}
                    status = 400
                else:
                    payload = _run_consultation(presentation)
                    status = 200
            except Exception as exc:
                payload = {'error': f'consultation failed: {exc}'}
                status = 500
            self.send_response(status)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode())
            return
        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        # Serve the dashboard
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Increment cycle count to simulate activity
            GPDISCDashboardHandler.cycle_count += 1

            status_data = {
                'engine': {
                    'cycle_count': GPDISCDashboardHandler.cycle_count,
                    'system_confidence': 0.85 + (0.01 * (GPDISCDashboardHandler.cycle_count % 10)),
                    'status': 'running'
                },
                'corpus': _clinical_corpus_stats(),
                'timestamp': time.time()
            }
            self.wfile.write(json.dumps(status_data).encode())
            return

        elif self.path == '/api/discoveries':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Generate mock discoveries
            if len(GPDISCDashboardHandler.discoveries) < 5:
                domains = ['Molecular Biology', 'Biochemistry', 'Genetics', 'Cell Biology',
                          'Biophysics', 'Bioinformatics', 'Computational Biology', 'Genomics']
                import random
                discovery = {
                    'id': len(GPDISCDashboardHandler.discoveries) + 1,
                    'title': f'Novel {random.choice(domains)} insight discovered',
                    'domain': random.choice(domains),
                    'confidence': round(0.85 + random.random() * 0.14, 2),
                    'timestamp': time.time()
                }
                GPDISCDashboardHandler.discoveries.insert(0, discovery)

            discoveries_data = {
                'discoveries': GPDISCDashboardHandler.discoveries[:10],
                'total': len(GPDISCDashboardHandler.discoveries)
            }
            self.wfile.write(json.dumps(discoveries_data).encode())
            return

        return super().do_GET()

    def log_message(self, format, *args):
        """Custom log messages"""
        print(f"[GPDISC Medical Consultation Dashboard] {args[0]}")


class GPDISCDashboardServer:
    """GPDISC Medical Consultation Dashboard Server"""

    def __init__(self, port=PORT):
        self.port = port
        self.handler = GPDISCDashboardHandler
        self.server = None
        self.server_thread = None

    def start(self):
        """Start the dashboard server"""
        try:
            # Create server
            self.server = socketserver.TCPServer(("", self.port), self.handler)
            self.server.allow_reuse_address = True

            # Start in background thread
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()

            print(f"✓ GPDISC Medical Consultation Dashboard started successfully!")
            print(f"  Dashboard: http://localhost:{self.port}")
            print(f"  API: http://localhost:{self.port}/api/status")
            return True

        except Exception as e:
            print(f"✗ Failed to start dashboard: {e}")
            return False

    def stop(self):
        """Stop the dashboard server"""
        if self.server:
            self.server.shutdown()
            print("Dashboard stopped")


def start_dashboard(port=PORT):
    """Start the GPDISC Medical Consultation dashboard server"""
    server = GPDISCDashboardServer(port)
    return server.start()


if __name__ == '__main__':
    import sys

    # script-mode bootstrap: gpdisc_core imports need the repo root on path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

    port = PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}")
            print(f"Using default port: {PORT}")

    print("Starting GPDISC Medical Consultation Dashboard Server...")
    print("-" * 50)

    server = GPDISCDashboardServer(port)
    if server.start():
        print("-" * 50)
        print("Press Ctrl+C to stop...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping dashboard...")
            server.stop()
    else:
        print("Failed to start dashboard")
        sys.exit(1)
