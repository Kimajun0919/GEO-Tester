from __future__ import annotations

from typing import Any, Dict, List


class HeadingAnalyzer:
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        headings: Dict[str, List[str]] = context.get("headings", {})
        h1 = headings.get("h1", [])
        h2 = headings.get("h2", [])

        hierarchy_valid = bool(h1) and (bool(h2) or len(h1) == 1)

        checks = {
            "h1_present": len(h1) > 0,
            "multiple_h1": len(h1) > 1,
            "hierarchy_valid": hierarchy_valid,
        }

        return {"heading_checks": checks, "headings": headings}
