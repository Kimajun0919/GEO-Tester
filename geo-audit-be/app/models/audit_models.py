from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class AuditRequest(BaseModel):
    url: HttpUrl
    multi_page: bool = Field(default=False, description="Enable multi-page scanning")
    max_pages: int = Field(default=3, ge=1, le=20, description="Maximum pages to crawl")


class AuditChecks(BaseModel):
    title: bool
    meta_description: bool
    og_title: bool
    og_description: bool
    og_image: bool
    canonical: bool
    h1_present: bool
    multiple_h1: bool
    hierarchy_valid: bool
    faq_detected: bool
    llms_txt: bool
    ai_txt: bool
    robots_txt: bool
    sitemap_xml: bool
    company_name_detected: bool
    service_name_detected: bool
    location_detected: bool
    contact_info_detected: bool


class AuditResponse(BaseModel):
    url: HttpUrl
    geo_score: int = Field(ge=0, le=100)
    checks: Dict[str, bool]
    structured_data: List[str]
    recommendations: List[str]
    details: Optional[Dict[str, Any]] = None
