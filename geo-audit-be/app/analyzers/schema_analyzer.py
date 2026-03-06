from __future__ import annotations

from typing import Any, Dict, List, Set

TARGET_TYPES = {"Organization", "WebSite", "Article", "FAQPage", "BreadcrumbList"}


class SchemaAnalyzer:
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        json_ld: List[Dict[str, Any]] = context.get("json_ld", [])
        types: Set[str] = set()

        for item in json_ld:
            extracted = self._extract_types(item)
            types.update(t for t in extracted if t in TARGET_TYPES)

        return {"structured_data": sorted(types)}

    def _extract_types(self, obj: Dict[str, Any]) -> List[str]:
        raw_type = obj.get("@type")
        values: List[str] = []

        if isinstance(raw_type, str):
            values.append(raw_type)
        elif isinstance(raw_type, list):
            values.extend([item for item in raw_type if isinstance(item, str)])

        graph = obj.get("@graph")
        if isinstance(graph, list):
            for node in graph:
                if isinstance(node, dict):
                    values.extend(self._extract_types(node))

        return values
