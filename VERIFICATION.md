# Portfolio verification — October 21, 2026

## Coverage

- 64 HTML pages: homepage, project index, 33 project case studies, writing index, 21 writing readers, six artwork galleries and credits.
- All pages reachable from the homepage; every local link and fragment resolves.
- 102 linked local resources returned HTTP 200, including the CV and every image.
- All 33 project pages checked in the browser at 390px mobile width with no horizontal overflow. Project collection checked at desktop and mobile widths; new case-study rendering visually inspected. Page-heading and landmark checks cover all 64 pages.
- No browser console warnings or errors reported during the page sweep.
- External destinations were not rechecked in this update.

## Behavior

- Writing search filters by words, handles no results and restores all 21 entries when cleared with the keyboard.
- Project search returns the three Pac-Man projects; status and scope filters compose correctly (25 completed entries, three ongoing proposals). Empty results render a message. Homepage links open the 33-entry collection.
- Essay contents links navigate to their matching question headings.
- Back-to-top stays on the current page.
- Shared navigation follows the homepage section order.

## Visuals and content

- Original requested heading restored, including italic “real world.”
- 54 different SVG compositions and animation sequences, one for each project and writing entry. All motion loops continuously. Writing-index illustrations animate with the same subject-specific palettes as their readers.
- Every SVG parsed successfully. All 54 palettes are distinct, and gradient/filter references resolve. Native SVG motion uses eased transitions, glows and gentle ambient lighting.
- Original 28 archive image files retained with distinct hashes; source images decoded and checked for exact duplicate pixels. Similar process views remain distinct source photographs.
- The same work intentionally retains its identity between its preview and detail page. No stock photograph or generic animation is shared between unrelated projects.
- All images have alternative text. Decorative SVGs are hidden from assistive technology.
- Project status labels, excluded essay titles, private-reference checks and restored heading are covered by `verify.py`.

## Scope

These checks verify site structure, rendering and navigation. They do not independently re-run project benchmarks or revalidate every historical essay claim. Performance and research limitations remain explicit in the case studies.
