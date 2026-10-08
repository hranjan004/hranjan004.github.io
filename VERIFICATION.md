# Portfolio verification — October 8, 2026

## Coverage

- 43 HTML pages: homepage, 13 project case studies, writing index, 21 writing readers, six artwork galleries and credits.
- All pages reachable from the homepage; every local link and fragment resolves.
- 81 linked local resources returned HTTP 200, including the CV and every image.
- All 43 pages checked in the browser at desktop width and 390px mobile width: one main heading, one main landmark, no horizontal overflow and no broken loaded images.
- No browser console warnings or errors reported during the page sweep.
- GitHub profile, LF Edge article and design reference each returned HTTP 200.

## Behavior

- Writing search filters by words, handles no results and restores all 21 entries when cleared with the keyboard.
- Project archive and tool list expand successfully.
- Essay contents links navigate to their matching question headings.
- Back-to-top stays on the current page.
- Shared navigation follows the homepage section order.

## Visuals and content

- Original requested heading restored, including italic “real world.”
- 34 different SVG compositions and animation sequences, one for each project and writing entry. All motion loops continuously. Writing-index illustrations are static previews.
- Every SVG parsed successfully; static previews contain no animation elements.
- Original 28 archive image files retained with distinct hashes; source images decoded and checked for exact duplicate pixels. Similar process views remain distinct source photographs.
- The same work intentionally retains its identity between its preview and detail page. No stock photograph or generic animation is shared between unrelated projects.
- All images have alternative text. Decorative SVGs are hidden from assistive technology.
- Project status labels, excluded essay titles, private-reference checks and restored heading are covered by `verify.py`.

## Scope

These checks verify site structure, rendering and navigation. They do not independently re-run project benchmarks or revalidate every historical essay claim. Performance and research limitations remain explicit in the case studies.
