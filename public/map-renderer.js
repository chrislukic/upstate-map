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
        this.strawberryPoints = null;
        this.cherryPoints = null;
        this.pointsOfInterest = null;
        this.isMobile = this.detectMobile();
    }

    // Detect if the device is mobile/touch
    detectMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
               ('ontouchstart' in window) || 
               (navigator.maxTouchPoints > 0);
    }

    // Get mobile-optimized popup options
    getPopupOptions(maxWidth = 300) {
        if (this.isMobile) {
            return {
                maxWidth: Math.min(maxWidth, window.innerWidth - 40),
                maxHeight: window.innerHeight - 100,
                className: 'mobile-popup'
            };
        }
        return { maxWidth: maxWidth };
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
            const [mapRes, wfRes, brRes, rsRes, orchRes, strawRes, cherryRes, poiRes] = await Promise.all([
                fetch(`/data/map-data.json?t=${ts}`),
                fetch(`/data/waterfalls.json?t=${ts}`),
                fetch(`/data/breweries.json?t=${ts}`),
                fetch(`/data/restaurants.json?t=${ts}`),
                fetch(`/data/pyo_apples.json?t=${ts}`),
                fetch(`/data/pyo_strawberries.json?t=${ts}`),
                fetch(`/data/pyo_cherries.json?t=${ts}`),
                fetch(`/data/points_of_interest.json?t=${ts}`)
            ]);

            this.data = await mapRes.json();
            this.scenicAreas = this.data.scenicAreas || [];
            this.cities = this.data.cities || [];

            this.waterfalls = wfRes.ok ? await wfRes.json() : [];
            this.breweries = brRes.ok ? await brRes.json() : [];
            this.restaurants = rsRes.ok ? await rsRes.json() : [];
            this.orchardPoints = orchRes.ok ? await orchRes.json() : [];
            this.strawberryPoints = strawRes.ok ? await strawRes.json() : [];
            this.cherryPoints = cherryRes.ok ? await cherryRes.json() : [];
            this.pointsOfInterest = poiRes.ok ? await poiRes.json() : [];

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
            // Mobile-optimized settings
            tap: !this.isMobile, // Disable tap delay on mobile
            touchZoom: true,
            doubleClickZoom: true,
            scrollWheelZoom: !this.isMobile, // Disable scroll wheel zoom on mobile
            dragging: true,
            keyboard: !this.isMobile, // Disable keyboard navigation on mobile
            // Mobile-specific zoom limits
            minZoom: this.isMobile ? 6 : 4,
            maxZoom: this.isMobile ? 16 : 18,
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

            // Add tooltip (only on non-mobile devices)
            if (!this.isMobile) {
                polygon.bindTooltip(
                    `<div class="map-tooltip">${area.name} (Score ${area.score}) - ${area.driveTime}</div>`,
                    { sticky: true }
                );
            }

            // Create popup for the polygon itself
            const popup = L.popup(this.getPopupOptions(360));
            const popupContent = $(`
                <div class="map-popup">
                    <h3 class="popup-title">${area.name}</h3>
                    <span class="popup-meta">Scenery/Hiking Score: ${area.score} / 10</span>
                    <span class="popup-meta">Drive time from NYC (off‑peak): <strong>${area.driveTime}</strong></span>
                    <div class="popup-description">${area.description}</div>
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
                radius: radius,
                fillColor: driveTimeColor,
                color: driveTimeColor,
                weight: 2,
                opacity: 0.8,
                fillOpacity: 0.6,
                className: 'city-marker'
            }).addTo(cityGroup);

            // Create popup
            const popup = L.popup(this.getPopupOptions(260));
            const googleMapsLink = city.google_maps_url ? 
                `<a href="${city.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                    <i class="fa fa-map-marker"></i> View on Google Maps
                </a>` : '';
            
            const popupContent = $(`
                <div class="map-popup">
                    <h3 class="popup-title">${city.name}</h3>
                    <span class="popup-meta">Population (approx): ${city.population.toLocaleString()}</span>
                    <span class="popup-meta">Drive time: <strong>${city.driveTime}</strong></span>
                    <div class="popup-description">${city.scenicArea}</div>
                    ${googleMapsLink}
                </div>
            `)[0];
            popup.setContent(popupContent);
            marker.bindPopup(popup);

            // Add tooltip with drive time (only on non-mobile devices)
            if (!this.isMobile) {
                const description = city.description ? `<br/><small>${city.description}</small>` : '';
                marker.bindTooltip(
                    `<div class="map-tooltip">${city.name} (~${city.population.toLocaleString()}) - ${city.driveTime}${description}</div>`,
                    { sticky: true }
                );
            }
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

            // Add route tooltip (only on non-mobile devices)
            if (!this.isMobile) {
                routeLine.bindTooltip(
                    `<div class="map-tooltip"><b>${route.name}</b><br>${route.operator}</div>`,
                    { sticky: true }
                );
            }

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
                const popup = L.popup(this.getPopupOptions(280));
                const popupContent = $(`
                    <div class="map-popup">
                        <h3 class="popup-title">${stop.name}</h3>
                        <span class="popup-meta route-name" style="color: ${route.color};">${route.name}</span>
                        <span class="popup-meta">Travel time from NYC: <strong>${stop.travelTime}</strong></span>
                        <div class="popup-description">${route.operator} • ${stop.type}</div>
                    </div>
                `)[0];
                popup.setContent(popupContent);
                stationMarker.bindPopup(popup);

                // Add station tooltip (only on non-mobile devices)
                if (!this.isMobile) {
                    stationMarker.bindTooltip(
                        `<div class="map-tooltip">${stop.name} - ${stop.travelTime}</div>`,
                        { sticky: true }
                    );
                }
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
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    marker.bindTooltip(`<div class="map-tooltip">${o.name}${notes}</div>`, { sticky: true });
                }
                const linkHtml = o.website ? `<a href="${o.website}" target="_blank" rel="noopener">Website</a>` : '';
                const googleMapsLink = o.google_maps_url ? 
                    `<a href="${o.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                
                const websiteLink = o.website ? 
                    `<a href="${o.website}" target="_blank" rel="noopener" class="popup-link">Website</a>` : '';
                
                const links = [websiteLink, googleMapsLink].filter(Boolean).join(' • ');
                
                marker.bindPopup(`
                    <div class="map-popup">
                        <h3 class="popup-title">${o.name}${o.organic ? ' <span style="color: #4CAF50; font-size: 14px;">🌱 Organic</span>' : ''}</h3>
                        ${o.address ? `<span class="popup-meta">${o.address}</span>` : ''}
                        ${o.approx_drive ? `<span class="popup-meta"><strong>Drive:</strong> ${o.approx_drive}</span>` : ''}
                        ${o.notes ? `<div class="popup-description">${o.notes}</div>` : ''}
                        ${links ? `<div class="popup-details-text-small">${links}</div>` : ''}
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

    async renderStrawberries() {
        try {
            const points = Array.isArray(this.strawberryPoints) ? this.strawberryPoints : [];

            const strawberries = Array.isArray(points)
                ? points.map(p => ({
                    name: p.name,
                    address: p.address,
                    website: p.website,
                    reservation_required: p.reservation_required,
                    notes: p.notes,
                    coords: [p.lat, p.lng],
                    place_id: p.place_id,
                    google_maps_url: p.google_maps_url
                }))
                : [];
 
            if (!strawberries.length) return;

            const strawberryGroup = L.featureGroup({});
            const strawberryDivIcon = (L.divIcon({
                className: 'icon-marker icon-strawberry',
                html: '<span style="font-size: 16px;">🍓</span>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            }));

            strawberries.forEach(s => {
                if (!s.coords || isNaN(s.coords[0]) || isNaN(s.coords[1])) return;
                const marker = L.marker(s.coords, { icon: strawberryDivIcon }).addTo(strawberryGroup);
                const notes = s.notes ? `<br/><small>${s.notes}</small>` : '';
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    marker.bindTooltip(`<div class="map-tooltip">${s.name}${notes}</div>`, { sticky: true });
                }
                
                const googleMapsLink = s.google_maps_url ? 
                    `<a href="${s.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                
                const websiteLink = s.website ? 
                    `<a href="${s.website}" target="_blank" rel="noopener" class="popup-link">Website</a>` : '';
                
                const links = [websiteLink, googleMapsLink].filter(Boolean).join(' • ');
                
                marker.bindPopup(`
                    <div class="map-popup">
                        <h3 class="popup-title">${s.name}${s.organic ? ' <span style="color: #4CAF50; font-size: 14px;">🌱 Organic</span>' : ''}</h3>
                        ${s.address ? `<span class="popup-meta">${s.address}</span>` : ''}
                        ${s.reservation_required ? `<span class="popup-meta"><strong>Reservation:</strong> ${s.reservation_required}</span>` : ''}
                        ${s.notes ? `<div class="popup-description">${s.notes}</div>` : ''}
                        ${links ? `<div class="popup-details-text-small">${links}</div>` : ''}
                    </div>
                `);
            });

            this.overlays = this.overlays || {};
            this.overlays['Strawberries (PYO)'] = strawberryGroup;
            strawberryGroup.addTo(this.map);
        } catch (e) {
            // swallow
        }
    }

    async renderCherries() {
        try {
            const points = Array.isArray(this.cherryPoints) ? this.cherryPoints : [];

            const cherries = Array.isArray(points)
                ? points.map(p => ({
                    name: p.name,
                    address: p.address,
                    website: p.website,
                    reservation_required: p.reservation_required,
                    notes: p.notes,
                    coords: [p.lat, p.lng],
                    place_id: p.place_id,
                    google_maps_url: p.google_maps_url,
                    organic: p.organic || false
                }))
                : [];
 
            if (!cherries.length) return;

            const cherryGroup = L.featureGroup({});
            const cherryDivIcon = (L.divIcon({
                className: 'icon-marker icon-cherry',
                html: '<span style="font-size: 16px;">🍒</span>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            }));

            cherries.forEach(c => {
                if (!c.coords || isNaN(c.coords[0]) || isNaN(c.coords[1])) return;
                const marker = L.marker(c.coords, { icon: cherryDivIcon }).addTo(cherryGroup);
                const notes = c.notes ? `<br/><small>${c.notes}</small>` : '';
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    marker.bindTooltip(`<div class="map-tooltip">${c.name}${notes}</div>`, { sticky: true });
                }
                
                const googleMapsLink = c.google_maps_url ? 
                    `<a href="${c.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                
                const websiteLink = c.website ? 
                    `<a href="${c.website}" target="_blank" rel="noopener" class="popup-link">Website</a>` : '';
                
                const links = [websiteLink, googleMapsLink].filter(Boolean).join(' • ');
                
                marker.bindPopup(`
                    <div class="map-popup">
                        <h3 class="popup-title">${c.name}${c.organic ? ' <span style="color: #4CAF50; font-size: 14px;">🌱 Organic</span>' : ''}</h3>
                        ${c.address ? `<span class="popup-meta">${c.address}</span>` : ''}
                        ${c.reservation_required ? `<span class="popup-meta"><strong>Reservation:</strong> ${c.reservation_required}</span>` : ''}
                        ${c.notes ? `<div class="popup-description">${c.notes}</div>` : ''}
                        ${links ? `<div class="popup-details-text-small">${links}</div>` : ''}
                    </div>
                `);
            });

            this.overlays = this.overlays || {};
            this.overlays['Cherries (PYO)'] = cherryGroup;
            cherryGroup.addTo(this.map);
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
                    className: 'icon-marker icon-water waterfall-icon',
                    html: `<i class="fa fa-tint" style="font-size: ${iconSize}px;"></i>`,
                    iconSize: [iconSize, iconSize],
                    iconAnchor: [iconAnchor, iconAnchor]
                });
                
                const marker = L.marker(coords, { icon: waterDivIcon }).addTo(wfGroup);

                const description = w.description ? `<br/><small>${w.description}</small>` : '';
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    marker.bindTooltip(`<div class="map-tooltip">${w.name}${description}</div>`, { sticky: true });
                }

                const meta = [];
                if (w.height_ft) meta.push(`Height: ${w.height_ft} ft`);
                if (w.park_or_area) meta.push(w.park_or_area);
                if (w.nearby_town) meta.push(`Near: ${w.nearby_town}`);
                if (w.best_season) meta.push(`Best: ${w.best_season}`);
                if (w.access) meta.push(w.access);

                const hasDescription = w.description ? true : false;
                const googleMapsLink = w.google_maps_url ? 
                    `<a href="${w.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';

                const popupContent = `
                    <div class="map-popup">
                        <h3 class="popup-title">${w.name}</h3>
                        <div class="popup-details-text-small">${meta.join(' • ')}</div>
                        ${hasDescription ? `<div class="popup-description">${w.description}</div>` : ''}
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

                // Use description for tooltip (mouseover)
                const shortDesc = b.description ? `<br/><small>${b.description}</small>` : '';
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    marker.bindTooltip(`<div class="map-tooltip">${b.name}${shortDesc}</div>`, { sticky: true });
                }

                const meta = [];
                if (b.location) meta.push(b.location);
                if (b.founded) meta.push(`Founded: ${b.founded}`);
                if (b.specialty) meta.push(b.specialty);
                if (b.visitor_experience) meta.push(b.visitor_experience);

                // Create popup with full description
                const googleMapsLink = b.google_maps_url ? 
                    `<a href="${b.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';

                const popupContent = `
                    <div class="map-popup">
                        <h3 class="popup-title">${b.name}</h3>
                        <div class="popup-details-text-small">${meta.join(' • ')}</div>
                        ${b.full_description ? `<div class="popup-description">${b.full_description}</div>` : ''}
                        ${googleMapsLink}
                    </div>
                `;

                marker.bindPopup(popupContent);
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
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    marker.bindTooltip(`<div class="map-tooltip">${rst.name}${description}</div>`, { sticky: true });
                }

                const meta = [];
                if (rst.location) meta.push(rst.location);
                if (rst.specialty) meta.push(rst.specialty);
                if (rst.atmosphere) meta.push(rst.atmosphere);
                if (typeof rst.family_friendly === 'boolean') meta.push(rst.family_friendly ? 'Family-friendly' : 'Adults-oriented');
                const hasDescription = rst.description ? true : false;
                const googleMapsLink = rst.google_maps_url ? 
                    `<a href="${rst.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';

                marker.bindPopup(`
                    <div class="map-popup">
                        <h3 class="popup-title">${rst.name}</h3>
                        <div class="popup-details-text-small">${meta.join(' • ')}</div>
                        ${hasDescription ? `<div class="popup-description">${rst.description}</div>` : ''}
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

    async renderPointsOfInterest() {
        try {
            if (!this.pointsOfInterest || !Array.isArray(this.pointsOfInterest) || !this.pointsOfInterest.length) {
                console.log('No points of interest data to render');
                return;
            }

            const poiGroup = L.featureGroup({}).addTo(this.map);

            this.pointsOfInterest.forEach(poi => {
                // Skip if coordinates are invalid
                if (poi.lat === null || poi.lng === null || isNaN(poi.lat) || isNaN(poi.lng)) {
                    return;
                }

                // Create icon based on category (FontAwesome 4 compatible)
                let iconClass = 'fa-map-marker'; // Default icon
                let iconColor = '#8B4513'; // Brown color for cultural sites
                
                switch (poi.category) {
                    case 'Museum':
                        iconClass = 'fa-university';
                        iconColor = '#4169E1'; // Royal blue
                        break;
                    case 'Art Museum':
                    case 'Art Center':
                        iconClass = 'fa-paint-brush';
                        iconColor = '#FF6347'; // Tomato
                        break;
                    case 'Historic Site':
                        iconClass = 'fa-building';
                        iconColor = '#8B4513'; // Saddle brown
                        break;
                    case 'Educational Institution':
                        iconClass = 'fa-graduation-cap';
                        iconColor = '#228B22'; // Forest green
                        break;
                    case 'Performing Arts':
                        iconClass = 'fa-music';
                        iconColor = '#9370DB'; // Medium purple
                        break;
                    case 'Sports Venue':
                        iconClass = 'fa-trophy';
                        iconColor = '#FFD700'; // Gold
                        break;
                    case 'Natural Attraction':
                    case 'State Park':
                        iconClass = 'fa-tree';
                        iconColor = '#32CD32'; // Lime green
                        break;
                    case 'Historic Garden':
                        iconClass = 'fa-leaf';
                        iconColor = '#228B22'; // Forest green
                        break;
                }

                // Create div icon for points of interest
                const poiIcon = L.divIcon({
                    className: 'icon-marker icon-poi poi-icon',
                    html: `<i class="fa ${iconClass}" style="color: ${iconColor}; font-size: 16px;"></i>`,
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });

                const marker = L.marker([poi.lat, poi.lng], { 
                    icon: poiIcon,
                    zIndexOffset: 500 // Above restaurants/breweries but below cities
                }).addTo(poiGroup);

                // Add tooltip with brief description
                const shortDesc = poi.description ? `<br/><small>${poi.description}</small>` : '';
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    marker.bindTooltip(`<div class="map-tooltip">${poi.name}${shortDesc}</div>`, { sticky: true });
                }

                // Create popup content
                const websiteLink = poi.website ? 
                    `<a href="${poi.website}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-external-link-alt"></i> Visit Website
                    </a>` : '';

                const googleMapsLink = poi.place_id ? 
                    `<a href="https://www.google.com/maps/place/?q=place_id:${poi.place_id}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';

                marker.bindPopup(`
                    <div class="map-popup">
                        <h3 class="popup-title">${poi.name}</h3>
                        <span class="popup-meta">${poi.category}</span>
                        <span class="popup-meta">${poi.location}</span>
                        <div class="popup-description">${poi.description}</div>
                        <div class="popup-links-container">
                            ${websiteLink}
                            ${googleMapsLink}
                        </div>
                    </div>
                `);
            });

            poiGroup.addTo(this.map);
            if (this.layerControl) {
                this.layerControl.addOverlay(poiGroup, 'Points of Interest');
            }

            console.log(`Rendered ${this.pointsOfInterest.length} points of interest`);
        } catch (e) {
            console.error('Failed to load points of interest:', e);
        }
    }

    async render() {
        try {
            await this.loadData();
            this.initializeMap();
            this.renderScenicAreas();
            this.renderTrainRoutes();
            await this.renderOrchards();
            await this.renderStrawberries();
            await this.renderCherries();
            await this.renderWaterfalls();
            await this.renderBreweries();
            await this.renderRestaurants();
            await this.renderPointsOfInterest();
            this.renderCities(); // Render cities last so they appear on top
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
