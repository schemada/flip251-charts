# 251 Charts — notes for whoever works on this next

A teaching tool: build a ii–V–I (and related) drill through the keys, preview it as a lead sheet, send it to
iReal Pro, or save it as a PDF / image. Live at https://schemada.github.io/flip251-charts/ (GitHub Pages, `main`, root).

## How it's built
- **Edit only `src/chart251.html`.** It's one self-contained page (HTML + CSS + JS, no framework). It was written as a
  claude.ai Artifact, so it has no `<!doctype>`/`<head>` of its own; the build adds those.
- **Then run `python3 tools/build.py`.** It regenerates `index.html`, `manifest.webmanifest`, `sw.js` (offline cache,
  versioned per build so installed apps update), `dist/flip251-charts.html` and `dist/squarespace-code-block.html`.
  Never hand-edit those outputs.
- Icons: `python3 tools/make_icons.py` (only if the icon design changes).
- External loads: Google Fonts (Barlow Condensed, IBM Plex Mono, Noto Music) and jsPDF 2.5.1 from cdnjs.
- Commit the source *and* the rebuilt outputs together; Pages serves the repo root.

## Things the owner has decided (keep these unless asked)
**Music**
- Spelling: a **♭ Flats / ♯ Sharps** toggle (next to All 12 / Starter) decides how the five black-key keys are written
  (D♭/C♯, E♭/D♯, G♭/F♯, A♭/G♯, B♭/A♯), major and minor alike; default Flats. It only changes how keys are written,
  never which keys are chosen or their order. Chords are spelled from the key. iReal roots are ASCII (`Bb`, `F#`);
  E♯/B♯/C♭/F♭ and double accidentals are respelled (so D♯ major's ii shows as F–7). There are no flat-key/sharp-key presets.
- Qualities in iReal syntax: ii `-7` (major) / `h7` (minor), I `^7` / i `-6`, dominants `7`, `13`, `7b9`, `7alt`.
  Minor keys never get `13` (a natural 13 fights the key) — "13" falls back to `7` there.
- Progressions: ii–V–I (long 4 bars: ii|V|I|bar 4, short 2), ii–V (2 / 1), iii–VI–ii–V (4 / 2, major only),
  Backdoor iv–♭VII7–I (4 / 2, major only, bar 4 holds I). Order in the picker: ii–V–I, ii–V, iii–VI–ii–V, Backdoor.
- Bar 4 of long ii–V–I: hold I (bar-repeat `%`, iReal `x`) or VI7 (V7/ii). V7 and VI7 sounds are chosen separately;
  "Random mix" picks a type per dominant and greys out those two selectors.
- Order (a menu): Cycle of 4ths (default), Down whole steps, Down half steps, Up minor 3rds, Up major 3rds (Coltrane),
  Shuffled. All but Shuffled walk from "Start on" (greyed out, not hidden, for Shuffled). When a walk closes up before
  12 keys (whole steps, 3rds) it slips a half step in the same direction to the next unused key and continues, so
  every key appears once. "Shuffle again" picks a new start key (or a new random order for Shuffled). Default title
  ends with "(Cycle)", "(Whole Steps)", "(Half Steps)", "(Minor 3rds)", "(Major 3rds)" or "(Shuffled)" — never
  "Shuffle" (sounds like a groove).

**Chart / PDF**
- Four bars per line; each key's name sits **under its first bar** (iReal style), never in a side column.
- Barlines: single for every measure (same ink as doubles, just thinner), double at each key change, repeat signs when
  "Twice" (`{ }` in iReal) including `:‖:` where two keys meet mid-line, thin-thick final bar.
- Dark look = clock colours with gold key names; Light look = black on white with deep-red key names. The "Chart look"
  switch changes both the preview and the PDF.
- The preview is a canvas-drawn **image** (press-and-hold to save), drawn by the same code as the PDF.
- Flats and sharps are drawn as vector shapes (thin stem, open bowl; thin uprights, thick rising bars) sized from the
  letter's cap height — not font glyphs — so they look the same everywhere.
  The half-diminished ø is drawn the same way: an open ring with a thin slash (iReal-like), never the font's heavy ø.
- The app's name is **251 Charts** (home screen, top-right plate, PDF header). iReal composer field is `Charts 251` so
  iReal displays "251 Charts". Legacy `irealbook://` links (no tempo field). 4/4 only (a 3/4 option was tried and dropped).

**Copy and layout**
- Intro: "Design a custom exercise with basic chord progressions, then send it to iReal Pro or save it as a PDF."
- Never mention Claude or AI in the page. Settings sit two per row on phones, three on tablet portrait, and
  side-by-side with the chart on wide screens.

## Related
The flash-card app "Flip 251" (split-flap clock with sound) is a separate artifact, not in this repo yet.
