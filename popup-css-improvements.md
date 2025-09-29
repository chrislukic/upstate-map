# Popup CSS Class Improvements

## Current Issues
- Inconsistent naming patterns (popup-*, map-popup, trip-popup, event-popup)
- Redundant prefixes (everything starts with popup-)
- Unclear hierarchy and component structure
- Size variants scattered and inconsistent
- Mixed layout and styling responsibilities

## Proposed BEM-Style Component Structure

### Base Component: `.popup`
```css
.popup {
  /* Base popup container */
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-height: 100px;
}
```

### Element Classes (children of .popup)
```css
/* Header Elements */
.popup__header { }
.popup__title { }
.popup__subtitle { }

/* Content Elements */
.popup__content { }
.popup__description { }
.popup__meta { }
.popup__meta-container { }

/* Footer Elements */
.popup__footer { }
.popup__links { }
.popup__link { }
```

### Modifier Classes
```css
/* Size Modifiers */
.popup--small { }
.popup--large { }
.popup--compact { }

/* Type Modifiers */
.popup--trip { }
.popup--event { }
.popup--location { }
.popup--farm { }

/* State Modifiers */
.popup--loading { }
.popup--error { }
```

### Utility Classes
```css
/* Layout Utilities */
.popup__meta--inline { }
.popup__meta--stacked { }
.popup__links--horizontal { }
.popup__links--vertical { }

/* Spacing Utilities */
.popup__spacing--tight { }
.popup__spacing--loose { }

/* Color Utilities */
.popup__meta--muted { }
.popup__meta--accent { }
.popup__link--primary { }
.popup__link--secondary { }
```

## Specific Improvements

### 1. Container Classes
**Current:** `.map-popup`, `.trip-popup`, `.event-popup`
**Improved:** `.popup`, `.popup--trip`, `.popup--event`

### 2. Title Classes
**Current:** `.popup-title`, `.popup-title-large`
**Improved:** `.popup__title`, `.popup__title--large`

### 3. Meta Information
**Current:** `.popup-meta`, `.popup-meta-small`, `.popup-meta-container`
**Improved:** `.popup__meta`, `.popup__meta--small`, `.popup__meta-container`

### 4. Links
**Current:** `.popup-link`, `.popup-links`
**Improved:** `.popup__link`, `.popup__links`

### 5. Descriptions
**Current:** `.popup-description`, `.popup-description-small`
**Improved:** `.popup__description`, `.popup__description--small`

## Benefits of New Structure

1. **Clear Hierarchy** - BEM methodology makes relationships obvious
2. **Consistent Naming** - All popup classes follow same pattern
3. **Better Maintainability** - Easy to find and modify related styles
4. **Scalable** - Easy to add new modifiers and variants
5. **Self-Documenting** - Class names explain their purpose and relationship
6. **Reduced Specificity Issues** - Clear cascade order
7. **Component-Based** - Each popup type is a clear component variant

## Migration Strategy

1. **Phase 1:** Add new BEM classes alongside existing ones
2. **Phase 2:** Update JavaScript to use new classes
3. **Phase 3:** Remove old classes and consolidate styles
4. **Phase 4:** Add new modifiers and utilities as needed

## Example Implementation

```css
/* Base popup component */
.popup {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-height: 100px;
}

/* Popup elements */
.popup__title {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.popup__title--large {
  font-size: 18px;
}

.popup__meta {
  color: #666;
  font-size: 12px;
  margin: 0;
}

.popup__meta--small {
  font-size: 11px;
}

.popup__meta--inline:not(:last-child)::after {
  content: " • ";
  margin: 0 4px;
  color: #999;
}

.popup__links {
  margin-top: auto;
  padding-top: 8px;
  font-size: 13px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.popup__link {
  color: #4CAF50;
  text-decoration: none;
  font-size: 13px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.popup__link:hover {
  color: #45a049;
  text-decoration: underline;
  background-color: rgba(76, 175, 80, 0.1);
}

/* Popup modifiers */
.popup--trip {
  min-width: 300px;
}

.popup--event {
  min-width: 320px;
}

.popup--compact {
  min-height: 80px;
  gap: 2px;
}

.popup--compact .popup__title {
  font-size: 14px;
}

.popup--compact .popup__meta {
  font-size: 11px;
}
```

This structure provides:
- Clear component hierarchy
- Consistent naming patterns
- Easy maintenance and updates
- Scalable modifier system
- Better developer experience


