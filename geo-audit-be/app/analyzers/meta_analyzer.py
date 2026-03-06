from __future__ import annotations

from typing import Any, Dict


class MetaAnalyzer:
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        meta = context.get("meta", {})
        checks = {
            "title": bool(meta.get("title")),
            "meta_description": bool(meta.get("meta_description")),
            "og_title": bool(meta.get("og_title")),
            "og_description": bool(meta.get("og_description")),
            "og_image": bool(meta.get("og_image")),
            "canonical": bool(meta.get("canonical")),
        }
        return {"meta": meta, "meta_checks": checks}
