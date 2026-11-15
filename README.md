# Harsh Ranjan — portfolio

Static GitHub Pages portfolio at https://hranjan004.github.io/.

## Structure

The homepage introduces Harsh through engineering results, selected projects, writing, experience and original art. The project collection contains 37 entries with search, status and scope filters; projects with repository links appear first. Concise cards lead to detailed implementation narratives, tools and expandable measurement context.

- 37 projects, 21 essays and six artwork galleries across 68 HTML pages.
- 58 distinct SVG illustrations: 15 bespoke text-free compositions and 43 refined diagrams.
- All 28 original artwork images retained.
- Existing destination links and the one-page Carlito resume preserved.
- Shared motion control with a saved preference; reduced-motion, offscreen and hidden-tab handling.

## Source and build

- `content.json`: project copy, tools, results and status.
- `writing.json` and `editorial.py`: essay content and reader layouts.
- `art-content.json`: artwork galleries, statements and reflections.
- `build.py`: shared layout and generated pages.
- `visuals.py`, `motion_refinements.py` and `cinematic_motion.py`: palettes, compositions and native SVG motion.
- `styles.css`: the established pale background, blue accents, typography and responsive layouts.
- `site.js`: search, filters and motion controls.

Run `python3 build.py`, then commit the generated HTML with source changes. Preview with `python3 -m http.server 4174 --bind 127.0.0.1`. GitHub Pages publishes the root of `main`; `.nojekyll` keeps the site static.

Generate the resume with `python3 build_resume.py --font-dir /path/to/carlito/fonts`. This requires ReportLab and Carlito Regular, Bold, Italic and BoldItalic TTFs.

## Verification

Run `python3 verify.py` to check page reachability, links and anchors, headings, image alternatives, content coverage, private references, SVG validity and illustration uniqueness. Add `--base-url http://127.0.0.1:4174/` to check local resources over HTTP. See `VERIFICATION.md` for the November 15, 2026 verification scope.

## Content boundaries

Copy leads with results while distinguishing completed implementations, coursework, prototypes and proposals. Model agreement, physics-derived evaluation and independent measurements retain their respective scope. ESP32 benchmark results are separate from the planned sensing and telemetry build. Graphics illustrate concepts; they are not measured traces or captured product output.

Private transcripts, credentials and deployment addresses remain outside the repository. Source project claims are not independently re-benchmarked by the website checks. Original artwork previews retain the same identity as their galleries, including distinct process views.
