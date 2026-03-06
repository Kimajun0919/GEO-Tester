from __future__ import annotations

import re
from typing import Any, Dict, List


class GeoScorer:
    WEIGHTS = {
        "files": 20,
        "meta": 20,
        "heading": 15,
        "schema": 20,
        "faq": 10,
        "entity": 15,
    }

    FAQ_PATTERN = re.compile(r"\b(what|how|why|can|should)\b", re.IGNORECASE)

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        file_checks = context.get("file_checks", {})
        meta_checks = context.get("meta_checks", {})
        heading_checks = context.get("heading_checks", {})
        structured_data: List[str] = context.get("structured_data", [])
        entity_checks = context.get("entity_checks", {})
        faq_detected = self._detect_faq(context)

        files_score = self._ratio_score(file_checks, self.WEIGHTS["files"])
        meta_score = self._ratio_score(meta_checks, self.WEIGHTS["meta"])

        heading_parts = {
            "h1_present": heading_checks.get("h1_present", False),
            "hierarchy_valid": heading_checks.get("hierarchy_valid", False),
            "single_h1": not heading_checks.get("multiple_h1", False),
        }
        heading_score = self._ratio_score(heading_parts, self.WEIGHTS["heading"])

        schema_score = min(len(structured_data), 2) / 2 * self.WEIGHTS["schema"]
        faq_score = self.WEIGHTS["faq"] if faq_detected else 0
        entity_score = self._ratio_score(entity_checks, self.WEIGHTS["entity"])

        total = round(files_score + meta_score + heading_score + schema_score + faq_score + entity_score)

        checks = {
            **meta_checks,
            **heading_checks,
            "faq_detected": faq_detected,
            **file_checks,
            **entity_checks,
        }

        return {
            "geo_score": max(0, min(100, total)),
            "faq_detected": faq_detected,
            "checks": checks,
            "score_breakdown": {
                "files": round(files_score, 2),
                "meta": round(meta_score, 2),
                "heading": round(heading_score, 2),
                "schema": round(schema_score, 2),
                "faq": faq_score,
                "entity": round(entity_score, 2),
            },
        }

    def _ratio_score(self, checks: Dict[str, Any], weight: int) -> float:
        if not checks:
            return 0
        passed = sum(1 for val in checks.values() if bool(val))
        return (passed / len(checks)) * weight

    def _detect_faq(self, context: Dict[str, Any]) -> bool:
        soup = context.get("soup")
        text = soup.get_text(" ", strip=True).lower() if soup else ""

        if len(self.FAQ_PATTERN.findall(text)) >= 3:
            return True

        if soup:
            faq_containers = soup.select(
                "section.faq, div.faq, [id*='faq'], [class*='faq'], details, summary"
            )
            if faq_containers:
                return True

        return False
