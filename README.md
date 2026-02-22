# Kaitse

Kaitse is a modular football analytics platform focused on structured
data ingestion, normalization, storage, and visualization.

The project is built as a monorepo and designed for scalability from the
beginning.

------------------------------------------------------------------------

## 🏗 Architecture Overview

Kaitse is divided into three main modules:

Kaitse/ │ ├── kaitse-web/ \# Next.js frontend (App Router + TypeScript)
├── kaitse-batch/ \# Python ingestion & ETL jobs └── shared/ \# Shared
utilities (future cross-module logic)

### 1. Frontend (`kaitse-web`)

-   Next.js (App Router)
-   TypeScript
-   Server Components
-   SEO-ready dynamic routes (e.g. `/players/[slug]`)
-   Supabase client integration

### 2. Batch / Ingestion (`kaitse-batch`)

-   Python
-   Transfermarkt scraping
-   Structured logging
-   Idempotent UPSERT logic
-   Supabase integration

### 3. Database

-   Supabase (PostgreSQL)
-   Structured relational schema
-   Versioned competitions & seasons
-   Designed for extensibility (players, stats, analytics)

------------------------------------------------------------------------

## 🗄 Database Model (Core Tables)

-   competitions
-   teams
-   seasons
-   competition_seasons
-   competition_season_teams

All ingestion operations are designed to be idempotent using proper
UNIQUE constraints and UPSERT.

------------------------------------------------------------------------

## 🚀 Getting Started

### 1️⃣ Clone Repository

git clone https://github.com/Markof87/kaitse.git cd kaitse

------------------------------------------------------------------------

# 🌐 Frontend Setup (Next.js)

cd kaitse-web npm install npm run dev

Application runs at:

http://localhost:3000

### Required Environment Variables

Create `.env.local` inside `kaitse-web/`:

NEXT_PUBLIC_SUPABASE_URL= NEXT_PUBLIC_SUPABASE_ANON_KEY=

------------------------------------------------------------------------

# 🧪 Batch Setup (Python)

cd kaitse-batch python -m venv .venv

Activate environment:

Windows: .venv`\Scripts`{=tex}`\activate`{=tex}

macOS / Linux: source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

### Required Environment Variables

Create `.env` inside `kaitse-batch/`:

SUPABASE_URL= SUPABASE_SERVICE_ROLE_KEY=

------------------------------------------------------------------------

# ▶ Running the Ingestion

From inside `kaitse-batch`:

python -m ingestion.teams

This will: - Scrape Transfermarkt competition data - Upsert
competitions - Upsert teams - Link teams to competition seasons

------------------------------------------------------------------------

# 🛡 Design Principles

-   Idempotent ingestion
-   Clear separation of concerns
-   Server-side rendering for SEO
-   Storage abstraction (image_path, not hardcoded URLs)
-   Clean relational modeling (season-aware data)

------------------------------------------------------------------------

# 📦 Tech Stack

Frontend: - Next.js (App Router) - TypeScript - Supabase JS Client

Backend / Batch: - Python - httpx - BeautifulSoup - Supabase Python
Client

Database: - PostgreSQL (Supabase)

------------------------------------------------------------------------

# 📈 Roadmap

-   Player ingestion
-   Squad rosters per season
-   Player profile pages
-   Advanced metrics layer
-   Analytics microservices
-   Automated scheduled batch execution
-   Dashboard UI improvements

------------------------------------------------------------------------

# 🔒 Security Notes

-   Service Role keys are used only in batch processes.
-   Frontend uses only public anon keys.
-   Environment files are excluded from version control.

------------------------------------------------------------------------

# 📜 License

Private project. Not licensed for redistribution.
