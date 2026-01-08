import logging
from tools.search_tools import SearchTool
from agent.execution import ExecutionEngine
from agent.agent import Agent
from agent.evaluator import Evaluator
from memory.error_memory import ErrorMemory
from memory.patterns import PatternDetector
from agent.adaptation import Adapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def simulate():
    tools = {
        "search_tool": SearchTool()
    }

    execution_engine = ExecutionEngine(tools)
    agent = Agent(execution_engine)
    evaluator = Evaluator()
    memory = ErrorMemory()
    pattern_detector = PatternDetector()
    adapter = Adapter()

    task = "tell me about ai"
    
    failures = 0

    for i in range(1, 6):
        print("\nRUN", i)
        
        try:
            # Ensure agent has planner attribute
            if not hasattr(agent, "planner"):
                logger.error("Agent does not have a planner attribute")
                failures += 1
                continue
            
            if not callable(getattr(agent.planner, "apply_rules", None)):
                logger.error("Agent planner does not have apply_rules method")
                failures += 1
                continue

            run_result = agent.run(task)
            
            # Validate run_result before use
            if run_result is None:
                logger.error("agent.run() returned None")
                print("OUTPUT: Error - no result")
                failures += 1
                continue
            
            if not isinstance(run_result, dict):
                logger.error(f"agent.run() returned non-dict type: {type(run_result)}")
                print("OUTPUT:", run_result)
                failures += 1
                continue

            evaluation = evaluator.evaluate(run_result)

            for mistake in evaluation.mistakes:
                memory.add(task, mistake)

            patterns = pattern_detector.find_repeated(memory.all())

            adaptation = adapter.adapt(patterns)
            
            # Guard adaptation.rules access
            if adaptation and hasattr(adaptation, 'rules') and adaptation.rules:
                agent.planner.apply_rules(adaptation.rules)

            # Safe output access
            output = run_result.get("output") if isinstance(run_result, dict) else str(run_result)
            print("OUTPUT:", output)
            print("MISTAKES:", evaluation.mistakes)
            print("MEMORY:", memory.all())
            print("ADAPTATION RULES:", adaptation.rules if adaptation and hasattr(adaptation, 'rules') else [])
            
        except Exception as e:
            logger.exception(f"Error in run {i} for task '{task}': {e}")
            failures += 1
            print(f"RUN {i} FAILED: {str(e)}")
            continue
    
    print(f"\n\nSimulation complete. Failures: {failures}/5")


if __name__ == "__main__":
    simulate()
