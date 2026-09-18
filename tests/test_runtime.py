import sys
from types import SimpleNamespace

import pytest
from nexus_atom_core import Task

from nexus_atom_agents import AgentContext, AgentRouter, LocalRuntime, OpenAIRuntime


@pytest.mark.asyncio
async def test_local_json_protocol(tmp_path):
    runtime = LocalRuntime(
        (
            sys.executable,
            "-c",
            'import json,sys; data=json.load(sys.stdin); print(json.dumps({"proposal":{"objective":data["objective"]},"rationale":"test"}))',
        )
    )
    router = AgentRouter({"local": runtime}, {"optimize": "local"})
    result = await router.execute(
        Task(capability="optimize"), AgentContext(objective="optimize", directory=tmp_path), []
    )
    assert result.proposal == {"objective": "optimize"}
    with pytest.raises(ValueError):
        await router.execute(
            Task(capability="unknown"), AgentContext(objective="x", directory=tmp_path), []
        )


@pytest.mark.asyncio
async def test_responses_contract(tmp_path):
    calls = []

    async def create(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(
            status="completed",
            output_text='{"proposal":{},"rationale":"candidate"}',
            usage=SimpleNamespace(total_tokens=20),
        )

    runtime = OpenAIRuntime(
        "explicit-model", client=SimpleNamespace(responses=SimpleNamespace(create=create))
    )
    result = await runtime.execute(
        Task(capability="x"), AgentContext(objective="x", directory=tmp_path), []
    )
    assert result.usage.tokens == 20
    assert calls[0]["store"] is False
