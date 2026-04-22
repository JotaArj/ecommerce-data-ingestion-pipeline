# E-commerce Data Ingestion Pipeline

A modular scraping engine built with Python and Playwright, designed to extract, normalize, and persist e-commerce data from multiple sources.

## Overview

This project demonstrates a production-oriented scraping architecture:

- Multi-source scraping engine (extensible)
- Playwright-based browser automation
- Structured data extraction (categories, products, pricing)
- SQLite persistence with historical snapshots
- Clean separation of concerns (domain, infrastructure, scraping, services)

## Architecture

The project is structured into several layers:

- `domain`: core business models and enums
- `core`: configuration, constants, logging
- `infra`: database and browser interaction
- `scraper`: scraping logic (base + source-specific)
- `services`: orchestration layer
- `app`: entry point

## Data Source

Initial implementation targets:

- Oxylabs Sandbox (scraping-friendly environment)

Future sources can be added via the `scraper/sources` module.

## Tech Stack

- Python 3.11+
- Playwright
- SQLite
- Pytest

## Installation

```bash
pip install -r requirements.txt
playwright install
```

## Run

```bash
python -m scraper_engine.app.main
```

## Testing

```bash
pytest
```

## Notes

- This project is intended for educational and portfolio purposes.
- Target websites used are scraping-friendly sandbox environments.
