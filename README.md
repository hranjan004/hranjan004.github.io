# Harsh Ranjan — portfolio

Static GitHub Pages portfolio at https://hranjan004.github.io/.

## Final structure

The homepage introduces Harsh, then presents selected work, writing and notes, experience, About, and original art. Additional projects sit in an expandable archive. Detail pages retain technical depth without making the homepage dense.

- 13 project case studies, each labeled Completed or Ongoing.
- 21 essays and engineering notes, with searchable summaries and full readers.
- Six artwork galleries preserving all 28 archive images, with statements and reflections.
- Shared navigation, contact links and the original downloadable CV.

## Source and build

- `content.json`: project narratives, tools, outcomes and status.
- `writing.json`: essays, summaries and source context.
- `art-content.json`: artwork images, statements and reflections.
- `build.py`: shared layout, homepage, experience and page generation.
- `editorial.py`: essay formatting, summaries and reader navigation.
- `visuals.py`: 34 distinct topic-specific SVG compositions and continuous motion sequences. Writing previews and readers both animate, using their own palettes. The same subject retains its identity on its card and detail page; unrelated subjects never share illustrations.
- `styles.css`: one consolidated blue design system and responsive layouts.
- `site.js`: writing search.

Run `python3 build.py` and commit the generated HTML with the source edits. Preview with `python3 -m http.server 4174 --bind 127.0.0.1`. GitHub Pages publishes the root of `main`; `.nojekyll` keeps it static.

## Verification

Run `python3 verify.py` for local links and anchors, reachable pages, page headings, image alt text, project status, essay exclusions, image coverage, SVG validity and composition/motion uniqueness. Add `--base-url http://127.0.0.1:4174/` to verify all linked resources over HTTP. Browser verification covers all 43 pages at desktop and mobile widths, followed by search, expandable sections and reading navigation checks.

## Content boundaries

The site reconciles the Complete Record with Essays, Project and Writing Archive and Collected Essays. Source PDFs, private chat URLs, deployment addresses and household appliance wattages are not published. The Intelligent Energy Management Systems essay and application statements are excluded; the Microgrid technical case study remains.

Microgrid is completed October 2026; the Tesphase role is CTO. The proxy's 50% cached-response-time result matches the resume and was explicitly confirmed by Harsh. The benchmark is scoped to cached requests. Rule-derived ML evaluation is distinguished from independent measurements. Slug Board is completed coursework with an incomplete MVP, as explained in its retrospective.

Project graphics are conceptual illustrations, not measured traces or captured product output. Original artwork previews link to the same work in its gallery. Distinct process views from the archive are retained.
