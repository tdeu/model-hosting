from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        if self.path.endswith('.json'):
            self.send_header('Content-Type', 'application/json')
        elif self.path.endswith('.bin'):
            self.send_header('Content-Type', 'application/octet-stream')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(__file__)))  # Change to repo root
    server = HTTPServer(('localhost', 8000), CORSRequestHandler)
    print('Starting server at http://localhost:8000')
    server.serve_forever() 