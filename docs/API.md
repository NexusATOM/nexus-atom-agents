# nexus-atom-agents Python API

Public definitions below are generated from the shipped source. See USAGE.md and the README for runnable setup, semantics and limits. Contracts inherit strict extra-field rejection and finite-number validation where declared. Source links include the implementation for details.

## `nexus_atom_agents.runtime`

Agents produce proposals; only external deterministic evaluators award success.

### `AgentContext`

[Source](../src/nexus_atom_agents/runtime.py#L17)

```python
class AgentContext(Contract):
    objective: str
    evidence: dict[str, Any] = Field(default_factory=dict)
    directory: Path
    max_output_tokens: int = Field(default=4096, gt=0)
```

### `AgentResult`

[Source](../src/nexus_atom_agents/runtime.py#L24)

```python
class AgentResult(Contract):
    proposal: dict[str, Any]
    rationale: str
    usage: Usage = Field(default_factory=Usage)
    runtime: str
```

### `AgentRuntime`

[Source](../src/nexus_atom_agents/runtime.py#L31)

```python
class AgentRuntime(ABC):
    async def execute(self, task: Task, context: AgentContext, capabilities: list[Capability]) -> AgentResult: ...
```

### `payload`

[Source](../src/nexus_atom_agents/runtime.py#L38)

```python
def payload(task, context, capabilities): ...
```

### `LocalRuntime`

[Source](../src/nexus_atom_agents/runtime.py#L49)

JSON-in/JSON-out subprocess adapter for local models or coding agents.

```python
class LocalRuntime(AgentRuntime):
    def __init__(self, argv: tuple[str, ...], *, timeout=120, max_bytes=1000000): ...
    async def execute(self, task, context, capabilities): ...
```

### `OpenAIRuntime`

[Source](../src/nexus_atom_agents/runtime.py#L102)

```python
class OpenAIRuntime(AgentRuntime):
    def __init__(self, model: str, *, client=None, timeout=120): ...
    async def execute(self, task, context, capabilities): ...
```

### `NOOARuntime`

[Source](../src/nexus_atom_agents/runtime.py#L135)

```python
class NOOARuntime(AgentRuntime):
    def __init__(self, model: str, *, agent=None): ...
    async def execute(self, task, context, capabilities): ...
```

### `AgentRouter`

[Source](../src/nexus_atom_agents/runtime.py#L163)

```python
class AgentRouter():
    def __init__(self, runtimes: dict[str, AgentRuntime], routes: dict[str, str]): ...
    async def execute(self, task, context, capabilities): ...
```
