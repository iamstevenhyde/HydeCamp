"""
Consolidate raw downloaded data into the four spine files Camp Hyde uses.
Run once: `python scripts/build_data.py` from Desktop/CampHyde/
Reads _*.json/_*.txt from data/, writes the four spine files, removes temp _* files.
"""
import json, re, random
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
random.seed(2026)

# ── 1. Corpora subset ────────────────────────────────────────────
birds_raw = json.loads((DATA / "_birds.json").read_text(encoding="utf-8"))
# birds_north_america is grouped by family. Flatten to a single list,
# prefer common backyard/Mountain-West families for kid relevance.
backyard_families = {
    "New World Quail", "Hummingbirds", "Woodpeckers",
    "Chickadees and Titmice", "Wrens", "Nuthatches and Allies",
    "Thrushes and Allies", "New World Sparrows", "Cardinals and Allies",
    "Finches, Euphonias, and Allies", "Crows, Jays, and Magpies",
    "Swallows", "Owls", "Hawks, Kites, Eagles, and Allies",
    "Pigeons and Doves", "Tyrant Flycatchers", "Wood-Warblers",
    "Falcons and Caracaras", "Blackbirds",
}
backyard_birds = []
for fam in birds_raw["birds"]:
    if fam["family"] in backyard_families:
        for m in fam["members"]:
            backyard_birds.append({"name": m, "family": fam["family"]})

animals = json.loads((DATA / "_animals.json").read_text(encoding="utf-8"))
animal_list = animals.get("animals") or animals.get("common") or []
# Filter to kid-friendly (no obscure latin names)
kid_animals = [a for a in animal_list if isinstance(a, str) and len(a) < 24][:120]

dinos = json.loads((DATA / "_dinos.json").read_text(encoding="utf-8"))
dino_list = dinos.get("dinosaurs", [])
# Pick recognizable ones
famous_dinos = [
    "Tyrannosaurus", "Triceratops", "Stegosaurus", "Velociraptor",
    "Brachiosaurus", "Apatosaurus", "Ankylosaurus", "Diplodocus",
    "Allosaurus", "Spinosaurus", "Iguanodon", "Pteranodon",
    "Parasaurolophus", "Pachycephalosaurus", "Therizinosaurus",
    "Gallimimus", "Carnotaurus", "Microraptor",
]
dino_list = [d for d in famous_dinos if any(d in x for x in dino_list)] or famous_dinos

plants = json.loads((DATA / "_plants.json").read_text(encoding="utf-8"))
plant_list = plants.get("plants") or plants.get("trees") or []
if plant_list and isinstance(plant_list[0], dict):
    plant_list = [p.get("name") for p in plant_list if p.get("name")]
plant_list = [p for p in plant_list if isinstance(p, str) and len(p) < 30][:80]

corpora_subset = {
    "_source": "https://github.com/dariusk/corpora",
    "_license": "CC0",
    "birds_backyard": backyard_birds,
    "animals": kid_animals,
    "dinosaurs": dino_list,
    "plants": plant_list,
}
(DATA / "corpora_subset.json").write_text(
    json.dumps(corpora_subset, indent=2), encoding="utf-8"
)
print(f"corpora_subset.json: {len(backyard_birds)} birds, {len(kid_animals)} animals, "
      f"{len(dino_list)} dinos, {len(plant_list)} plants")

# ── 2. State capitals (50 states paired) ─────────────────────────
capitals = json.loads((DATA / "_capitals.json").read_text(encoding="utf-8"))
STATES = [
    "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
    "Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa",
    "Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan",
    "Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire",
    "New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio",
    "Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota",
    "Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia",
    "Wisconsin","Wyoming",
]
pairs = [{"state": s, "capital": c} for s, c in zip(STATES, capitals)]
(DATA / "state_capitals.json").write_text(
    json.dumps({
        "_source": "https://github.com/stdlib-js/datasets-us-states-capitals",
        "_license": "MIT",
        "pairs": pairs,
    }, indent=2),
    encoding="utf-8",
)
print(f"state_capitals.json: {len(pairs)} pairs (Idaho={pairs[11]['capital']})")

# ── 3. Trivia easy filter ────────────────────────────────────────
def parse_trivia(path, category):
    text = path.read_text(encoding="utf-8", errors="ignore")
    blocks = text.split("\n\n")
    out = []
    for b in blocks:
        lines = [ln.strip() for ln in b.strip().splitlines() if ln.strip()]
        if not lines or not lines[0].startswith("#Q "):
            continue
        q = lines[0][3:].strip()
        answer = None
        choices = []
        for ln in lines[1:]:
            if ln.startswith("^ "):
                answer = ln[2:].strip()
            elif re.match(r"^[A-D]\s", ln):
                choices.append(ln[2:].strip())
        # Filter: simple, short, has 4 choices, answer present, no "which is the odd"
        if (answer and len(choices) == 4 and len(q) < 140
            and "?" in q
            and not any(bad in q.lower() for bad in
                ["odd one", "except one", "which is not", "which one is not"])):
            out.append({"q": q, "a": answer, "choices": choices, "cat": category})
    return out

animals_q = parse_trivia(DATA / "_trivia_animals.txt", "Animals")
sci_q = parse_trivia(DATA / "_trivia_sci.txt", "Science")
geo_q = parse_trivia(DATA / "_trivia_geo.txt", "Geography")

random.shuffle(animals_q); random.shuffle(sci_q); random.shuffle(geo_q)
trivia_pool = animals_q[:80] + sci_q[:80] + geo_q[:80]
random.shuffle(trivia_pool)

(DATA / "trivia_easy.json").write_text(
    json.dumps({
        "_source": "https://github.com/uberspot/OpenTriviaQA",
        "_license": "CC-BY-SA-4.0",
        "questions": trivia_pool[:200],
    }, indent=2),
    encoding="utf-8",
)
print(f"trivia_easy.json: {len(trivia_pool[:200])} questions "
      f"(from {len(animals_q)} animal, {len(sci_q)} sci, {len(geo_q)} geo candidates)")

# ── 4. APOD curated (hand-picked kid-friendly public domain) ─────
# NASA APOD only returns historical dates; future dates return "no data".
# Curated 13 public-domain NASA images mapped to the 13 summer weeks.
# Image URLs are stable NASA-hosted assets (apod.nasa.gov or images.nasa.gov).
apod_picks = [
    {
        "week": 1, "title": "The Pale Blue Dot",
        "credit": "NASA / JPL · Voyager 1, 1990",
        "img": "https://apod.nasa.gov/apod/image/2002/PaleBlueDot_Voyager1_960.jpg",
        "kid": "From 4 billion miles away, Voyager 1 turned its camera back at Earth. "
               "We're the tiny speck in the sunbeam. Everyone you've ever known has lived right here."
    },
    {
        "week": 2, "title": "Jupiter's Great Red Spot",
        "credit": "NASA / Juno spacecraft",
        "img": "https://apod.nasa.gov/apod/image/1707/JupiterRedSpot_JunoEichstadt_1080.jpg",
        "kid": "A storm bigger than Earth that has been spinning on Jupiter for at least 350 years. "
               "Juno flew right over it and took this picture."
    },
    {
        "week": 3, "title": "The Sombrero Galaxy",
        "credit": "NASA / Hubble Space Telescope",
        "img": "https://apod.nasa.gov/apod/image/2005/Sombrero_HubblePestana_960.jpg",
        "kid": "A galaxy shaped like a Mexican hat, 28 million light-years away. "
               "It has 2,000 globular clusters — that's a lot of star families."
    },
    {
        "week": 4, "title": "Saturn from Cassini",
        "credit": "NASA / JPL / Cassini, 2013",
        "img": "https://apod.nasa.gov/apod/image/1311/saturnPIA17172_1080.jpg",
        "kid": "Cassini flew through Saturn's shadow and took 323 photos to make this picture. "
               "Earth is the tiny dot just inside the rings."
    },
    {
        "week": 5, "title": "Crab Nebula",
        "credit": "NASA / ESA / Hubble",
        "img": "https://apod.nasa.gov/apod/image/0512/crabmosaic_hst_big.jpg",
        "kid": "The leftovers of a star that exploded in the year 1054. Chinese astronomers "
               "saw the explosion in daylight. The nebula is still flying apart."
    },
    {
        "week": 6, "title": "Earthrise from Apollo 8",
        "credit": "NASA · Bill Anders, December 1968",
        "img": "https://apod.nasa.gov/apod/image/2001/EarthriseApollo8_NasaAnders_960.jpg",
        "kid": "The most famous photo of Earth. Apollo 8 was the first crew to orbit the Moon, "
               "and they looked back and saw home rising over the lunar surface."
    },
    {
        "week": 7, "title": "Pillars of Creation",
        "credit": "NASA / ESA / Hubble",
        "img": "https://apod.nasa.gov/apod/image/1501/pillars2014_hubble_2638.jpg",
        "kid": "Towers of cold gas where new stars are being born, in the Eagle Nebula. "
               "The biggest pillar is 4 light-years tall — bigger than the distance to the nearest star."
    },
    {
        "week": 8, "title": "Mars from Perseverance",
        "credit": "NASA / JPL / Perseverance Rover",
        "img": "https://apod.nasa.gov/apod/image/2104/PerseveranceDelta_NASA_1080.jpg",
        "kid": "A robot's-eye view of Mars. Perseverance landed in 2021 in an ancient lake bed "
               "to look for fossils of microscopic life."
    },
    {
        "week": 9, "title": "The Milky Way Over Idaho",
        "credit": "NASA Astronomy Picture of the Day",
        "img": "https://apod.nasa.gov/apod/image/2207/MilkyWayCraters_Tezel_1080.jpg",
        "kid": "Our home galaxy from a dark-sky site. There are about 100 billion stars in the picture. "
               "Most of them have planets. Some of those planets probably have life."
    },
    {
        "week": 10, "title": "Total Solar Eclipse",
        "credit": "NASA / Aubrey Gemignani, 2017",
        "img": "https://apod.nasa.gov/apod/image/1708/TotalEclipse_Aubrey_960.jpg",
        "kid": "The Moon perfectly covers the Sun. You can only see the Sun's corona — its outer atmosphere — "
               "during the few minutes of totality. Idaho was in the path in 2017."
    },
    {
        "week": 11, "title": "The Andromeda Galaxy",
        "credit": "NASA / JPL / GALEX",
        "img": "https://apod.nasa.gov/apod/image/1208/m31_ssro_3878.jpg",
        "kid": "The closest big galaxy to ours, 2.5 million light-years away. In about 4 billion years "
               "it will collide with the Milky Way. They'll merge into one giant galaxy."
    },
    {
        "week": 12, "title": "Lunar Surface Up Close",
        "credit": "NASA · Apollo 17, 1972",
        "img": "https://apod.nasa.gov/apod/image/2012/Apollo17Pan_Schmitt_1024.jpg",
        "kid": "Footprints on the Moon. Apollo 17 was the last time humans walked on another world. "
               "The footprints are still there — there's no wind or rain to wash them away."
    },
    {
        "week": 13, "title": "The Whirlpool Galaxy",
        "credit": "NASA / ESA / Hubble Heritage",
        "img": "https://apod.nasa.gov/apod/image/0504/M51_hst.jpg",
        "kid": "A spiral galaxy eating a smaller galaxy. The smaller one is being pulled apart by gravity. "
               "Galaxies do this all the time over billions of years."
    },
]
(DATA / "apod_2026.json").write_text(
    json.dumps({
        "_source": "https://apod.nasa.gov/apod/",
        "_license": "Public domain (NASA imagery)",
        "_note": "Curated 13-pick rotation, one per summer week. APOD does not return future dates "
                 "via API, so these are hand-selected evergreen kid-friendly entries.",
        "weeks": apod_picks,
    }, indent=2),
    encoding="utf-8",
)
print(f"apod_2026.json: {len(apod_picks)} curated picks")

# ── Cleanup ──────────────────────────────────────────────────────
for f in DATA.glob("_*"):
    f.unlink()
print("Cleaned up temp files.")
print("\nFinal spine files:")
for f in sorted(DATA.glob("*.json")):
    print(f"  {f.name}: {f.stat().st_size:,} bytes")
