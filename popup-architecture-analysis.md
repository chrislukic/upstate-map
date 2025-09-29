# Popup Architecture Analysis & Restructure Proposal

## Current Issues

### 1. **Repetitive Code Patterns**
Each marker type (events, farms, restaurants, etc.) has nearly identical popup creation logic:
- Same `popupOptions` object structure
- Same `bindPopupToMarker` calls
- Repeated link generation patterns
- Duplicate meta information formatting

### 2. **Inconsistent Data Handling**
- Some types use `coordinates: [lat, lng]`, others don't
- Different meta formatting approaches
- Inconsistent link generation
- Mixed custom content patterns

### 3. **Tight Coupling**
- Popup logic is embedded in each render method
- No separation between data transformation and popup creation
- Hard to maintain and extend

### 4. **No Type-Specific Customization**
- All popups use the same base structure
- No way to add type-specific styling or behavior
- Limited extensibility for new marker types

## Proposed Architecture

### 1. **Base Popup System**
```javascript
class PopupBuilder {
  constructor(mapInstance) {
    this.map = mapInstance;
    this.tripPlan = mapInstance.tripPlan;
  }

  // Base popup creation
  createBasePopup(data, type) {
    return {
      title: data.name || data.title,
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

  // Type-specific implementations
  getSubtitle(data, type) { /* override in subclasses */ }
  getMeta(data, type) { /* override in subclasses */ }
  getDescription(data, type) { /* override in subclasses */ }
  getLinks(data, type) { /* override in subclasses */ }
  getCustomContent(data, type) { /* override in subclasses */ }
  getMaxWidth(type) { return 350; }
  getClassName(type) { return `popup--${type}`; }
}
```

### 2. **Type-Specific Popup Builders**
```javascript
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
    return `<div class="popup-address"><strong>Address:</strong> ${data.address}</div>`;
  }

  getLinks(data) {
    const links = [];
    
    if (data.website) {
      links.push(`<a href="${data.website}" target="_blank" rel="noopener" class="popup__link popup__link--primary">
        <i class="fa fa-external-link"></i> Visit Website
      </a>`);
    }
    
    return links;
  }

  getMaxWidth() {
    return 350;
  }
}

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

  getLinks(data) {
    const links = [];
    
    if (data.website) {
      links.push(`<a href="${data.website}" target="_blank" rel="noopener" class="popup__link">Website</a>`);
    }
    
    if (data.google_maps_url) {
      links.push(`<a href="${data.google_maps_url}" target="_blank" rel="noopener" class="popup__link">
        <i class="fa fa-map-marker"></i> View on Google Maps
      </a>`);
    }
    
    return links;
  }

  getCustomContent(data) {
    const organicBadge = data.organic ? 
      ' <span style="color: #4CAF50; font-size: 14px;">🌱 Organic</span>' : '';
    return organicBadge;
  }

  getMaxWidth() {
    return 300;
  }
}
```

### 3. **Popup Factory**
```javascript
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
      const directionsLink = this.createDirectionsLink(popupOptions.coordinates);
      if (directionsLink) {
        popupOptions.links.push(directionsLink);
      }
    }

    return popupOptions;
  }

  createDirectionsLink(coordinates) {
    if (!this.map.tripPlan || !this.map.tripPlan.address || !this.map.tripPlan.lat || !this.map.tripPlan.lng) {
      return null;
    }

    const [lat, lng] = coordinates;
    const origin = `${this.map.tripPlan.lat},${this.map.tripPlan.lng}`;
    const destination = `${lat},${lng}`;
    const directionsUrl = `https://www.google.com/maps/dir/${origin}/${destination}`;
    
    return `<a href="${directionsUrl}" target="_blank" class="popup__link popup__link--primary">
      <i class="fa fa-directions"></i> Directions from ${this.map.formatAddress(this.map.tripPlan.address)}
    </a>`;
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
```

### 4. **Integration with ScenicNYMap**
```javascript
class ScenicNYMap {
  constructor() {
    // ... existing code ...
    this.popupFactory = new PopupFactory(this);
  }

  // Simplified render methods
  async renderEvents() {
    // ... existing event processing ...
    
    events.forEach(event => {
      // ... marker creation ...
      
      // Simple popup creation
      this.popupFactory.bindPopupToMarker(marker, event, 'event');
    });
  }

  async renderOrchards() {
    // ... existing orchard processing ...
    
    orchards.forEach(orchard => {
      // ... marker creation ...
      
      // Simple popup creation
      this.popupFactory.bindPopupToMarker(marker, orchard, 'farm');
    });
  }
}
```

## Benefits of New Architecture

### 1. **Separation of Concerns**
- Data transformation separated from popup creation
- Type-specific logic isolated in dedicated classes
- Base functionality shared across all types

### 2. **Maintainability**
- Easy to modify popup behavior for specific types
- Centralized popup creation logic
- Consistent API across all marker types

### 3. **Extensibility**
- Easy to add new marker types
- Simple to customize popup behavior
- Plugin-like architecture for popup builders

### 4. **Reusability**
- Common popup patterns extracted to base class
- Shared utilities for links, formatting, etc.
- Consistent styling and behavior

### 5. **Testability**
- Each popup builder can be tested independently
- Mock data easily injected for testing
- Clear interfaces for each component

## Migration Strategy

### Phase 1: Create Base Infrastructure
1. Create `PopupBuilder` base class
2. Create `PopupFactory` class
3. Add to `ScenicNYMap` constructor

### Phase 2: Migrate One Type at a Time
1. Start with events (most complex)
2. Create `EventPopupBuilder`
3. Update `renderEvents()` method
4. Test and refine

### Phase 3: Migrate Remaining Types
1. Create builders for each marker type
2. Update render methods
3. Remove old popup creation code

### Phase 4: Enhance and Optimize
1. Add type-specific customizations
2. Implement advanced features
3. Add comprehensive testing

## Example Usage

```javascript
// Before (current approach)
const popupOptions = {
  title: event.name,
  meta: [`📅 ${dateRange}`, `📍 ${event.location_name}`],
  description: `<strong>Description:</strong> ${event.description}`,
  links: [websiteLink],
  coordinates: [event.lat, event.lng],
  maxWidth: 350
};
this.bindPopupToMarker(marker, popupOptions);

// After (new approach)
this.popupFactory.bindPopupToMarker(marker, event, 'event');
```

This architecture provides:
- **Cleaner code** - No repetitive popup creation logic
- **Better maintainability** - Type-specific logic isolated
- **Easier testing** - Each component can be tested independently
- **Enhanced extensibility** - Easy to add new marker types or customize existing ones
- **Consistent behavior** - All popups follow the same patterns


