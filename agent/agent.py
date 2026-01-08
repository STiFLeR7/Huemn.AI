from typing import Dict, Any

from agent.planner import Planner
from agent.execution import ExecutionEngine, ExecutionResult


class Agent:
    def __init__(self, execution_engine: ExecutionEngine) -> None:
        self.planner = Planner()
        self.execution_engine = execution_engine

    def run(self, task: str) -> Dict[str, Any]:
        plan = self.planner.create_plan(task)

        execution_result = None
        final_output = None

        if plan.use_tool:
            execution_result = self.execution_engine.run_tool(
                plan.tool_name,
                plan.tool_input
            )

            if execution_result.tool_outputs:
                # Aggregate all tool outputs into a list to preserve all values
                final_output = list(execution_result.tool_outputs.values())
            else:
                final_output = "tool failed"
        else:
            final_output = task

        return {
            "task": task,
            "plan": {
                "use_tool": plan.use_tool,
                "tool_name": plan.tool_name
            },
            "execution": execution_result,
            "output": final_output
        }
