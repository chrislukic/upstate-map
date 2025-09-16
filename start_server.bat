@echo off
echo Starting web server on http://localhost:8000
echo Serving files from public/ directory
cd public
python -m http.server 8000

