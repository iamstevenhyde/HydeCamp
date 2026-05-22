// ════════════ CAMP HYDE MERIT BADGES ════════════
// Earned by completing N activities in a category.
// SVG icons are inline so the scrapbook export works offline.
// Each badge: { id, title, blurb, threshold, match(activity) -> bool, svg }

const MERIT_BADGES = [
  {
    id:'naturalist', title:'Naturalist', threshold:3,
    blurb:'Three or more nature-rooted activities completed in the foothills, backyard, or river.',
    match: a => /nature|leaf|cairn|river|sage|garden|botan|wild|forag/i.test(a.title + ' ' + (a.description||'')),
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#F4D35E" stroke="#0B1418" stroke-width="3"/><path d="M50 22 C 32 38, 32 62, 50 78 C 68 62, 68 38, 50 22 Z" fill="#1B5E20" stroke="#0B1418" stroke-width="2"/><line x1="50" y1="22" x2="50" y2="78" stroke="#0B1418" stroke-width="1.5"/></svg>'
  },
  {
    id:'maker', title:'Maker', threshold:3,
    blurb:'Three or more engineering or build-it activities completed.',
    match: a => a.cat === 'engineering' || /build|maker|cardboard|automata/i.test(a.title),
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#E63946" stroke="#0B1418" stroke-width="3"/><path d="M30 60 L 50 30 L 70 60 Z" fill="#F4D35E" stroke="#0B1418" stroke-width="2"/><circle cx="50" cy="64" r="6" fill="#0B1418"/></svg>'
  },
  {
    id:'cartographer', title:'Cartographer', threshold:2,
    blurb:'Two or more map-making, travel, or place-based projects completed.',
    match: a => /map|travel|sketch|forced-pers|basalt|relief/i.test(a.title),
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#1098C7" stroke="#0B1418" stroke-width="3"/><path d="M22 70 L 38 30 L 60 50 L 78 30 L 78 70 Z" fill="#F4D35E" stroke="#0B1418" stroke-width="2"/><circle cx="55" cy="58" r="4" fill="#E63946"/></svg>'
  },
  {
    id:'printmaker', title:'Printmaker', threshold:2,
    blurb:'Two or more printmaking projects (gelli, linocut, cyanotype, rubbing).',
    match: a => a.cat === 'printmaking' || /print|cyanotype|linocut|gelli|rubbing/i.test(a.title),
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#F4D35E" stroke="#0B1418" stroke-width="3"/><rect x="28" y="32" width="44" height="32" fill="#1098C7" stroke="#0B1418" stroke-width="2"/><rect x="34" y="38" width="32" height="6" fill="#F4D35E"/><rect x="34" y="50" width="32" height="6" fill="#F4D35E"/></svg>'
  },
  {
    id:'starcharter', title:'Star Charter', threshold:2,
    blurb:'Two or more astronomy or night-sky activities completed.',
    match: a => /star|galaxy|constellat|sky|night|circuit/i.test(a.title),
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#0B1418" stroke="#0B1418" stroke-width="3"/><polygon points="50,22 56,42 78,42 60,54 66,76 50,62 34,76 40,54 22,42 44,42" fill="#F4D35E"/></svg>'
  },
  {
    id:'painter', title:'Painter', threshold:3,
    blurb:'Three or more painting projects completed.',
    match: a => a.cat === 'painting',
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#E63946" stroke="#0B1418" stroke-width="3"/><path d="M30 60 Q 50 28 70 60 Q 50 70 30 60 Z" fill="#1098C7" stroke="#0B1418" stroke-width="2"/><circle cx="40" cy="55" r="4" fill="#F4D35E"/><circle cx="55" cy="50" r="4" fill="#F4D35E"/><circle cx="62" cy="58" r="3" fill="#0B1418"/></svg>'
  },
  {
    id:'sculptor', title:'Sculptor', threshold:2,
    blurb:'Two or more sculpture or 3D projects completed.',
    match: a => a.cat === 'sculpture' || /clay|wire|sculpture|automata/i.test(a.title),
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#1B5E20" stroke="#0B1418" stroke-width="3"/><path d="M35 72 L 35 50 Q 35 30 50 30 Q 65 30 65 50 L 65 72 Z" fill="#F4D35E" stroke="#0B1418" stroke-width="2"/><circle cx="50" cy="45" r="6" fill="#0B1418"/></svg>'
  },
  {
    id:'coder', title:'Coder', threshold:2,
    blurb:'Two or more technology or digital projects completed.',
    match: a => a.cat === 'technology' || a.cat === 'digital',
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#1098C7" stroke="#0B1418" stroke-width="3"/><text x="50" y="62" text-anchor="middle" font-family="monospace" font-size="34" font-weight="900" fill="#0B1418">&lt;/&gt;</text></svg>'
  },
  {
    id:'mathematician', title:'Mathematician', threshold:2,
    blurb:'Two or more math activities completed.',
    match: a => a.cat === 'math',
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#F4D35E" stroke="#0B1418" stroke-width="3"/><text x="50" y="64" text-anchor="middle" font-family="Georgia,serif" font-size="38" font-style="italic" font-weight="700" fill="#0B1418">π</text></svg>'
  },
  {
    id:'storyteller', title:'Storyteller', threshold:2,
    blurb:'Two or more drawing, comic, journal, or stop-motion projects completed.',
    match: a => a.cat === 'drawing' || /comic|book|story|journal|stop-motion|zentangle|sketch/i.test(a.title),
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#E63946" stroke="#0B1418" stroke-width="3"/><rect x="28" y="32" width="44" height="36" fill="#F4D35E" stroke="#0B1418" stroke-width="2"/><line x1="50" y1="32" x2="50" y2="68" stroke="#0B1418" stroke-width="2"/><line x1="34" y1="42" x2="46" y2="42" stroke="#0B1418" stroke-width="1.5"/><line x1="34" y1="50" x2="46" y2="50" stroke="#0B1418" stroke-width="1.5"/><line x1="54" y1="42" x2="66" y2="42" stroke="#0B1418" stroke-width="1.5"/><line x1="54" y1="50" x2="66" y2="50" stroke="#0B1418" stroke-width="1.5"/></svg>'
  },
  {
    id:'fabricartist', title:'Fabric Artist', threshold:2,
    blurb:'Two or more textile projects (tie-dye, weaving, embroidery).',
    match: a => /tie-dye|loom|weav|embroid|patch|stitch/i.test(a.title),
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#1098C7" stroke="#0B1418" stroke-width="3"/><path d="M28 35 Q 50 50 72 35 M28 50 Q 50 65 72 50 M28 65 Q 50 80 72 65" fill="none" stroke="#F4D35E" stroke-width="3" stroke-linecap="round"/><path d="M28 35 Q 50 50 72 35 M28 50 Q 50 65 72 50 M28 65 Q 50 80 72 65" fill="none" stroke="#0B1418" stroke-width="1"/></svg>'
  },
  {
    id:'bookworm', title:'Bookworm', threshold:1,
    blurb:'Logged at least 3 hours of reading in a single week. Keep those pages turning.',
    match: () => false, // Special — computed from schedule reading cells per week.
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#4A6741" stroke="#0B1418" stroke-width="3"/><rect x="27" y="30" width="30" height="40" rx="2" fill="#F4EDD2" stroke="#0B1418" stroke-width="2"/><rect x="29" y="30" width="5" height="40" fill="#B5D4A2" stroke="#0B1418" stroke-width="1"/><line x1="36" y1="40" x2="53" y2="40" stroke="#0B1418" stroke-width="1.5"/><line x1="36" y1="46" x2="53" y2="46" stroke="#0B1418" stroke-width="1.5"/><line x1="36" y1="52" x2="48" y2="52" stroke="#0B1418" stroke-width="1.5"/><rect x="43" y="33" width="30" height="40" rx="2" fill="#F4D35E" stroke="#0B1418" stroke-width="2"/><rect x="45" y="33" width="5" height="40" fill="#C9A82F" stroke="#0B1418" stroke-width="1"/><line x1="52" y1="43" x2="69" y2="43" stroke="#0B1418" stroke-width="1.5"/><line x1="52" y1="49" x2="69" y2="49" stroke="#0B1418" stroke-width="1.5"/><line x1="52" y1="55" x2="62" y2="55" stroke="#0B1418" stroke-width="1.5"/></svg>'
  },
  {
    id:'campveteran', title:'Camp Veteran', threshold:13,
    blurb:'Completed at least one activity in every week of summer. The full thirteen-week ribbon.',
    match: () => false, // Special — earned by week coverage, not category. Computed separately.
    svg:'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#0B1418" stroke="#0B1418" stroke-width="3"/><circle cx="50" cy="50" r="34" fill="none" stroke="#F4D35E" stroke-width="2"/><text x="50" y="46" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="14" fill="#F4D35E">CAMP</text><text x="50" y="62" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="14" fill="#E63946">HYDE</text><text x="50" y="76" text-anchor="middle" font-family="monospace" font-size="9" fill="#F4D35E">MMXXVI</text></svg>'
  }
];
