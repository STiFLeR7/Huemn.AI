from typing import List, Dict


class AdaptationResult:
    def __init__(self) -> None:
        self.rules: List[str] = []


class Adapter:
    def adapt(self, patterns: List[Dict[str, str]]) -> AdaptationResult:
        result = AdaptationResult()

        for item in patterns:
            mistake = item.get("mistake")

            if mistake == "REQUIRED_TOOL_NOT_USED":
                result.rules.append("force_tool_usage")

            if mistake == "PREMATURE_FINAL_OUTPUT":
                result.rules.append("block_early_output")

        return result
