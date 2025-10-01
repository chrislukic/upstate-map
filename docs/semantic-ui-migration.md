# Semantic UI Migration Checklist

## Phase 0 · Baseline & Safety
- Snapshot current UI, trip planner, map popups, legend toggles.
- Record manual observations on layout, spacing, z-index quirks.
- Catalog current `public/styles.css` usage, noting global selectors, resets, and dependencies on Bootstrap.
- Confirm third-party assets (Font Awesome, Bootstrap) that Semantic UI will replace.
- Capture performance metrics (Lighthouse, bundle size) to monitor regressions.

## Phase 1 · Foundation & Dependencies
- Add Semantic UI packages (already in `package.json`), verify CSS import in `src/main.js`.
- Establish custom theme overrides (variables, global styles) in new `src/styles/semantic-overrides.css`.
- Review Vite config for CSS order; ensure Semantic UI loads before custom overrides.
- Audit Bootstrap usage; plan for controlled removal after component migration.
- Bootstrap 3.2 (CSS + theme) still linked via CDN in `src/index.html`. Current UI relies on `.btn`, `.btn-primary`, `.btn-default`, and grid utilities. We already shadowed `.btn*` in `public/styles.css`, but Semantic UI button classes will replace both, allowing Bootstrap removal once migration reaches Phase 3.
- Font Awesome 4.6 remains for map icons and popup glyphs; Semantic UI icon set overlaps but Leaflet markers currently expect Font Awesome classes. Need dedicated replacement plan (either keep Font Awesome or migrate markers to Semantic UI icon font/SVG).
- Legacy Leaflet Awesome Markers CSS depends on Font Awesome glyph classes; must evaluate alternative marker packs if Font Awesome removed.

## Phase 2 · Layout Skeleton
- Rebuild top-level layout with Semantic UI Grid/Container components.
- Transition trip planner shell to Semantic UI `Segment`/`Card` while keeping map unaffected.
- Verify Leaflet map width/height remain dynamic; adjust flexbox interactions.

## Phase 3 · Interactive Components
- Replace popups, buttons, forms with Semantic UI equivalents.
- Ensure directions buttons retain subtle styling and accessible labels.
- Integrate form validation messaging within Semantic UI form patterns.

## Phase 4 · Data Views & Legends
- Convert legends, lists, and toggles to Semantic UI `List`, `Menu`, `Accordion` as appropriate.
- Maintain seasonal indicator behaviors and out-of-season styling.
- Re-test tooltip rendering and dynamic updates.

## Phase 5 · Theming & Accessibility
- Tune Semantic UI theme variables for typography, colors, spacings.
- Run contrast checks and keyboard navigation audits.
- Document brand tokens and component usage.

## Phase 6 · Cleanup & Regression Testing
- Remove unused Bootstrap dependencies and obsolete CSS rules.
- Run `npm run build` and Lighthouse; compare metrics with baseline.
- Update README documentation referencing Semantic UI migration.

## Tracking & QA
- Use branch `feature/semantic-ui-refresh`.
- Log notable UI changes and follow-up issues in `docs/semantic-ui-migration.md`.
- Mark each phase complete with regression test notes.

