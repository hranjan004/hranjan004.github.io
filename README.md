# Harsh Ranjan — portfolio

Static GitHub Pages site with project case studies, writing and original artwork.

## Edit and build

- Edit `content.json` for project narratives and statuses.
- Edit `writing.json` for writing text and descriptions.
- Edit `build.py` for shared layout, experience and artwork descriptions.
- Edit `styles.css` and `site.js` for presentation and filtering.
- Run `python3 build.py` and commit the generated HTML with the source changes.
- Preview with `python3 -m http.server 4174 --bind 127.0.0.1`.

GitHub Pages publishes the root of `main`. `.nojekyll` keeps the build static.

## Content and imagery

The October 2026 redesign consolidates the supplied Complete Record with Essays and Project and Writing Archive. Duplicate versions are combined where appropriate. Writing overviews, original drafts and proposals are labeled separately. Source archives and private conversation links are not published.

Microgrid completion and the CTO title follow the October record. Incompatible proxy variants and unreconciled benchmark figures are not combined into a single performance claim. Model results distinguish rule-derived evaluation from independent measurement.

Original art images come from the supplied archive. Contextual photographs and their licenses are listed on `credits.html`. Animated graphics are conceptual illustrations, not captured project output.

The blue editorial update incorporates the Collected Essays PDF: 19 distinct writing entries, with overlapping texts reconciled and summaries beneath their headings. The Intelligent Energy Management Systems essay and application statements are excluded. Existing engineering case studies remain separate from that exclusion. Slug Board is labeled completed coursework with an incomplete MVP, as documented in the retrospective.

`art-content.json` maps every one of the earlier archive's 28 embedded image occurrences to six artwork galleries, including alternate views and presentation sheets. It also contains the artist statements and reflections. `editorial.py` handles rich text, reading layouts, and topic-specific animated SVG motifs. Source PDFs and private chat URLs remain outside the published site.
