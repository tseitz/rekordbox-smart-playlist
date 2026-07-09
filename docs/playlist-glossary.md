# Playlist & Tag Glossary

The authoritative "what does each playlist/tag mean and why does it exist" reference.
Structure/counts live in the [architecture spec](superpowers/specs/2026-07-07-playlist-architecture-design.md);
this doc is about **meaning and intent**, so future sessions don't have to re-ask.

**DJ:** Tegan, aka **Dane Dubz**. Plays a genre-diverse bass/underground library across
many settings and hardware types (laptop Rekordbox, CDJ-3000, and notably the **XDJ-RR**,
which has weak live filtering — hence folder-navigable structure). Builds his own sound
systems.

**Legend:** ✅ confirmed with the DJ · ❓ inferred/unknown — **please confirm or correct.**

---

## The two organizing concepts

- **Context** — *fixed for the duration of a gig; you navigate TO it.* Time, venue, format,
  audience. Each context is a top-level folder with the full 82-leaf anatomy.
- **Caliber** — *slides WITHIN a gig; you refine a context WITH it.* A quality tier. Two
  levels, nested inside every context: **My Set** (S-tier) and **The Rotation** (A-tier).

Every leaf playlist is `Context tag AND <lens tag(s)>`, minus anything tagged `Archive`.

---

## Contexts (top-level folders)

| Context | Meaning | Notes |
|---|---|---|
| **Daytime** ✅ | Outdoor festivals, day parties | Mid-energy, day/up cluster with Pool Party |
| **Pool Party** ✅ | Fun, upbeat, crowd-friendly | Day/up cluster |
| **Morningtime Vibes** ✅ | Warm, easy listening, early | Warm/low cluster |
| **Sunrise** ✅ | Morning sets, comedown | Warm/low cluster |
| **Chillin** ✅ | Background music, lounge | Warm/low cluster |
| **Nighttime** ✅ | Club sets, evening | Peak; canonical template context |
| **Late Night** ✅ | Dark rooms, 2am+ | Peak-dark |
| **Afterparty** ✅ | Low-key, intimate, late | Where **The Rotation** shines |
| **Silent Disco** ✅ | Headphone sets | A *format*, not a time — selection differs |
| **Crispy Speakers** ✅ | The best tracks for the best speakers | Tracks built to sound huge on a great rig. Dane builds his own systems and enjoys playing nice ones, so these get a dedicated context |
| **Missy** ✅ | Curated pool for B2B sets with his wife, **Missy** | Songs picked for her vibe |
| **B2B** ✅ | General back-to-back / collaborative-set pool | Format context, like Missy but not partner-specific |
| **My Set** (global) ✅ | Situation-independent **S-tier** browse — "the songs that represent me / Dane Dubz" | The best of the best; a showcase context. No caliber nesting (nesting My Set in My Set is redundant) |

### Caliber tiers (nested inside every context)

| Tier | Tag | Meaning |
|---|---|---|
| **My Set** ✅ | `My Set` | S-tier. The absolute best; the tracks that represent Dane Dubz |
| **The Rotation** ✅ | `The Rotation` | A-tier, a notch below My Set. Reliable floor-movers you play out at an afterparty "just messing around" — not all absolute bangers, but guaranteed to move the floor or pique interest. Can overlap with My Set |

---

## Lenses (the sub-folders inside each context)

You browse a context by **one lens at a time** (Situation-first, one-lens-second).

### Flow — set position ✅ (top level only, not inside caliber)
`Openers` → `Beginning` → `Middle` → `End` → `Closers`. Where a track sits in a set's arc.
(Energy is separate — see Ratings below.)

### Texture — how it SOUNDS (genre-blind) ✅ (from README)
The unifying cross-genre lens: every genre can be any texture, and same-texture tracks mix.

| Texture (tag) | Feel |
|---|---|
| **GROOVY (The Pocket)** | Swing, shuffle, broken beats, syncopation |
| **DEEP (The Head)** | Minimal, spacious, dark, hypnotic |
| **HEAVY (The Face)** | Aggressive, distorted, high energy, "bass face" |
| **ORGANIC (The Soul)** | Melodic, warm, emotional, acoustic samples |
| **WEIRD (The Brain)** | Experimental, psychedelic, unexpected |
| **VOCALS** | Lyrical focus, rap, grime, vocal-led |
| **PALATE CLEANSER** | Transitions, palette shifts, breathers |

**Texture Combos** (curated pairs, materialized as folders because the RR can't filter
them live): Groovy+Deep, Groovy+Heavy, Groovy+Organic, Groovy+Vocals, Deep+Organic,
Deep+Heavy, Deep+Weird, Heavy+Weird, Heavy+Vocals, Organic+Vocals. *This is a starting
set — adjust to the combos actually reached for.*

### Genre — what it IS ✅ (texture-blind)
`Beats`, `DnB`, `Dub`, `Dubstep`, `Feels`, `House`, `Jungle`, `Riddim`, `UKG`, `Vibes`, `Weapons`

Meanings needing confirmation:
- **Weapons** ❓ — *what is this?* Inferred: a catch-all for "killer/secret-weapon" tracks
  regardless of genre. It's a genre-*lens* filter only (present in every context) but is
  **excluded from the global Genres tree** (it has no sub-styles). **Please confirm.**
- **Feels** ❓ — inferred: emotional / melodic / in-your-feelings tracks. **Confirm.**
- **Vibes** ❓ — inferred: general good-vibes / groove tracks. **Confirm.**
- `Beats`, `DnB`, `Dub`, `Dubstep`, `House`, `Jungle`, `Riddim`, `UKG` — standard genres.

---

## Global Genres tree (situation-independent, sub-styles)

Genre-first browsing with sub-styles. Only Dub and DnB have sub-styles today; the rest
show just `All`. `Weapons` is deliberately omitted (see above).

**Dub sub-styles:**
- `Dub Doubles` ❓ · `Dub Wobblers` ❓ · `Dub Sound System` ❓ · `Dub Slimzee` ❓
  (Slimzee the grime DJ?) · `Dub Trippy/Interesting` ❓ · `Dub Reggae` ❓
  — **all inferred; please give one-line meanings.**

**DnB sub-styles** (standard DnB subgenres ✅):
- `DnB Jump Up` · `DnB Rollers` · `DnB Liquid` · `DnB Dancefloor`

---

## Utility

### Go Through — a to-do / QA bucket
| Tag | Meaning |
|---|---|
| **Bad Quality** ✅ | Low audio-quality tracks flagged to review/replace |
| **Bad Grid** ✅ | Tracks with a bad beatgrid that needs fixing |
| **Jayden** ❓ | *Unknown — a person? tracks from/for Jayden? a to-review source?* **Confirm.** |

### `Archive` ✅
A global exclusion tag. Anything tagged `Archive` is filtered OUT of every playlist
(`negativeConditions`). Use it to retire a track without deleting it.

### Ratings = Energy ✅ (not quality)
1★ warmup/ambient → 5★ maximum/headliner. Sortable on all hardware, so energy is handled
by rating sort rather than by folders.

---

## Open confirmations for the DJ
The ❓ items above — most importantly **Weapons**, **Feels**, **Vibes**, **Jayden**, and the
**Dub sub-styles** — are inferred and should be corrected here so they're settled for good.
