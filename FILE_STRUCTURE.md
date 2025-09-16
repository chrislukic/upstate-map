# Scenic NY Map - File Structure

## Overview
The map has been separated into modular files for better organization and maintainability.

## Files

### Core Files (Data-Driven)
- **`index.html`** - Main HTML file with clean structure
- **`styles.css`** - All CSS styles and responsive design
- **`map-renderer.js`** - JavaScript class that loads and renders map from JSON data
- **`map-data.json`** - All map data (scenic areas, cities, train routes, coordinates, scores, drive times, travel times)

### Legacy Files (Backup)
- **`map.js`** - Original JavaScript code (99KB - now replaced by data-driven approach)

### Original Files (Backup)
- **`ny_hiking_map_polygons_times_centers.html`** - Original monolithic HTML file
- **`index_clean.html`** - Clean HTML template (backup)

### Utility Files
- **`start_server.bat`** - Windows batch file to start web server
- **`start_server.sh`** - Unix shell script to start web server
- **`copy_and_serve.py`** - Python script to copy and serve files

## File Sizes
- **Original HTML**: ~102KB (monolithic)
- **New HTML**: ~3KB (clean structure)
- **CSS**: ~1.3KB (styles only)
- **JSON Data**: ~33KB (all map data including train routes)
- **JavaScript Renderer**: ~6KB (data-driven rendering)
- **Legacy JavaScript**: ~99KB (original hardcoded approach)

## Benefits of Separation

### 1. **Maintainability**
- Easier to edit styles without touching JavaScript
- JavaScript logic is isolated and easier to debug
- HTML structure is clean and readable

### 2. **Performance**
- CSS can be cached separately
- JavaScript can be minified independently
- Better browser caching

### 3. **Development**
- Multiple developers can work on different files
- Version control shows cleaner diffs
- Easier to add new features

### 4. **Reusability**
- CSS styles can be reused across pages
- JavaScript functions can be modularized
- Components can be extracted

### 5. **Data Management** (NEW!)
- **Easy Updates**: Change scores, drive times, or add new locations in JSON
- **No Code Changes**: Update data without touching JavaScript
- **Structured Data**: Clear organization of scenic areas, cities, and train routes
- **API Ready**: JSON structure ready for backend integration
- **Version Control**: Clean diffs when updating data

### 6. **Transportation Options** (NEW!)
- **Train Routes**: 6 major passenger rail lines (Metro-North & Amtrak)
- **Travel Times**: Train travel times from NYC to all stops
- **Visual Distinction**: Different line styles for Metro-North vs Amtrak
- **Station Information**: Terminal vs regular station markers
- **Multi-Modal Planning**: Compare driving vs train options

## Usage

### Start the Web Server
```bash
# Windows
start_server.bat

# Unix/Mac
chmod +x start_server.sh && ./start_server.sh

# Manual
python -m http.server 8000
```

### Access the Map
Open your browser to: `http://localhost:8000`

## Features
- ✅ Interactive map with scenic area polygons
- ✅ City markers with population and drive times
- ✅ Responsive design for mobile devices
- ✅ Full-screen map capability
- ✅ Hover tooltips with detailed information
- ✅ Color-coded scenic quality ratings
- ✅ Drive times from NYC for all locations

## Browser Compatibility
- Modern browsers with ES6 support
- Mobile responsive design
- Touch-friendly interface
