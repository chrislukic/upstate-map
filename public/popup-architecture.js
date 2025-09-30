// Popup Architecture Implementation
// Base classes for the new popup system

// ===== GLOBAL LOGGER =====
const Logger = (() => {
  const LEVELS = { none: 0, basic: 1, extend: 2, verbose: 3 };
  function getLevel() {
    const level = (typeof window !== 'undefined' && window.LOG_LEVEL) ? window.LOG_LEVEL : 'basic';
    return LEVELS[level] ?? LEVELS.basic;
  }
  const api = {
    setLevel(level) { if (typeof window !== 'undefined') window.LOG_LEVEL = level; },
    basic(...args) { if (getLevel() >= LEVELS.basic) console.log(...args); },
    extend(...args) { if (getLevel() >= LEVELS.extend) console.log(...args); },
    verbose(...args) { if (getLevel() >= LEVELS.verbose) console.log(...args); },
    warn: (...args) => console.warn(...args),
    error: (...args) => console.error(...args)
  };
  if (typeof window !== 'undefined') window.Logger = api;
  return api;
})();

// ===== GLOBAL DATA STORE =====
class GlobalDataStore {
  constructor() {
    this.data = new Map(); // Store data by unique ID
    this.nextId = 1;
  }

  // Generate unique ID for any data object
  generateId() {
    return `popup_${this.nextId++}`;
  }

  // Store data with unique ID
  storeData(data, type) {
    const id = this.generateId();
    const storeItem = {
      id,
      type,
      data,
      timestamp: Date.now()
    };
    this.data.set(id, storeItem);
    return id;
  }

  // Retrieve data by ID
  getData(id) {
    return this.data.get(id);
  }

  // Get all data of a specific type
  getDataByType(type) {
    return Array.from(this.data.values()).filter(item => item.type === type);
  }

  // Clear all data
  clear() {
    this.data.clear();
    this.nextId = 1;
  }
}

// Global instance
const globalDataStore = new GlobalDataStore();

// ===== BASE POPUP BUILDER =====
class PopupBuilder {
  constructor(mapInstance) {
    this.map = mapInstance;
    this.tripPlan = mapInstance.tripPlan;
  }

  // Base popup creation - override in subclasses
  createBasePopup(data, type) {
    return {
      // Core content structure
      content: {
        title: this.getTitle(data, type),
        subtitle: this.getSubtitle(data, type),
        meta: this.getMeta(data, type),
        description: this.getDescription(data, type),
        customContent: this.getCustomContent(data, type)
      },
      // Links structure - now part of the popup object
      links: {
        website: this.getWebsiteLink(data),
        googleMaps: this.getGoogleMapsLink(data),
        directions: this.getDirectionsLink(data)
      },
      // Technical properties
      coordinates: this.getCoordinates(data),
      maxWidth: this.getMaxWidth(type),
      className: this.getClassName(type)
    };
  }

  // Default implementations - override in subclasses
  getTitle(data, type) {
    return data.name || data.title || 'Unknown';
  }

  getSubtitle(data, type) {
    return data.location || data.address || null;
  }

  getMeta(data, type) {
    return [];
  }

  getDescription(data, type) {
    return data.description || data.notes || null;
  }

  // Individual link getters - now part of the popup object structure
  getWebsiteLink(data) {
    if (!data.website) return null;
    return {
      url: data.website,
      text: 'Website',
      icon: 'fa-external-link',
      className: 'popup__link--secondary'
    };
  }

  getGoogleMapsLink(data) {
    if (!data.google_maps_url) return null;
    return {
      url: data.google_maps_url,
      text: 'View on Google Maps',
      icon: 'fa-map-marker',
      className: 'popup__link--secondary'
    };
  }

  getDirectionsLink(data) {
    Logger.extend('getDirectionsLink called with tripPlan:', this.tripPlan);
    
    if (!this.tripPlan || !this.tripPlan.address || !this.tripPlan.lat || !this.tripPlan.lng) {
      Logger.basic('No trip plan or missing coordinates/address');
      return null;
    }

    const coordinates = this.getCoordinates(data);
    Logger.extend('Coordinates for directions:', coordinates);
    if (!coordinates) return null;

    const [lat, lng] = coordinates;
    const origin = `${this.tripPlan.lat},${this.tripPlan.lng}`;
    const destination = `${lat},${lng}`;
    const directionsUrl = `https://www.google.com/maps/dir/${origin}/${destination}`;
    Logger.verbose('Creating directions link:', { origin, destination, directionsUrl });
    
    return {
      url: directionsUrl,
      text: `Directions from ${this.map.formatAddress(this.tripPlan.address)}`,
      icon: 'fa-directions',
      className: 'popup__link--primary'
    };
  }

  getCoordinates(data) {
    if (data.lat && data.lng) {
      return [data.lat, data.lng];
    }
    if (data.coords && Array.isArray(data.coords)) {
      return data.coords;
    }
    return null;
  }

  getCustomContent(data, type) {
    return null;
  }

  getMaxWidth(type) {
    return 350;
  }

  getClassName(type) {
    return `popup--${type}`;
  }

  // Helper method to render a link object as HTML
  renderLink(linkObj) {
    if (!linkObj) return '';
    return `<a href="${linkObj.url}" target="_blank" rel="noopener" class="popup__link ${linkObj.className}">
      <i class="fa ${linkObj.icon}"></i> ${linkObj.text}
    </a>`;
  }
}

// ===== EVENT POPUP BUILDER =====
class EventPopupBuilder extends PopupBuilder {
  getSubtitle(data) {
    return data.location_name;
  }

  getMeta(data) {
    const meta = [];
    
    // Date formatting
    const startDate = new Date(data.start_date);
    const endDate = new Date(data.end_date);
    const dateFormat = startDate.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: startDate.getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
    });
    
    let dateRange = dateFormat;
    if (data.start_date !== data.end_date) {
      const endDateFormat = endDate.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: endDate.getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
      });
      dateRange = `${dateFormat} - ${endDateFormat}`;
    }
    
    meta.push(`📅 ${dateRange}`);
    meta.push(`📍 ${data.location_name}`);
    
    if (data.family_friendly === 'yes') {
      meta.push('👨‍👩‍👧‍👦 Family Friendly');
    }
    
    return meta;
  }

  getDescription(data) {
    return `<strong>Description:</strong> ${data.short_description || data.description}`;
  }

  getCustomContent(data) {
    return `<div class="popup__address"><strong>Address:</strong> ${data.address}</div>`;
  }

  getMaxWidth() {
    return 350;
  }
}

// ===== FARM POPUP BUILDER =====
class FarmPopupBuilder extends PopupBuilder {
  getMeta(data, type) {
    const meta = [];
    
    // Address is already displayed as subtitle, so don't add it here
    
    // Add fruit types available with seasonal styling
    if (data.fruits && data.fruits.length > 0) {
      const fruitTypes = data.fruits.map(fruit => {
        const isInSeason = this.getSeasonalStatus(fruit, type);
        const style = isInSeason ? '' : 'style="color: #999; text-decoration: line-through;"';
        return `<span ${style}>${fruit.type}</span>`;
      }).join(', ');
      meta.push(`<strong>Available:</strong> ${fruitTypes}`);
    }
    
    return meta;
  }

  getDescription(data) {
    // Combine notes from all fruits
    if (data.fruits && data.fruits.length > 0) {
      const allNotes = data.fruits
        .map(fruit => fruit.notes)
        .filter(note => note && note.trim())
        .join(' • ');
      return allNotes || '';
    }
    return data.notes || '';
  }

  getCustomContent(data) {
    let content = '';
    
    // Add organic badges for each fruit
    if (data.fruits && data.fruits.length > 0) {
      const organicFruits = data.fruits.filter(fruit => fruit.organic);
      if (organicFruits.length > 0) {
        const organicTypes = organicFruits.map(fruit => fruit.type).join(', ');
        content += `<div style="color: #4CAF50; font-size: 14px;">🌱 Organic: ${organicTypes}</div>`;
      }
    }
    
    // Add fruit-specific information
    if (data.fruits && data.fruits.length > 0) {
      content += '<div class="popup__fruit-info">';
      data.fruits.forEach(fruit => {
        const isInSeason = this.getSeasonalStatus(fruit, fruit.type);
        const seasonStatus = isInSeason ? '✅' : '❌';
        const reservationText = fruit.reservation_required ? ' (Reservation Required)' : '';
        const fruitStyle = isInSeason ? '' : 'style="color: #999; text-decoration: line-through;"';
        const descriptionStyle = isInSeason ? '' : 'style="color: #ccc;"';
        
        // Use specific season range if available, otherwise fall back to generic description
        const seasonInfo = (fruit.season_start_week && fruit.season_end_week) 
          ? this.formatSeasonRange(fruit.season_start_week, fruit.season_end_week)
          : fruit.season_description || 'Season varies';
        
        content += `<div class="popup__fruit-item">
          <strong ${fruitStyle}>${fruit.type.charAt(0).toUpperCase() + fruit.type.slice(1)}</strong> ${seasonStatus}
          <small ${descriptionStyle}>${seasonInfo}${reservationText}</small>
        </div>`;
      });
      content += '</div>';
    }
    
    return content;
  }

  getMaxWidth() {
    return 350;
  }

  getSeasonalStatus(fruit, type) {
    // Use the map instance's seasonal logic
    if (this.map && this.map.isInSeason) {
      return this.map.isInSeason(fruit.season_start_week, fruit.season_end_week);
    }
    // Fallback: assume in season if no map instance
    return true;
  }

  // Convert season weeks to approximate human-readable date ranges
  formatSeasonRange(startWeek, endWeek) {
    if (!startWeek || !endWeek) return 'Season varies';
    
    const weekToApproximateDate = (week) => {
      // Week 1 = January 1st, each week = 7 days
      const startOfYear = new Date(2024, 0, 1); // January 1st
      const weekDate = new Date(startOfYear.getTime() + (week - 1) * 7 * 24 * 60 * 60 * 1000);
      const month = weekDate.getMonth();
      const day = weekDate.getDate();
      
      const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ];
      
      const monthName = monthNames[month];
      
      // Convert to approximate periods
      if (day <= 7) {
        return `early ${monthName}`;
      } else if (day <= 14) {
        return `mid-${monthName}`;
      } else if (day <= 21) {
        return `mid-${monthName}`;
      } else {
        return `late ${monthName}`;
      }
    };
    
    const startApprox = weekToApproximateDate(startWeek);
    const endApprox = weekToApproximateDate(endWeek);
    
    return `Season runs from ${startApprox} to ${endApprox}`;
  }
}

// ===== RESTAURANT POPUP BUILDER =====
class RestaurantPopupBuilder extends PopupBuilder {
  getMeta(data) {
    const meta = [];
    
    // Location is already displayed as subtitle, so don't add it here
    if (data.cuisine) meta.push(`Cuisine: ${data.cuisine}`);
    if (data.price_range) meta.push(`Price: ${data.price_range}`);
    if (data.rating) meta.push(`⭐ ${data.rating}/5`);
    
    return meta;
  }

  getDescription(data) {
    return data.description || data.specialty || '';
  }

  getMaxWidth() {
    return 320;
  }
}

// ===== BREWERY POPUP BUILDER =====
class BreweryPopupBuilder extends PopupBuilder {
  getMeta(data) {
    const meta = [];
    
    // Location is already displayed as subtitle, so don't add it here
    if (data.region) meta.push(`Region: ${data.region}`);
    if (data.specialty) meta.push(`Specialty: ${data.specialty}`);
    
    return meta;
  }

  getDescription(data) {
    return data.description || data.visitor_experience || '';
  }

  getCustomContent(data) {
    if (data.full_description) {
      return `<div class="popup__full-description">${data.full_description}</div>`;
    }
    return null;
  }

  getMaxWidth() {
    return 350;
  }
}

// ===== WATERFALL POPUP BUILDER =====
class WaterfallPopupBuilder extends PopupBuilder {
  getMeta(data) {
    const meta = [];
    
    // Location is already displayed as subtitle, so don't add it here
    if (data.height) meta.push(`Height: ${data.height}`);
    if (data.difficulty) meta.push(`Difficulty: ${data.difficulty}`);
    if (data.distance) meta.push(`Distance: ${data.distance}`);
    
    return meta;
  }

  getDescription(data) {
    return data.description || data.notes || '';
  }

  getMaxWidth() {
    return 300;
  }
}

// ===== TRAIL POPUP BUILDER =====
class TrailPopupBuilder extends PopupBuilder {
  getMeta(data) {
    const meta = [];
    
    // Location is already displayed as subtitle, so don't add it here
    if (data.region) meta.push(`Region: ${data.region}`);
    if (data.difficulty) meta.push(`Difficulty: ${data.difficulty}`);
    if (data.distance) meta.push(`Distance: ${data.distance}`);
    if (data.elevation_gain) meta.push(`Elevation: ${data.elevation_gain}`);
    
    return meta;
  }

  getDescription(data) {
    return data.description || data.notes || '';
  }

  getMaxWidth() {
    return 350;
  }
}

// ===== AIRBNB POPUP BUILDER =====
class AirbnbPopupBuilder extends PopupBuilder {
  getMeta(data) {
    const meta = [];
    
    // Location is already displayed as subtitle, so don't add it here
    if (data.price) meta.push(`Price: ${data.price}`);
    if (data.rating) meta.push(`⭐ ${data.rating}/5`);
    if (data.guests) meta.push(`Guests: ${data.guests}`);
    
    return meta;
  }

  getDescription(data) {
    return data.description || data.amenities || '';
  }

  getMaxWidth() {
    return 400;
  }
}

// ===== CHILDREN ACTIVITY POPUP BUILDER =====
class ChildrenPopupBuilder extends PopupBuilder {
  getMeta(data) {
    const meta = [];
    
    // Location is already displayed as subtitle, so don't add it here
    if (data.cost) meta.push(`Cost: ${data.cost}`);
    if (data.season) meta.push(`Season: ${data.season}`);
    if (data.age_range) meta.push(`Ages: ${data.age_range}`);
    
    return meta;
  }

  getDescription(data) {
    return data.full_description || data.description || '';
  }

  getMaxWidth() {
    return 350;
  }
}

// ===== POI POPUP BUILDER =====
class POIPopupBuilder extends PopupBuilder {
  getMeta(data) {
    const meta = [];
    
    // Location is already displayed as subtitle, so don't add it here
    if (data.category) meta.push(`Category: ${data.category}`);
    if (data.rating) meta.push(`⭐ ${data.rating}/5`);
    
    return meta;
  }

  getDescription(data) {
    return data.description || data.notes || '';
  }

  getMaxWidth() {
    return 300;
  }
}

// ===== CITY POPUP BUILDER =====
class CityPopupBuilder extends PopupBuilder {
  getSubtitle(data) {
    return data.scenicArea || data.region || null;
  }

  getMeta(data) {
    const meta = [];
    
    if (data.population) {
      meta.push(`Population: ${data.population.toLocaleString()}`);
    }
    
    if (data.driveTime) {
      meta.push(`Drive time: <strong>${data.driveTime}</strong>`);
    }
    
    if (data.county) {
      meta.push(`County: ${data.county}`);
    }
    
    return meta;
  }

  getDescription(data) {
    return data.description || '';
  }

  getMaxWidth() {
    return 300;
  }
}

// ===== TRAIN STATION POPUP BUILDER =====
class TrainStationPopupBuilder extends PopupBuilder {
  getSubtitle(data) {
    return data.operator || data.route || null;
  }

  getMeta(data) {
    const meta = [];
    
    if (data.type) {
      const typeLabel = data.type === 'terminal' ? 'Terminal Station' : 'Station';
      meta.push(`Type: ${typeLabel}`);
    }
    
    if (data.route) {
      meta.push(`Route: ${data.route}`);
    }
    
    if (data.operator) {
      meta.push(`Operator: ${data.operator}`);
    }
    
    return meta;
  }

  getDescription(data) {
    return data.description || data.notes || '';
  }

  getMaxWidth() {
    return 280;
  }
}

// ===== SCENIC AREA POPUP BUILDER =====
class ScenicAreaPopupBuilder extends PopupBuilder {
  getSubtitle(data) {
    return data.region || data.county || null;
  }

  getMeta(data) {
    const meta = [];
    
    if (data.county) {
      meta.push(`County: ${data.county}`);
    }
    
    if (data.region) {
      meta.push(`Region: ${data.region}`);
    }
    
    if (data.elevation) {
      meta.push(`Elevation: ${data.elevation}`);
    }
    
    return meta;
  }

  getDescription(data) {
    return data.description || data.notes || '';
  }

  getMaxWidth() {
    return 320;
  }
}

// ===== POPUP FACTORY =====
class PopupFactory {
  constructor(mapInstance) {
    this.map = mapInstance;
    this.builders = {
      event: new EventPopupBuilder(mapInstance),
      farm: new FarmPopupBuilder(mapInstance),
      restaurant: new RestaurantPopupBuilder(mapInstance),
      brewery: new BreweryPopupBuilder(mapInstance),
      waterfall: new WaterfallPopupBuilder(mapInstance),
      trail: new TrailPopupBuilder(mapInstance),
      airbnb: new AirbnbPopupBuilder(mapInstance),
      children: new ChildrenPopupBuilder(mapInstance),
      poi: new POIPopupBuilder(mapInstance),
      city: new CityPopupBuilder(mapInstance),
      trainStation: new TrainStationPopupBuilder(mapInstance),
      scenicArea: new ScenicAreaPopupBuilder(mapInstance)
    };
  }

  // Update trip plan in all builders
  updateTripPlan(tripPlan) {
    console.log('PopupFactory.updateTripPlan called with:', tripPlan);
    Object.values(this.builders).forEach(builder => {
      builder.tripPlan = tripPlan;
      console.log('Updated builder tripPlan:', builder.tripPlan);
    });
  }

  createPopup(data, type) {
    const builder = this.builders[type];
    if (!builder) {
      console.warn(`No popup builder found for type: ${type}`);
      return this.builders.farm.createBasePopup(data, type); // fallback
    }

    // Ensure builder has current trip plan
    builder.tripPlan = this.map.tripPlan;
    console.log(`Creating popup for ${type}, builder tripPlan:`, builder.tripPlan);
    const popupOptions = builder.createBasePopup(data, type);
    console.log(`Created popup for ${type}:`, popupOptions);
    console.log('Links object:', popupOptions.links);
    console.log('Directions link:', popupOptions.links?.directions);
    
    // Directions link is now automatically handled in the getDirectionsLink method
    // No need to manually add it here since it's part of the links structure

    return popupOptions;
  }

  bindPopupToMarker(marker, data, type) {
    console.log(`bindPopupToMarker called for ${type} with data:`, data);
    
    // Store data in global store and get unique ID
    const dataId = globalDataStore.storeData(data, type);
    console.log(`Stored data with ID: ${dataId}`);
    
    // Create a popup that will be generated dynamically when opened
    const popup = L.popup({
      maxWidth: 350,
      className: `popup--${type}`
    });
    
    // Bind the popup with a dynamic content function that uses the global store
    marker.bindPopup(() => {
      console.log('Popup opened, retrieving data from global store');
      const storeItem = globalDataStore.getData(dataId);
      if (!storeItem) {
        console.error('Data not found in global store for ID:', dataId);
        return '<div class="popup">Error: Data not found</div>';
      }
      
      console.log('Retrieved data:', storeItem);
      const popupOptions = this.createPopup(storeItem.data, storeItem.type);
      console.log('Dynamic popup options:', popupOptions);
      return this.map.createPopup(popupOptions);
    });
    
    return popup;
  }
}

// Export for use in main application
if (typeof window !== 'undefined') {
  window.PopupBuilder = PopupBuilder;
  window.EventPopupBuilder = EventPopupBuilder;
  window.FarmPopupBuilder = FarmPopupBuilder;
  window.RestaurantPopupBuilder = RestaurantPopupBuilder;
  window.BreweryPopupBuilder = BreweryPopupBuilder;
  window.WaterfallPopupBuilder = WaterfallPopupBuilder;
  window.TrailPopupBuilder = TrailPopupBuilder;
  window.AirbnbPopupBuilder = AirbnbPopupBuilder;
  window.ChildrenPopupBuilder = ChildrenPopupBuilder;
  window.POIPopupBuilder = POIPopupBuilder;
  window.CityPopupBuilder = CityPopupBuilder;
  window.TrainStationPopupBuilder = TrainStationPopupBuilder;
  window.ScenicAreaPopupBuilder = ScenicAreaPopupBuilder;
  window.PopupFactory = PopupFactory;
  window.GlobalDataStore = GlobalDataStore;
  window.globalDataStore = globalDataStore;
}
