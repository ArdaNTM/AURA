"""Calculator tool implementation."""

from __future__ import annotations

import ast
import operator
from typing import Any

from aura.core.tools import Tool


class CalculatorTool(Tool):
    """Evaluate basic mathematical expressions."""

    OPERATORS: dict[type[Any], Any] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    @property
    def name(self) -> str:
        """Return the tool name."""

        return "calculator"

    @property
    def description(self) -> str:
        """Return the tool description."""

        return "Evaluate basic mathematical expressions."

    @property
    def parameters(self) -> dict[str, Any]:
        """Return parameter schema."""

        return {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to evaluate.",
            }
        }

    def execute(
        self,
        expression: str,
    ) -> str:
        """Evaluate an arithmetic expression."""

        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )

            result = self._evaluate(
                tree.body,
            )

            return str(result)

        except Exception as exc:
            raise ValueError(f"Invalid expression: {expression!r}") from exc

    def _evaluate(
        self,
        node: ast.AST,
    ) -> Any:
        """Safely evaluate AST nodes."""

        if isinstance(
            node,
            ast.Constant,
        ):
            if isinstance(
                node.value,
                (int, float),
            ):
                return node.value

        if isinstance(
            node,
            ast.BinOp,
        ):
            operator_func = self.OPERATORS.get(
                type(node.op),
            )

            if operator_func is None:
                raise ValueError("Unsupported operator.")

            return operator_func(
                self._evaluate(
                    node.left,
                ),
                self._evaluate(
                    node.right,
                ),
            )

        if isinstance(
            node,
            ast.UnaryOp,
        ):
            operator_func = self.OPERATORS.get(
                type(node.op),
            )

            if operator_func is None:
                raise ValueError("Unsupported unary operator.")

            return operator_func(
                self._evaluate(
                    node.operand,
                ),
            )

        raise ValueError("Unsupported expression.")
