# GEO Audit Backend

Modular FastAPI backend for GEO (Generative Engine Optimization) audits.

## Run

```bash
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload
```

From project directory `geo-audit-be`.

## Endpoint

### `POST /audit`

Request:

```json
{
  "url": "https://example.com",
  "multi_page": false,
  "max_pages": 3
}
```

Response includes:
- GEO score (0-100)
- checks map
- detected structured data
- recommendations
- score breakdown

## Architecture

Pipeline:

`URL -> crawler -> HTML -> parser -> analyzers -> geo score -> recommendations -> response`

Analyzers are independent modules and can be extended with future modules such as:
- `seo_analyzer`
- `accessibility_analyzer`
- `performance_analyzer`
- `qa_analyzer`
