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
        this.peachPoints = null;
        this.childrenActivities = null;
        this.trailheads = null;
        this.airbnbs = null;
        this.pointsOfInterest = null;
        this.regions = null;
        this.events = null;
        this.tripPlan = null; // Trip planning data
        this.isMobile = this.detectMobile();
        this.seasonalVisibility = {
            apples: true,
            strawberries: true,
            cherries: true,
            peaches: true
        };
        this.popupFactory = null; // Will be initialized after map is ready
        // Ensure logger is available (defined in popup-architecture.js); provide a fallback
        if (typeof window !== 'undefined' && !window.Logger) {
            window.Logger = {
                setLevel() {},
                basic: (...args) => console.log(...args),
                extend: (...args) => console.log(...args),
                verbose: (...args) => console.log(...args),
                warn: (...args) => console.warn(...args),
                error: (...args) => console.error(...args)
            };
        }
    }

    // Detect if the device is mobile/touch
    detectMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               ('ontouchstart' in window) ||
               (navigator.maxTouchPoints > 0);
    }

    // Get current week number (1-52)
    getCurrentWeek() {
        const now = new Date();
        const start = new Date(now.getFullYear(), 0, 1);
        const days = Math.floor((now - start) / (24 * 60 * 60 * 1000));
        return Math.ceil((days + start.getDay() + 1) / 7);
    }

    // Check if a crop is in season based on start/end week (inclusive)
    // Supports either explicit start/end or legacy season_weeks array
    isInSeason(startWeekOrArray, endWeek) {
        const currentWeek = this.getCurrentWeek();
        // Legacy support: if first arg is an array, check membership
        if (Array.isArray(startWeekOrArray)) {
            const seasonWeeks = startWeekOrArray;
            if (!seasonWeeks || !seasonWeeks.length) return true;
            return seasonWeeks.includes(currentWeek);
        }
        const startWeek = Number(startWeekOrArray);
        const endWk = Number(endWeek);
        if (!startWeek || !endWk || isNaN(startWeek) || isNaN(endWk)) {
            return true; // If missing data, default visible
        }
        if (startWeek <= endWk) {
            // Normal range within same year
            return currentWeek >= startWeek && currentWeek <= endWk;
        }
        // Wrap-around range (e.g., week 48 to week 5)
        return currentWeek >= startWeek || currentWeek <= endWk;
    }

    // Check if a crop is in season during trip dates
    isInSeasonForTrip(fruitStartWeek, fruitEndWeek, tripStartDate, tripEndDate) {
        const startWeek = Number(fruitStartWeek);
        const endWk = Number(fruitEndWeek);
        if (!startWeek || !endWk || isNaN(startWeek) || isNaN(endWk)) {
            return true; // If missing data, default visible
        }

        // Get weeks for trip dates
        const tripStartWeek = this.getWeekForDate(tripStartDate);
        const tripEndWeek = this.getWeekForDate(tripEndDate);

        // Check if fruit season overlaps with trip dates
        if (startWeek <= endWk) {
            // Normal fruit season range within same year
            // Fruit season overlaps with trip if:
            // - Fruit starts before/on trip end AND fruit ends after/on trip start
            return startWeek <= tripEndWeek && endWk >= tripStartWeek;
        } else {
            // Wrap-around fruit season (e.g., week 48 to week 5)
            // Check if trip overlaps with either part of the season
            return (tripStartWeek >= startWeek || tripEndWeek <= endWk) || 
                   (tripStartWeek <= endWk && tripEndWeek >= startWeek);
        }
    }

    // Get week number for a specific date
    getWeekForDate(dateString) {
        const date = new Date(dateString + 'T00:00:00');
        const start = new Date(date.getFullYear(), 0, 1);
        const days = Math.floor((date - start) / (24 * 60 * 60 * 1000));
        return Math.ceil((days + start.getDay() + 1) / 7);
    }

    // Get seasonal status for PYO crops using actual data from JSON files
    getSeasonalStatus() {
        const currentWeek = this.getCurrentWeek();
        
        // Try to get seasonal status from consolidated fruit farms data first
        if (this.fruitFarmsData && Array.isArray(this.fruitFarmsData)) {
            const status = { apples: false, strawberries: false, cherries: false, peaches: false };
            
            // Check each farm's fruits for seasonal status
            this.fruitFarmsData.forEach(farm => {
                if (farm.fruits && Array.isArray(farm.fruits)) {
                    farm.fruits.forEach(fruit => {
                        if (fruit.type && this.isInSeason(fruit.season_start_week, fruit.season_end_week)) {
                            status[fruit.type] = true;
                        }
                    });
                }
            });
            
            return status;
        }
        
        // Fallback to old individual arrays if consolidated data not available
        const appleSample = this.orchardPoints && this.orchardPoints[0];
        const strawberrySample = this.strawberryPoints && this.strawberryPoints[0];
        const cherrySample = this.cherryPoints && this.cherryPoints[0];
        const peachSample = this.peachPoints && this.peachPoints[0];
        
        return {
            apples: appleSample ? this.isInSeason(appleSample.season_start_week, appleSample.season_end_week) : true,
            strawberries: strawberrySample ? this.isInSeason(strawberrySample.season_start_week, strawberrySample.season_end_week) : true,
            cherries: cherrySample ? this.isInSeason(cherrySample.season_start_week, cherrySample.season_end_week) : true,
            peaches: peachSample ? this.isInSeason(peachSample.season_start_week, peachSample.season_end_week) : true
        };
    }

    // Update legend based on seasonal status
    updateSeasonalLegend() {
        const seasonalStatus = this.getSeasonalStatus();
        
        Object.keys(seasonalStatus).forEach(crop => {
            const legendItem = document.querySelector(`[data-crop="${crop}"]`);
            if (legendItem) {
                if (seasonalStatus[crop]) {
                    legendItem.classList.remove('out-of-season');
                } else {
                    legendItem.classList.add('out-of-season');
                }
            }
        });
    }

    // Toggle seasonal visibility
    toggleSeasonalVisibility(crop) {
        this.seasonalVisibility[crop] = !this.seasonalVisibility[crop];
        this.updateSeasonalLegend();
        // Re-render the specific crop layer
        this.renderSpecificCrop(crop);
    }

    // Render specific crop based on visibility
    async renderSpecificCrop(crop) {
        // All fruit types are now handled by the consolidated method
        await this.renderFruitFarms();
    }

    // Add click handlers for seasonal legend items
    addSeasonalClickHandlers() {
        const pyoItems = document.querySelectorAll('.pyo-item');
        pyoItems.forEach(item => {
            item.addEventListener('click', (e) => {
                const crop = e.currentTarget.getAttribute('data-crop');
                if (crop) {
                    this.toggleSeasonalVisibility(crop);
                }
            });
        });
    }

    // Trip planning functionality
    initializeTripPlanning() {
        Logger.get('trip').basic('Initializing trip planning...');
        this.tripPlan = this.loadTripPlan();
        Logger.get('trip').extend('Loaded trip plan:', this.tripPlan);
        this.updateTripDisplay();
        this.setInitialDateValues();
        
        // Set up periodic countdown updates (every hour)
        if (this.tripPlan) {
            this.tripCountdownInterval = setInterval(() => {
                this.updateTripDisplay();
            }, 60 * 60 * 1000); // Update every hour
        }
        
        Logger.get('trip').basic('Trip planning initialized');
    }

    loadTripPlan() {
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('tripPlan='));
        if (cookie) {
            try {
                return JSON.parse(decodeURIComponent(cookie.split('=')[1]));
            } catch (e) {
                Logger.warn('Error parsing trip plan cookie:', e);
            }
        }
        return null;
    }

    saveTripPlan(tripPlan, forceRerender = false) {
        const maxAge = 30 * 24 * 60 * 60; // 30 days
        document.cookie = `tripPlan=${encodeURIComponent(JSON.stringify(tripPlan))}; max-age=${maxAge}; path=/`;
        
        // Check if trip plan actually changed
        const tripChanged = !this.tripPlan || 
            this.tripPlan.startDate !== tripPlan.startDate || 
            this.tripPlan.endDate !== tripPlan.endDate;
            
        this.tripPlan = tripPlan;
        
        // Update popup factory with new trip plan
        if (this.popupFactory) {
            this.popupFactory.updateTripPlan(tripPlan);
        }
        
        // Clear existing countdown interval if it exists
        if (this.tripCountdownInterval) {
            clearInterval(this.tripCountdownInterval);
        }
        
        // Set up new countdown interval
        this.tripCountdownInterval = setInterval(() => {
            this.updateTripDisplay();
        }, 60 * 60 * 1000); // Update every hour
        
        // Only re-render fruit farms if trip dates changed or forced
        if (tripChanged || forceRerender) {
            this.renderFruitFarms();
        }
    }

    setInitialDateValues() {
        const today = new Date();
        const nextWeek = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000);
        
        if (!this.tripPlan) {
            const startDateEl = document.getElementById('tripStartDate');
            const endDateEl = document.getElementById('tripEndDate');
            
            if (startDateEl && endDateEl) {
                startDateEl.value = today.toISOString().split('T')[0];
                endDateEl.value = nextWeek.toISOString().split('T')[0];
            }
        }
    }

    // Format date range with smart year handling
    formatDateRange(startDate, endDate) {
        const start = new Date(startDate + 'T00:00:00');
        const end = new Date(endDate + 'T00:00:00');
        const currentYear = new Date().getFullYear();
        
        const startYear = start.getFullYear();
        const endYear = end.getFullYear();
        
        // Format dates
        const startFormatted = start.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric',
            year: startYear !== currentYear ? 'numeric' : undefined
        });
        
        const endFormatted = end.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric',
            year: endYear !== currentYear ? 'numeric' : undefined
        });
        
        // If same year, compress the display
        if (startYear === endYear) {
            if (startYear === currentYear) {
                // Same year as current year - no year shown
                return `${startFormatted} - ${endFormatted}`;
            } else {
                // Different year - show year only once
                const startWithoutYear = start.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                return `${startWithoutYear} - ${endFormatted}`;
            }
        } else {
            // Different years - show both years
            return `${startFormatted} - ${endFormatted}`;
        }
    }

    // Calculate countdown to trip start with friendly formatting
    getTripCountdown(startDate) {
        const today = new Date();
        const tripStart = new Date(startDate + 'T00:00:00');
        const diffTime = tripStart - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays < 0) {
            return 'Trip has started';
        } else if (diffDays === 0) {
            return 'Trip starts today!';
        } else if (diffDays === 1) {
            return 'Trip starts tomorrow';
        } else if (diffDays < 7) {
            if (diffDays === 2) {
                return 'Trip starts in 2 days';
            } else if (diffDays === 3) {
                return 'Trip starts in 3 days';
            } else {
                return `Trip starts in ${diffDays} days`;
            }
        } else if (diffDays < 30) {
            const weeks = Math.floor(diffDays / 7);
            const remainingDays = diffDays % 7;
            
            if (weeks === 1) {
                if (remainingDays === 0) {
                    return 'Trip starts in a week';
                } else if (remainingDays <= 2) {
                    return 'Trip starts in about a week';
                } else if (remainingDays === 3 || remainingDays === 4) {
                    return 'Trip starts in a week and a half';
                } else {
                    return 'Trip starts in a bit more than a week';
                }
            } else if (weeks === 2) {
                if (remainingDays === 0) {
                    return 'Trip starts in 2 weeks';
                } else if (remainingDays <= 2) {
                    return 'Trip starts in about 2 weeks';
                } else {
                    return 'Trip starts in a bit more than 2 weeks';
                }
            } else if (weeks === 3) {
                if (remainingDays === 0) {
                    return 'Trip starts in 3 weeks';
                } else if (remainingDays <= 2) {
                    return 'Trip starts in about 3 weeks';
                } else {
                    return 'Trip starts in around 3 weeks';
                }
            } else {
                if (remainingDays === 0) {
                    return `Trip starts in ${weeks} weeks`;
                } else if (remainingDays <= 2) {
                    return `Trip starts in about ${weeks} weeks`;
                } else {
                    return `Trip starts in around ${weeks} weeks`;
                }
            }
        } else if (diffDays < 365) {
            const months = Math.floor(diffDays / 30);
            const remainingDays = diffDays % 30;
            const weeks = Math.floor(remainingDays / 7);
            
            if (months === 1) {
                if (weeks === 0) {
                    return 'Trip starts in about a month';
                } else if (weeks === 1) {
                    return 'Trip starts in about a month';
                } else if (weeks === 2) {
                    return 'Trip starts in about a month and a half';
                } else if (remainingDays >= 14 && remainingDays <= 16) {
                    return 'Trip starts in a month and a half';
                } else {
                    return 'Trip starts in a bit more than a month';
                }
            } else if (months === 2) {
                if (weeks === 0) {
                    return 'Trip starts in about 2 months';
                } else if (weeks <= 2) {
                    return 'Trip starts in about 2 months';
                } else {
                    return 'Trip starts in around 2 months';
                }
            } else if (months === 3) {
                if (weeks === 0) {
                    return 'Trip starts in about 3 months';
                } else if (weeks <= 2) {
                    return 'Trip starts in about 3 months';
                } else {
                    return 'Trip starts in around 3 months';
                }
            } else if (months === 6) {
                return 'Trip starts in about 6 months';
            } else if (months < 12) {
                if (weeks === 0) {
                    return `Trip starts in about ${months} months`;
                } else if (weeks <= 2) {
                    return `Trip starts in about ${months} months`;
                } else {
                    return `Trip starts in around ${months} months`;
                }
            } else {
                const years = Math.floor(months / 12);
                const remainingMonths = months % 12;
                if (remainingMonths === 0) {
                    return `Trip starts in about ${years} year${years > 1 ? 's' : ''}`;
                } else if (remainingMonths <= 3) {
                    return `Trip starts in about ${years} year${years > 1 ? 's' : ''}`;
                } else {
                    return `Trip starts in around ${years} year${years > 1 ? 's' : ''}`;
                }
            }
        } else {
            const years = Math.floor(diffDays / 365);
            const remainingDays = diffDays % 365;
            const months = Math.floor(remainingDays / 30);
            
            if (years === 1) {
                if (months === 0) {
                    return 'Trip starts in about a year';
                } else if (months <= 3) {
                    return 'Trip starts in about a year';
                } else {
                    return 'Trip starts in around a year';
                }
            } else {
                if (months === 0) {
                    return `Trip starts in about ${years} years`;
                } else if (months <= 3) {
                    return `Trip starts in about ${years} years`;
                } else {
                    return `Trip starts in around ${years} years`;
                }
            }
        }
    }

    updateTripDisplay() {
        Logger.get('trip').extend('Updating trip display...');
        const currentTripEl = document.getElementById('currentTrip');
        const tripFormEl = document.getElementById('tripForm');
        const tripDisplayEl = document.getElementById('tripDisplay');
        const tripLoadingEl = document.getElementById('tripLoading');
        
        Logger.get('trip').verbose('DOM elements found:', {
            currentTrip: !!currentTripEl,
            tripForm: !!tripFormEl,
            tripLoading: !!tripLoadingEl
        });
        
        // Safety check for DOM elements
        if (!currentTripEl || !tripFormEl || !tripLoadingEl) {
                Logger.get('trip').warn('Trip planning DOM elements not found');
            return;
        }
        
        // Hide loading state
        tripLoadingEl.style.display = 'none';
        
        if (this.tripPlan) {
            // Update the new separate elements
            const tripLocationEl = document.getElementById('tripLocation');
            const tripDatesEl = document.getElementById('tripDates');
            const countdownEl = document.getElementById('tripCountdown');
            
            // Handle location display
            if (tripLocationEl) {
                if (this.tripPlan.address) {
                    tripLocationEl.innerHTML = `<span>${this.formatAddress(this.tripPlan.address)}</span>`;
                    // Show clear location button, hide set location button
                    const clearLocationBtn = document.querySelector('.btn-clear-location');
                    const setLocationBtn = document.querySelector('.btn-set-location');
                    if (clearLocationBtn) clearLocationBtn.style.display = 'flex';
                    if (setLocationBtn) setLocationBtn.style.display = 'none';
                } else {
                    tripLocationEl.innerHTML = `<span>No location set</span>`;
                    // Hide clear location button, show set location button
                    const clearLocationBtn = document.querySelector('.btn-clear-location');
                    const setLocationBtn = document.querySelector('.btn-set-location');
                    if (clearLocationBtn) clearLocationBtn.style.display = 'none';
                    if (setLocationBtn) setLocationBtn.style.display = 'flex';
                }
            }
            
            // Handle dates display
            if (tripDatesEl) {
                if (this.tripPlan.startDate && this.tripPlan.endDate) {
                    const dateRange = this.formatDateRange(this.tripPlan.startDate, this.tripPlan.endDate);
                    tripDatesEl.innerHTML = `
                        <div class="date-range">
                            <span>${dateRange}</span>
                        </div>
                    `;
                    // Show clear dates button
                    const clearDatesBtn = document.querySelector('.btn-clear-dates');
                    if (clearDatesBtn) clearDatesBtn.style.display = 'flex';
                } else {
                    tripDatesEl.innerHTML = `<span>No dates set</span>`;
                    // Hide clear dates button
                    const clearDatesBtn = document.querySelector('.btn-clear-dates');
                    if (clearDatesBtn) clearDatesBtn.style.display = 'none';
                }
            }
            
            // Handle countdown display
            if (countdownEl) {
                if (this.tripPlan.startDate) {
                    const countdown = this.getTripCountdown(this.tripPlan.startDate);
                    countdownEl.innerHTML = `<span>${countdown}</span>`;
                } else {
                    countdownEl.innerHTML = `<span>No trip dates set</span>`;
                }
            }
            
            currentTripEl.style.display = 'block';
            tripFormEl.style.display = 'none';
            
            // Apply trip filtering to map data
            this.applyTripFiltering();
            
            // Plot trip location marker if coordinates are available
            if (this.tripPlan.lat && this.tripPlan.lng) {
                this.plotTripLocation();
            } else if (this.tripPlan.address) {
                // Geocode the address to get coordinates
                this.geocodeTripAddress();
            }
        } else {
            Logger.get('trip').basic('No trip plan - showing form');
            currentTripEl.style.display = 'none';
            tripFormEl.style.display = 'block';
            
            // Hide all clear buttons
            const clearLocationBtn = document.querySelector('.btn-clear-location');
            const clearDatesBtn = document.querySelector('.btn-clear-dates');
            if (clearLocationBtn) clearLocationBtn.style.display = 'none';
            if (clearDatesBtn) clearDatesBtn.style.display = 'none';
            
            // Remove trip location marker if it exists
            this.removeTripLocationMarker();
        }
    }

    applyTripFiltering() {
        if (!this.tripPlan) return;
        
        // Filter events based on trip dates
        this.filterEventsByTrip();
        
        // Filter PYO based on trip season
        this.filterPYOByTrip();
        
        // Update popup factory with current trip plan for directions links
        if (this.popupFactory) {
            this.popupFactory.updateTripPlan(this.tripPlan);
        }
        
        Logger.extend('Applied trip filtering for:', this.tripPlan);
    }

    filterEventsByTrip() {
        if (!this.events || !this.events.events) return;
        
        const tripStart = new Date(this.tripPlan.startDate);
        const tripEnd = new Date(this.tripPlan.endDate);
        
        // Re-render events with filtering
        this.renderEvents(); // This will need to be modified to respect trip filtering
    }

    filterPYOByTrip() {
        const tripStartMonth = new Date(this.tripPlan.startDate).getMonth() + 1;
        const tripEndMonth = new Date(this.tripPlan.endDate).getMonth() + 1;
        
        // Update seasonal visibility based on trip dates
        const seasonalStatus = this.getSeasonalStatusForTrip(tripStartMonth, tripEndMonth);
        
        // Update the seasonal visibility object with trip-based status
        this.seasonalVisibility = seasonalStatus;
        
        // Re-render PYO layers with trip-based filtering
        this.renderFruitFarms();
        
        // Update legend to reflect trip-based seasonal status
        this.updateSeasonalLegend();
    }

    getSeasonalStatusForTrip(startMonth, endMonth) {
        // Determine what's in season during the trip
        return {
            apples: this.isInSeasonDuringTrip([9, 10, 11], startMonth, endMonth),
            strawberries: this.isInSeasonDuringTrip([5, 6, 7], startMonth, endMonth),
            cherries: this.isInSeasonDuringTrip([6, 7], startMonth, endMonth),
            peaches: this.isInSeasonDuringTrip([7, 8, 9], startMonth, endMonth)
        };
    }

    isInSeasonDuringTrip(seasonMonths, tripStartMonth, tripEndMonth) {
        for (let month = tripStartMonth; month <= tripEndMonth; month++) {
            if (seasonMonths.includes(month)) {
                return true;
            }
        }
        return false;
    }

    isEventRelevantToTrip(event) {
        if (!this.tripPlan) return true;
        
        const tripStart = new Date(this.tripPlan.startDate);
        const tripEnd = new Date(this.tripPlan.endDate);
        const eventStart = new Date(event.start_date);
        const eventEnd = event.end_date ? new Date(event.end_date) : eventStart;
        
        // Check if event overlaps with trip dates
        return eventStart <= tripEnd && eventEnd >= tripStart;
    }

    clearTripFiltering() {
        // Remove any trip-based filtering and restore normal display
        if (this.map) {
            this.map.eachLayer(layer => {
                if (layer.getElement) {
                    const element = layer.getElement();
                    if (element) {
                        element.classList.remove('trip-filtered', 'trip-relevant');
                    }
                }
            });
        }
        
        // Reset seasonal visibility to current status
        this.seasonalVisibility = this.getSeasonalStatus();
        
        // Re-render PYO layers with current seasonal status
        this.renderFruitFarms();
        
        // Re-render everything without trip filtering
        this.updateSeasonalLegend();
    }

    formatAddress(address) {
        if (!address) return '';
        
        // Handle common abbreviations and special cases
        const abbreviations = {
            'ny': 'NY',
            'nyc': 'NYC', 
            'usa': 'USA',
            'us': 'US',
            'st': 'St',
            'ave': 'Ave',
            'rd': 'Rd',
            'blvd': 'Blvd',
            'dr': 'Dr',
            'ln': 'Ln',
            'ct': 'Ct',
            'pl': 'Pl',
            'pkwy': 'Pkwy',
            'hwy': 'Hwy'
        };
        
        // Split by common separators and capitalize each part
        return address
            .split(/[,\s]+/) // Split by commas and spaces
            .map(part => {
                const lowerPart = part.toLowerCase().trim();
                
                // Handle abbreviations
                if (abbreviations[lowerPart]) {
                    return abbreviations[lowerPart];
                }
                
                // Handle empty parts
                if (!part.trim()) return '';
                
                // Capitalize first letter of each word
                return part.charAt(0).toUpperCase() + part.slice(1).toLowerCase();
            })
            .filter(part => part.length > 0) // Remove empty parts
            .join(' ')
            .replace(/\s+/g, ' ') // Clean up multiple spaces
            .trim();
    }

    createPopup(options) {
        // Handle both old and new popup structure for backward compatibility
        let content, links, coordinates, maxWidth;
        
        if (options.content && options.links) {
            // New structure
            content = options.content;
            links = options.links;
            coordinates = options.coordinates;
            maxWidth = options.maxWidth || 350;
        } else {
            // Legacy structure - convert to new structure
            content = {
                title: options.title,
                subtitle: options.subtitle,
                meta: options.meta || [],
                description: options.description,
                customContent: options.customContent || ''
            };
            links = {
                website: options.website ? { url: options.website, text: 'Website', icon: 'fa-external-link', className: 'popup__link--secondary' } : null,
                googleMaps: options.google_maps_url ? { url: options.google_maps_url, text: 'View on Google Maps', icon: 'fa-map-marker', className: 'popup__link--secondary' } : null,
                directions: null
            };
            coordinates = options.coordinates;
            maxWidth = options.maxWidth || 350;
        }
        
        // Build meta information
        const metaHtml = content.meta && content.meta.length > 0 ? 
            `<div class="popup__meta-container">${content.meta.map(item => `<span class="popup__meta">${item}</span>`).join('')}</div>` : '';
        
        // Build links from the new structure
        const linkElements = [];
        
        // Add website link if available
        if (links.website) {
            linkElements.push(this.renderLink(links.website));
        }
        
        // Add Google Maps link if available
        if (links.googleMaps) {
            linkElements.push(this.renderLink(links.googleMaps));
        }
        
        // Add directions link if available
        if (links.directions) {
            linkElements.push(this.renderLink(links.directions));
        }
        
        // Build links section
        const linksHtml = linkElements.length > 0 ? 
            `<div class="popup__links">${linkElements.join(' • ')}</div>` : '';
        
        // Build description
        const descriptionHtml = content.description ? 
            `<div class="popup__description">${content.description}</div>` : '';
        
        // Build subtitle
        const subtitleHtml = content.subtitle ? 
            `<div class="popup__subtitle">${content.subtitle}</div>` : '';
        
        // Create base popup content
        let popupContent = `
            <div class="popup">
                <h3 class="popup__title">${content.title}</h3>
                ${subtitleHtml}
                ${metaHtml}
                ${descriptionHtml}
                ${content.customContent || ''}
                ${linksHtml}
            </div>
        `;
        
        return popupContent;
    }

    // Helper method to render a link object as HTML
    renderLink(linkObj) {
        if (!linkObj) return '';
        return `<a href="${linkObj.url}" target="_blank" rel="noopener" class="popup__link ${linkObj.className}">
            <i class="fa ${linkObj.icon}"></i> ${linkObj.text}
        </a>`;
    }

    bindPopupToMarker(marker, options) {
        const popupContent = this.createPopup(options);
        const popup = L.popup(this.getPopupOptions(options.maxWidth || 350));
        popup.setContent(popupContent);
        marker.bindPopup(popup);
        return popup;
    }

    async geocodeTripAddress() {
        if (!this.tripPlan || !this.tripPlan.address) {
            Logger.basic('No trip plan or address to geocode');
            return;
        }
        
        try {
            Logger.extend('Geocoding trip address:', this.tripPlan.address);
            
            // Use a simple geocoding service (Nominatim - free and no API key required)
            const encodedAddress = encodeURIComponent(this.tripPlan.address);
            const geocodingUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodedAddress}&limit=1&countrycodes=us`;
            Logger.verbose('Geocoding URL:', geocodingUrl);
            
            const response = await fetch(geocodingUrl);
            
            if (!response.ok) {
                throw new Error(`Geocoding failed: ${response.status}`);
            }
            
            const data = await response.json();
            Logger.verbose('Geocoding response:', data);
            
            if (data && data.length > 0) {
                const result = data[0];
                const lat = parseFloat(result.lat);
                const lng = parseFloat(result.lon);
                
                Logger.extend('Geocoding successful:', { lat, lng, display_name: result.display_name });
                
                // Update trip plan with coordinates
                this.tripPlan.lat = lat;
                this.tripPlan.lng = lng;
                this.tripPlan.geocodedAddress = result.display_name;
                
                // Save updated trip plan
                this.saveTripPlan(this.tripPlan);
                
                // Plot the location
                this.plotTripLocation();
                
                Logger.basic('Trip address geocoded successfully:', lat, lng);
            } else {
                Logger.warn('No geocoding results found for:', this.tripPlan.address);
                this.showGeocodingError();
            }
        } catch (error) {
            Logger.error('Error geocoding trip address:', error);
            this.showGeocodingError();
        }
    }

    plotTripLocation() {
        // Plot trip marker/radius whenever coordinates exist, even if address is missing
        if (!this.tripPlan || this.tripPlan.lat == null || this.tripPlan.lng == null) return;
        if (!this.map) {
            Logger.warn('Map not ready for plotting trip location');
            return;
        }
        
        // Remove existing trip marker if it exists
        this.removeTripLocationMarker();
        
        // Create custom trip location icon
        const tripIcon = L.divIcon({
            className: 'trip-location-marker',
            html: '<div class="trip-icon">🏠</div>',
            iconSize: [35, 35],
            iconAnchor: [17, 17],
            popupAnchor: [0, -17]
        });
        
        // Create marker
        this.tripLocationMarker = L.marker([this.tripPlan.lat, this.tripPlan.lng], { 
            icon: tripIcon 
        }).addTo(this.map);
        
        // Create 25-mile radius circle
        this.tripRadiusCircle = L.circle([this.tripPlan.lat, this.tripPlan.lng], {
            radius: 25 * 1609.34, // Convert 25 miles to meters
            color: '#4CAF50',
            fillColor: '#4CAF50',
            fillOpacity: 0.05,
            weight: 1,
            opacity: 0.4,
            interactive: false, // Make it non-interactive so it doesn't interfere with clicks
            zIndexOffset: -1000 // Put it at the very bottom of the z-order
        }).addTo(this.map);
        
        // Create popup content
        const startDate = this.tripPlan.startDate ? new Date(this.tripPlan.startDate + 'T00:00:00').toLocaleDateString() : null;
        const endDate = this.tripPlan.endDate ? new Date(this.tripPlan.endDate + 'T00:00:00').toLocaleDateString() : null;
        const addressHtml = this.tripPlan.address ? `<p><strong>${this.formatAddress(this.tripPlan.address)}</strong></p>` : '';
        const datesHtml = (startDate && endDate) ? `<p><i class="fa fa-calendar"></i> ${startDate} - ${endDate}</p>` : '';
        const popupContent = `
            <div class="trip-popup">
                <h4><i class="fa fa-home"></i> Your Trip Location</h4>
                ${addressHtml}
                ${datesHtml}
                <p><i class="fa fa-circle-o"></i> 25-mile exploration radius</p>
            </div>
        `;
        
        this.tripLocationMarker.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'trip-popup-content'
        });
        
        // Center map on trip location with appropriate zoom
        this.map.setView([this.tripPlan.lat, this.tripPlan.lng], Math.max(this.map.getZoom(), 10));
        
        Logger.basic('Trip location plotted:', this.tripPlan.lat, this.tripPlan.lng);
    }

    removeTripLocationMarker() {
        if (this.tripLocationMarker) {
            this.map.removeLayer(this.tripLocationMarker);
            this.tripLocationMarker = null;
            Logger.extend('Trip location marker removed');
        }
        
        if (this.tripRadiusCircle) {
            this.map.removeLayer(this.tripRadiusCircle);
            this.tripRadiusCircle = null;
            Logger.extend('Trip radius circle removed');
        }
    }

    showGeocodingError() {
        // Show a user-friendly error message
        const errorMsg = document.createElement('div');
        errorMsg.className = 'geocoding-error';
        errorMsg.innerHTML = `
            <div style="background: #ffebee; border: 1px solid #f44336; border-radius: 4px; padding: 8px; margin: 8px 0; color: #c62828; font-size: 12px;">
                <i class="fa fa-exclamation-triangle"></i> 
                Could not find location for "${this.tripPlan.address}". Please try a more specific address.
            </div>
        `;
        
        const tripForm = document.getElementById('tripForm');
        if (tripForm) {
            tripForm.appendChild(errorMsg);
            
            // Remove error message after 5 seconds
            setTimeout(() => {
                if (errorMsg.parentNode) {
                    errorMsg.parentNode.removeChild(errorMsg);
                }
            }, 5000);
        }
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
            const [mapRes, wfRes, brRes, rsRes, orchRes, strawRes, cherryRes, peachRes, childrenRes, trailheadsRes, airbnbsRes, poiRes, regionsRes, eventsRes] = await Promise.all([
                fetch(`/data/map-data.json?t=${ts}`),
                fetch(`/data/waterfalls.json?t=${ts}`),
                fetch(`/data/breweries.json?t=${ts}`),
                fetch(`/data/restaurants.json?t=${ts}`),
                fetch(`/data/pyo_apples.json?t=${ts}`),
                fetch(`/data/pyo_strawberries.json?t=${ts}`),
                fetch(`/data/pyo_cherries.json?t=${ts}`),
                fetch(`/data/pyo_peaches.json?t=${ts}`),
                fetch(`/data/children.json?t=${ts}`),
                fetch(`/data/trail-heads.json?t=${ts}`),
                fetch(`/data/our-airbnbs.json?t=${ts}`),
                fetch(`/data/points_of_interest.json?t=${ts}`),
                fetch(`/data/nys_regions_redc_simplified_200m_disjoint.geojson?t=${ts}`),
                fetch(`/data/events.json?t=${ts}`)
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
            this.peachPoints = peachRes.ok ? await peachRes.json() : [];
            this.childrenActivities = childrenRes.ok ? await childrenRes.json() : [];
            this.trailheads = trailheadsRes.ok ? await trailheadsRes.json() : [];
            this.airbnbs = airbnbsRes.ok ? await airbnbsRes.json() : [];
            this.pointsOfInterest = poiRes.ok ? await poiRes.json() : [];
            if (regionsRes.ok) {
                this.regions = await regionsRes.json();
                console.log('Regions loaded:', this.regions.features?.length || 0, 'features');
            } else {
            Logger.error('Failed to load regions:', regionsRes.status, regionsRes.statusText);
                this.regions = [];
            }
            // Handle optional events.json gracefully (avoid parsing HTML fallback)
            try {
                const isJson = eventsRes.ok && (eventsRes.headers.get('content-type') || '').includes('application/json');
                this.events = isJson ? await eventsRes.json() : null;
            } catch (_) {
                this.events = null;
            }

            return this.data;
        } catch (error) {
            Logger.error('Error loading map data:', error);
            throw error;
        }
    }

    initializeMap() {
        const config = this.data.mapConfig;
        
        // Support both legacy and new map IDs present in different HTML variants
        const containerId = document.getElementById('scenic-ny-map') ? 'scenic-ny-map' : 'map_9eb96eb1fe9bc3ea56b51a20c1cf6a00';
        this.map = L.map(containerId, {
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

        // Initialize popup factory after map is ready
        this.popupFactory = new PopupFactory(this);
        Logger.extend('PopupFactory initialized:', this.popupFactory);
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
                // Build tooltip content with location info if available
                let tooltipContent = `<div class="map-tooltip">
                    <b>${area.name}</b>`;
                
                if (area.location_info) {
                    tooltipContent += `<small>${area.location_info}</small>`;
                }
                
                tooltipContent += `<small>Scenery Score: ${area.score}/10 • <span style="white-space: nowrap;">Drive: ${area.driveTime}</span></small>
                </div>`;
                
                polygon.bindTooltip(tooltipContent, { sticky: true });
            }

            // Use popup architecture for scenic areas
            const scenicData = {
                name: area.name,
                description: area.description,
                location_info: area.location_info,
                score: area.score,
                driveTime: area.driveTime,
                coordinates: area.coordinates
            };
            this.popupFactory.bindPopupToMarker(polygon, scenicData, 'scenicArea');
        });

        // Optionally register scenic areas as an overlay later if desired
    }

    renderRegions() {
        if (!this.regions || !this.regions.features || !Array.isArray(this.regions.features) || !this.regions.features.length) {
            Logger.basic('No regions data to render');
            return;
        }

        Logger.extend('Rendering regions:', this.regions.features.length, 'regions from GeoJSON');
        const regionGroup = L.featureGroup({}).addTo(this.map);

        // Define colors for each region (NYS REDC 10 regions)
        const regionColors = {
            'Western New York': '#FF6B6B',
            'Finger Lakes': '#4ECDC4', 
            'Southern Tier': '#45B7D1',
            'Central New York': '#96CEB4',
            'North Country': '#FFEAA7',
            'Mohawk Valley': '#DDA0DD',
            'Capital Region': '#98D8C8',
            'Mid-Hudson': '#F7DC6F',
            'New York City': '#BB8FCE',
            'Long Island': '#85C1E9'
        };

        this.regions.features.forEach((feature, index) => {
            if (!feature.properties || !feature.properties.name) {
                Logger.extend('Skipping feature with no name:', feature);
                return;
            }

            // Skip features with empty or invalid coordinates
            if (!feature.geometry || !feature.geometry.coordinates || !feature.geometry.coordinates[0] || feature.geometry.coordinates[0].length === 0) {
                Logger.extend('Skipping feature with empty coordinates:', feature.properties.name);
                return;
            }

            const regionName = feature.properties.name;
            const color = regionColors[regionName] || '#CCCCCC';
            Logger.verbose(`Creating region ${index + 1}:`, regionName);
            Logger.verbose('Feature geometry type:', feature.geometry.type);
            Logger.verbose('Feature coordinates sample:', feature.geometry.coordinates[0].slice(0, 3));
            
            // Just log coordinate ranges without filtering - let Leaflet handle any coordinate issues
            try {
                const coords = feature.geometry.coordinates[0];
                const lngValues = coords.map(c => c[0]).filter(v => typeof v === 'number' && !isNaN(v));
                const latValues = coords.map(c => c[1]).filter(v => typeof v === 'number' && !isNaN(v));
                
                if (lngValues.length > 0 && latValues.length > 0) {
                    Logger.extend('Coordinate range - Longitude:', Math.min(...lngValues), 'to', Math.max(...lngValues));
                    Logger.extend('Coordinate range - Latitude:', Math.min(...latValues), 'to', Math.max(...latValues));
                } else {
                    Logger.extend('No valid coordinates found for region:', regionName);
                }
            } catch (error) {
                Logger.warn('Error calculating coordinate ranges for region:', regionName, error);
            }
            
            // Use Leaflet's built-in GeoJSON support with explicit coordinate handling
            const geoJsonLayer = L.geoJSON(feature, {
                style: {
                    color: color,
                    weight: 0,
                    opacity: 0,
                    fillColor: color,
                    fillOpacity: 0.15, // Slightly increased opacity for better visibility
                    zIndexOffset: -50 // Behind other layers but more visible
                },
                coordsToLatLng: function(coords) {
                    // Explicitly handle coordinate conversion
                    return L.latLng(coords[1], coords[0]); // [lat, lng] from [lng, lat]
                }
            }).addTo(regionGroup);

            Logger.verbose('GeoJSON layer created and added to group:', regionName);
            Logger.verbose('Layer bounds:', geoJsonLayer.getBounds());

            // Add tooltip (only on non-mobile devices)
            if (!this.isMobile) {
                geoJsonLayer.bindTooltip(
                    `<div class="map-tooltip">${regionName}</div>`,
                    { sticky: true }
                );
            }

            // Create popup for the region
            const popup = L.popup(this.getPopupOptions(280));
            const countiesHint = feature.properties.counties_hint ? 
                `<div class="popup-meta"><strong>Counties:</strong> ${feature.properties.counties_hint.join(', ')}</div>` : '';
            const popupContent = $(`
                <div class="map-popup">
                    <h3 class="popup-title">${regionName}</h3>
                    <div class="popup-description">NYS REDC Region</div>
                    ${countiesHint}
                </div>
            `)[0];
            popup.setContent(popupContent);
            geoJsonLayer.bindPopup(popup);
        });

        Logger.extend('All regions processed. Region group has', regionGroup.getLayers().length, 'layers');
        Logger.verbose('Region group bounds:', regionGroup.getBounds());
        
        // Add regions directly to map first to test visibility
        regionGroup.addTo(this.map);
        Logger.extend('Regions added directly to map');

        // Register regions as an overlay for toggling
        if (this.layerControl) {
            this.layerControl.addOverlay(regionGroup, 'NY Regions');
            Logger.extend('Regions layer registered with layer control');
            Logger.verbose('Layer control overlays:', this.layerControl._overlays ? Object.keys(this.layerControl._overlays) : 'No overlays object');
            Logger.verbose('Layer control base layers:', this.layerControl._layers ? Object.keys(this.layerControl._layers) : 'No layers object');
        } else {
            Logger.basic('No layer control available for regions');
        }
        
        Logger.extend('Regions layer added to map with', this.regions.features.length, 'regions');
        
        // Force a map refresh to ensure visibility
        this.map.invalidateSize();
        
        // Try to fit the map to show the regions
        if (regionGroup.getBounds().isValid()) {
            Logger.extend('Fitting map to region bounds');
            Logger.verbose('Region group bounds:', regionGroup.getBounds());
            Logger.verbose('Map center:', this.map.getCenter());
            Logger.verbose('Map zoom:', this.map.getZoom());
            this.map.fitBounds(regionGroup.getBounds());
        }
    }

    async renderEvents() {
        if (!this.events || !this.events.events || !Array.isArray(this.events.events) || !this.events.events.length) {
            Logger.basic('No events data to render');
            return;
        }

        Logger.extend('Rendering events:', this.events.events.length, 'events');
        const eventGroup = L.featureGroup({}).addTo(this.map);

        for (const event of this.events.events) {
            // Require precomputed coordinates
            if (typeof event.lat !== 'number' || typeof event.lng !== 'number') {
                Logger.warn('Skipping event without coordinates:', event.name, event.address);
                continue;
            }

            Logger.verbose(`Creating event marker: ${event.name} at ${event.lat}, ${event.lng}`);

            // Check if event is relevant to trip
            const isRelevant = this.isEventRelevantToTrip(event);
            const tripClass = this.tripPlan ? (isRelevant ? 'trip-relevant' : 'trip-filtered') : '';

            // Create custom event icon
            const eventIcon = L.divIcon({
                className: `event-marker ${tripClass}`,
                html: '<div class="event-icon">🎪</div>',
                iconSize: [30, 30],
                iconAnchor: [15, 15],
                popupAnchor: [0, -15]
            });

            // Create marker
            const marker = L.marker([event.lat, event.lng], { icon: eventIcon }).addTo(eventGroup);

            // Format dates
            const startDate = new Date(event.start_date);
            const endDate = new Date(event.end_date);
            const dateFormat = startDate.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric',
                year: startDate.getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
            });
            
            let dateRange = dateFormat;
            if (event.start_date !== event.end_date) {
                const endDateFormat = endDate.toLocaleDateString('en-US', { 
                    month: 'short', 
                    day: 'numeric',
                    year: endDate.getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
                });
                dateRange = `${dateFormat} - ${endDateFormat}`;
            }

            // Add tooltip (only on non-mobile devices)
            if (!this.isMobile) {
                marker.bindTooltip(
                    `<div class="map-tooltip">
                        <b>${event.name}</b>
                        <small>${dateRange} • ${event.location_name}</small>
                    </div>`,
                    { sticky: true }
                );
            }

            // Create popup using new popup architecture
            this.popupFactory.bindPopupToMarker(marker, event, 'event');
        }

        Logger.extend('Events processed. Group has', eventGroup.getLayers().length, 'markers');
        
        // Register as an overlay for toggling
        if (this.layerControl) {
            this.layerControl.addOverlay(eventGroup, 'Events');
            Logger.extend('Events layer registered with layer control');
        }
        
        Logger.extend('Events layer added to map with', eventGroup.getLayers().length, 'events');
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

            // Use popup architecture for cities
            this.popupFactory.bindPopupToMarker(marker, city, 'city');

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

                // Use popup architecture for train stations
                const stationData = {
                    name: stop.name,
                    route: route.name,
                    operator: route.operator,
                    type: stop.type,
                    travelTime: stop.travelTime,
                    coordinates: stop.coordinates
                };
                this.popupFactory.bindPopupToMarker(stationMarker, stationData, 'trainStation');

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

    async renderFruitFarms() {
        try {
            // Clear existing farm markers
            if (this.overlays && this.overlays['Fruit Farms (PYO)']) {
                this.map.removeLayer(this.overlays['Fruit Farms (PYO)']);
            }
            
            // Load the new consolidated fruit farms data
            const response = await fetch('/data/pyo-fruit-farms.json');
            if (!response.ok) {
                Logger.error('Failed to load fruit farms data');
                return;
            }
            
            const farms = await response.json();
            if (!Array.isArray(farms) || !farms.length) {
                Logger.basic('No fruit farms data found');
                return;
            }
            
            // Store farms data for seasonal status checking
            this.fruitFarmsData = farms;
            
            // Debug current week
            const currentWeek = this.getCurrentWeek();
            Logger.extend(`Current week: ${currentWeek}`);
            
            const farmGroup = L.featureGroup({});
            
            // Create icons for different fruit types
            const fruitIcons = {
                apples: { icon: 'fa-apple', color: '#ff6b6b' },
                strawberries: { icon: 'fa-heart', color: '#ff6b6b' },
                cherries: { icon: 'fa-circle', color: '#ff6b6b' },
                peaches: { icon: 'fa-circle', color: '#ffa500' }
            };
            
            farms.forEach(farm => {
                if (!farm.lat || !farm.lng || isNaN(farm.lat) || isNaN(farm.lng)) return;
                
                // Determine which fruits are in season using trip dates if available, otherwise current date
                const inSeasonFruits = farm.fruits.filter(fruit => {
                    if (this.tripPlan && this.tripPlan.startDate && this.tripPlan.endDate) {
                        // Use trip dates for seasonal filtering
                        return this.isInSeasonForTrip(fruit.season_start_week, fruit.season_end_week, this.tripPlan.startDate, this.tripPlan.endDate);
                    } else {
                        // Use current date for seasonal filtering
                        return this.isInSeason(fruit.season_start_week, fruit.season_end_week);
                    }
                });
                
                // Debug logging
                const usingTripDates = this.tripPlan && this.tripPlan.startDate && this.tripPlan.endDate;
                Logger.verbose(`Farm: ${farm.name}, Fruits: ${farm.fruits.map(f => f.type).join(', ')}, In Season: ${inSeasonFruits.map(f => f.type).join(', ')} (using ${usingTripDates ? 'trip dates' : 'current date'})`);
                
                // Use the first in-season fruit icon, or first fruit if none in season
                const displayFruit = inSeasonFruits.length > 0 ? inSeasonFruits[0] : farm.fruits[0];
                const iconData = fruitIcons[displayFruit.type] || { icon: 'fa-seedling', color: '#8B4513' };
                
                Logger.verbose(`Displaying fruit: ${displayFruit.type} for ${farm.name}`);
                
                // Determine if any fruits are in season for styling
                const hasInSeasonFruits = inSeasonFruits.length > 0;
                const iconClass = hasInSeasonFruits ? 'icon-marker icon-farm' : 'icon-marker icon-farm out-of-season';
                
                const farmDivIcon = L.divIcon({
                    className: iconClass,
                    html: `<i class="fa ${iconData.icon}" style="color: ${iconData.color}; font-size: 16px;"></i>`,
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });
                
                const marker = L.marker([farm.lat, farm.lng], { 
                    icon: farmDivIcon,
                    zIndexOffset: hasInSeasonFruits ? 0 : -200 
                }).addTo(farmGroup);
                
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    const fruitTypes = farm.fruits.map(f => f.type).join(', ');
                    const tooltipLine = hasInSeasonFruits ? 
                        `<br/><small>${fruitTypes}</small>` : 
                        '<br/><small>All fruits out of season</small>';
                    marker.bindTooltip(`<div class="map-tooltip">${farm.name}${tooltipLine}</div>`, { sticky: true });
                }
                
                // Use popup architecture for farms
                Logger.extend('Binding popup to farm marker, popupFactory available:', !!this.popupFactory);
                this.popupFactory.bindPopupToMarker(marker, farm, 'farm');
            });
            
            this.overlays = this.overlays || {};
            this.overlays['Fruit Farms (PYO)'] = farmGroup;
            farmGroup.addTo(this.map);
            
            Logger.extend('Fruit farms rendered:', farms.length);
        } catch (e) {
            Logger.error('Error rendering fruit farms:', e);
        }
    }

    async renderOrchards() {
        try {
            // Clear existing orchard markers
            if (this.overlays && this.overlays['Orchards (PYO)']) {
                this.map.removeLayer(this.overlays['Orchards (PYO)']);
            }
            
            const points = Array.isArray(this.orchardPoints) ? this.orchardPoints : [];
            
            // Determine seasonal status based on trip or current season
            let seasonalStatus;
            if (this.tripPlan) {
                const tripStartMonth = new Date(this.tripPlan.startDate).getMonth() + 1;
                const tripEndMonth = new Date(this.tripPlan.endDate).getMonth() + 1;
                seasonalStatus = this.getSeasonalStatusForTrip(tripStartMonth, tripEndMonth);
            } else {
                seasonalStatus = this.getSeasonalStatus();
            }

            const orchards = Array.isArray(points)
                ? points.map(p => ({
                    name: p.name,
                    address: p.address,
                    website: p.website,
                    approx_drive: p.approx_drive,
                    notes: p.notes,
                    season_start_week: p.season_start_week,
                    season_end_week: p.season_end_week,
                    coords: [p.lat, p.lng],
                    place_id: p.place_id,
                    google_maps_url: p.google_maps_url,
                    organic: p.organic || false
                }))
                : [];
 
            if (!orchards.length) return;

            const orchardGroup = L.featureGroup({});

            orchards.forEach(o => {
                if (!o.coords || isNaN(o.coords[0]) || isNaN(o.coords[1])) return;
                
                // Use the seasonal status determined above (trip-based or current)
                const farmInSeason = seasonalStatus.apples;
                
                
                // Create icon with appropriate styling
                const iconClass = farmInSeason ? 'icon-marker icon-apple' : 'icon-marker icon-apple out-of-season';
                const orchardIcon = L.divIcon({
                    className: iconClass,
                    html: '<span style="font-size: 16px;">🍎</span>',
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });
                
                const marker = L.marker(o.coords, { icon: orchardIcon, zIndexOffset: farmInSeason ? 0 : -200 }).addTo(orchardGroup);
                const notes = o.notes ? `<br/><small>${o.notes}</small>` : '';
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    const tooltipLine = farmInSeason ? notes : '<br/><small>Apples — Out of Season</small>';
                    marker.bindTooltip(`<div class="map-tooltip">${o.name}${tooltipLine}</div>`, { sticky: true });
                }
                const linkHtml = o.website ? `<a href="${o.website}" target="_blank" rel="noopener">Website</a>` : '';
                const googleMapsLink = o.google_maps_url ? 
                    `<a href="${o.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                
                const websiteLink = o.website ? 
                    `<a href="${o.website}" target="_blank" rel="noopener" class="popup-link">Website</a>` : '';
                
                const links = [websiteLink, googleMapsLink].filter(Boolean).join(' • ');
                
                const seasonStatus = farmInSeason ? '' : '<span class="popup-meta" style="color: #ff6b6b;"><strong>⚠️ Out of Season</strong></span>';
                
                // Create popup using unified architecture
                const organicBadge = o.organic ? ' <span style="color: #4CAF50; font-size: 14px;">🌱 Organic</span>' : '';
                
                // Use popup architecture for orchards
                this.popupFactory.bindPopupToMarker(marker, o, 'farm');
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
            // Clear existing strawberry markers
            if (this.overlays && this.overlays['Strawberries (PYO)']) {
                this.map.removeLayer(this.overlays['Strawberries (PYO)']);
            }
            
            const points = Array.isArray(this.strawberryPoints) ? this.strawberryPoints : [];
            
            // Determine seasonal status based on trip or current season
            let seasonalStatus;
            if (this.tripPlan) {
                const tripStartMonth = new Date(this.tripPlan.startDate).getMonth() + 1;
                const tripEndMonth = new Date(this.tripPlan.endDate).getMonth() + 1;
                seasonalStatus = this.getSeasonalStatusForTrip(tripStartMonth, tripEndMonth);
            } else {
                seasonalStatus = this.getSeasonalStatus();
            }

            const strawberries = Array.isArray(points)
                ? points.map(p => ({
                    name: p.name,
                    address: p.address,
                    website: p.website,
                    reservation_required: p.reservation_required,
                    notes: p.notes,
                    season_start_week: p.season_start_week,
                    season_end_week: p.season_end_week,
                    coords: [p.lat, p.lng],
                    place_id: p.place_id,
                    google_maps_url: p.google_maps_url,
                    organic: p.organic || false
                }))
                : [];
 
            if (!strawberries.length) return;

            const strawberryGroup = L.featureGroup({});

            strawberries.forEach(s => {
                if (!s.coords || isNaN(s.coords[0]) || isNaN(s.coords[1])) return;
                
                // Use the seasonal status determined above (trip-based or current)
                const farmInSeason = seasonalStatus.strawberries;
                
                // Create icon with appropriate styling
                const iconClass = farmInSeason ? 'icon-marker icon-strawberry' : 'icon-marker icon-strawberry out-of-season';
                const strawberryIcon = L.divIcon({
                    className: iconClass,
                    html: '<span style="font-size: 16px;">🍓</span>',
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });
                
                const marker = L.marker(s.coords, { icon: strawberryIcon, zIndexOffset: farmInSeason ? 0 : -200 }).addTo(strawberryGroup);
                const notes = s.notes ? `<br/><small>${s.notes}</small>` : '';
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    const tooltipLine = farmInSeason ? notes : '<br/><small>Strawberries — Out of Season</small>';
                    marker.bindTooltip(`<div class="map-tooltip">${s.name}${tooltipLine}</div>`, { sticky: true });
                }
                
                const googleMapsLink = s.google_maps_url ? 
                    `<a href="${s.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                
                const websiteLink = s.website ? 
                    `<a href="${s.website}" target="_blank" rel="noopener" class="popup-link">Website</a>` : '';
                
                const links = [websiteLink, googleMapsLink].filter(Boolean);
                
                const seasonStatus = farmInSeason ? '' : '<span class="popup-meta" style="color: #ff6b6b;"><strong>⚠️ Out of Season</strong></span>';
                
                // Use popup architecture for strawberries
                this.popupFactory.bindPopupToMarker(marker, s, 'farm');
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
            // Clear existing cherry markers
            if (this.overlays && this.overlays['Cherries (PYO)']) {
                this.map.removeLayer(this.overlays['Cherries (PYO)']);
            }
            
            const points = Array.isArray(this.cherryPoints) ? this.cherryPoints : [];
            
            // Determine seasonal status based on trip or current season
            let seasonalStatus;
            if (this.tripPlan) {
                const tripStartMonth = new Date(this.tripPlan.startDate).getMonth() + 1;
                const tripEndMonth = new Date(this.tripPlan.endDate).getMonth() + 1;
                seasonalStatus = this.getSeasonalStatusForTrip(tripStartMonth, tripEndMonth);
            } else {
                seasonalStatus = this.getSeasonalStatus();
            }

            const cherries = Array.isArray(points)
                ? points.map(p => ({
                    name: p.name,
                    address: p.address,
                    website: p.website,
                    reservation_required: p.reservation_required,
                    notes: p.notes,
                    season_start_week: p.season_start_week,
                    season_end_week: p.season_end_week,
                    coords: [p.lat, p.lng],
                    place_id: p.place_id,
                    google_maps_url: p.google_maps_url,
                    organic: p.organic || false
                }))
                : [];
 
            if (!cherries.length) return;

            const cherryGroup = L.featureGroup({});

            cherries.forEach(c => {
                if (!c.coords || isNaN(c.coords[0]) || isNaN(c.coords[1])) return;
                
                // Use the seasonal status determined above (trip-based or current)
                const farmInSeason = seasonalStatus.cherries;
                
                // Create icon with appropriate styling
                const iconClass = farmInSeason ? 'icon-marker icon-cherry' : 'icon-marker icon-cherry out-of-season';
                const cherryIcon = L.divIcon({
                    className: iconClass,
                    html: '<span style="font-size: 16px;">🍒</span>',
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });
                
                const marker = L.marker(c.coords, { icon: cherryIcon, zIndexOffset: farmInSeason ? 0 : -200 }).addTo(cherryGroup);
                const notes = c.notes ? `<br/><small>${c.notes}</small>` : '';
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    const tooltipLine = farmInSeason ? notes : '<br/><small>Cherries — Out of Season</small>';
                    marker.bindTooltip(`<div class="map-tooltip">${c.name}${tooltipLine}</div>`, { sticky: true });
                }
                
                const googleMapsLink = c.google_maps_url ? 
                    `<a href="${c.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                
                const websiteLink = c.website ? 
                    `<a href="${c.website}" target="_blank" rel="noopener" class="popup-link">Website</a>` : '';
                
                const links = [websiteLink, googleMapsLink].filter(Boolean);
                
                const seasonStatus = farmInSeason ? '' : '<span class="popup-meta" style="color: #ff6b6b;"><strong>⚠️ Out of Season</strong></span>';
                
                // Use popup architecture for cherries
                this.popupFactory.bindPopupToMarker(marker, c, 'farm');
            });

            this.overlays = this.overlays || {};
            this.overlays['Cherries (PYO)'] = cherryGroup;
            cherryGroup.addTo(this.map);
        } catch (e) {
            // swallow
        }
    }

    async renderPeaches() {
        try {
            // Clear existing peach markers
            if (this.overlays && this.overlays['Peaches (PYO)']) {
                this.map.removeLayer(this.overlays['Peaches (PYO)']);
            }
            
            const points = Array.isArray(this.peachPoints) ? this.peachPoints : [];
            
            // Determine seasonal status based on trip or current season
            let seasonalStatus;
            if (this.tripPlan) {
                const tripStartMonth = new Date(this.tripPlan.startDate).getMonth() + 1;
                const tripEndMonth = new Date(this.tripPlan.endDate).getMonth() + 1;
                seasonalStatus = this.getSeasonalStatusForTrip(tripStartMonth, tripEndMonth);
            } else {
                seasonalStatus = this.getSeasonalStatus();
            }

            const peaches = Array.isArray(points)
                ? points.map(p => ({
                    name: p.name,
                    address: p.address,
                    website: p.website,
                    reservation_required: p.reservation_required,
                    notes: p.notes,
                    season_start_week: p.season_start_week,
                    season_end_week: p.season_end_week,
                    coords: [p.lat, p.lng],
                    place_id: p.place_id,
                    google_maps_url: p.google_maps_url,
                    organic: p.organic || false
                }))
                : [];
 
            if (!peaches.length) return;

            const peachGroup = L.featureGroup({});

            peaches.forEach(p => {
                if (!p.coords || isNaN(p.coords[0]) || isNaN(p.coords[1])) return;
                
                // Use the seasonal status determined above (trip-based or current)
                const farmInSeason = seasonalStatus.peaches;
                
                // Create icon with appropriate styling
                const iconClass = farmInSeason ? 'icon-marker icon-peach' : 'icon-marker icon-peach out-of-season';
                const peachIcon = L.divIcon({
                    className: iconClass,
                    html: '<span style="font-size: 16px;">🍑</span>',
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });
                
                const marker = L.marker(p.coords, { icon: peachIcon, zIndexOffset: farmInSeason ? 0 : -200 }).addTo(peachGroup);
                const notes = p.notes ? `<br/><small>${p.notes}</small>` : '';
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    const tooltipLine = farmInSeason ? notes : '<br/><small>Peaches — Out of Season</small>';
                    marker.bindTooltip(`<div class="map-tooltip">${p.name}${tooltipLine}</div>`, { sticky: true });
                }
                
                const googleMapsLink = p.google_maps_url ? 
                    `<a href="${p.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                
                const websiteLink = p.website ? 
                    `<a href="${p.website}" target="_blank" rel="noopener" class="popup-link">Website</a>` : '';
                
                const links = [websiteLink, googleMapsLink].filter(Boolean);
                
                const seasonStatus = farmInSeason ? '' : '<span class="popup-meta" style="color: #ff6b6b;"><strong>⚠️ Out of Season</strong></span>';
                
                // Use popup architecture for peaches
                this.popupFactory.bindPopupToMarker(marker, p, 'farm');
            });

            this.overlays = this.overlays || {};
            this.overlays['Peaches (PYO)'] = peachGroup;
            peachGroup.addTo(this.map);
        } catch (e) {
            // swallow
        }
    }

    async renderChildren() {
        try {
            const activities = Array.isArray(this.childrenActivities) ? this.childrenActivities : [];

            if (!activities.length) return;

            const childrenGroup = L.featureGroup({});
            const childrenDivIcon = (L.divIcon({
                className: 'icon-marker icon-children',
                html: '<span style="font-size: 16px;">🎠</span>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            }));

            activities.forEach(activity => {
                if (!activity.lat || !activity.lng || isNaN(activity.lat) || isNaN(activity.lng)) return;
                const marker = L.marker([activity.lat, activity.lng], { icon: childrenDivIcon }).addTo(childrenGroup);
                
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    const shortDesc = activity.description || activity.name;
                    marker.bindTooltip(`<div class="map-tooltip">${activity.name}<br/><small>${shortDesc}</small></div>`, { sticky: true });
                }
                
                const googleMapsLink = activity.place_id ? 
                    `<a href="https://maps.google.com/?place_id=${activity.place_id}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                
                const websiteLink = activity.website ? 
                    `<a href="${activity.website}" target="_blank" rel="noopener" class="popup-link">Website</a>` : '';
                
                const links = [websiteLink, googleMapsLink].filter(Boolean);
                
                // Use popup architecture for children activities
                this.popupFactory.bindPopupToMarker(marker, activity, 'children');
            });

            this.overlays = this.overlays || {};
            this.overlays['Children\'s Activities'] = childrenGroup;
            childrenGroup.addTo(this.map);
        } catch (e) {
            // swallow
        }
    }

    async renderTrailheads() {
        try {
            const trailheadsData = Array.isArray(this.trailheads) ? this.trailheads : [];

            if (!trailheadsData.length) return;

            const trailheadsGroup = L.featureGroup({});
            const trailheadDivIcon = (L.divIcon({
                className: 'icon-marker icon-trailhead',
                html: '<span style="font-size: 16px; color: #2E8B57;">▲</span>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            }));

            // Process each region's trails
            trailheadsData.forEach(region => {
                if (region.trails && Array.isArray(region.trails)) {
                    region.trails.forEach(trail => {
                        if (!trail.lat || !trail.lng || isNaN(trail.lat) || isNaN(trail.lng)) return;
                        const marker = L.marker([trail.lat, trail.lng], { icon: trailheadDivIcon }).addTo(trailheadsGroup);
                        
                        // Only show tooltips on non-mobile devices
                        if (!this.isMobile) {
                            const shortDesc = trail.description || trail.name;
                            marker.bindTooltip(`<div class="map-tooltip">${trail.name}<br/><small>${shortDesc}</small></div>`, { sticky: true });
                        }
                        
                        const googleMapsLink = trail.place_id ? 
                            `<a href="https://maps.google.com/?place_id=${trail.place_id}" target="_blank" rel="noopener" class="popup-link">
                                <i class="fa fa-map-marker"></i> View on Google Maps
                            </a>` : '';
                        
                        const links = googleMapsLink ? [googleMapsLink] : [];
                        
                        // Use popup architecture for trailheads
                        this.popupFactory.bindPopupToMarker(marker, trail, 'trail');
                    });
                }
            });

            this.overlays = this.overlays || {};
            this.overlays['Trailheads'] = trailheadsGroup;
            trailheadsGroup.addTo(this.map);
        } catch (e) {
            // swallow
        }
    }

    async renderAirbnbs() {
        try {
            const airbnbs = Array.isArray(this.airbnbs) ? this.airbnbs : [];
            Logger.extend('Airbnbs loaded:', airbnbs.length);

            if (!airbnbs.length) {
                Logger.basic('No airbnbs found');
                return;
            }

            const airbnbGroup = L.featureGroup({});
            const airbnbDivIcon = (L.divIcon({
                className: 'icon-marker icon-airbnb',
                html: '<span style="font-size: 16px;">🏠</span>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            }));

            airbnbs.forEach(airbnb => {
                if (!airbnb.lat || !airbnb.lng || isNaN(airbnb.lat) || isNaN(airbnb.lng)) {
                    Logger.warn('Invalid coordinates for:', airbnb.name, airbnb.lat, airbnb.lng);
                    return;
                }
                Logger.verbose('Adding Airbnb:', airbnb.name, 'at', airbnb.lat, airbnb.lng);
                const marker = L.marker([airbnb.lat, airbnb.lng], { icon: airbnbDivIcon }).addTo(airbnbGroup);
                
                // Only show tooltips on non-mobile devices
                if (!this.isMobile) {
                    marker.bindTooltip(`<div class="map-tooltip">${airbnb.name}</div>`, { sticky: true });
                }
                
                const googleMapsLink = airbnb.url ? 
                    `<a href="${airbnb.url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';
                
                const links = googleMapsLink ? [googleMapsLink] : [];
                
                // Use popup architecture for airbnbs
                this.popupFactory.bindPopupToMarker(marker, airbnb, 'airbnb');
            });

            this.overlays = this.overlays || {};
            this.overlays['Our Airbnbs'] = airbnbGroup;
            airbnbGroup.addTo(this.map);
            Logger.extend('Airbnbs layer added to map');
        } catch (e) {
            Logger.error('Error rendering airbnbs:', e);
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

                // Use popup architecture for waterfalls
                this.popupFactory.bindPopupToMarker(marker, w, 'waterfall');
            });

            // Add to map by default and register as overlay for toggling
            wfGroup.addTo(this.map);
            if (this.layerControl) {
                this.layerControl.addOverlay(wfGroup, 'Waterfalls');
            }
        } catch (e) {
            Logger.error('Failed to load waterfalls:', e);
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

                // Use popup architecture for breweries
                this.popupFactory.bindPopupToMarker(marker, b, 'brewery');
            });

            brGroup.addTo(this.map);
            if (this.layerControl) {
                this.layerControl.addOverlay(brGroup, 'Breweries');
            }
        } catch (e) {
            Logger.error('Failed to load breweries:', e);
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
                
                const googleMapsLink = rst.google_maps_url ? 
                    `<a href="${rst.google_maps_url}" target="_blank" rel="noopener" class="popup-link">
                        <i class="fa fa-map-marker"></i> View on Google Maps
                    </a>` : '';

                const links = googleMapsLink ? [googleMapsLink] : [];
                
                // Use popup architecture for restaurants
                this.popupFactory.bindPopupToMarker(marker, rst, 'restaurant');
            });

            rsGroup.addTo(this.map);
            if (this.layerControl) {
                this.layerControl.addOverlay(rsGroup, 'Restaurants');
            }
        } catch (e) {
            Logger.error('Failed to load restaurants:', e);
        }
    }

    async renderPointsOfInterest() {
        try {
            if (!this.pointsOfInterest || !Array.isArray(this.pointsOfInterest) || !this.pointsOfInterest.length) {
            Logger.basic('No points of interest data to render');
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

                const links = [websiteLink, googleMapsLink].filter(Boolean);
                
                // Use popup architecture for points of interest
                this.popupFactory.bindPopupToMarker(marker, poi, 'poi');
            });

            poiGroup.addTo(this.map);
            if (this.layerControl) {
                this.layerControl.addOverlay(poiGroup, 'Points of Interest');
            }

            Logger.extend(`Rendered ${this.pointsOfInterest.length} points of interest`);
        } catch (e) {
            Logger.error('Failed to load points of interest:', e);
        }
    }

    // Parse URL parameters for custom markers
    parseUrlParameters() {
        const urlParams = new URLSearchParams(window.location.search);
        const lat = parseFloat(urlParams.get('lat'));
        const lng = parseFloat(urlParams.get('lng'));
        
        if (!isNaN(lat) && !isNaN(lng) && lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
            const data = {
                lat,
                lng,
                id: urlParams.get('id'),
                title: urlParams.get('title') ? decodeURIComponent(urlParams.get('title')) : null,
                location: urlParams.get('location') ? decodeURIComponent(urlParams.get('location')) : null,
                rating: urlParams.get('rating'),
                bedrooms: urlParams.get('bedrooms'),
                bathrooms: urlParams.get('bathrooms'),
                airbnb_url: urlParams.get('airbnb_url') ? decodeURIComponent(urlParams.get('airbnb_url')) : null,
                source: urlParams.get('source'),
                // Legacy support for 'label' parameter
                label: urlParams.get('label') ? decodeURIComponent(urlParams.get('label')) : null
            };
            
            // Use title as the main label, fallback to legacy label, then default
            data.displayLabel = data.title || data.label || 'Custom Location';
            
            return data;
        }
        return null;
    }

    // Render custom marker from URL parameters
    renderCustomMarker() {
        const customLocation = this.parseUrlParameters();
        if (!customLocation) return;

        // Create a distinctive icon for custom markers
        const customIcon = L.divIcon({
            className: 'icon-marker icon-custom',
            html: '<span style="font-size: 18px; color: #ff4444;">📍</span>',
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });

        // Add the custom marker
        const marker = L.marker([customLocation.lat, customLocation.lng], { 
            icon: customIcon,
            zIndexOffset: 1000 // Above all other markers
        }).addTo(this.map);

        // Add tooltip
        if (!this.isMobile) {
            marker.bindTooltip(`<div class="map-tooltip"><b>${customLocation.displayLabel}</b></div>`, { sticky: true });
        }

        // Build rich popup content with better formatting
        let popupContent = `<div class="map-popup custom-location-popup">
            <h3 class="popup-title">${customLocation.displayLabel}</h3>`;
        
        // Add location if available
        if (customLocation.location) {
            popupContent += `<div class="popup-location">
                <i class="fa fa-map-marker-alt" style="color: #ff4444; margin-right: 6px;"></i>
                <span class="popup-meta">${customLocation.location}</span>
            </div>`;
        }
        
        // Add rating and accommodation info in a row
        if (customLocation.rating || customLocation.bedrooms || customLocation.bathrooms) {
            popupContent += `<div class="popup-details-row">`;
            
            // Add rating if available
            if (customLocation.rating) {
                const stars = '★'.repeat(Math.floor(parseFloat(customLocation.rating))) + 
                             (parseFloat(customLocation.rating) % 1 >= 0.5 ? '☆' : '');
                popupContent += `<div class="popup-rating">
                    <span style="color: #ffd700; font-size: 14px;">${stars}</span>
                    <span class="popup-meta-small" style="margin-left: 4px;">${customLocation.rating}/5.0</span>
                </div>`;
            }
            
            // Add bedrooms and bathrooms if available
            if (customLocation.bedrooms || customLocation.bathrooms) {
                const bedText = customLocation.bedrooms ? `${customLocation.bedrooms} bed${customLocation.bedrooms !== '1' ? 's' : ''}` : '';
                const bathText = customLocation.bathrooms ? `${customLocation.bathrooms} bath${customLocation.bathrooms !== '1' ? 's' : ''}` : '';
                const separator = bedText && bathText ? ' • ' : '';
                popupContent += `<div class="popup-accommodation">
                    <i class="fa fa-home" style="color: #666; margin-right: 4px; font-size: 12px;"></i>
                    <span class="popup-meta-small">${bedText}${separator}${bathText}</span>
                </div>`;
            }
            
            popupContent += `</div>`;
        }
        
        // Add source and coordinates in a subtle way
        popupContent += `<div class="popup-footer">
            <span class="popup-meta-small" style="color: #999;">
                ${customLocation.source ? customLocation.source.charAt(0).toUpperCase() + customLocation.source.slice(1) : 'Custom'} • 
                ${customLocation.lat.toFixed(5)}, ${customLocation.lng.toFixed(5)}
            </span>
        </div>`;
        
        // Add action buttons
        popupContent += `<div class="popup-links-container">`;
        
        // Add directions link
        const directionsUrl = `https://www.google.com/maps/dir/Bedford+Stuyvesant,+Brooklyn,+NY/${customLocation.lat},${customLocation.lng}`;
        popupContent += `<a href="${directionsUrl}" target="_blank" rel="noopener" class="popup-link directions-link">
            <i class="fa fa-route"></i> Get Directions
        </a>`;
        
        // Add Airbnb link if available
        if (customLocation.airbnb_url) {
            popupContent += `<a href="${customLocation.airbnb_url}" target="_blank" rel="noopener" class="popup-link airbnb-link">
                <i class="fa fa-external-link-alt"></i> View on Airbnb
            </a>`;
        }
        
        popupContent += `</div>`;
        
        popupContent += '</div>';

        // Add popup
        const popup = L.popup(this.getPopupOptions(350));
        popup.setContent(popupContent);
        marker.bindPopup(popup);

        // Center map on the custom marker
        this.map.setView([customLocation.lat, customLocation.lng], Math.max(this.map.getZoom(), 12));
        
        // Open the popup automatically
        marker.openPopup();

        Logger.extend('Custom marker added:', customLocation);
    }

    async render() {
        try {
            await this.loadData();
            this.initializeMap();
            this.renderRegions(); // Render regions first (behind everything)
            this.renderScenicAreas();
            await this.renderEvents();
            this.renderTrainRoutes();
            await this.renderFruitFarms();
            await this.renderChildren();
            await this.renderTrailheads();
            await this.renderAirbnbs();
            await this.renderWaterfalls();
            await this.renderBreweries();
            await this.renderRestaurants();
            await this.renderPointsOfInterest();
            this.renderCities(); // Render cities last so they appear on top
            
            // Render custom marker from URL parameters (after all other markers)
            this.renderCustomMarker();
            
            // Update seasonal legend and add click handlers
            this.updateSeasonalLegend();
            this.addSeasonalClickHandlers();
            
            // Initialize trip planning
            this.initializeTripPlanning();
            
            // Make map instance globally accessible for trip planning functions
            window.mapInstance = this;
            
            // Test if setTrip function is accessible
            Logger.verbose('setTrip function available:', typeof window.setTrip);
            Logger.verbose('setTrip function available globally:', typeof setTrip);
            
            // Add event listener directly to the form
            const tripForm = document.getElementById('tripForm');
            if (tripForm) {
                const form = tripForm.querySelector('form');
                if (form) {
                    Logger.extend('Adding event listener to form');
                    form.addEventListener('submit', function(event) {
                        Logger.verbose('Form submit event listener triggered');
                        event.preventDefault();
                        window.setTrip(event);
                    });
                }
            }
            
            // Debug: Log current week and seasonal status
            const currentWeek = this.getCurrentWeek();
            Logger.extend('Current week:', currentWeek);
            Logger.extend('Seasonal status:', this.getSeasonalStatus());
            
            // Debug: Show sample of individual farm seasonal data
            if (this.orchardPoints && this.orchardPoints.length > 0) {
                const sampleFarm = this.orchardPoints[0];
                Logger.verbose('Sample apple farm seasonal data:', {
                    name: sampleFarm.name,
                    season_start_week: sampleFarm.season_start_week,
                    season_end_week: sampleFarm.season_end_week,
                    inSeason: this.isInSeason(sampleFarm.season_start_week, sampleFarm.season_end_week)
                });
            }
            
            Logger.basic('Map rendered successfully with', this.scenicAreas.length, 'scenic areas,', this.cities.length, 'cities, and', this.data.trainRoutes.length, 'train routes');
        } catch (error) {
            Logger.error('Error rendering map:', error);
        }
    }
}

// Global functions for trip planning
window.setTrip = function(event) {
    Logger.extend('setTrip function called');
    event.preventDefault();
    Logger.verbose('Event prevented, continuing...');
    
    if (!window.mapInstance) {
        Logger.error('Map instance not available yet');
        alert('Map is still loading. Please wait a moment and try again.');
        return;
    }
    
    const address = document.getElementById('tripAddress').value.trim();
    const startDate = document.getElementById('tripStartDate').value;
    const endDate = document.getElementById('tripEndDate').value;
    
    if (!startDate || !endDate) {
        alert('Please fill in start and end dates');
        return;
    }
    
    if (new Date(startDate) > new Date(endDate)) {
        alert('End date must be after start date');
        return;
    }
    
    const tripPlan = {
        address: address || null, // Allow null address
        startDate: startDate,
        endDate: endDate,
        createdAt: new Date().toISOString()
    };
    
    Logger.basic('Setting trip plan:', tripPlan);
    
    // Save trip plan
    window.mapInstance.saveTripPlan(tripPlan, true);
    window.mapInstance.updateTripDisplay();
}

window.clearTrip = function() {
    if (!window.mapInstance) {
        Logger.error('Map instance not available yet');
        alert('Map is still loading. Please wait a moment and try again.');
        return;
    }
    
    // Clear countdown interval
    if (window.mapInstance.tripCountdownInterval) {
        clearInterval(window.mapInstance.tripCountdownInterval);
        window.mapInstance.tripCountdownInterval = null;
    }
    
    // Clear cookie
    document.cookie = 'tripPlan=; max-age=0; path=/';
    window.mapInstance.tripPlan = null;
    
    // Update popup factory to clear trip plan
    if (window.mapInstance.popupFactory) {
        window.mapInstance.popupFactory.updateTripPlan(null);
    }
    
    window.mapInstance.updateTripDisplay();
    
    // Clear any trip filtering
    window.mapInstance.clearTripFiltering();
    
    // Re-render fruit farms to reflect seasonal filtering based on current date
    window.mapInstance.renderFruitFarms();
    
    // Remove trip location marker
    window.mapInstance.removeTripLocationMarker();
}

window.clearTripLocation = function() {
    if (!window.mapInstance || !window.mapInstance.tripPlan) {
        return;
    }
    
    // Clear location-related fields
    window.mapInstance.tripPlan.address = null;
    window.mapInstance.tripPlan.lat = null;
    window.mapInstance.tripPlan.lng = null;
    window.mapInstance.tripPlan.geocodedAddress = null;
    
    // Save updated trip plan
    window.mapInstance.saveTripPlan(window.mapInstance.tripPlan);
    window.mapInstance.updateTripDisplay();
    
    // Remove trip location marker
    window.mapInstance.removeTripLocationMarker();
}

window.clearTripDates = function() {
    if (!window.mapInstance || !window.mapInstance.tripPlan) {
        return;
    }
    
    // Clear date-related fields
    window.mapInstance.tripPlan.startDate = null;
    window.mapInstance.tripPlan.endDate = null;
    
    // Save updated trip plan
    window.mapInstance.saveTripPlan(window.mapInstance.tripPlan);
    window.mapInstance.updateTripDisplay();
    
    // Re-render fruit farms to reflect seasonal filtering based on current date
    window.mapInstance.renderFruitFarms();
}

window.setTripLocation = function() {
    if (!window.mapInstance) {
        Logger.error('Map instance not available yet');
        alert('Map is still loading. Please wait a moment and try again.');
        return;
    }
    
    // Show the trip form to set location
    const tripFormEl = document.getElementById('tripForm');
    const currentTripEl = document.getElementById('currentTrip');
    
    if (tripFormEl && currentTripEl) {
        // Hide current trip display
        currentTripEl.style.display = 'none';
        
        // Show form
        tripFormEl.style.display = 'block';
        
        // Pre-populate form with existing trip data if available
        if (window.mapInstance.tripPlan) {
            const addressInput = document.getElementById('tripAddress');
            const startDateInput = document.getElementById('tripStartDate');
            const endDateInput = document.getElementById('tripEndDate');
            
            // Pre-fill address if it exists
            if (addressInput && window.mapInstance.tripPlan.address) {
                addressInput.value = window.mapInstance.tripPlan.address;
            }
            
            // Pre-fill dates if they exist
            if (startDateInput && window.mapInstance.tripPlan.startDate) {
                startDateInput.value = window.mapInstance.tripPlan.startDate;
            }
            if (endDateInput && window.mapInstance.tripPlan.endDate) {
                endDateInput.value = window.mapInstance.tripPlan.endDate;
            }
        }
        
        // Focus on address input
        const addressInput = document.getElementById('tripAddress');
        if (addressInput) {
            addressInput.focus();
        }
    }
}

// Initialize the map when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const map = new ScenicNYMap();
    map.render();
});
