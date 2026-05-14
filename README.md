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
- `config`: settings and constants
- `db`: SQLite schema and repositories
- `browser`: Playwright session management
- `sources`: source-specific discovery and parsing
- `app`: entry point

## Data Source

Initial implementation targets:

- Oxylabs Sandbox (scraping-friendly environment)

Future sources can be added via the `ecommerce_ingestion.sources` package.

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
python -m ecommerce_ingestion.app.main
```

## Testing

```bash
pytest
```

## Notes

- This project is intended for educational and portfolio purposes.
- Target websites used are scraping-friendly sandbox environments.
