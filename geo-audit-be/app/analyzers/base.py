from __future__ import annotations

from typing import Any, Dict, Protocol


class Analyzer(Protocol):
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ...
