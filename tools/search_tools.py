from typing import Dict, Any

from tools.base import BaseTool, ToolValidationError


class SearchTool(BaseTool):
    @property
    def name(self) -> str:
        return "search_tool"

    def validate_input(self, input_data: Dict[str, Any]) -> None:
        if "query" not in input_data:
            raise ToolValidationError("missing query")
        if not isinstance(input_data["query"], str):
            raise ToolValidationError("query must be string")
        if input_data["query" == ""]:
            raise ToolValidationError("query is empty")

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data["query"].lower()

        data = {
            "ai": "Artificial intelligence is about making machines do smart things",
            "agent": "An agent can take actions using tools",
            "tool": "A tool is used to perform a specific task",
        }

        results = []
        for key, value in data.items():
            if key in query:
                results.append(value)

        if len(results) == 0:
            results.append("no results found")

        return {
            "query": input_data["query"],
            "results": results
        }

    def validate_output(self, output_data: Dict[str, Any]) -> None:
        if "results" not in output_data:
            raise ToolValidationError("missing results")
        if not isinstance(output_data["results"], list):
            raise ToolValidationError("results must be list")
