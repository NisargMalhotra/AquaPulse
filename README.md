# 🌊 AquaPulse: Nano-Aquarium Nitrogen Cycle & Ecosystem Tracker

A production-ready desktop application built with Python that brings **data science and predictive analytics** to aquarium management. AquaPulse tracks water chemistry, visualizes the nitrogen cycle, predicts maintenance schedules, and provides **AI-powered fish health diagnoses**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 📊 Live Dashboard & Analytics
- **Nitrogen Cycle Visualization** — Real-time line plots tracking Ammonia (NH₃), Nitrite (NO₂⁻), and Nitrate (NO₃⁻) trends over time using Matplotlib & Seaborn.
- **Parameter Stability Graphs** — pH and Temperature rolling trends with safety band overlays.

### 🔮 Predictive Maintenance Engine
- **Toxicity Scoring** — Weighted algorithm (NH₃ 40%, NO₂⁻ 30%, NO₃⁻ 15%, pH 10%, Temp 5%) with Safe/Warning/Critical indicators.
- **Dilution Calculator** — Uses C₁V₁ = C_fV_f to compute exact water change percentages.
- **Days-Until-Change Countdown** — NumPy gradient calculates nitrate accumulation rate and forecasts when thresholds will be breached.
- **Ecosystem Stability** — 7-day and 14-day rolling standard deviations for pH and temperature.

### 🩺 AI-Powered Fish Health Diagnosis
- **Rule-Based Expert System** — NLP-powered symptom analysis against a curated knowledge base.
- **12 Common Diseases** — Fin Rot, Ich, Velvet, Swim Bladder, Dropsy, Columnaris, Fungal Infection, Popeye, Constipation, Ammonia Poisoning, Lethargy, and Color Loss.
- **10 Fish Species Profiles** — Betta, Goldfish, Neon Tetra, Guppy, Angelfish, Molly, Corydoras, Cherry Shrimp, Oscar, and Platy.
- **Species-Specific Treatment Plans** — Ranked diagnoses with actionable medication dosages and prevention tips.

### 🐟 Aquarium Profile
- Tank size configuration with litre ↔ gallon conversion.
- Species-specific ideal parameter ranges and tank size warnings.

### 📋 History & Data Management
- Searchable records table with **bulk select & delete**.
- **CSV Import/Export** for data portability.
- SQLite with WAL mode for high-performance reads/writes.
- **Parameterized queries** to prevent SQL injection.

---

## 🏗️ Architecture

Built with a strict **Model-View-Controller (MVC)** pattern:

```
AquaPulse/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── utils/
│   ├── constants.py                 # Thresholds, colors, validation ranges
│   └── fish_data.py                 # 10 species profiles + 12 disease knowledge base
├── models/
│   └── database.py                  # SQLite CRUD, CSV I/O, Pandas integration
├── controllers/
│   ├── analytics_engine.py          # Toxicity, dilution, predictions, stability
│   └── diagnosis_engine.py          # NLP rule-based expert system
├── views/
│   ├── app.py                       # Main window with sidebar navigation
│   ├── aquarium_view.py             # Tank profile setup
│   ├── log_data_view.py             # Validated data entry form
│   ├── dashboard_view.py            # Embedded Matplotlib/Seaborn charts
│   ├── predictive_view.py           # KPI cards and maintenance countdown
│   ├── diagnosis_view.py            # Chat-style diagnosis interface
│   └── history_view.py              # Treeview table with search & bulk ops
└── sample_data/                     # 4 CSV datasets for demo/testing
    ├── 01_healthy_cycled_tank.csv
    ├── 02_new_tank_cycling.csv
    ├── 03_neglected_tank_recovery.csv
    └── 04_ich_outbreak_treatment.csv
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/NisargMalhotra/AquaPulse.git
cd AquaPulse

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Sample Data
4 ready-to-import CSV datasets are included in `sample_data/`:

| File | Scenario | Highlights |
|------|----------|------------|
| `01_healthy_cycled_tank.csv` | Stable, well-maintained tank | Zero ammonia/nitrite, routine water changes |
| `02_new_tank_cycling.csv` | New Tank Syndrome | Classic NH₃ → NO₂⁻ → NO₃⁻ cycling curve |
| `03_neglected_tank_recovery.csv` | Post-vacation rescue | Nitrate at 45 ppm → recovered to 8 ppm |
| `04_ich_outbreak_treatment.csv` | Disease outbreak | Ich treatment with heat + medication protocol |

Import them via the **📋 History** tab → **📥 Import CSV** button.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | CustomTkinter | Modern dark-theme desktop GUI |
| **Backend** | SQLite3 (WAL mode) | Local relational data storage |
| **Analytics** | NumPy | Gradient calculations, statistical derivatives |
| **Data Processing** | Pandas | DataFrame operations, rolling statistics |
| **Visualization** | Matplotlib + Seaborn | Embedded analytical charts |

---

## 📈 Future Scope

- **IoT Integration** — Raspberry Pi / Arduino sensors for automated real-time parameter logging.
- **Mobile Companion** — Cross-platform mobile app for on-the-go monitoring.
- **Cloud Sync** — Migration from local SQLite to PostgreSQL/Firebase for multi-device access.

---

## 📄 License

This project is licensed under the MIT License.
