"""
Tool Registry and Coordinator

Central registry and coordinator for medical tools.
Manages tool registration, discovery, and coordinated execution.
"""

from typing import Dict, List, Any, Optional, Type
from .medical_tools import MedicalTool, ToolResult
import inspect


class ToolRegistry:
    """
    Central registry for medical tools.

    Manages tool registration, discovery, and metadata.
    """

    def __init__(self):
        self._tools: Dict[str, Type[MedicalTool]] = {}
        self._tool_instances: Dict[str, MedicalTool] = {}

    def register_tool(self, tool_class: Type[MedicalTool]) -> None:
        """
        Register a medical tool class.

        Args:
            tool_class: MedicalTool subclass to register
        """
        # Create instance to get metadata
        instance = tool_class()

        # Register by name
        self._tools[instance.name] = tool_class
        self._tool_instances[instance.name] = instance

    def register_tools(self, tool_classes: List[Type[MedicalTool]]) -> None:
        """
        Register multiple medical tool classes.

        Args:
            tool_classes: List of MedicalTool subclasses to register
        """
        for tool_class in tool_classes:
            self.register_tool(tool_class)

    def get_tool(self, tool_name: str) -> Optional[MedicalTool]:
        """
        Get tool instance by name.

        Args:
            tool_name: Name of tool to retrieve

        Returns:
            Tool instance or None if not found
        """
        return self._tool_instances.get(tool_name)

    def list_tools(self) -> List[str]:
        """Get list of registered tool names."""
        return list(self._tools.keys())

    def get_tool_schemas(self) -> Dict[str, Dict]:
        """Get parameter schemas for all registered tools."""
        schemas = {}

        for tool_name, tool_instance in self._tool_instances.items():
            schemas[tool_name] = {
                "name": tool_name,
                "description": tool_instance.description,
                "parameters": tool_instance.get_parameters_schema()
            }

        return schemas

    def find_tools_by_capability(self, capability: str) -> List[str]:
        """
        Find tools that provide a specific capability.

        Args:
            capability: Capability to search for

        Returns:
            List of tool names
        """
        matching_tools = []

        for tool_name, tool_instance in self._tool_instances.items():
            if capability.lower() in tool_instance.description.lower():
                matching_tools.append(tool_name)

        return matching_tools


class ToolCoordinator:
    """
    Coordinate tool execution for medical consultations.

    Manages:
    - Tool selection based on requirements
    - Parallel execution where possible
    - Result aggregation
    - Error handling and fallback
    """

    def __init__(self, registry: Optional[ToolRegistry] = None):
        self.registry = registry or ToolRegistry()

    def execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Execute a single tool.

        Args:
            tool_name: Name of tool to execute
            **kwargs: Parameters for tool execution

        Returns:
            ToolResult from execution
        """
        tool = self.registry.get_tool(tool_name)

        if tool is None:
            return ToolResult(
                success=False,
                data={},
                confidence=0.0,
                metadata={},
                error_message=f"Tool '{tool_name}' not found in registry"
            )

        return tool.execute(**kwargs)

    def execute_tools(self, tool_configs: List[Dict[str, Any]]) -> List[ToolResult]:
        """
        Execute multiple tools in sequence.

        Args:
            tool_configs: List of dicts with 'tool_name' and parameters

        Returns:
            List of ToolResults
        """
        results = []

        for config in tool_configs:
            tool_name = config.pop("tool_name")
            result = self.execute_tool(tool_name, **config)
            results.append(result)

        return results

    def execute_tools_parallel(self, tool_configs: List[Dict[str, Any]]) -> Dict[str, ToolResult]:
        """
        Execute multiple tools in parallel (conceptual).

        Note: True parallel execution requires async/threading.
        This implementation executes sequentially but returns
        results in a format compatible with parallel execution.

        Args:
            tool_configs: List of dicts with 'tool_name' and parameters

        Returns:
            Dict mapping tool_name to ToolResult
        """
        results = {}

        for config in tool_configs:
            tool_name = config.pop("tool_name")
            result = self.execute_tool(tool_name, **config)
            results[tool_name] = result

        return results

    def select_tool_for_query(self, query: str) -> Optional[str]:
        """
        Select appropriate tool for a given query.

        Args:
            query: Medical query string

        Returns:
            Name of most appropriate tool or None
        """
        query_lower = query.lower()

        # Tool keyword mapping
        tool_keywords = {
            "ECGInterpreterTool": ["ecg", "ekg", "electrocardiogram", "heart rhythm"],
            "DrugInteractionCheckerTool": ["drug", "interaction", "medication", "pharmacy"],
            "DiagnosticReasoningTool": ["diagnos", "symptom", "differential"],
            "LaboratoryInterpreterTool": ["lab", "test", "blood", "result"]
        }

        # Score each tool based on keyword matches
        tool_scores = {}

        for tool_name, keywords in tool_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                tool_scores[tool_name] = score

        # Return tool with highest score
        if tool_scores:
            return max(tool_scores, key=tool_scores.get)

        return None

    def auto_execute_query(self, query: str, **parameters) -> Optional[ToolResult]:
        """
        Automatically select and execute appropriate tool for query.

        Args:
            query: Medical query string
            **parameters: Parameters for tool execution

        Returns:
            ToolResult or None if no appropriate tool found
        """
        tool_name = self.select_tool_for_query(query)

        if tool_name:
            return self.execute_tool(tool_name, **parameters)

        return None


def create_standard_tool_registry() -> ToolRegistry:
    """
    Create and populate a tool registry with standard medical tools.

    Returns:
        ToolRegistry populated with standard tools
    """
    from .medical_tools import (
        ECGInterpreterTool,
        DrugInteractionCheckerTool,
        DiagnosticReasoningTool,
        LaboratoryInterpreterTool
    )

    registry = ToolRegistry()

    # Register standard tools
    registry.register_tools([
        ECGInterpreterTool,
        DrugInteractionCheckerTool,
        DiagnosticReasoningTool,
        LaboratoryInterpreterTool
    ])

    return registry


def create_standard_tool_coordinator() -> ToolCoordinator:
    """
    Create a tool coordinator with standard medical tools.

    Returns:
        ToolCoordinator with standard tools registered
    """
    registry = create_standard_tool_registry()
    return ToolCoordinator(registry)
