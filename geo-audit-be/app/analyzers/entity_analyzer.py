from __future__ import annotations

import re
from typing import Any, Dict


class EntityAnalyzer:
    PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{7,}\d")
    EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    LOCATION_RE = re.compile(
        r"\b(?:street|st\.|road|rd\.|avenue|ave\.|boulevard|blvd\.|city|state|country|zip)\b",
        re.IGNORECASE,
    )
    SERVICE_RE = re.compile(
        r"\b(?:services?|solutions?|consulting|platform|software|agency|product)\b",
        re.IGNORECASE,
    )

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        soup = context.get("soup")
        text = soup.get_text(" ", strip=True) if soup else ""

        company_name_detected = bool(context.get("meta", {}).get("og_title") or context.get("meta", {}).get("title"))
        service_name_detected = bool(self.SERVICE_RE.search(text))
        location_detected = bool(self.LOCATION_RE.search(text))
        contact_info_detected = bool(self.PHONE_RE.search(text) or self.EMAIL_RE.search(text))

        return {
            "entity_checks": {
                "company_name_detected": company_name_detected,
                "service_name_detected": service_name_detected,
                "location_detected": location_detected,
                "contact_info_detected": contact_info_detected,
            }
        }
