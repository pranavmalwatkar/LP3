import http.server
import socketserver
import requests
import threading

PORT = 8080
servers = ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]
lock = threading.Lock()
index = 0

class LoadBalancerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global index
        with lock:  # ensure round-robin is thread-safe
            target = servers[index % len(servers)]
            index += 1

        # forward the original request path to the backend and avoid connection reuse
        url = target + self.path
        try:
            response = requests.get(url, timeout=5, headers={"Connection": "close"})
            self.send_response(response.status_code)
            # copy simple headers
            content_type = response.headers.get("Content-Type", "text/html")
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(response.content)
            print(f"Forwarded to {target}")  # for debugging: shows round-robin sequence
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server error: {e}".encode())

if __name__ == "__main__":
    print(f"Load Balancer running on http://127.0.0.1:{PORT}")
    with socketserver.ThreadingTCPServer(("", PORT), LoadBalancerHandler) as httpd:
        httpd.serve_forever()
