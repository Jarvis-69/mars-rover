import http.server
import socketserver
import os

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), 'web') # Optional: Serve files from a 'web' subdirectory

# Create a dummy index.html in the web directory if it doesn't exist
# In a real scenario, you'd have your actual web files here.
if not os.path.exists(WEB_DIR):
    os.makedirs(WEB_DIR)
index_path = os.path.join(WEB_DIR, 'index.html')
if not os.path.exists(index_path):
    with open(index_path, 'w') as f:
        f.write('<html><body><h1>Python Server Running!</h1></body></html>')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

print(f"Serving files from '{WEB_DIR}' directory")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()