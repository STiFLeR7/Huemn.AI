import logging
import sys
from tools.search_tools import SearchTool
from agent.execution import ExecutionEngine
from agent.agent import Agent
from agent.evaluator import Evaluator
from memory.error_memory import ErrorMemory
from memory.patterns import PatternDetector
from agent.adaptation import Adapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
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

        # Step 1: Run agent with error handling
        run_result = None
        try:
            run_result = agent.run(task)
        except Exception as e:
            logger.exception(f"Error running agent: {e}")
            return 1

        # Step 2: Evaluate with error handling
        evaluation = None
        try:
            evaluation = evaluator.evaluate(run_result)
        except Exception as e:
            logger.exception(f"Error evaluating run: {e}")
            evaluation = None

        # Step 3: Add mistakes to memory with error handling
        if evaluation:
            try:
                for mistake in evaluation.mistakes:
                    memory.add(task, mistake)
            except Exception as e:
                logger.exception(f"Error adding mistakes to memory: {e}")

        # Step 4: Find patterns with error handling
        patterns = []
        try:
            patterns = pattern_detector.find_repeated(memory.all())
        except Exception as e:
            logger.exception(f"Error finding patterns: {e}")

        # Step 5: Adapt with error handling
        adaptation = None
        try:
            adaptation = adapter.adapt(patterns)
        except Exception as e:
            logger.exception(f"Error adapting patterns: {e}")

        # Print results with safe access
        print("TASK:", task)
        print("OUTPUT:", run_result.get("output") if run_result else "N/A")
        print("MISTAKES:", evaluation.mistakes if evaluation else [])
        print("MEMORY:", memory.all() if memory else [])
        print("ADAPTATION RULES:", adaptation.rules if adaptation and hasattr(adaptation, 'rules') else [])
        
        return 0
        
    except Exception as e:
        logger.exception(f"Fatal error in main: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
