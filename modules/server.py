import os
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

def start_server():
    port = 8000

    # Open the browser after starting the server
    def open_browser():
        url = f"http://localhost:{port}"
        webbrowser.open(url)

    # Serve current directory with http.server
    def run_server():
        os.chdir("C:\\Users\\anubh\\OneDrive\\Desktop\\Projects\\Cohesive-Ai\\website")  # Change to project directory
        httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
        # print(f"Serving at {url}")
        httpd.serve_forever()

    # Run the server and open the browser in parallel
    threading.Thread(target=open_browser).start()
    run_server()

if __name__ == '__main__':
    start_server()