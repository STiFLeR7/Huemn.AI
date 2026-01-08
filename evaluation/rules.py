def is_tool_required(task: str) -> bool:
    text = task.lower()
    if "ai" in text or "information" in text or "about" in text:
        return True
    return False

def is_premature_output(plan_used_tool: bool, execution_result) -> bool:
    if plan_used_tool and execution_result is None:
        return True
    return False
