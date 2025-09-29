# Popup Architecture Diagram

## Current Architecture (Problems)

```
ScenicNYMap
├── renderEvents()
│   ├── create popupOptions object
│   ├── format dates, meta, links
│   ├── call bindPopupToMarker()
│   └── [REPEATED LOGIC]
├── renderOrchards()
│   ├── create popupOptions object
│   ├── format meta, links
│   ├── call bindPopupToMarker()
│   └── [REPEATED LOGIC]
├── renderRestaurants()
│   ├── create popupOptions object
│   ├── format meta, links
│   ├── call bindPopupToMarker()
│   └── [REPEATED LOGIC]
└── [8 more render methods with same pattern]
```

**Issues:**
- ❌ Code duplication across 11+ methods
- ❌ Inconsistent data formatting
- ❌ Hard to maintain and extend
- ❌ No separation of concerns

## New Architecture (Solution)

```
ScenicNYMap
├── popupFactory: PopupFactory
│   ├── builders: {
│   │   ├── event: EventPopupBuilder
│   │   ├── farm: FarmPopupBuilder
│   │   ├── restaurant: RestaurantPopupBuilder
│   │   ├── brewery: BreweryPopupBuilder
│   │   ├── waterfall: WaterfallPopupBuilder
│   │   ├── trail: TrailPopupBuilder
│   │   ├── airbnb: AirbnbPopupBuilder
│   │   ├── children: ChildrenPopupBuilder
│   │   └── poi: POIPopupBuilder
│   └── createPopup(data, type)
│       ├── get builder for type
│       ├── call builder.createBasePopup()
│       ├── add trip directions if applicable
│       └── return popupOptions
│
├── renderEvents()
│   ├── create marker
│   ├── add tooltip
│   └── popupFactory.bindPopupToMarker(marker, event, 'event')
├── renderOrchards()
│   ├── create marker
│   └── popupFactory.bindPopupToMarker(marker, orchard, 'farm')
└── [all other render methods follow same simple pattern]
```

## PopupBuilder Hierarchy

```
PopupBuilder (Base Class)
├── getTitle(data, type)
├── getSubtitle(data, type)
├── getMeta(data, type)
├── getDescription(data, type)
├── getLinks(data, type)
├── getCoordinates(data)
├── getCustomContent(data, type)
├── getMaxWidth(type)
├── getClassName(type)
├── createWebsiteLink(url)
├── createGoogleMapsLink(url)
└── createDirectionsLink(coordinates)

EventPopupBuilder extends PopupBuilder
├── getSubtitle(data) → data.location_name
├── getMeta(data) → formatted dates, location, family friendly
├── getDescription(data) → formatted description
├── getCustomContent(data) → address section
└── getMaxWidth() → 350

FarmPopupBuilder extends PopupBuilder
├── getMeta(data, type) → address, drive time, reservation, seasonal status
├── getDescription(data) → notes
├── getCustomContent(data) → organic badge
└── getMaxWidth() → 300

RestaurantPopupBuilder extends PopupBuilder
├── getMeta(data) → location, cuisine, price, rating
├── getDescription(data) → description or specialty
└── getMaxWidth() → 320

BreweryPopupBuilder extends PopupBuilder
├── getMeta(data) → location, region, specialty
├── getDescription(data) → description or visitor experience
├── getCustomContent(data) → full description
└── getMaxWidth() → 350

[6 more type-specific builders...]
```

## Data Flow

```
1. User clicks marker
2. renderMethod() calls popupFactory.bindPopupToMarker(marker, data, type)
3. PopupFactory.createPopup(data, type)
4. Get appropriate builder for type
5. Builder.createBasePopup(data, type)
6. Builder.getTitle(), getMeta(), getDescription(), etc.
7. Add trip directions if applicable
8. Return popupOptions object
9. PopupFactory.bindPopupToMarker() creates Leaflet popup
10. Marker displays popup to user
```

## Benefits

### Code Quality
- ✅ **90% reduction** in popup code duplication
- ✅ **Consistent patterns** across all marker types
- ✅ **Single responsibility** for each builder
- ✅ **Easy to test** individual components

### Maintainability
- ✅ **Centralized logic** in base class
- ✅ **Type-specific customization** in builders
- ✅ **Simple API** for adding new types
- ✅ **Clear separation** of concerns

### Extensibility
- ✅ **Plugin architecture** for new marker types
- ✅ **Override methods** for custom behavior
- ✅ **Shared utilities** for common patterns
- ✅ **Consistent styling** across all popups

## Migration Path

### Phase 1: Infrastructure
1. Create base classes (no breaking changes)
2. Add PopupFactory to ScenicNYMap
3. Test with one type (events)

### Phase 2: Migration
1. Migrate events first
2. Migrate farms second
3. Migrate remaining types one by one
4. Test each migration thoroughly

### Phase 3: Cleanup
1. Remove old popup creation code
2. Update CSS to new class structure
3. Add comprehensive tests
4. Document new patterns

## Example Usage

### Before (Current)
```javascript
// In each render method
const popupOptions = {
  title: data.name,
  meta: [/* complex formatting */],
  description: data.description,
  links: [/* link generation */],
  coordinates: [data.lat, data.lng],
  maxWidth: 350
};
this.bindPopupToMarker(marker, popupOptions);
```

### After (New)
```javascript
// In each render method
this.popupFactory.bindPopupToMarker(marker, data, type);
```

**Result:** 90% less code, 100% more maintainable!


