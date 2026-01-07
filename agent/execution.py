from typing import Dict, Any, List

from tools.base import BaseTool, ToolExecutionError


class ExecutionResult:
    def __init__(self) -> None:
        self.tools_called: List[str] = []
        self.tool_inputs: Dict[str, Any] = {}
        self.tool_outputs: Dict[str, Any] = {}
        self.errors: List[str] = []


class ExecutionEngine:
    def __init__(self, tools: Dict[str, BaseTool]) -> None:
        self.tools = tools

    def run_tool(self, tool_name: str, input_data: Dict[str, Any]) -> ExecutionResult:
        result = ExecutionResult()

        if tool_name not in self.tools:
            result.errors.append(f"tool not found: {tool_name}")
            return result

        tool = self.tools[tool_name]
        result.tools_called.append(tool_name)
        result.tool_inputs[tool_name] = input_data

        try:
            output = tool.run(input_data)
            result.tool_outputs[tool_name] = output
        except ToolExecutionError as exc:
            result.errors.append(str(exc))

        return result
