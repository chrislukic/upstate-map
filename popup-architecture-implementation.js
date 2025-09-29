// Popup Architecture Implementation
// This file demonstrates the new popup architecture for the Scenic NY Map

// ===== BASE POPUP BUILDER =====
class PopupBuilder {
  constructor(mapInstance) {
    this.map = mapInstance;
    this.tripPlan = mapInstance.tripPlan;
  }

  // Base popup creation - override in subclasses
  createBasePopup(data, type) {
    return {
      title: this.getTitle(data, type),
      subtitle: this.getSubtitle(data, type),
      meta: this.getMeta(data, type),
      description: this.getDescription(data, type),
      links: this.getLinks(data, type),
      coordinates: this.getCoordinates(data),
      customContent: this.getCustomContent(data, type),
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

  getLinks(data, type) {
    const links = [];
    
    // Add website link if available
    if (data.website) {
      links.push(this.createWebsiteLink(data.website));
    }
    
    // Add Google Maps link if available
    if (data.google_maps_url) {
      links.push(this.createGoogleMapsLink(data.google_maps_url));
    }
    
    return links;
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

  // Helper methods
  createWebsiteLink(url) {
    return `<a href="${url}" target="_blank" rel="noopener" class="popup__link">
      <i class="fa fa-external-link"></i> Website
    </a>`;
  }

  createGoogleMapsLink(url) {
    return `<a href="${url}" target="_blank" rel="noopener" class="popup__link">
      <i class="fa fa-map-marker"></i> View on Google Maps
    </a>`;
  }

  createDirectionsLink(coordinates) {
    if (!this.tripPlan || !this.tripPlan.address || !this.tripPlan.lat || !this.tripPlan.lng) {
      return null;
    }

    const [lat, lng] = coordinates;
    const origin = `${this.tripPlan.lat},${this.tripPlan.lng}`;
    const destination = `${lat},${lng}`;
    const directionsUrl = `https://www.google.com/maps/dir/${origin}/${destination}`;
    
    return `<a href="${directionsUrl}" target="_blank" class="popup__link popup__link--primary">
      <i class="fa fa-directions"></i> Directions from ${this.map.formatAddress(this.tripPlan.address)}
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
    
    if (data.address) meta.push(data.address);
    if (data.approx_drive) meta.push(`<strong>Drive:</strong> ${data.approx_drive}`);
    if (data.reservation_required) meta.push(`<strong>Reservation:</strong> ${data.reservation_required}`);
    
    // Add seasonal status
    const farmInSeason = this.getSeasonalStatus(data, type);
    if (!farmInSeason) {
      meta.push('<span class="popup__meta--warning"><strong>⚠️ Out of Season</strong></span>');
    }
    
    return meta;
  }

  getDescription(data) {
    return data.notes || '';
  }

  getCustomContent(data) {
    const organicBadge = data.organic ? 
      ' <span style="color: #4CAF50; font-size: 14px;">🌱 Organic</span>' : '';
    return organicBadge;
  }

  getMaxWidth() {
    return 300;
  }

  getSeasonalStatus(data, type) {
    // This would integrate with the existing seasonal logic
    // For now, return true as a placeholder
    return true;
  }
}

// ===== RESTAURANT POPUP BUILDER =====
class RestaurantPopupBuilder extends PopupBuilder {
  getMeta(data) {
    const meta = [];
    
    if (data.location) meta.push(data.location);
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
    
    if (data.location) meta.push(data.location);
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
    
    if (data.location) meta.push(data.location);
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
    
    if (data.location) meta.push(data.location);
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
    
    if (data.location) meta.push(data.location);
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
    
    if (data.location) meta.push(data.location);
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
    
    if (data.location) meta.push(data.location);
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
      poi: new POIPopupBuilder(mapInstance)
    };
  }

  createPopup(data, type) {
    const builder = this.builders[type];
    if (!builder) {
      console.warn(`No popup builder found for type: ${type}`);
      return this.builders.farm.createBasePopup(data, type); // fallback
    }

    const popupOptions = builder.createBasePopup(data, type);
    
    // Add trip-based directions if applicable
    if (this.map.tripPlan && this.map.tripPlan.address && popupOptions.coordinates) {
      const directionsLink = builder.createDirectionsLink(popupOptions.coordinates);
      if (directionsLink) {
        popupOptions.links.push(directionsLink);
      }
    }

    return popupOptions;
  }

  bindPopupToMarker(marker, data, type) {
    const popupOptions = this.createPopup(data, type);
    const popupContent = this.map.createPopup(popupOptions);
    const popup = L.popup(this.map.getPopupOptions(popupOptions.maxWidth || 350));
    popup.setContent(popupContent);
    marker.bindPopup(popup);
    return popup;
  }
}

// ===== INTEGRATION WITH SCENICNYMAP =====
// This would be added to the ScenicNYMap class constructor:
/*
class ScenicNYMap {
  constructor() {
    // ... existing code ...
    this.popupFactory = new PopupFactory(this);
  }

  // Simplified render methods would look like this:
  async renderEvents() {
    try {
      const events = Array.isArray(this.events) ? this.events : [];
      const eventGroup = L.featureGroup({});

      events.forEach(event => {
        if (!event.lat || !event.lng) return;

        const eventIcon = L.divIcon({
          className: 'event-marker',
          html: '<div class="event-icon">🎉</div>',
          iconSize: [30, 30],
          iconAnchor: [15, 15]
        });

        const marker = L.marker([event.lat, event.lng], { icon: eventIcon }).addTo(eventGroup);
        
        // Add tooltip (only on non-mobile devices)
        if (!this.isMobile) {
          marker.bindTooltip(
            `<div class="map-tooltip">
              <b>${event.name}</b>
              <small>${event.location_name}</small>
            </div>`,
            { sticky: true }
          );
        }

        // Simple popup creation using factory
        this.popupFactory.bindPopupToMarker(marker, event, 'event');
      });

      // ... rest of the method ...
    } catch (e) {
      console.error('Error rendering events:', e);
    }
  }
}
*/

// Export for use in main application
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    PopupBuilder,
    EventPopupBuilder,
    FarmPopupBuilder,
    RestaurantPopupBuilder,
    BreweryPopupBuilder,
    WaterfallPopupBuilder,
    TrailPopupBuilder,
    AirbnbPopupBuilder,
    ChildrenPopupBuilder,
    POIPopupBuilder,
    PopupFactory
  };
}


