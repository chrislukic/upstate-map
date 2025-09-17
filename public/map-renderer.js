// Scenic NY Map Renderer
// Loads data from JSON and renders the interactive map

class ScenicNYMap {
    constructor() {
        this.map = null;
        this.data = null;
        this.scenicAreas = [];
        this.cities = [];
        this.layerControl = null; // layers control for overlays
        // Prefetched datasets
        this.waterfalls = null;
        this.breweries = null;
        this.restaurants = null;
        this.orchardPoints = null;
    }

    // Convert drive time string to color based on gradient
    getDriveTimeColor(driveTimeString) {
        // Parse drive time string (e.g., "2h 30m", "1h 15m", "45m")
        const timeMatch = driveTimeString.match(/(\d+)h?\s*(\d+)?m?/);
        if (!timeMatch) return "#000000"; // Default to black if parsing fails
        
        const hours = parseInt(timeMatch[1]) || 0;
        const minutes = parseInt(timeMatch[2]) || 0;
        const totalMinutes = hours * 60 + minutes;
        
        // Color transitions:
        // 0-3 hours: Green to Orange
        // 3-4 hours: Orange to Red  
        // 4+ hours: Red
        
        if (totalMinutes <= 180) { // 0-3 hours: Green to Orange
            const ratio = totalMinutes / 180; // 0 to 1
            const r = Math.round(34 + (255 - 34) * ratio); // 34 to 255
            const g = Math.round(139 + (165 - 139) * ratio); // 139 to 165
            const b = Math.round(34 + (0 - 34) * ratio); // 34 to 0
            return `rgb(${r}, ${g}, ${b})`;
        } else if (totalMinutes <= 240) { // 3-4 hours: Orange to Red
            const ratio = (totalMinutes - 180) / 60; // 0 to 1
            const r = 255; // Stay at 255
            const g = Math.round(165 - 165 * ratio); // 165 to 0
            const b = 0; // Stay at 0
            return `rgb(${r}, ${g}, ${b})`;
        } else { // 4+ hours: Red
            return "#FF0000";
        }
    }

    async loadData() {
        try {
            const ts = Date.now();
            const [mapRes, wfRes, brRes, rsRes, orchRes] = await Promise.all([
                fetch(`/data/map-data.json?t=${ts}`),
                fetch(`/data/waterfalls.json?t=${ts}`),
                fetch(`/data/breweries.json?t=${ts}`),
                fetch(`/data/restaurants.json?t=${ts}`),
                fetch(`/data/orchards_points.json?t=${ts}`)
            ]);

            this.data = await mapRes.json();
            this.scenicAreas = this.data.scenicAreas || [];
            this.cities = this.data.cities || [];

            this.waterfalls = wfRes.ok ? await wfRes.json() : [];
            this.breweries = brRes.ok ? await brRes.json() : [];
            this.restaurants = rsRes.ok ? await rsRes.json() : [];
            this.orchardPoints = orchRes.ok ? await orchRes.json() : [];

            return this.data;
        } catch (error) {
            console.error('Error loading map data:', error);
            throw error;
        }
    }

    initializeMap() {
        const config = this.data.mapConfig;
        
        this.map = L.map('map_9eb96eb1fe9bc3ea56b51a20c1cf6a00', {
            center: config.center,
            crs: L.CRS.EPSG3857,
            zoom: config.zoom,
            zoomControl: true,
            preferCanvas: false,
        });

        // Add tile layer
        const tileLayer = L.tileLayer(
            this.data.tileLayer.url,
            {
                attribution: this.data.tileLayer.attribution,
                ...this.data.tileLayer.options
            }
        ).addTo(this.map);

        // Add fullscreen control
        L.control.fullscreen({
            forceSeparateButton: false,
            position: "topleft",
            title: "Full Screen",
            titleCancel: "Exit Full Screen"
        }).addTo(this.map);

        // Add empty layers control (we'll register overlays as we create them)
        this.layerControl = L.control.layers({}, {}).addTo(this.map);

        // Add place search (Nominatim via Leaflet Control Geocoder)
        if (L.Control && L.Control.Geocoder) {
            const geocoder = L.Control.geocoder({
                defaultMarkGeocode: false,
                placeholder: 'Search place…',
                geocoder: L.Control.Geocoder.nominatim()
            })
            .on('markgeocode', (e) => {
                const bbox = e.geocode.bbox;
                const bounds = L.latLngBounds(bbox.getSouthEast(), bbox.getNorthWest());
                this.map.fitBounds(bounds.pad(0.2));

                // Drop a temporary minimalist marker at center
                const c = e.geocode.center;
                const tempIcon = L.divIcon({
                    className: 'icon-marker',
                    html: '<i class="fa fa-map-marker"></i>',
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });
                const m = L.marker(c, { icon: tempIcon }).addTo(this.map);
                m.bindPopup(`<b>${e.geocode.name}</b>`).openPopup();
                setTimeout(() => { this.map.removeLayer(m); }, 8000);
            })
            .addTo(this.map);
        }
    }

    renderScenicAreas() {
        const scenicGroup = L.featureGroup({}).addTo(this.map);

        this.scenicAreas.forEach(area => {
            // Create polygon
            const polygon = L.polygon(area.coordinates, {
                bubblingMouseEvents: true,
                color: area.color,
                dashArray: null,
                dashOffset: null,
                fill: true,
                fillColor: area.color,
                fillOpacity: 0.18,
                fillRule: "evenodd",
                lineCap: "round",
                lineJoin: "round",
                noClip: false,
                opacity: 1.0,
                smoothFactor: 1.0,
                stroke: true,
                weight: 2
            }).addTo(scenicGroup);

            // Add tooltip
            polygon.bindTooltip(
                `<div>${area.name} (Score ${area.score}) - ${area.driveTime}</div>`,
                { sticky: true }
            );

            // Create popup for the polygon itself
            const popup = L.popup({ maxWidth: 360 });
            const popupContent = $(`
                <div style="width: 100.0%; height: 100.0%;">
                    <b>${area.name}</b><br>
                    Scenery/Hiking Score: ${area.score} / 10<br>
                    Drive time from NYC (off‑peak): <b>${area.driveTime}</b><br>
                    <i>${area.description}</i>
                </div>
            `)[0];
            popup.setContent(popupContent);
            polygon.bindPopup(popup);
        });

        // Optionally register scenic areas as an overlay later if desired
    }

    renderCities() {
        const cityGroup = L.featureGroup({}).addTo(this.map);

        this.cities.forEach(city => {
            // Calculate marker size based on population
            const radius = Math.max(3, Math.min(8, 3 + (city.population / 10000) * 5));
            
            // Get color based on drive time
            const driveTimeColor = this.getDriveTimeColor(city.driveTime);

            const marker = L.circleMarker(city.coordinates, {
                bubblingMouseEvents: true,
                color: driveTimeColor,
                dashArray: null,
                dashOffset: null,
                fill: true,
                fillColor: driveTimeColor,
                fillOpacity: 0.8,
                fillRule: "evenodd",
                lineCap: "round",
                lineJoin: "round",
                opacity: 1.0,
                radius: radius,
                stroke: true,
                weight: 2
            }).addTo(cityGroup);

            // Create popup
            const popup = L.popup({ maxWidth: 260 });
            const googleMapsLink = city.google_maps_url ? 
                `<br/><a href="${city.google_maps_url}" target="_blank" rel="noopener" style="color: #1976d2; text-decoration: none;">
                    <i class="fa fa-map-marker"></i> View on Google Maps
                </a>` : '';
            
            const popupContent = $(`
                <div style="width: 100.0%; height: 100.0%;">
                    <b>${city.name}</b><br>
                    Population (approx): ${city.population.toLocaleString()}<br>
                    Drive time: <b>${city.driveTime}</b><br>
                    <i>${city.scenicArea}</i>
                    ${googleMapsLink}
                </div>
            `)[0];
            popup.setContent(popupContent);
            marker.bindPopup(popup);

            // Add tooltip with drive time
            const description = city.description ? `<br/><small>${city.description}</small>` : '';
            marker.bindTooltip(
                `<div>${city.name} (~${city.population.toLocaleString()}) - ${city.driveTime}${description}</div>`,
                { sticky: true }
            );
        });

        // Optionally register cities as overlay later
    }

    renderTrainRoutes() {
        const trainGroup = L.featureGroup({}).addTo(this.map);
        const stationGroup = L.featureGroup({}).addTo(this.map);

        this.data.trainRoutes.forEach(route => {
            // Create route line connecting all stops
            const routeCoordinates = route.stops.map(stop => stop.coordinates);
            const routeLine = L.polyline(routeCoordinates, {
                color: route.color,
                weight: 4,
                opacity: 0.8,
                dashArray: route.operator === 'Amtrak' ? '10, 5' : null
            }).addTo(trainGroup);

            // Add route tooltip
            routeLine.bindTooltip(
                `<div><b>${route.name}</b><br>${route.operator}</div>`,
                { sticky: true }
            );

            // Create station markers
            route.stops.forEach(stop => {
                const isTerminal = stop.type === 'terminal';
                const radius = isTerminal ? 6 : 4;
                const weight = isTerminal ? 3 : 2;

                const stationMarker = L.circleMarker(stop.coordinates, {
                    bubblingMouseEvents: true,
                    color: route.color,
                    dashArray: null,
                    dashOffset: null,
                    fill: true,
                    fillColor: route.color,
                    fillOpacity: 0.8,
                    fillRule: "evenodd",
                    lineCap: "round",
                    lineJoin: "round",
                    opacity: 1.0,
                    radius: radius,
                    stroke: true,
                    weight: weight
                }).addTo(stationGroup);

                // Create station popup
                const popup = L.popup({ maxWidth: 280 });
                const popupContent = $(`
                    <div style="width: 100.0%; height: 100.0%;">
                        <b>${stop.name}</b><br>
                        <span style="color: ${route.color}; font-weight: bold;">${route.name}</span><br>
                        Travel time from NYC: <b>${stop.travelTime}</b><br>
                        <i>${route.operator} • ${stop.type}</i>
                    </div>
                `)[0];
                popup.setContent(popupContent);
                stationMarker.bindPopup(popup);

                // Add station tooltip
                stationMarker.bindTooltip(
                    `<div>${stop.name} - ${stop.travelTime}</div>`,
                    { sticky: true }
                );
            });
        });

        // Optionally register train layers later
    }

    async renderOrchards() {
        try {
            const points = Array.isArray(this.orchardPoints) ? this.orchardPoints : [];

            const orchards = Array.isArray(points)
                ? points.map(p => ({
                    name: p.name,
                    address: p.address,
                    website: p.website,
                    approx_drive: p.approx_drive,
                    notes: p.notes,
                    coords: [p.lat, p.lng],
                    place_id: p.place_id,
                    google_maps_url: p.google_maps_url
                }))
                : [];
 
            if (!orchards.length) return;

            const orchardGroup = L.featureGroup({});
            const orchardDivIcon = (L.divIcon({
                className: 'icon-marker icon-apple',
                html: '<i class="fa fa-apple"></i>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            }));

            orchards.forEach(o => {
                if (!o.coords || isNaN(o.coords[0]) || isNaN(o.coords[1])) return;
                const marker = L.marker(o.coords, { icon: orchardDivIcon }).addTo(orchardGroup);
                const notes = o.notes ? `<br/><small>${o.notes}</small>` : '';
                marker.bindTooltip(`<div>${o.name}${notes}</div>`, { sticky: true });
                const linkHtml = o.website ? `<a href="${o.website}" target="_blank" rel="noopener">Website</a>` : '';
                const googleMapsLink = o.google_maps_url ? 
                    `<a href="${o.google_maps_url}" target="_blank" rel="noopener" style="color: #1976d2; text-decoration: none;">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                const addr = o.address ? `${o.address}<br/>` : '';
                const drive = o.approx_drive ? `Drive: <b>${o.approx_drive}</b><br/>` : '';
                const popupNotes = o.notes ? `<i>${o.notes}</i><br/>` : '';
                const links = [linkHtml, googleMapsLink].filter(Boolean).join(' • ');
                
                // Debug: Log popup content for first orchard
                if (o.name === 'Fishkill Farms') {
                    console.log('Orchard popup content for Fishkill Farms:', {
                        name: o.name,
                        google_maps_url: o.google_maps_url,
                        googleMapsLink: googleMapsLink,
                        links: links
                    });
                }
                
                marker.bindPopup(`
                    <div style="width:100%">
                        <b>${o.name}</b><br/>
                        ${addr}
                        ${drive}
                        ${popupNotes}
                        ${links}
                    </div>
                `);
            });

            this.overlays = this.overlays || {};
            this.overlays['Orchards (PYO)'] = orchardGroup;
            orchardGroup.addTo(this.map);
        } catch (e) {
            // swallow
        }
    }

    async renderWaterfalls() {
        try {
            const r = await fetch(`/data/waterfalls.json?t=${Date.now()}`);
            if (!r.ok) return;
            const waterfalls = await r.json();
            if (!Array.isArray(waterfalls) || !waterfalls.length) return;
            
            const wfGroup = L.featureGroup({});
            
            // Calculate scaling range based on waterfall heights
            const heights = waterfalls.map(w => w.height_ft || 0).filter(h => h > 0);
            const minHeight = Math.min(...heights);
            const maxHeight = Math.max(...heights);
            
            // Scale icons from 12px to 32px based on height for more visible difference
            const minIconSize = 12;
            const maxIconSize = 32;

            waterfalls.forEach(w => {
                if (w.lat === null || w.lng === null || isNaN(w.lat) || isNaN(w.lng)) return;
                const coords = [w.lat, w.lng];
                
                // Calculate icon size based on waterfall height
                const height = w.height_ft || minHeight;
                const heightRatio = (height - minHeight) / (maxHeight - minHeight);
                const iconSize = Math.round(minIconSize + (maxIconSize - minIconSize) * heightRatio);
                const iconAnchor = iconSize / 2;
                
                const waterDivIcon = L.divIcon({
                    className: 'icon-marker icon-water',
                    html: `<i class="fa fa-tint" style="font-size: ${iconSize}px;"></i>`,
                    iconSize: [iconSize, iconSize],
                    iconAnchor: [iconAnchor, iconAnchor]
                });
                
                const marker = L.marker(coords, { icon: waterDivIcon }).addTo(wfGroup);

                const description = w.description ? `<br/><small>${w.description}</small>` : '';
                marker.bindTooltip(`<div>${w.name}${description}</div>`, { sticky: true });

                const meta = [];
                if (w.height_ft) meta.push(`Height: ${w.height_ft} ft`);
                if (w.park_or_area) meta.push(w.park_or_area);
                if (w.nearby_town) meta.push(`Near: ${w.nearby_town}`);
                if (w.best_season) meta.push(`Best: ${w.best_season}`);
                if (w.access) meta.push(w.access);

                const desc = w.description ? `<br/><i>${w.description}</i>` : '';
                const googleMapsLink = w.google_maps_url ? 
                    `<br/><a href="${w.google_maps_url}" target="_blank" rel="noopener" style="color: #1976d2; text-decoration: none;">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';

                const popupContent = `
                    <div style="width:100%">
                        <b>${w.name}</b><br/>
                        ${meta.join(' • ')}
                        ${desc}
                        ${googleMapsLink}
                    </div>
                `;
                marker.bindPopup(popupContent);
            });

            // Add to map by default and register as overlay for toggling
            wfGroup.addTo(this.map);
            if (this.layerControl) {
                this.layerControl.addOverlay(wfGroup, 'Waterfalls');
            }
        } catch (e) {
            console.error('Failed to load waterfalls:', e);
        }
    }

    async renderBreweries() {
        try {
            const r = await fetch(`/data/breweries.json?t=${Date.now()}`);
            if (!r.ok) return;
            const breweries = await r.json();
            if (!Array.isArray(breweries) || !breweries.length) return;

            const brGroup = L.featureGroup({});
            const beerDivIcon = (L.divIcon({
                className: 'icon-marker icon-beer',
                html: '<i class="fa fa-beer"></i>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            }));

            breweries.forEach(b => {
                if (b.lat === null || b.lng === null || isNaN(b.lat) || isNaN(b.lng)) return;
                const coords = [b.lat, b.lng];
                const marker = L.marker(coords, { icon: beerDivIcon }).addTo(brGroup);

                const description = b.description ? `<br/><small>${b.description}</small>` : '';
                marker.bindTooltip(`<div>${b.name}${description}</div>`, { sticky: true });

                const meta = [];
                if (b.location) meta.push(b.location);
                if (b.founded) meta.push(`Founded: ${b.founded}`);
                if (b.specialty) meta.push(b.specialty);
                if (b.visitor_experience) meta.push(b.visitor_experience);

                const desc = b.description ? `<br/><i>${b.description}</i>` : '';
                const googleMapsLink = b.google_maps_url ? 
                    `<br/><a href="${b.google_maps_url}" target="_blank" rel="noopener" style="color: #1976d2; text-decoration: none;">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';

                marker.bindPopup(`
                    <div style="width:100%">
                        <b>${b.name}</b><br/>
                        ${meta.join(' • ')}
                        ${desc}
                        ${googleMapsLink}
                    </div>
                `);
            });

            brGroup.addTo(this.map);
            if (this.layerControl) {
                this.layerControl.addOverlay(brGroup, 'Breweries');
            }
        } catch (e) {
            console.error('Failed to load breweries:', e);
        }
    }

    async renderRestaurants() {
        try {
            const r = await fetch(`/data/restaurants.json?t=${Date.now()}`);
            if (!r.ok) return;
            const restaurants = await r.json();
            if (!Array.isArray(restaurants) || !restaurants.length) return;

            const rsGroup = L.featureGroup({});
            const foodDivIcon = (L.divIcon({
                className: 'icon-marker',
                html: '<i class="fa fa-cutlery"></i>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            }));

            restaurants.forEach(rst => {
                // Hide restaurants that are marked closed (temporary or permanent)
                const isClosed = (rst && (rst.closed_flag === 'temporary' || rst.closed_flag === 'permanent' || rst.business_status === 'CLOSED_TEMPORARILY' || rst.business_status === 'CLOSED_PERMANENTLY'));
                if (isClosed) return;
                if (rst.lat === null || rst.lng === null || isNaN(rst.lat) || isNaN(rst.lng)) return;
                const coords = [rst.lat, rst.lng];
                const marker = L.marker(coords, { icon: foodDivIcon }).addTo(rsGroup);

                const description = rst.description ? `<br/><small>${rst.description}</small>` : '';
                marker.bindTooltip(`<div>${rst.name}${description}</div>`, { sticky: true });

                const meta = [];
                if (rst.location) meta.push(rst.location);
                if (rst.specialty) meta.push(rst.specialty);
                if (rst.atmosphere) meta.push(rst.atmosphere);
                if (typeof rst.family_friendly === 'boolean') meta.push(rst.family_friendly ? 'Family-friendly' : 'Adults-oriented');
                const desc = rst.description ? `<br/><i>${rst.description}</i>` : '';
                const googleMapsLink = rst.google_maps_url ? 
                    `<br/><a href="${rst.google_maps_url}" target="_blank" rel="noopener" style="color: #1976d2; text-decoration: none;">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';

                marker.bindPopup(`
                    <div style="width:100%">
                        <b>${rst.name}</b><br/>
                        ${meta.join(' • ')}
                        ${desc}
                        ${googleMapsLink}
                    </div>
                `);
            });

            rsGroup.addTo(this.map);
            if (this.layerControl) {
                this.layerControl.addOverlay(rsGroup, 'Restaurants');
            }
        } catch (e) {
            console.error('Failed to load restaurants:', e);
        }
    }

    async render() {
        try {
            await this.loadData();
            this.initializeMap();
            this.renderScenicAreas();
            this.renderCities();
            this.renderTrainRoutes();
            await this.renderOrchards();
            await this.renderWaterfalls();
            await this.renderBreweries();
            await this.renderRestaurants();
            console.log('Map rendered successfully with', this.scenicAreas.length, 'scenic areas,', this.cities.length, 'cities, and', this.data.trainRoutes.length, 'train routes');
        } catch (error) {
            console.error('Error rendering map:', error);
        }
    }
}

// Initialize the map when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const map = new ScenicNYMap();
    map.render();
});
