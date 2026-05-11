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
- **Sports Camp week (Jun 15–19)** — mornings blocked out as Sports Camp
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
- **Art tab** — 12 projects, same shape
- **17 Boise field trips** — 5 free, 12 paid, click to copy the name
- **Custom SVG icon set** — 24 icons in field-journal/woodblock stroke style, no
  emojis anywhere in the UI
- **Print stylesheet** — clean B&W landscape view for posting on the fridge

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
