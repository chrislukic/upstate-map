#!/bin/bash
echo "🌐 Starting web server on http://localhost:8000"
echo "📁 Serving files from public/ directory"
cd public
python3 -m http.server 8000

