#!/usr/bin/env python3
import shutil
import http.server
import socketserver
import os

# Copy the file to index.html
shutil.copy('ny_hiking_map_polygons_times_centers.html', 'index.html')
print("✅ File copied to index.html")

# Start web server
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🌐 Web server started at http://localhost:{PORT}")
    print("📁 Serving files from current directory")
    print("🗺️  Open http://localhost:8000 to view your map")
    print("⏹️  Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

