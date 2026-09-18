# Using agent runtimes

**NOOA performs agent reasoning. Pydantic validates the structured inputs and outputs. ATOM controls execution and acceptance.** None replaces the other.

NOOA is NVIDIA's Python agent framework (`nooa==0.0.10`), not NOAA, the US agency. ATOM keeps NOOA optional so deterministic workflows and local examples can run without an LLM. The retained GEOS specialists already use real NOOA `@strategy(PredictStrategy(...))` dispatch.

## Specialist agents versus proposal backends

GEOS has six specialist classes: RepositoryAgent, ArchitectureAgent, CUDAAgent,
PerformanceAgent, ValidationAgent, and the coordinating GEOSAgent. See the
[agent usage guide](https://github.com/NexusATOM/nexus-atom-geos/blob/main/docs/AGENTS.md)
for runnable examples and tool composition. They are distinct from the three
runtime backends in this package: selecting NOOARuntime does not automatically
invoke that specialist team. GEOS's built-in specialist workflow uses one model
client sequentially; direct Python composition can assign different clients.

The agent implementation now lives in `nexus-atom-geos`, alongside its ATOM
plugin. Install that package with `[nooa]`; do not co-install the old
`nexus-geos-agent` distribution, which owns the same import and CLI names.

## Local JSON adapter

This complete example runs a tiny stand-in proposal process. Replace the command with a real locally installed model/coding-agent wrapper that obeys the same JSON protocol:

```python
import asyncio
import sys
from pathlib import Path
from nexus_atom_core import Task
from nexus_atom_agents import AgentContext, LocalRuntime

async def main():
    runtime = LocalRuntime((sys.executable, "-c",
        'import json,sys; request=json.load(sys.stdin); '
        'print(json.dumps({"proposal":{"idea":"cache repeated work"},"rationale":"example only"}))'))
    result = await runtime.execute(Task(capability="example.optimize"),
        AgentContext(objective="Improve runtime", directory=Path.cwd()), [])
    print(result.model_dump_json(indent=2))

asyncio.run(main())
```

Requests include the task, objective, selected evidence, capability descriptions and proposal contract. Output must be one JSON object with `proposal` and `rationale`. The adapter limits output bytes, applies a deadline and kills the process group on exit/cancellation. It executes an argument vector, not an implicit shell. The process remains trusted executable code with the user's permissions.

## NOOA

Install the `nooa` extra and select an explicit provider/model recognized by NOOA. Credentials use that provider's normal environment configuration. Instantiate `NOOARuntime("provider/model")` and call the same `execute` contract. It constructs a NOOA Agent with a PredictStrategy and typed AgentResult. Do not replace its ellipsis method with handwritten model simulation: NOOA implements that decorated method at runtime.

Offline tests use NOOA's `FakeLLMClient` to exercise its actual strategy dispatch and typed parsing. They do not establish live-provider connectivity, model quality or successful GEOS transformations. Reported usage from NOOA may be incomplete; enforce strict spend limits at the provider.

## OpenAI

Install `[openai]`, configure `OPENAI_API_KEY`, and instantiate `OpenAIRuntime(model="your-explicit-model")`. The adapter uses asynchronous Responses requests with JSON output, a bounded output-token setting, no SDK retries, and `store=False`. It rejects incomplete responses and invalid JSON. API billing and availability depend on the selected account/model; ATOM does not select or purchase access automatically.

## Routing and safety boundary

`AgentRouter({"runtime-name": runtime}, {"capability-name": "runtime-name"})` makes routing explicit. Unmapped capabilities fail. The router neither executes the proposal nor approves it. A consuming plugin must validate the proposal schema, allowed targets and source hashes, then run independent software/science/performance checks.

The local and hosted adapters never confer approval by returning text such as “passed.” Credential values must not be added to AgentContext evidence, command arguments or persisted reports. The generic subprocess adapter is not a dedicated Codex CLI integration; that would require a tested wrapper for its actual protocol.

See [API](API.md), [tests](../tests/test_runtime.py) and the [main architecture](https://github.com/NexusATOM/nexus-atom-controller/blob/main/docs/ARCHITECTURE.md).
