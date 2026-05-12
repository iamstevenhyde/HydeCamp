# Camp Hyde · Summer 2026

### → **[Open the app](https://iamstevenhyde.github.io/HydeCamp/)** ←

A home curriculum app for two kids (ages 8 & 10) in Boise, ID. Built on top of
Maggie Hyde's original `Summer_2026_Schedule.html`, with content variety pulled
in from open-source GitHub repos.

**Live design:** Risograph Camp Poster — cherry + cyan overprint on cream, sticker
cells with offset shadows, Caprasimo + Bricolage Grotesque + DM Mono.

## Open

Easiest: click **[iamstevenhyde.github.io/HydeCamp](https://iamstevenhyde.github.io/HydeCamp/)**.

Offline: clone the repo or download the ZIP, then double-click `index.html`.
Google Fonts and the Open-Meteo forecast load over the internet if available;
the app falls back gracefully if they don't.

## Files

```
HydeCamp/
├── index.html                   ← the app (riso build)
├── index-v2-fieldjournal.html   ← v2 backup (editorial field-journal aesthetic)
├── experiments/
│   ├── 01-risograph-camp.html   ← static design experiments
│   ├── 02-cosmic-editorial.html
│   └── 03-nordic-almanac.html
├── data/
│   ├── legacy_catalogs.js       ← STEM activities (27), art projects (12),
│   │                              default schedule, field trips — verbatim from
│   │                              Maggie's original
│   ├── spines.js                ← consolidated corpora + trivia + capitals + APOD
│   ├── corpora_subset.json      ← raw spine data (also embedded in spines.js)
│   ├── trivia_easy.json
│   ├── state_capitals.json
│   └── apod_2026.json
├── scripts/
│   └── build_data.py            ← run once to rebuild spines from raw downloads
├── CREDITS.md
└── README.md
```

## Features

- **13 weeks** auto-generated from May 18 → Aug 17, 2026
- **Click-to-edit cells** — type + activity, saved to localStorage
- **Parent badges** — click any cell's M/S/M+S badge to assign Mom, Dad, or Both
- **Weekly themes** — one per week, each rotating in a STEM activity, an art
  project, and a Boise field trip ("Water & Wonder", "Build It Week", etc.)
- **Sports Camp week (Jun 15–19)** — full days (9 AM–4 PM) blocked out as Sports Camp
- **Today highlight** — current day's cells get a cherry marching-ant shadow
- **Spotlight card** — NASA APOD with kid-friendly caption, plus State of the
  Week, Capital, and Plant of the Week
- **Daily trivia** — one 3-choice question per day, deterministic by day-of-year
- **Reading log** — Big Kid / Little Kid, book title + pages, persisted per week
- **Heat-flag indoor swap** — Open-Meteo 14-day forecast for Boise; outdoor
  afternoon blocks ≥ 95°F get a SWAP flag, click to dismiss
- **Screen-time tracker** — average hours/day across the week, capped at 2 hr
- **STEM tab** — 27 activities with materials/steps/pro tips, filter by S/T/E/M,
  print a checklist shopping list
- **Art tab** — 32 projects, same shape
- **22 Boise field trips** — 5 free, 17 paid (incl. 8 day-trip options), click to copy the name
- **Custom SVG icon set** — 24 icons in field-journal/woodblock stroke style, no
  emojis anywhere in the UI
- **Print stylesheet** — clean B&W landscape view for posting on the fridge

## Summer Keepsake Features

These turn the planner into a keepsake the kids keep.

- **📸 Photo capture** — Every activity card has an "Add Photo" button. Take a
  picture of the finished project; thumbnails appear on the card. Compressed
  to ~80KB and stored in localStorage.
- **Album tab** — All photos grouped by week, with a one-click **Export
  Scrapbook** that downloads a standalone HTML page (`camphyde-2026-scrapbook.html`)
  — email or AirDrop the whole summer to grandparents in one file.
- **Badges tab** — 12 merit badges (Naturalist, Maker, Cartographer,
  Printmaker, Star Charter, Painter, Sculptor, Coder, Mathematician,
  Storyteller, Fabric Artist, Camp Veteran). Earn by completing activities in
  a category. Locked badges grayscaled; unlocked badges show earned date.
- **Shopping tab** — Pick which weeks to include and get a deduplicated
  materials list across all assigned art + STEM projects. Email or print.
  Checkbox state persists.
- **Poster tab** — Pre-formatted printable fridge poster for the current
  week: 5-day grid, this week's art + STEM + field trip, weather strip,
  shopping mini-list. Save as PDF or print landscape. Includes a "Share
  with co-parent" `mailto:` button.
- **Parent divide pivot** — Counts Maggie/Steven/Both badges across the
  current week; flags imbalance.
- **Mark Done** — Activity cards and individual schedule cells have a
  done toggle that feeds the badge engine.
- **Boredom button ("I'm bored")** — Header button picks a random
  not-yet-done activity, weighted to indoor on hot days and easy on late
  evenings.
- **Kid Mode** — Header toggle (or `?mode=kid` URL) hides parent badges,
  screen-time bar, week notes, heat banner, and bumps font sizes.

## Content sources

All data spines are open-source and embedded:

- [dariusk/corpora](https://github.com/dariusk/corpora) (CC0) — birds, plants, animals
- [uberspot/OpenTriviaQA](https://github.com/uberspot/OpenTriviaQA) (CC-BY-SA) — daily trivia
- [stdlib-js/datasets-us-states-capitals](https://github.com/stdlib-js/datasets-us-states-capitals) (MIT) — State of the Week
- [NASA APOD](https://apod.nasa.gov) (public domain) — 13 hand-curated kid-friendly entries
- [Open-Meteo](https://open-meteo.com) (CC-BY) — Boise heat forecast

See `CREDITS.md` for full attribution.

## Rebuilding the spines

```bash
cd HydeCamp
# (re-download raw corpora / trivia files into data/ first — URLs in build_data.py)
python scripts/build_data.py
```

APOD picks are hand-curated, not auto-generated.

## Design history

Three sharply different design experiments are preserved in `experiments/`:
- **01 Risograph Camp Poster** — kid-facing, loud, cherry/cyan/canary on cream
- **02 Cosmic Editorial** — dark NYT-science-section feel, PT Serif + Newsreader
- **03 Nordic Almanac** — calm Hay-catalog/Skandi planner, sage + dusty rose

The main `index.html` ships the riso direction built out into a full app.
The v2 field-journal version is preserved as `index-v2-fieldjournal.html`.

## License

Family / educational use. Content spines retain their original licenses (see
`CREDITS.md`). Maggie's original schedule structure and activity content remain
hers.
