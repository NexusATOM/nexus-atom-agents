# Nexus ATOM Agents

Runtime-neutral proposal generation and explicit capability routing. `AgentRuntime.execute(task, context, capabilities)` returns an `AgentResult` with proposal, rationale and reported usage. Agents cannot award scientific or software success.

* `LocalRuntime`: a bounded, cancellable JSON-in/JSON-out subprocess for local models or coding tools. No shell interpolation. The subprocess is trusted executable code, not an OS sandbox.
* `OpenAIRuntime`: optional asynchronous Responses API adapter; configure an explicit model and `OPENAI_API_KEY`. Install `[openai]`. Responses must complete and parse as a proposal/rationale JSON object. Network retries are disabled; the controller controls retry policy.
* `NOOARuntime`: optional NVIDIA NOOA structured-prediction adapter; install `[nooa]` and configure the model/provider. NOOA stays a backend rather than the controller's foundation.
* `AgentRouter`: maps capability names to explicit runtime names; unknown routes fail instead of silently choosing a provider.

```python
from nexus_atom_agents import AgentRouter, LocalRuntime
router = AgentRouter({"local": LocalRuntime(("my-local-agent", "--json"))},
                     {"geos.optimize": "local"})
```

The local command reads one JSON request from stdin and returns `{"proposal": {...}, "rationale": "..."}` on stdout. Context includes objective, bounded selected evidence and available capability descriptions. The consuming capability validates proposal schema, allowed targets and source hashes before changes are applied. For hosted providers, only send project data you intend to disclose to that configured provider.

API contract reference: [OpenAI Responses create](https://developers.openai.com/api/reference/python/resources/responses/methods/create). Live provider calls are not required by offline tests and were not used to validate this release. NOOA's reported usage may be incomplete; provider-side quotas are needed for strict monetary enforcement.

## Install

Python 3.12–3.13, Linux or macOS. The six packages are released together; they are not yet published to PyPI. Clone `nexus-atom-controller` and run its `scripts/bootstrap.py --directory ../NexusATOM` to clone the matching release and create a virtual environment. Use `--ref main --dev` for development. Existing checkouts are preserved.

From a workspace containing all six repositories:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ./nexus-atom-core -e ./nexus-atom-controller \
  -e ./nexus-atom-agents -e ./nexus-atom-hpc -e ./nexus-atom-science -e ./nexus-atom-geos
.venv/bin/atom plugins
```

Run package tests with `python -m pytest tests` after installing the `dev` extra and sibling dependencies. The GEOS legacy tests also require the `nooa` extra; GEOS integration tests require the controller. CI tests Python 3.12 and 3.13 and builds wheel/sdist artifacts. See the [architecture and implementation map](https://github.com/NexusATOM/nexus-atom-controller/blob/main/docs/ARCHITECTURE.md).

Apache-2.0. This is an independent implementation for model orchestration, not an official NASA model distribution or endorsement.

## Documentation

- [Usage and configuration](docs/USAGE.md)
- [Python API reference](docs/API.md)
- [Contributing](CONTRIBUTING.md)
- [Execution boundaries](SECURITY.md)
- [Changes](CHANGELOG.md)
