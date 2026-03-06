from __future__ import annotations

from typing import Dict, List


def generate_recommendations(result: Dict) -> List[str]:
    checks = result.get("checks", {})
    structured_data = result.get("structured_data", [])
    recommendations: List[str] = []

    if not checks.get("llms_txt"):
        recommendations.append("Add llms.txt to the root directory to guide AI crawlers.")
    if not checks.get("ai_txt"):
        recommendations.append("Consider adding ai.txt to declare AI usage and crawling preferences.")
    if not checks.get("meta_description"):
        recommendations.append("Add a concise meta description for better snippet generation.")
    if not checks.get("og_title") or not checks.get("og_description"):
        recommendations.append("Add Open Graph title and description tags for richer context extraction.")
    if not checks.get("canonical"):
        recommendations.append("Add a canonical URL tag to avoid duplicate-content ambiguity.")
    if checks.get("multiple_h1"):
        recommendations.append("Use a single primary H1 to clarify main page intent.")
    if not checks.get("faq_detected"):
        recommendations.append("Add a FAQ section with 3–5 Q&A items.")
    if "FAQPage" not in structured_data:
        recommendations.append("Add FAQPage schema for question-answer content.")
    if not structured_data:
        recommendations.append("Add Organization or WebSite structured data.")
    if not checks.get("contact_info_detected"):
        recommendations.append("Include clear contact information (email and/or phone) for trust signals.")

    return recommendations
