# 📍 Samplead Inspector

Samplead Inspector is a **location-based prospect qualification engine** designed to match prospects with users based on geographic preferences.  
It processes raw JSON/CSV input files, applies matching rules (country, state, region), and stores the results asynchronously in a PostgreSQL database running inside Docker.

The system is lightweight, fast, and built for clear separation between configuration, logic, and infrastructure.

## ✨ Features

- 🔍 Location-based qualification (country → region mapping)  
- ⚡ Fast asynchronous processing using `asyncpg`  
- 🗄️ Fully containerized PostgreSQL setup (Docker)  
- 📁 Clean configuration structure (environment-driven)  
- ✔️ Pydantic models for validation  
- 🧪 Simple testing-ready architecture  

## 🚀 Getting Started

### 1. Ensure Docker Engine is running
You must have Docker installed and active.

### 2. Build the PostgreSQL Docker image
```bash
docker build -t inspector-postgres .
```

### 3. Run the container
```bash
docker run --name postgres inspector-postgres
```

Your database is now ready to accept connections.

## 📦 Installation (Python)

Install all dependencies using **uv**:

```bash
uv sync
```

This will automatically create a virtual environment and install everything from `pyproject.toml`.

## ⚙️ Configuration

The application uses default values but all can be overridden via **environment variables**.

| Environment Variable | Default Value |
|----------------------|---------------|
| `postgres_dsn` | `postgresql://app_user:app_password@localhost:5432/app_db` |
| `prospects_path` | `./raw_data/prospects.csv` |
| `country_to_region_mapping_path` | `./raw_data/country-to-regions-mapping.json` |
| `user_locations_settings_path` | `./raw_data/users-locations-settings.json` |

You may adjust paths or DB credentials according to your setup.

## ▶️ Run the Application

Simply run:

```bash
python main.py
```

The inspector will:

1. Load raw data  
2. Match prospects to users based on location settings  
3. Produce `InspectedProspect` objects  
4. Write the results to PostgresSQL

## 📘 Notes

- The project is designed for **local execution**, with Docker only powering the PostgreSQL backend.
- The matching logic can easily be extended to more geographic types (city, zipcode, etc.).
- All models use Pydantic to guarantee type safety and predictable data shapes.
