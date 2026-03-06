from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.analyzers.entity_analyzer import EntityAnalyzer
from app.analyzers.geo_score import GeoScorer
from app.analyzers.heading_analyzer import HeadingAnalyzer
from app.analyzers.meta_analyzer import MetaAnalyzer
from app.analyzers.schema_analyzer import SchemaAnalyzer
from app.crawler.crawler import check_root_files, crawl_pages
from app.models.audit_models import AuditRequest, AuditResponse
from app.parser.html_parser import extract_headings, extract_json_ld, extract_meta, parse_html
from app.recommendations.generator import generate_recommendations

router = APIRouter()


@router.post("/audit", response_model=AuditResponse)
async def audit_website(payload: AuditRequest) -> AuditResponse:
    try:
        pages = await crawl_pages(str(payload.url), payload.multi_page, payload.max_pages)
    except Exception as exc:  # pragma: no cover - runtime/network dependent
        raise HTTPException(status_code=502, detail=f"Failed to crawl website: {exc}") from exc

    if not pages:
        raise HTTPException(status_code=400, detail="No pages were crawled")

    homepage = pages[0]
    soup = parse_html(homepage.html)
    context: Dict[str, Any] = {
        "url": str(payload.url),
        "soup": soup,
        "meta": extract_meta(soup),
        "headings": extract_headings(soup),
        "json_ld": extract_json_ld(soup),
    }

    context["file_checks"] = await check_root_files(str(payload.url))

    analyzers = [MetaAnalyzer(), HeadingAnalyzer(), SchemaAnalyzer(), EntityAnalyzer()]
    for analyzer in analyzers:
        context.update(analyzer.analyze(context))

    score_result = GeoScorer().analyze(context)
    context.update(score_result)

    response_payload = {
        "url": str(payload.url),
        "geo_score": context["geo_score"],
        "checks": context["checks"],
        "structured_data": context.get("structured_data", []),
        "recommendations": generate_recommendations(context),
        "details": {
            "score_breakdown": context.get("score_breakdown", {}),
            "pages_crawled": [p.url for p in pages],
        },
    }

    return AuditResponse(**response_payload)
