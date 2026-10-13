"""
AquaPulse – Fish Species Profiles & Disease Knowledge Base
===========================================================
Centralised reference data powering:

* Species-specific water-parameter thresholds.
* Rule-based disease diagnosis (symptom → disease → treatment).
* Medication dosage charts with species-specific cautions.

The data here is curated from established aquarium-keeping guidelines
and is intentionally conservative (erring on the side of caution).
"""

from typing import Any, Dict, List


# ═════════════════════════════════════════════════════════════════════════════
#  FISH SPECIES PROFILES
# ═════════════════════════════════════════════════════════════════════════════

FISH_PROFILES: Dict[str, Dict[str, Any]] = {
    "betta": {
        "name": "Betta (Siamese Fighting Fish)",
        "scientific_name": "Betta splendens",
        "emoji": "🐠",
        "min_tank_liters": 19,
        "care_level": "Easy",
        "temperament": "Semi-aggressive (males)",
        "lifespan_years": "3–5",
        "diet": "Carnivore — pellets, bloodworms, brine shrimp",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
            "ph": {
                "safe_min": 6.5, "safe_max": 7.5,
                "warning_min": 6.0, "warning_max": 8.0,
            },
            "temperature_c": {
                "safe_min": 24.0, "safe_max": 28.0,
                "warning_min": 22.0, "warning_max": 30.0,
            },
        },
        "notes": (
            "Labyrinth breather — needs surface air access. "
            "Males must be housed alone. Long fins make them "
            "susceptible to fin rot and snagging on sharp décor."
        ),
    },
    "goldfish": {
        "name": "Goldfish",
        "scientific_name": "Carassius auratus",
        "emoji": "🐟",
        "min_tank_liters": 75,
        "care_level": "Easy",
        "temperament": "Peaceful",
        "lifespan_years": "10–15",
        "diet": "Omnivore — flakes, gel food, blanched vegetables",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
            "ph": {
                "safe_min": 7.0, "safe_max": 8.4,
                "warning_min": 6.5, "warning_max": 9.0,
            },
            "temperature_c": {
                "safe_min": 18.0, "safe_max": 23.0,
                "warning_min": 15.0, "warning_max": 26.0,
            },
        },
        "notes": (
            "Cold-water species — typically no heater required. "
            "Heavy bioload; strong filtration and frequent water changes essential."
        ),
    },
    "neon_tetra": {
        "name": "Neon Tetra",
        "scientific_name": "Paracheirodon innesi",
        "emoji": "🐟",
        "min_tank_liters": 38,
        "care_level": "Easy",
        "temperament": "Peaceful (schooling)",
        "lifespan_years": "5–8",
        "diet": "Omnivore — micro pellets, flakes, baby brine shrimp",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
            "ph": {
                "safe_min": 5.5, "safe_max": 7.0,
                "warning_min": 5.0, "warning_max": 7.5,
            },
            "temperature_c": {
                "safe_min": 20.0, "safe_max": 26.0,
                "warning_min": 18.0, "warning_max": 28.0,
            },
        },
        "notes": (
            "Must be kept in schools of 6+. Prefers soft, slightly acidic water. "
            "Susceptible to Neon Tetra Disease (Pleistophora)."
        ),
    },
    "guppy": {
        "name": "Guppy",
        "scientific_name": "Poecilia reticulata",
        "emoji": "🐠",
        "min_tank_liters": 38,
        "care_level": "Easy",
        "temperament": "Peaceful",
        "lifespan_years": "2–3",
        "diet": "Omnivore — flakes, micro pellets, algae wafers",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
            "ph": {
                "safe_min": 6.8, "safe_max": 7.8,
                "warning_min": 6.0, "warning_max": 8.5,
            },
            "temperature_c": {
                "safe_min": 22.0, "safe_max": 28.0,
                "warning_min": 20.0, "warning_max": 30.0,
            },
        },
        "notes": (
            "Prolific breeders — separate males and females to control population. "
            "Hardy and beginner-friendly."
        ),
    },
    "angelfish": {
        "name": "Angelfish",
        "scientific_name": "Pterophyllum scalare",
        "emoji": "🐠",
        "min_tank_liters": 114,
        "care_level": "Moderate",
        "temperament": "Semi-aggressive",
        "lifespan_years": "8–10",
        "diet": "Omnivore — flakes, pellets, frozen/live foods",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
            "ph": {
                "safe_min": 6.0, "safe_max": 7.5,
                "warning_min": 5.5, "warning_max": 8.0,
            },
            "temperature_c": {
                "safe_min": 24.0, "safe_max": 28.0,
                "warning_min": 22.0, "warning_max": 30.0,
            },
        },
        "notes": (
            "Tall-bodied cichlid — needs a tall tank (45 cm+ height). "
            "Can be territorial; may eat very small tank mates."
        ),
    },
    "molly": {
        "name": "Molly",
        "scientific_name": "Poecilia sphenops",
        "emoji": "🐟",
        "min_tank_liters": 75,
        "care_level": "Easy",
        "temperament": "Peaceful",
        "lifespan_years": "3–5",
        "diet": "Omnivore — flakes, algae, blanched vegetables",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
            "ph": {
                "safe_min": 7.0, "safe_max": 8.5,
                "warning_min": 6.5, "warning_max": 9.0,
            },
            "temperature_c": {
                "safe_min": 22.0, "safe_max": 28.0,
                "warning_min": 20.0, "warning_max": 30.0,
            },
        },
        "notes": (
            "Tolerates slightly brackish water. Livebearers — separate sexes "
            "to prevent overpopulation."
        ),
    },
    "corydoras": {
        "name": "Corydoras Catfish",
        "scientific_name": "Corydoras spp.",
        "emoji": "🐡",
        "min_tank_liters": 38,
        "care_level": "Easy",
        "temperament": "Peaceful (schooling)",
        "lifespan_years": "5–7",
        "diet": "Omnivore — sinking pellets, algae wafers, bloodworms",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
            "ph": {
                "safe_min": 6.0, "safe_max": 7.5,
                "warning_min": 5.5, "warning_max": 8.0,
            },
            "temperature_c": {
                "safe_min": 22.0, "safe_max": 26.0,
                "warning_min": 20.0, "warning_max": 28.0,
            },
        },
        "notes": (
            "Bottom-dweller — needs smooth substrate (sand preferred). "
            "Keep in groups of 6+. Sensitive to salt-based treatments."
        ),
    },
    "cherry_shrimp": {
        "name": "Cherry Shrimp",
        "scientific_name": "Neocaridina davidi",
        "emoji": "🦐",
        "min_tank_liters": 19,
        "care_level": "Easy",
        "temperament": "Peaceful",
        "lifespan_years": "1–2",
        "diet": "Omnivore — algae, biofilm, shrimp pellets, blanched vegetables",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.1},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.1},
            "nitrate_ppm": {"safe_max": 15.0, "warning_max": 30.0},
            "ph": {
                "safe_min": 6.5, "safe_max": 7.5,
                "warning_min": 6.0, "warning_max": 8.0,
            },
            "temperature_c": {
                "safe_min": 20.0, "safe_max": 26.0,
                "warning_min": 18.0, "warning_max": 28.0,
            },
        },
        "notes": (
            "Extremely sensitive to copper — avoid copper-based medications entirely. "
            "Sensitive to parameter swings; drip-acclimate new arrivals."
        ),
    },
    "oscar": {
        "name": "Oscar",
        "scientific_name": "Astronotus ocellatus",
        "emoji": "🐠",
        "min_tank_liters": 200,
        "care_level": "Moderate",
        "temperament": "Aggressive",
        "lifespan_years": "10–15",
        "diet": "Carnivore — pellets, frozen shrimp, earthworms",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
            "ph": {
                "safe_min": 6.0, "safe_max": 8.0,
                "warning_min": 5.5, "warning_max": 8.5,
            },
            "temperature_c": {
                "safe_min": 23.0, "safe_max": 28.0,
                "warning_min": 21.0, "warning_max": 30.0,
            },
        },
        "notes": (
            "Large, messy, and intelligent cichlid. Needs powerful filtration "
            "and weekly 30–40 % water changes."
        ),
    },
    "platy": {
        "name": "Platy",
        "scientific_name": "Xiphophorus maculatus",
        "emoji": "🐠",
        "min_tank_liters": 38,
        "care_level": "Easy",
        "temperament": "Peaceful",
        "lifespan_years": "2–3",
        "diet": "Omnivore — flakes, micro pellets, spirulina",
        "thresholds": {
            "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
            "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
            "ph": {
                "safe_min": 7.0, "safe_max": 8.2,
                "warning_min": 6.5, "warning_max": 8.5,
            },
            "temperature_c": {
                "safe_min": 20.0, "safe_max": 26.0,
                "warning_min": 18.0, "warning_max": 28.0,
            },
        },
        "notes": "Hardy livebearer, good beginner fish. Prefers hard, alkaline water.",
    },
}


# Helper: sorted list of (key, display_name) for dropdowns
FISH_SPECIES_LIST: List[tuple[str, str]] = sorted(
    [(k, v["name"]) for k, v in FISH_PROFILES.items()],
    key=lambda t: t[1],
)


def get_thresholds_for_species(species_key: str) -> Dict[str, Dict[str, float]]:
    """Return the parameter thresholds for a species, or generic defaults."""
    profile = FISH_PROFILES.get(species_key)
    if profile:
        return profile["thresholds"]
    # Fallback: generic freshwater defaults
    return {
        "ammonia_ppm": {"safe_max": 0.0, "warning_max": 0.25},
        "nitrite_ppm": {"safe_max": 0.0, "warning_max": 0.25},
        "nitrate_ppm": {"safe_max": 20.0, "warning_max": 40.0},
        "ph": {
            "safe_min": 6.5, "safe_max": 7.5,
            "warning_min": 6.0, "warning_max": 8.0,
        },
        "temperature_c": {
            "safe_min": 24.0, "safe_max": 28.0,
            "warning_min": 22.0, "warning_max": 30.0,
        },
    }


# ═════════════════════════════════════════════════════════════════════════════
#  DISEASE KNOWLEDGE BASE
# ═════════════════════════════════════════════════════════════════════════════

DISEASE_DATABASE: Dict[str, Dict[str, Any]] = {

    # ── 1. Fin Rot ──────────────────────────────────────────────────────
    "fin_rot": {
        "name": "Fin Rot",
        "emoji": "🩹",
        "severity": "Moderate → Severe if untreated",
        "keywords": [
            "fin rot", "rotting fins", "fins rotting", "tail rot",
            "frayed fins", "ragged fins", "torn fins", "tattered fins",
            "fins falling apart", "fins dissolving", "fins disintegrating",
            "fins getting shorter", "fins shrinking", "fin edges dark",
            "blackened fin edges", "fin edges turning black",
            "losing fins", "fin loss", "fins look eaten",
            "fins melting", "fin damage", "fins decaying",
        ],
        "description": (
            "A bacterial infection that causes progressive deterioration "
            "of fin tissue, starting from the edges and working inward. "
            "If left untreated it can reach the body and become fatal."
        ),
        "causes": [
            "Poor water quality (elevated ammonia or nitrite)",
            "Stress from overcrowding or aggressive tank mates",
            "Fin nipping by other fish",
            "Temperature fluctuations or low temperature",
            "Weakened immune system",
        ],
        "treatment_steps": [
            "1. Test water immediately — perform a 25–30 % water change if ammonia or nitrite is above 0.",
            "2. Continue daily 20 % water changes for 7–10 days to keep water pristine.",
            "3. Add Indian Almond Leaves (1 leaf per 5 gallons) — releases tannins with mild antibacterial properties.",
            "4. Add Methylene Blue (1 drop per gallon) to a hospital/quarantine tank if available.",
            "5. If no improvement after 5 days, treat with API Melafix or Seachem KanaPlex.",
            "6. Maintain a stable temperature at the upper end of your species' range to boost immune response.",
            "7. Remove sharp decorations that could further damage fins.",
        ],
        "medications": [
            {"name": "Methylene Blue", "dosage": "1 drop per gallon", "notes": "Mild, safe for most fish"},
            {"name": "Indian Almond Leaves", "dosage": "1 leaf per 5 gallons", "notes": "Natural antibacterial, lowers pH slightly"},
            {"name": "API Melafix", "dosage": "5 ml per 10 gallons daily for 7 days", "notes": "Tea-tree-oil based; avoid for labyrinth fish at full strength"},
            {"name": "Seachem KanaPlex", "dosage": "Follow package directions", "notes": "Kanamycin — effective for resistant infections"},
            {"name": "Aquarium Salt", "dosage": "1 tablespoon per 5 gallons", "notes": "Not for scaleless fish or shrimp"},
        ],
        "species_notes": {
            "betta": (
                "Bettas are especially prone to fin rot due to their long, delicate fins. "
                "Use Indian Almond Leaf extract (1 drop per litre) and raise temperature to 27–28 °C. "
                "Avoid Melafix at full strength — it can damage their labyrinth organ; use at half dose or choose Bettafix instead."
            ),
            "goldfish": (
                "Goldfish fin rot often stems from overcrowding and high bioload. "
                "Increase water changes to 30 % every other day. Aquarium salt (1 tbsp / 5 gal) is well-tolerated."
            ),
            "corydoras": (
                "Corydoras are scaleless and sensitive to salt. "
                "Do NOT use aquarium salt. Rely on pristine water, Indian Almond Leaves, and KanaPlex if needed."
            ),
            "cherry_shrimp": (
                "Shrimp are extremely sensitive to most medications. "
                "Rely only on water quality improvements and Indian Almond Leaves. "
                "NEVER use copper-based treatments."
            ),
        },
        "prevention": [
            "Maintain 0 ppm ammonia and nitrite at all times.",
            "Perform regular weekly water changes (20–30 %).",
            "Avoid overcrowding and fin-nipping species.",
            "Keep temperature stable within species' ideal range.",
        ],
    },

    # ── 2. Ich (White Spot Disease) ─────────────────────────────────────
    "ich": {
        "name": "Ich (White Spot Disease)",
        "emoji": "⚪",
        "severity": "Moderate — fatal if untreated",
        "keywords": [
            "ich", "ick", "white spots", "white dot", "white dots",
            "white spot disease", "salt grain spots",
            "spots on body", "spots on fins", "white specks",
            "rubbing against objects", "flashing", "scratching",
            "itching", "fish scratching", "fish rubbing",
            "tiny white bumps",
        ],
        "description": (
            "Ichthyophthirius multifiliis — a protozoan parasite that forms "
            "visible white cysts on the skin, fins, and gills. Highly contagious "
            "and can wipe out an entire tank if left untreated."
        ),
        "causes": [
            "Introduction of infected fish without quarantine",
            "Sudden temperature drops that stress the immune system",
            "Contaminated equipment, plants, or water",
        ],
        "treatment_steps": [
            "1. Gradually raise the temperature to 28–30 °C over 24–48 hours (speeds up the parasite life cycle).",
            "2. Add aquarium salt: 1 tablespoon per 5 gallons (dissolve first).",
            "3. Treat with Ich-X (Hikari) or Super Ick Cure following package directions.",
            "4. Maintain treatment for at least 3 days after the last visible spot disappears.",
            "5. Perform 25 % water changes every 2 days during treatment, re-dosing medication after each change.",
            "6. Remove activated carbon from the filter (it absorbs medication).",
            "7. Keep lights dimmed — ich parasites are photosensitive.",
        ],
        "medications": [
            {"name": "Ich-X (Hikari)", "dosage": "5 ml per 10 gallons", "notes": "Safe for most fish including scaleless species"},
            {"name": "Aquarium Salt", "dosage": "1 tbsp per 5 gallons", "notes": "Not for scaleless fish, plants, or shrimp"},
            {"name": "Methylene Blue", "dosage": "1 drop per gallon", "notes": "Alternative for sensitive species"},
            {"name": "Kordon Rid-Ich Plus", "dosage": "Follow package", "notes": "Formalin + malachite green"},
        ],
        "species_notes": {
            "betta": "Raise temperature to 28–29 °C. Bettas tolerate heat well. Use half-dose salt if using salt at all.",
            "corydoras": "DO NOT use salt. Use Ich-X which is safe for scaleless fish. Raise temp slowly.",
            "cherry_shrimp": "Most ich medications are lethal to shrimp. Remove shrimp to a separate container during treatment. Temperature method alone may work.",
            "goldfish": "Goldfish are cold-water; raising temp to 28 °C is stressful. Prefer medication over heat method.",
            "neon_tetra": "Ensure it's true Ich and not Neon Tetra Disease (NTD), which has no cure. Ich spots are raised and uniform; NTD causes color loss and irregular white patches.",
        },
        "prevention": [
            "Quarantine all new fish for 2–4 weeks before adding to main tank.",
            "Maintain stable temperature — avoid sudden drops.",
            "Keep fish stress-free with proper tank size, hiding spots, and compatible mates.",
        ],
    },

    # ── 3. Velvet Disease ───────────────────────────────────────────────
    "velvet": {
        "name": "Velvet Disease (Oodinium)",
        "emoji": "✨",
        "severity": "Severe — fast-acting and lethal",
        "keywords": [
            "velvet", "gold dust", "rust disease", "golden spots",
            "gold dust on skin", "yellowish dust", "dusty appearance",
            "velvet disease", "rust colored", "shimmer on skin",
            "clamped fins velvet", "gasping velvet",
        ],
        "description": (
            "Caused by the dinoflagellate parasite Oodinium (Piscinoodinium). "
            "Appears as a fine gold or rust-coloured dust on the body. "
            "More lethal and harder to spot than ich."
        ),
        "causes": [
            "Stressed fish with weakened immunity",
            "Poor water quality",
            "Sudden temperature or pH swings",
            "Introduction of infected fish",
        ],
        "treatment_steps": [
            "1. Immediately darken the tank — Oodinium is photosynthetic and light accelerates its growth. Cover the tank or turn off lights.",
            "2. Raise temperature to 28–30 °C gradually.",
            "3. Add aquarium salt: 1 tbsp per 5 gallons.",
            "4. Treat with Copper-based medication (e.g., Seachem Cupramine) per package instructions.",
            "5. Continue treatment for 10–14 days even if symptoms disappear.",
            "6. Perform 25 % water changes every 3 days, re-dosing after each change.",
            "7. Remove activated carbon from filter.",
        ],
        "medications": [
            {"name": "Seachem Cupramine", "dosage": "Follow package (copper-based)", "notes": "LETHAL to invertebrates and shrimp"},
            {"name": "API Super Ick Cure", "dosage": "Follow package", "notes": "Also effective against velvet"},
            {"name": "Methylene Blue", "dosage": "1 drop per gallon in hospital tank", "notes": "Supportive treatment"},
        ],
        "species_notes": {
            "betta": "Bettas are highly susceptible. Darken tank, raise temp to 28 °C, treat with Methylene Blue. Avoid copper if possible.",
            "cherry_shrimp": "NEVER use copper. Remove shrimp immediately. They will die if exposed.",
            "corydoras": "Copper at reduced dose only. Monitor closely.",
        },
        "prevention": [
            "Quarantine new fish for 2–4 weeks.",
            "Keep water quality high and temperature stable.",
            "Avoid stress-inducing conditions.",
        ],
    },

    # ── 4. Swim Bladder Disorder ────────────────────────────────────────
    "swim_bladder": {
        "name": "Swim Bladder Disorder",
        "emoji": "🫧",
        "severity": "Mild → Moderate",
        "keywords": [
            "swim bladder", "floating sideways", "floating upside down",
            "sinking to bottom", "can't swim straight", "swimming sideways",
            "buoyancy problem", "trouble swimming", "upside down",
            "swimming erratically", "listing to one side",
            "can't stay upright", "belly up", "floating at top",
            "struggling to swim", "swimming vertically",
        ],
        "description": (
            "A condition affecting the swim bladder that controls buoyancy. "
            "The fish may float uncontrollably, sink, or swim at odd angles. "
            "Often caused by overfeeding or constipation rather than infection."
        ),
        "causes": [
            "Overfeeding / constipation (most common)",
            "Swallowing air while surface-feeding",
            "Bacterial infection of the swim bladder",
            "Physical injury or birth defect",
            "Rapid temperature changes",
        ],
        "treatment_steps": [
            "1. Fast the fish for 2–3 days (no food at all).",
            "2. After fasting, feed a small piece of blanched, shelled pea (acts as a laxative).",
            "3. Ensure water temperature is at the upper end of the species' ideal range.",
            "4. Lower the water level to make surface access easier.",
            "5. If symptoms persist after 5 days, treat with API General Cure (may indicate bacterial cause).",
            "6. Avoid floating pellets — use sinking food to prevent air gulping.",
        ],
        "medications": [
            {"name": "Blanched Pea", "dosage": "1 small pea, shell removed", "notes": "Natural laxative — first-line treatment"},
            {"name": "Epsom Salt (Magnesium Sulfate)", "dosage": "1 tsp per 5 gallons", "notes": "Reduces swelling, acts as mild laxative"},
            {"name": "API General Cure", "dosage": "Follow package", "notes": "Only if bacterial cause is suspected"},
        ],
        "species_notes": {
            "betta": "Very common in bettas due to overfeeding. Fast 2–3 days, then feed daphnia (live or frozen) as a natural laxative. Avoid freeze-dried foods which can expand in the stomach.",
            "goldfish": "Fancy goldfish (round-bodied) are genetically prone. Feed gel food or sinking pellets instead of flakes. Pre-soak all dried food.",
        },
        "prevention": [
            "Feed small amounts 1–2 times daily.",
            "Pre-soak dry food before feeding.",
            "Include fibre-rich foods (daphnia, blanched peas) weekly.",
            "Maintain stable water temperature.",
        ],
    },

    # ── 5. Dropsy ───────────────────────────────────────────────────────
    "dropsy": {
        "name": "Dropsy (Ascites)",
        "emoji": "🔴",
        "severity": "Critical — often fatal",
        "keywords": [
            "dropsy", "bloated", "swollen belly", "pinecone scales",
            "scales sticking out", "raised scales", "swollen body",
            "bloated fish", "puffed up", "edema",
            "fish looks like pinecone", "scales protruding",
            "abdominal swelling",
        ],
        "description": (
            "Dropsy is not a disease itself but a symptom of internal organ failure, "
            "typically kidney failure causing fluid retention. The hallmark sign is "
            "scales standing out from the body like a pinecone when viewed from above."
        ),
        "causes": [
            "Bacterial infection (Aeromonas) secondary to a weakened immune system",
            "Chronic poor water quality",
            "Internal parasites",
            "Liver or kidney failure",
            "Old age",
        ],
        "treatment_steps": [
            "1. Isolate the affected fish immediately in a hospital tank.",
            "2. Add Epsom salt: 1 tablespoon per 5 gallons (reduces fluid retention).",
            "3. Treat with a broad-spectrum antibiotic: Seachem KanaPlex + Seachem Focus (bound to food).",
            "4. Perform 25 % water changes daily in the hospital tank.",
            "5. Maintain elevated temperature (27–28 °C).",
            "6. Offer high-quality, easily digestible food (if the fish is eating).",
            "7. Be prepared: dropsy has a low survival rate once pineconing is visible. Early detection is key.",
        ],
        "medications": [
            {"name": "Epsom Salt (MgSO₄)", "dosage": "1 tbsp per 5 gallons", "notes": "Draws out excess fluid"},
            {"name": "Seachem KanaPlex", "dosage": "Follow package", "notes": "Broad-spectrum antibiotic"},
            {"name": "Seachem Focus", "dosage": "Mix with food per package", "notes": "Binds medication to food for internal delivery"},
            {"name": "API Furan-2", "dosage": "Follow package", "notes": "Alternative antibiotic"},
        ],
        "species_notes": {
            "betta": "Bettas are susceptible. Clamp-fin + bloating is an early warning. Act immediately — once pineconing starts, prognosis is very poor.",
            "goldfish": "Often related to kidney issues from chronic high-nitrate exposure. Improve water quality immediately.",
        },
        "prevention": [
            "Maintain pristine water quality — 0 ammonia, 0 nitrite, <20 ppm nitrate.",
            "Avoid chronic stress.",
            "Feed a varied, high-quality diet.",
            "Quarantine new fish.",
        ],
    },

    # ── 6. Columnaris (Cotton Wool Disease) ─────────────────────────────
    "columnaris": {
        "name": "Columnaris (Cotton Wool Disease)",
        "emoji": "🧶",
        "severity": "Severe — can kill within 24–72 hours",
        "keywords": [
            "columnaris", "cotton wool", "cotton mouth",
            "white cotton on body", "white fuzz", "white fluffy patches",
            "mouth fungus", "mouth rot", "white patches on body",
            "white growth on mouth", "white stuff on fish",
            "white lesion", "saddleback lesion",
        ],
        "description": (
            "A bacterial infection (Flavobacterium columnare) often mistaken "
            "for a fungus due to its cotton-like appearance. It can be acute "
            "(killing within 24 hours) or chronic."
        ),
        "causes": [
            "Bacterial (not fungal) — Flavobacterium columnare",
            "Triggered by stress and poor water quality",
            "High water temperature accelerates progression",
            "Skin injuries from handling or aggressive mates",
        ],
        "treatment_steps": [
            "1. LOWER the temperature to 23–24 °C (unlike ich — columnaris thrives in warmth).",
            "2. Perform an immediate 30 % water change.",
            "3. Treat with Seachem KanaPlex or API Furan-2 (antibiotics are essential — this is bacterial).",
            "4. Add Methylene Blue to a hospital tank for topical relief.",
            "5. Continue antibiotics for the full course even if symptoms improve.",
            "6. Remove activated carbon from filter.",
        ],
        "medications": [
            {"name": "Seachem KanaPlex", "dosage": "Follow package", "notes": "First-line antibiotic"},
            {"name": "API Furan-2", "dosage": "Follow package", "notes": "Nitrofurazone-based alternative"},
            {"name": "Methylene Blue", "dosage": "Topical dab or 1 drop/gallon bath", "notes": "Supportive, not a cure alone"},
        ],
        "species_notes": {
            "betta": "Can resemble fin rot — key difference is the cottony white texture. Treat aggressively with KanaPlex.",
            "guppy": "Guppies are very susceptible. Quarantine immediately.",
        },
        "prevention": [
            "Maintain excellent water quality.",
            "Avoid overcrowding.",
            "Handle fish gently to prevent skin injuries.",
            "Quarantine new arrivals.",
        ],
    },

    # ── 7. Fungal Infection ─────────────────────────────────────────────
    "fungal_infection": {
        "name": "Fungal Infection (Saprolegnia)",
        "emoji": "🍄",
        "severity": "Moderate",
        "keywords": [
            "fungus", "fungal", "white fuzzy growth", "cotton like growth",
            "mold on fish", "white mold", "grey fuzzy patches",
            "fungal infection", "saprolegnia", "white tuft",
            "fluffy white", "hairy growth",
        ],
        "description": (
            "True fungal infections (Saprolegnia spp.) appear as white or greyish "
            "cotton-like tufts, usually on damaged tissue. They are secondary infections "
            "that take hold when the fish's slime coat is compromised."
        ),
        "causes": [
            "Open wounds or damaged slime coat",
            "Handling injury",
            "Secondary to other diseases (ich, fin rot)",
            "Poor water quality",
            "Uneaten food decomposing near the fish",
        ],
        "treatment_steps": [
            "1. Perform a 25 % water change to improve water quality.",
            "2. Treat with Methylene Blue (1 drop per gallon) or an antifungal like API Pimafix.",
            "3. If localized, dab the affected area with a cotton swab dipped in Methylene Blue (out of water, briefly).",
            "4. Add Indian Almond Leaves for mild antifungal tannins.",
            "5. Ensure no rotting food or organic matter is accumulating in the tank.",
            "6. Treat any underlying primary infection (e.g., fin rot).",
        ],
        "medications": [
            {"name": "Methylene Blue", "dosage": "1 drop per gallon or topical dab", "notes": "Effective broad-spectrum antifungal"},
            {"name": "API Pimafix", "dosage": "5 ml per 10 gallons daily for 7 days", "notes": "Antifungal"},
            {"name": "Seachem ParaGuard", "dosage": "Follow package", "notes": "Broad-spectrum — anti-parasitic and antifungal"},
            {"name": "Indian Almond Leaves", "dosage": "1 leaf per 5 gallons", "notes": "Mild natural antifungal"},
        ],
        "species_notes": {
            "betta": "Often appears on damaged fin tissue. Treat the primary cause (fin rot) simultaneously.",
            "cherry_shrimp": "Avoid most antifungals. Use Indian Almond Leaves only.",
        },
        "prevention": [
            "Maintain healthy slime coat (avoid netting, use cups to transfer fish).",
            "Keep water clean — remove uneaten food promptly.",
            "Treat injuries immediately.",
        ],
    },

    # ── 8. Popeye ───────────────────────────────────────────────────────
    "popeye": {
        "name": "Popeye (Exophthalmia)",
        "emoji": "👁️",
        "severity": "Moderate → Severe",
        "keywords": [
            "popeye", "bulging eye", "swollen eye", "protruding eye",
            "eye swelling", "eye bulging out", "one eye bigger",
            "eyes sticking out", "exophthalmia", "cloudy eye swelling",
        ],
        "description": (
            "A condition where one or both eyes protrude from the head due to "
            "fluid buildup behind the eyeball. Can be unilateral (injury) "
            "or bilateral (systemic infection)."
        ),
        "causes": [
            "Unilateral (one eye): physical injury, bumping into objects",
            "Bilateral (both eyes): bacterial infection, poor water quality, tuberculosis",
            "Internal parasites (rare)",
        ],
        "treatment_steps": [
            "1. Test and correct water parameters immediately.",
            "2. Perform daily 20 % water changes for 7–10 days.",
            "3. Add Epsom salt: 1 tsp per 5 gallons (reduces swelling).",
            "4. If bilateral or no improvement: treat with Seachem KanaPlex (antibiotic).",
            "5. Unilateral popeye from injury often resolves on its own in 1–2 weeks with clean water.",
            "6. Do NOT attempt to drain the eye.",
        ],
        "medications": [
            {"name": "Epsom Salt", "dosage": "1 tsp per 5 gallons", "notes": "Reduces fluid buildup"},
            {"name": "Seachem KanaPlex", "dosage": "Follow package", "notes": "For bacterial cause"},
            {"name": "API Melafix", "dosage": "5 ml per 10 gallons", "notes": "Mild antibacterial support"},
        ],
        "species_notes": {
            "betta": "Often unilateral from bumping into hard décor. Smooth out tank decorations. Usually resolves with clean water.",
            "goldfish": "Telescope/bubble-eye goldfish are especially vulnerable. Ensure no sharp objects in tank.",
        },
        "prevention": [
            "Use smooth decorations without sharp edges.",
            "Maintain excellent water quality.",
            "Avoid sudden movements near the tank that startle fish.",
        ],
    },

    # ── 9. Constipation / Bloating ──────────────────────────────────────
    "constipation": {
        "name": "Constipation / Bloating",
        "emoji": "🫃",
        "severity": "Mild → Moderate",
        "keywords": [
            "constipation", "bloated", "not pooping", "no feces",
            "swollen belly", "big belly", "fat belly",
            "bloating", "belly swollen", "distended abdomen",
            "overfed", "overfeeding",
        ],
        "description": (
            "Digestive blockage from overfeeding or low-fibre diet. "
            "The belly appears swollen but scales lie flat "
            "(unlike dropsy where scales protrude)."
        ),
        "causes": [
            "Overfeeding",
            "Feeding only dry foods that expand in the stomach",
            "Lack of dietary fibre",
            "Low temperature slowing metabolism",
        ],
        "treatment_steps": [
            "1. Fast the fish for 2–3 days.",
            "2. Feed a blanched, shelled pea (natural laxative).",
            "3. Add Epsom salt: 1 tsp per 5 gallons (mild laxative effect).",
            "4. Ensure temperature is within the ideal range (warmer = faster metabolism).",
            "5. Resume feeding with small portions of high-quality food.",
            "6. Add daphnia to the diet as a regular fibre source.",
        ],
        "medications": [
            {"name": "Blanched Pea", "dosage": "1 small pea, shell removed", "notes": "First-line treatment"},
            {"name": "Daphnia (live or frozen)", "dosage": "Small pinch", "notes": "Natural laxative and enrichment"},
            {"name": "Epsom Salt", "dosage": "1 tsp per 5 gallons", "notes": "Mild osmotic laxative"},
        ],
        "species_notes": {
            "betta": "Very common. Feed betta pellets sparingly (2–3 pellets, twice daily). Include one fasting day per week.",
            "goldfish": "Extremely common in fancy varieties. Switch from flakes to gel food.",
        },
        "prevention": [
            "Do not overfeed — fish stomachs are roughly the size of their eye.",
            "Include a fasting day once per week.",
            "Pre-soak dry food before feeding.",
            "Include fibre-rich foods (daphnia, blanched pea) weekly.",
        ],
    },

    # ── 10. Ammonia Poisoning ───────────────────────────────────────────
    "ammonia_poisoning": {
        "name": "Ammonia Poisoning / Burns",
        "emoji": "☣️",
        "severity": "Critical — can be lethal within hours",
        "keywords": [
            "ammonia poisoning", "ammonia burn", "ammonia spike",
            "red gills", "inflamed gills", "gasping at surface",
            "gasping for air", "heavy breathing", "rapid gill movement",
            "burns on body", "red streaks", "red patches on body",
            "ammonia stress", "new tank syndrome",
            "fish gasping", "labored breathing",
        ],
        "description": (
            "Direct chemical burns to gills and skin from elevated ammonia (NH₃/NH₄⁺). "
            "Common in new, uncycled tanks ('new tank syndrome'). "
            "Even 0.25 ppm can be harmful; above 1 ppm is often lethal."
        ),
        "causes": [
            "Uncycled tank (no established beneficial bacteria)",
            "Overstocking or overfeeding",
            "Filter failure or cleaning filter media with tap water",
            "Dead fish or plant matter decomposing",
        ],
        "treatment_steps": [
            "1. EMERGENCY: Perform an immediate 50 % water change with dechlorinated water.",
            "2. Add Seachem Prime (double dose) — it detoxifies ammonia for 24–48 hours.",
            "3. Test water — repeat 25 % water changes every 12 hours until ammonia reads 0.",
            "4. Add beneficial bacteria supplement (e.g., Seachem Stability, API Quick Start).",
            "5. Reduce feeding to once daily, small portions.",
            "6. Do NOT clean the filter during this period.",
            "7. Monitor for secondary infections (ammonia-burned tissue is vulnerable to fin rot and fungus).",
        ],
        "medications": [
            {"name": "Seachem Prime", "dosage": "Double dose: 2 drops per gallon", "notes": "Detoxifies ammonia, nitrite, and heavy metals"},
            {"name": "Seachem Stability", "dosage": "Follow package", "notes": "Live beneficial bacteria to accelerate cycling"},
            {"name": "API Quick Start", "dosage": "Follow package", "notes": "Alternative bacteria supplement"},
            {"name": "API Stress Coat", "dosage": "5 ml per 10 gallons", "notes": "Replaces slime coat damaged by burns"},
        ],
        "species_notes": {
            "betta": "Bettas can breathe atmospheric air but are still harmed by ammonia. Prime + water changes are critical.",
            "cherry_shrimp": "Shrimp are the first to die in an ammonia spike. Act immediately.",
            "neon_tetra": "Very sensitive to ammonia. May develop secondary infections quickly.",
        },
        "prevention": [
            "Fully cycle the tank before adding fish (4–6 weeks).",
            "Use Seachem Prime as your primary water conditioner.",
            "Never clean filter media with untreated tap water (use tank water).",
            "Avoid overstocking and overfeeding.",
        ],
    },

    # ── 11. Loss of Appetite / Lethargy ─────────────────────────────────
    "lethargy": {
        "name": "Loss of Appetite / Lethargy",
        "emoji": "😴",
        "severity": "Variable — symptom of many conditions",
        "keywords": [
            "not eating", "won't eat", "refuses food", "loss of appetite",
            "lethargic", "inactive", "sitting at bottom", "hiding",
            "not moving", "lying on bottom", "barely moving",
            "no energy", "listless", "sluggish",
            "clamped fins", "fins clamped",
        ],
        "description": (
            "Lethargy and appetite loss are non-specific symptoms that accompany "
            "many conditions — from simple stress to serious disease. The key is "
            "to check water parameters and look for other symptoms."
        ),
        "causes": [
            "Poor water quality (ammonia, nitrite, or nitrate spike)",
            "Temperature too low or too high",
            "Stress from new environment, aggressive tank mates, or bright lights",
            "Early stages of disease (ich, velvet, internal parasites)",
            "Overfeeding or constipation",
            "Old age",
        ],
        "treatment_steps": [
            "1. Test ALL water parameters immediately (ammonia, nitrite, nitrate, pH, temperature).",
            "2. If any parameters are off, perform a 25 % water change.",
            "3. Inspect the fish closely for other symptoms (spots, fin damage, bloating, color changes).",
            "4. Ensure temperature is within the species' ideal range.",
            "5. Try offering different foods (live or frozen bloodworms, daphnia).",
            "6. Reduce tank light and disturbances for 24–48 hours.",
            "7. If no improvement in 3 days, consider treating with API General Cure for internal parasites.",
        ],
        "medications": [
            {"name": "Seachem StressGuard", "dosage": "Follow package", "notes": "Reduces stress, protects slime coat"},
            {"name": "Indian Almond Leaves", "dosage": "1 leaf per 5 gallons", "notes": "Calming, mildly antibacterial"},
            {"name": "API General Cure", "dosage": "Follow package", "notes": "If internal parasites suspected"},
        ],
        "species_notes": {
            "betta": "Bettas can be picky eaters. Try soaking pellets in garlic guard. Clamped fins + lethargy often = water quality issue.",
            "neon_tetra": "Could indicate early Neon Tetra Disease — watch for color fading.",
        },
        "prevention": [
            "Maintain stable, clean water conditions.",
            "Provide hiding spots and low-stress environment.",
            "Keep compatible species only.",
            "Feed a varied diet.",
        ],
    },

    # ── 12. Loss of Color / Fading ──────────────────────────────────────
    "color_loss": {
        "name": "Loss of Color / Fading",
        "emoji": "🎨",
        "severity": "Mild → Moderate",
        "keywords": [
            "losing color", "fading color", "pale", "turning white",
            "color fading", "dull color", "lost color",
            "not colorful", "washed out", "color change",
            "turning grey", "turning pale", "losing pigment",
            "stress stripes",
        ],
        "description": (
            "Color fading can indicate stress, poor diet, disease, or simply "
            "natural aging. Sudden color loss warrants investigation."
        ),
        "causes": [
            "Stress (new tank, aggressive mates, poor water quality)",
            "Nutritional deficiency — diet lacking colour-enhancing foods",
            "Disease (velvet, columnaris, NTD in tetras)",
            "Low light levels (some fish fade without adequate light)",
            "Natural aging",
            "Marble gene (bettas — natural color changes over time)",
        ],
        "treatment_steps": [
            "1. Check and correct water parameters.",
            "2. Ensure the tank has appropriate lighting (8–10 hours/day).",
            "3. Feed colour-enhancing foods rich in carotenoids (brine shrimp, bloodworms, spirulina).",
            "4. Use a dark substrate and background — fish show better colours against dark surfaces.",
            "5. Rule out diseases by looking for other symptoms.",
            "6. Reduce stress: provide hiding spots, reduce flow, dim lights temporarily.",
        ],
        "medications": [
            {"name": "Colour-enhancing pellets", "dosage": "Part of regular diet", "notes": "Contains astaxanthin / spirulina"},
            {"name": "Seachem Garlic Guard", "dosage": "Soak food before feeding", "notes": "Appetite stimulant, immune booster"},
        ],
        "species_notes": {
            "betta": "Marble bettas naturally change colour throughout their life — this is normal. Stress stripes (horizontal lines) indicate stress.",
            "neon_tetra": "Colour fading + erratic swimming may indicate Neon Tetra Disease (no cure). Isolate affected fish.",
            "goldfish": "Goldfish naturally change from dark to orange/white as they mature. Diet affects intensity.",
        },
        "prevention": [
            "Feed a varied, colour-enhancing diet.",
            "Maintain optimal water quality.",
            "Use dark substrates to bring out natural colours.",
            "Minimise stress.",
        ],
    },
}


# ── Convenience: list of disease names for UI ────────────────────────────────
DISEASE_NAMES: List[str] = [d["name"] for d in DISEASE_DATABASE.values()]


# ── Quick-symptom buttons for the Diagnosis UI ──────────────────────────────
QUICK_SYMPTOMS: List[Dict[str, str]] = [
    {"label": "🩹 Fin rot / torn fins", "query": "My fish has fin rot and its fins are fraying and rotting"},
    {"label": "⚪ White spots", "query": "My fish has small white spots all over its body and fins"},
    {"label": "🫧 Floating sideways", "query": "My fish is floating sideways and can't swim straight, swim bladder issue"},
    {"label": "😴 Not eating", "query": "My fish is not eating, lethargic, sitting at the bottom, won't eat food"},
    {"label": "🔴 Swollen belly", "query": "My fish has a swollen bloated belly and scales sticking out"},
    {"label": "👁️ Bulging eye", "query": "My fish has a bulging swollen protruding eye, popeye"},
    {"label": "🧶 White fuzz", "query": "My fish has white cotton fuzzy growth on its body, fungus or columnaris"},
    {"label": "☣️ Gasping at surface", "query": "My fish is gasping at the surface, heavy breathing, red gills, ammonia"},
]
