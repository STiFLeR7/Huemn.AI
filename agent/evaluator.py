from typing import Dict, Any, List

from evaluation.taxonomy import MistakeType
from evaluation import rules


class EvaluationResult:
    def __init__(self) -> None:
        self.mistakes: List[MistakeType] = []


class Evaluator:
    def evaluate(self, run_result: Dict[str, Any]) -> EvaluationResult:
        result = EvaluationResult()

        task = run_result.get("task")
        plan = run_result.get("plan")
        execution = run_result.get("execution")
        output = run_result.get("output")

        tool_required = rules.is_tool_required(task)

        if tool_required and plan and not plan.get("use_tool"):
            result.mistakes.append(MistakeType.REQUIRED_TOOL_NOT_USED)

        if plan and plan.get("use_tool") and execution is None:
            result.mistakes.append(MistakeType.PREMATURE_FINAL_OUTPUT)

        if execution:
            if execution.errors:
                result.mistakes.append(MistakeType.TOOL_EXECUTION_FAILED)
            
            if execution.tool_outputs and output == task:
                result.mistakes.append(MistakeType.TOOL_OUTPUT_IGNORED)

        return result
