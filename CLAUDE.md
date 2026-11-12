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
- Wording: minor is written lowercase **min** (min7, min6, min(maj7), key chips "Cmin"), never "m"; the symbol may follow in
  parentheses, e.g. "min7 (–7)".
- Qualities in iReal syntax: ii `-7` (major) / `h7` (minor), I `^7` / i `-6`, dominants `7`, `13`, `7b9`, `7alt`.
  Minor keys never get `13` (a natural 13 fights the key) — "13" falls back to `7` there.
- Progressions are one grouped menu (keep this order and grouping):
  ii–V–I: ii–V–I, ii–V. ii–V variations: Tritone sub ii–♭II7–I, Major ii–V → minor i, Minor ii–V → major I,
  Backdoor iv–♭VII7–I. Turnarounds: I–VI–ii–V, iii–VI–ii–V, iii–♭iii°–ii–V, I–♯I°–ii–V, Lady Bird
  (I–♭III7–♭VImaj7–♭II7). Drills: One chord quality (Dominants only was removed once all the dominant qualities were
  in this menu; old saves become One chord quality → 7) (for random-root practice): a curated everyday set in
  groups — Triads: major, min, dim, aug, sus4 · Major: maj7, maj9, maj13, 6, 6/9, maj7♯11, maj7♯5 · Minor: min7, min9, min11, min6, min(maj7) · Dominant: 7, 9,
  13, 7♭9, 7♯9, 7♯11, 7♭13, 7♯5, 7alt · Sus: 7sus4, 9sus4, 7♭9sus4 · Diminished: min7♭5, min9♭5, dim7 (list in
  `CHORD_GROUPS`). Not overloaded, nothing obscure. iReal has no min13, so it's left out.
  Your own: Custom progression. Quality (Major/Minor) applies to ii–V–I, ii–V, tritone sub and custom; the rest
  are fixed. The One chord drill has no key names (the chord names its root). No colour moves or whole forms (blues, rhythm
  changes) — the owner left those out for now.
- Custom progression: roman numerals over the key, always counted from the major scale; bars split by "|",
  up to 4 chords a bar, up to 16 bars, "%" repeats a bar. Bare numerals: lowercase –7 (vii ø7), uppercase 7,
  except I and IV maj7. Plain 7ths follow the Dominants setting; any other quality is used as written. Unknown
  tokens are skipped and listed under the box. There are no premade custom examples.
- Custom also takes plain chord symbols in any key (`D-7 G7 | Cmaj7 | Bmin7b5 E7 | Amin7`; m/min/-, maj7/Δ/^, ø/m7b5,
  °/dim…), mixed freely with numerals. The app works out the key (scores each key on chords that belong to it and on
  cadences — V7→I and ii–V — landing on its tonic, the first cadence counting most; major wins a close call; all
  dominants → the first chord), shows it in a "Written in" menu (Auto · <key>, or pick any of 24) that appears only
  for chord symbols, and greys Quality to "Quality (from chords)". Chords keep the letter relationships they were typed
  with. A plain 7 resolving down a 5th to a minor chord gets no natural 13. Slash chords are a must: `Cmaj7/G`, `D-7/G`, `A7/C#` (bass placed in the key like
  the root; iReal `C^7/G`; drawn as a smaller "/G" on the baseline). With numerals, `V7/ii` is an applied chord (V7 of ii).
- Bar 4 of long ii–V–I (and its tritone-sub and major/minor variants): hold I (bar-repeat `%`, iReal `x`) or VI7 (V7/ii). V7 and VI7 sounds are chosen separately;
  "Random mix" picks a type per dominant and greys out those two selectors.
- Order (a menu, in this order): Cycle of 4ths (default), Cycle of 5ths, Up / Down half steps, Up / Down whole steps,
  Up / Down minor 3rds, Up / Down major 3rds, Tritones, Shuffled — every interval both ways (nothing past a 5th: the
  rest are inversions). All but Shuffled walk from "Start on" (greyed out, not hidden, for Shuffled). When a walk
  closes up before 12 keys (whole steps, 3rds, tritones) it slips a half step in the same direction to the next unused
  key and continues, so every key appears once. Restarts are not marked on the chart (a ↑½/↓½ mark was tried and removed). "Shuffle again" picks a new start key (or a new random order for
  Shuffled). Default title ends with the order, e.g. "(Cycle)", "(Cycle of 5ths)", "(Down Whole Steps)", "(Tritones)",
  "(Shuffled)" — never "Shuffle" (sounds like a groove).

- Surprise me: random progression (not Custom), quality, length, bar 4, order, start, dominants; keeps keys,
  repeats, style, look, key names and the teaching note. No saved recipes (tried and removed: the settings are quick
  enough to set up).
- Starter keys: major C, F, G, B♭, D; minor A, D, E, C.

**Chart / PDF**
- Four bars per line; each key's name sits **under its first bar** (iReal style), never in a side column.
- "Twice": if the chart written out twice fits on one page (12 lines of 4 bars), each key is simply written out a
  second time (no repeat signs) — in the preview, the PDF and iReal alike. Only longer charts use repeats.
- Barlines: single for every measure (same ink as doubles, just thinner), double at each key change, repeat signs when
  "Twice" needs them (`{ }` in iReal) including `:‖:` where two keys meet mid-line, thin-thick final bar.
- Chord size: one size for the whole chart (like iReal's fixed cells) — the size at which the widest symbol fits its
  share of a bar (floor 40%). Never size chords one by one (it looked uneven with busy bars).
- Key names: Show / Hide switch (hides them in the preview, PDF and iReal).
- Teaching note (optional, 120 chars): shown under the header in the preview and PDF, and in iReal as a comment
  `<*72…>` on the first bar. Just a free-text box — no premade prompts.
- Dark look = clock colours with gold key names; Light look = black on white with deep-red key names. The "Chart look"
  switch changes both the preview and the PDF.
- The preview is a canvas-drawn **image** (press-and-hold to save), drawn by the same code as the PDF.
- Flats and sharps are drawn as vector shapes (thin stem, open bowl; thin uprights, thick rising bars) sized from the
  letter's cap height — not font glyphs — so they look the same everywhere.
  The half-diminished ø is drawn the same way: an open ring with a thin slash (iReal-like), never the font's heavy ø.
- The app's name is **251 Charts** (home screen, top-right plate, PDF header). iReal composer field is `Charts 251` so
  iReal displays "251 Charts". 4/4 only (a 3/4 option was tried and dropped).
- Links use iReal's own export format, `irealb://Title=Composer==Style=Key==Music=Playback=BPM=Repeats`, with the
  music scrambled exactly as iReal does (prefix `1r34LbKcu7`, 50-char blocks with their ends swapped) — checked
  against a chart the owner exported from iReal Pro 2026.9. Playback "" = iReal's default for the Style name.
- iReal style menu: all 50 built-in iReal playback styles (from the owner's iReal 2026.9 style list), sent by their
  exact iReal names (`Jazz-…`, `Latin-…`, `Pop-…`; paid packs Blues/Brazilian/Salsa left out), grouped by purpose:
  Hear the harmony (Long Notes) · Swing with comping · Ballads · Straight 8th feel with comping (owner's wording — not
  "straight feel") · Two feels · Traditional · Latin · Pop. The list lives in `STYLE_GROUPS`. iReal's style text field
  gets the short name ("Ballad Even", "Samba"). Son Montuno 2–3 / 3–2 use an en dash as shown in iReal (unverified).
  Tempo (BPM) box: blank = iReal's default, else 40–400. Instruments (Rhodes, strings bass, quieter drums) can't be
  set from a link — they live in iReal's mixer.

**Copy and layout**
- Intro: "Design a custom exercise with basic chord progressions, then send it to iReal Pro or save it as a PDF."
- Never mention Claude or AI in the page. Settings sit two per row on phones, three on tablet portrait, and
  side-by-side with the chart on wide screens.

## Related
The flash-card app "Flip 251" (split-flap clock with sound) is a separate artifact, not in this repo yet.
