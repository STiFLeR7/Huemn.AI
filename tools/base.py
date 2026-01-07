"""
Base Tool Contract for Huemn.AI

This module defines the abstract interface that all tools must implement.

Design goals:
- Deterministic behavior
- Explicit input/output contracts
- No silent failures
- Full observability

Tools are deliberately simple. They are not agents.
They do not reason. They execute.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class ToolExecutionError(Exception):
    """Raised when a tool fails during execution."""


class ToolValidationError(Exception):
    """Raised when tool input or output validation fails."""


class BaseTool(ABC):
    """
    Abstract base class for all tools.

    Every tool must:
    - Declare a unique name
    - Validate inputs
    - Execute deterministically
    - Return structured output
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique, stable identifier for the tool.
        Used for logging, evaluation, and memory.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        Validate tool input.

        Raises:
            ToolValidationError: if input is invalid
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool.

        Rules:
        - Must be deterministic
        - Must not mutate input
        - Must raise ToolExecutionError on failure
        """
        raise NotImplementedError

    @abstractmethod
    def validate_output(self, output_data: Dict[str, Any]) -> None:
        """
        Validate tool output.

        Raises:
            ToolValidationError: if output is invalid
        """
        raise NotImplementedError

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full tool execution lifecycle.

        This method enforces:
        - Input validation
        - Execution
        - Output validation
        """
        self.validate_input(input_data)

        try:
            output = self.execute(input_data)
        except Exception as exc:
            raise ToolExecutionError(
                f"Tool '{self.name}' failed during execution: {exc}"
            ) from exc

        self.validate_output(output)
        return output
