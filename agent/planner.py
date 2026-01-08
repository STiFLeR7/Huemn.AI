from typing import Any, Dict, List


class Plan:
    def __init__(self) -> None:
        self.use_tool = False
        self.tool_name = None
        self.tool_input = {}


class Planner:
    def __init__(self) -> None:
        self.force_tool_usage = False

    def apply_rules(self, rules: List[str]) -> None:
        self.force_tool_usage = "force_tool_usage" in rules

    def create_plan(self, task: str) -> Plan:
        plan = Plan()
        text = task.lower()

        if self.force_tool_usage:
            plan.use_tool = True
            plan.tool_name = "search_tool"
            plan.tool_input = {
                "query": task
            }
            return plan

        if "search" in text or "find" in text:
            plan.use_tool = True
            plan.tool_name = "search_tool"
            plan.tool_input = {
                "query": task
            }
        else:
            plan.use_tool = False

        return plan
