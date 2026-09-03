"""
V50 Program Synthesis - Automated reasoning program generation

Generates and executes reasoning programs from high-level specifications.
Supports learning reasoning primitives from examples.

Date: 2026-04-23
Version: 1.0.0
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
import re


class PrimitiveType(Enum):
    """Types of reasoning primitives"""
    ARITHMETIC = "arithmetic"
    LOGICAL = "logical"
    STRING = "string"
    LIST = "list"
    MATH = "math"
    COMPARISON = "comparison"
    CONTROL_FLOW = "control_flow"


@dataclass
class ReasoningPrimitive:
    """A basic reasoning operation"""
    name: str
    primitive_type: PrimitiveType
    function: Callable
    signature: str
    description: str


@dataclass
class ReasoningProgram:
    """A composed reasoning program"""
    nodes: List['ProgramNode'] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class ProgramNode:
    """A single node in a reasoning program"""
    primitive: ReasoningPrimitive
    arguments: List[Any] = field(default_factory=list)
    inputs_from: List[str] = field(default_factory=list)
    outputs_to: List[str] = field(default_factory=list)
    node_id: str = ""


@dataclass
class ExecutionContext:
    """Execution context for programs"""
    variables: Dict[str, Any] = field(default_factory=dict)
    step_count: int = 0
    max_steps: int = 1000


@dataclass
class SynthesisResult:
    """Result of program synthesis"""
    success: bool
    program: Optional[ReasoningProgram] = None
    execution_result: Optional[Any] = None
    error_message: Optional[str] = None
    steps_executed: int = 0


class ReasoningPrimitiveLibrary:
    """Library of reasoning primitives"""

    def __init__(self):
        self.primitives: Dict[str, ReasoningPrimitive] = {}
        self._initialize_default_primitives()

    def _initialize_default_primitives(self):
        """Initialize default reasoning primitives"""

        # Arithmetic primitives
        self.register_primitive(ReasoningPrimitive(
            name="add",
            primitive_type=PrimitiveType.ARITHMETIC,
            function=lambda a, b: a + b,
            signature="add(a, b) -> a + b",
            description="Add two numbers"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="subtract",
            primitive_type=PrimitiveType.ARITHMETIC,
            function=lambda a, b: a - b,
            signature="subtract(a, b) -> a - b",
            description="Subtract b from a"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="multiply",
            primitive_type=PrimitiveType.ARITHMETIC,
            function=lambda a, b: a * b,
            signature="multiply(a, b) -> a * b",
            description="Multiply two numbers"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="divide",
            primitive_type=PrimitiveType.ARITHMETIC,
            function=lambda a, b: a / b if b != 0 else float('inf'),
            signature="divide(a, b) -> a / b",
            description="Divide a by b"
        ))

        # Math primitives
        self.register_primitive(ReasoningPrimitive(
            name="sqrt",
            primitive_type=PrimitiveType.MATH,
            function=lambda x: x ** 0.5,
            signature="sqrt(x) -> square root of x",
            description="Calculate square root"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="power",
            primitive_type=PrimitiveType.MATH,
            function=lambda base, exp: base ** exp,
            signature="power(base, exp) -> base^exp",
            description="Calculate power"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="log",
            primitive_type=PrimitiveType.MATH,
            function=lambda x: __import__('math').log(x) if x > 0 else float('-inf'),
            signature="log(x) -> natural log of x",
            description="Calculate natural logarithm"
        ))

        # Comparison primitives
        self.register_primitive(ReasoningPrimitive(
            name="equal",
            primitive_type=PrimitiveType.COMPARISON,
            function=lambda a, b: a == b,
            signature="equal(a, b) -> a == b",
            description="Check equality"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="greater_than",
            primitive_type=PrimitiveType.COMPARISON,
            function=lambda a, b: a > b,
            signature="greater_than(a, b) -> a > b",
            description="Check if a > b"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="less_than",
            primitive_type=PrimitiveType.COMPARISON,
            function=lambda a, b: a < b,
            signature="less_than(a, b) -> a < b",
            description="Check if a < b"
        ))

        # String primitives
        self.register_primitive(ReasoningPrimitive(
            name="concat",
            primitive_type=PrimitiveType.STRING,
            function=lambda a, b: str(a) + str(b),
            signature="concat(a, b) -> concatenated string",
            description="Concatenate strings"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="length",
            primitive_type=PrimitiveType.STRING,
            function=lambda s: len(str(s)),
            signature="length(s) -> length of string",
            description="Get string length"
        ))

        # List primitives
        self.register_primitive(ReasoningPrimitive(
            name="first",
            primitive_type=PrimitiveType.LIST,
            function=lambda lst: lst[0] if lst and len(lst) > 0 else None,
            signature="first(lst) -> first element",
            description="Get first element of list"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="rest",
            primitive_type=PrimitiveType.LIST,
            function=lambda lst: lst[1:] if lst else [],
            signature="rest(lst) -> list without first element",
            description="Get rest of list"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="map",
            primitive_type=PrimitiveType.LIST,
            function=lambda lst, fn: [fn(x) for x in lst] if lst else [],
            signature="map(lst, fn) -> apply fn to each element",
            description="Apply function to list elements"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="filter",
            primitive_type=PrimitiveType.LIST,
            function=lambda lst, fn: [x for x in lst if fn(x)] if lst else [],
            signature="filter(lst, fn) -> elements matching predicate",
            description="Filter list by predicate"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="reduce",
            primitive_type=PrimitiveType.LIST,
            function=lambda lst, fn, init: __import__('functools').reduce(fn, lst, init) if lst else init,
            signature="reduce(lst, fn, init) -> reduced value",
            description="Reduce list to single value"
        ))

        # Logical primitives
        self.register_primitive(ReasoningPrimitive(
            name="and",
            primitive_type=PrimitiveType.LOGICAL,
            function=lambda a, b: bool(a) and bool(b),
            signature="and(a, b) -> a AND b",
            description="Logical AND"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="or",
            primitive_type=PrimitiveType.LOGICAL,
            function=lambda a, b: bool(a) or bool(b),
            signature="or(a, b) -> a OR b",
            description="Logical OR"
        ))

        self.register_primitive(ReasoningPrimitive(
            name="not",
            primitive_type=PrimitiveType.LOGICAL,
            function=lambda a: not bool(a),
            signature="not(a) -> NOT a",
            description="Logical NOT"
        ))

    def register_primitive(self, primitive: ReasoningPrimitive):
        """Register a new primitive"""
        self.primitives[primitive.name] = primitive

    def get_primitive(self, name: str) -> Optional[ReasoningPrimitive]:
        """Get a primitive by name"""
        return self.primitives.get(name)

    def list_primitives(self, primitive_type: Optional[PrimitiveType] = None) -> List[ReasoningPrimitive]:
        """List all primitives, optionally filtered by type"""
        if primitive_type is None:
            return list(self.primitives.values())
        return [p for p in self.primitives.values() if p.primitive_type == primitive_type]


class ExecutionEngine:
    """Executes reasoning programs"""

    def __init__(self, primitive_library: Optional[ReasoningPrimitiveLibrary] = None):
        self.primitive_library = primitive_library or ReasoningPrimitiveLibrary()

    def execute(self, program: ReasoningProgram, inputs: Dict[str, Any],
                max_steps: int = 1000) -> SynthesisResult:
        """Execute a reasoning program"""
        try:
            context = ExecutionContext(
                variables=inputs.copy(),
                max_steps=max_steps
            )

            # Execute each node in sequence
            for node in program.nodes:
                if context.step_count >= max_steps:
                    return SynthesisResult(
                        success=False,
                        error_message=f"Max steps ({max_steps}) exceeded"
                    )

                result = self._execute_node(node, context)
                if result is None:
                    return SynthesisResult(
                        success=False,
                        error_message=f"Failed to execute node: {node.node_id}"
                    )

                # Store outputs
                for output_var in node.outputs_to:
                    context.variables[output_var] = result

                context.step_count += 1

            # Collect final outputs
            final_outputs = {var: context.variables.get(var) for var in program.outputs}

            return SynthesisResult(
                success=True,
                program=program,
                execution_result=final_outputs,
                steps_executed=context.step_count
            )

        except Exception as e:
            return SynthesisResult(
                success=False,
                error_message=str(e)
            )

    def _execute_node(self, node: ProgramNode, context: ExecutionContext) -> Any:
        """Execute a single program node"""
        primitive = self.primitive_library.get_primitive(node.primitive.name)
        if primitive is None:
            raise ValueError(f"Unknown primitive: {node.primitive.name}")

        # Prepare arguments
        args = []
        for arg in node.arguments:
            if isinstance(arg, str) and arg in context.variables:
                args.append(context.variables[arg])
            else:
                args.append(arg)

        for input_var in node.inputs_from:
            if input_var in context.variables:
                args.append(context.variables[input_var])

        # Execute primitive function
        return primitive.function(*args)


class ProgramSynthesizer:
    """Synthesizes programs from examples or natural language"""

    def __init__(self, primitive_library: Optional[ReasoningPrimitiveLibrary] = None):
        self.primitive_library = primitive_library or ReasoningPrimitiveLibrary()

    def synthesize_from_examples(self, examples: List[Dict[str, Any]],
                                input_vars: List[str],
                                output_var: str) -> SynthesisResult:
        """Synthesize a program from input-output examples"""
        try:
            # Try different simple program structures
            programs = self._generate_candidate_programs(input_vars, output_var)

            for program in programs:
                # Test program against all examples
                if self._test_program(program, examples):
                    return SynthesisResult(
                        success=True,
                        program=program,
                        execution_result=program
                    )

            return SynthesisResult(
                success=False,
                error_message="Could not synthesize program from examples"
            )

        except Exception as e:
            return SynthesisResult(
                success=False,
                error_message=str(e)
            )

    def _generate_candidate_programs(self, input_vars: List[str],
                                     output_var: str) -> List[ReasoningProgram]:
        """Generate candidate programs to try"""
        programs = []

        # Try single primitive programs
        for primitive in self.primitive_library.list_primitives():
            if len(input_vars) == 2:
                program = ReasoningProgram(
                    nodes=[ProgramNode(
                        primitive=primitive,
                        inputs_from=input_vars,
                        outputs_to=[output_var],
                        node_id=f"{primitive.name}_node"
                    )],
                    inputs=input_vars,
                    outputs=[output_var],
                    description=f"{primitive.name} operation"
                )
                programs.append(program)

        # Try two-step programs
        if len(input_vars) >= 1:
            temp_var = "_temp"
            for prim1 in self.primitive_library.list_primitives():
                for prim2 in self.primitive_library.list_primitives():
                    program = ReasoningProgram(
                        nodes=[
                            ProgramNode(
                                primitive=prim1,
                                inputs_from=input_vars[:1],
                                outputs_to=[temp_var],
                                node_id="step1"
                            ),
                            ProgramNode(
                                primitive=prim2,
                                inputs_from=[temp_var] + input_vars[1:2],
                                outputs_to=[output_var],
                                node_id="step2"
                            )
                        ],
                        inputs=input_vars,
                        outputs=[output_var],
                        description=f"{prim1.name} then {prim2.name}"
                    )
                    programs.append(program)

        return programs

    def _test_program(self, program: ReasoningProgram,
                     examples: List[Dict[str, Any]]) -> bool:
        """Test program against examples"""
        engine = ExecutionEngine(self.primitive_library)

        for example in examples:
            inputs = {var: example.get(var) for var in program.inputs}
            expected = example.get(program.outputs[0])

            result = engine.execute(program, inputs, max_steps=100)
            if not result.success:
                return False

            actual = result.execution_result.get(program.outputs[0])
            if actual != expected:
                return False

        return True


class ProgramLearner:
    """Learns new reasoning primitives from examples"""

    def __init__(self, primitive_library: Optional[ReasoningPrimitiveLibrary] = None):
        self.primitive_library = primitive_library or ReasoningPrimitiveLibrary()

    def learn_primitive(self, name: str, examples: List[Dict[str, Any]],
                       input_vars: List[str], output_var: str) -> Optional[ReasoningPrimitive]:
        """Learn a new primitive from examples"""
        # Analyze examples to infer operation
        if len(examples) < 2:
            return None

        # Try to detect patterns
        pattern = self._detect_pattern(examples, input_vars, output_var)

        if pattern == "arithmetic_addition":
            return ReasoningPrimitive(
                name=name,
                primitive_type=PrimitiveType.ARITHMETIC,
                function=lambda a, b: a + b,
                signature=f"{name}(a, b) -> a + b",
                description=f"Learned primitive: {name}"
            )
        elif pattern == "arithmetic_multiplication":
            return ReasoningPrimitive(
                name=name,
                primitive_type=PrimitiveType.ARITHMETIC,
                function=lambda a, b: a * b,
                signature=f"{name}(a, b) -> a * b",
                description=f"Learned primitive: {name}"
            )

        return None

    def _detect_pattern(self, examples: List[Dict[str, Any]],
                       input_vars: List[str], output_var: str) -> Optional[str]:
        """Detect pattern in examples"""
        if len(input_vars) != 2:
            return None

        # Check for addition pattern
        is_addition = True
        for ex in examples:
            a = ex.get(input_vars[0])
            b = ex.get(input_vars[1])
            expected = ex.get(output_var)
            if expected != a + b:
                is_addition = False
                break

        if is_addition:
            return "arithmetic_addition"

        # Check for multiplication pattern
        is_multiplication = True
        for ex in examples:
            a = ex.get(input_vars[0])
            b = ex.get(input_vars[1])
            expected = ex.get(output_var)
            if expected != a * b:
                is_multiplication = False
                break

        if is_multiplication:
            return "arithmetic_multiplication"

        return None


class ProgramSynthesisReasoner:
    """Main reasoning system for program synthesis"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.primitive_library = ReasoningPrimitiveLibrary()
        self.execution_engine = ExecutionEngine(self.primitive_library)
        self.synthesizer = ProgramSynthesizer(self.primitive_library)
        self.learner = ProgramLearner(self.primitive_library)

    def synthesize_program(self, task_description: str,
                          examples: Optional[List[Dict[str, Any]]] = None) -> SynthesisResult:
        """Synthesize a program from description or examples"""
        if examples:
            input_vars = self._extract_input_vars(examples)
            output_var = self._extract_output_var(examples)
            return self.synthesizer.synthesize_from_examples(examples, input_vars, output_var)

        # Try to parse natural language
        return self._synthesize_from_description(task_description)

    def execute_program(self, program: ReasoningProgram,
                       inputs: Dict[str, Any]) -> SynthesisResult:
        """Execute a synthesized program"""
        return self.execution_engine.execute(program, inputs)

    def _extract_input_vars(self, examples: List[Dict[str, Any]]) -> List[str]:
        """Extract input variable names from examples"""
        if not examples:
            return []
        # Assume all keys except 'output' or 'result' are inputs
        output_keys = {'output', 'result', 'answer', 'out'}
        return [k for k in examples[0].keys() if k not in output_keys]

    def _extract_output_var(self, examples: List[Dict[str, Any]]) -> str:
        """Extract output variable name from examples"""
        if not examples:
            return "output"
        output_keys = {'output', 'result', 'answer', 'out'}
        for key in output_keys:
            if key in examples[0]:
                return key
        return "output"

    def _synthesize_from_description(self, description: str) -> SynthesisResult:
        """Synthesize program from natural language description"""
        description_lower = description.lower()

        # Simple pattern matching for common operations
        if "add" in description_lower or "sum" in description_lower:
            primitive = self.primitive_library.get_primitive("add")
            program = ReasoningProgram(
                nodes=[ProgramNode(
                    primitive=primitive,
                    inputs_from=["a", "b"],
                    outputs_to=["output"],
                    node_id="add_node"
                )],
                inputs=["a", "b"],
                outputs=["output"],
                description="Addition program"
            )
            return SynthesisResult(success=True, program=program)

        return SynthesisResult(
            success=False,
            error_message="Could not understand description"
        )


# Factory functions
def create_primitive_library() -> ReasoningPrimitiveLibrary:
    """Create a reasoning primitive library"""
    return ReasoningPrimitiveLibrary()


def create_program_synthesizer(library: Optional[ReasoningPrimitiveLibrary] = None) -> ProgramSynthesizer:
    """Create a program synthesizer"""
    return ProgramSynthesizer(library)


def create_program_synthesis_reasoner(config: Optional[Dict[str, Any]] = None) -> ProgramSynthesisReasoner:
    """Create a complete program synthesis reasoner"""
    return ProgramSynthesisReasoner(config)


__all__ = [
    'ReasoningPrimitive',
    'PrimitiveType',
    'ReasoningProgram',
    'ProgramNode',
    'ExecutionContext',
    'SynthesisResult',
    'ReasoningPrimitiveLibrary',
    'ExecutionEngine',
    'ProgramSynthesizer',
    'ProgramLearner',
    'ProgramSynthesisReasoner',
    'create_primitive_library',
    'create_program_synthesizer',
    'create_program_synthesis_reasoner',
]
