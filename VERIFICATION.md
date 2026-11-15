# Portfolio verification — November 15, 2026

## Automated checks

- 68 HTML pages are reachable from the homepage; local links and fragments resolve.
- 106 linked local resources return HTTP 200, including the resume and artwork assets.
- Coverage includes 37 projects, 21 essays and 28 original artwork images.
- All 58 distinct SVG compositions parse successfully; references, unique palettes and motion sequences pass the site verifier.
- Existing external destination URLs are preserved.
- Page headings, landmarks, image alternatives, project status and private-reference exclusions are checked by `verify.py`.

## Browser checks

- Homepage and Silicon Performance Lab detail page checked at 390px width with no horizontal overflow.
- Project search for GPT returns one result; Hardware scope returns one result; clearing filters restores all 37 projects.
- Keyboard Enter expands the engineering decisions and measurement-context disclosure.
- Pause and resume checked visually: successive paused frames are identical; playing frames change. The stored setting persists across navigation and reload.
- No browser console warnings or errors observed during these checks.

## Design and motion

The established visual style is retained. Homepage copy and project cards lead with results; full tools and implementation details remain on project pages. Measurement context is available in an expandable disclosure.

Fifteen new bespoke, text-free compositions use geometry and staged motion to show project behavior. The other 43 diagrams are refined; all 58 subjects retain distinct visual identities. Illustrations are conceptual rather than benchmark traces.

The implementation provides pause/play controls, a stored motion preference, reduced-motion handling and pausing for offscreen illustrations or hidden tabs. Twelve mocked-DOM controller checks passed for initial reduced motion, saved overrides, system-preference changes, visibility, viewport entry/exit, filtered-card restoration, storage errors and fallback behavior. Browser checks confirm native pause/resume; OS-level reduced-motion emulation was not available in the browser test surface.

## Limits

Browser coverage is representative, not a 68-page visual sweep. Preserved external URLs were not all independently revalidated. Website checks do not rerun hardware benchmarks, retrain models or verify every historical essay claim; case studies retain the relevant measurement and implementation context.
