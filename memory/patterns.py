from typing import List, Dict, Any


class PatternDetector:
    def find_repeated(self, records: List[Dict[str, Any]], threshold: int = 2) -> List[Dict[str, Any]]:
        repeated = []

        for record in records:
            if record.get("count", 0) >= threshold:
                repeated.append(record)

        return repeated
