from src.prefix import Divergence, first_divergence, render_blocks

TOOL = {"name": "lookup", "input_schema": {"type": "object"}}
SYS = {"type": "text", "text": "You are a handbook assistant."}
U1 = {"role": "user", "content": "Rule 5?"}
A1 = {"role": "assistant", "content": "45"}
U2 = {"role": "user", "content": "Rule 12?"}


def req(
    tools: list[object], system: list[object], messages: list[object]
) -> dict[str, list[object]]:
    return {"tools": tools, "system": system, "messages": messages}


def test_render_order_and_unsorted_serialization() -> None:
    blocks = render_blocks(req([TOOL], [SYS], [U1]))
    assert [(s, i) for s, i, _ in blocks] == [("tools", 0), ("system", 0), ("messages", 0)]
    assert blocks[2][2] == '{"role":"user","content":"Rule 5?"}'


def test_missing_sections_are_empty() -> None:
    expected = [("messages", 0, '{"role":"user","content":"Rule 5?"}')]
    assert render_blocks({"messages": [U1]}) == expected


def test_identical_requests_have_no_divergence() -> None:
    r = req([TOOL], [SYS], [U1])
    assert first_divergence(r, r) is None


def test_appending_turns_keeps_the_prefix() -> None:
    assert first_divergence(req([TOOL], [SYS], [U1]), req([TOOL], [SYS], [U1, A1, U2])) is None


def test_truncation_keeps_the_prefix() -> None:
    assert first_divergence(req([TOOL], [SYS], [U1, A1, U2]), req([TOOL], [SYS], [U1])) is None


def test_timestamp_in_system_prompt_is_found() -> None:
    old = {"type": "text", "text": "Now: 10:00. You are a handbook assistant."}
    new = {"type": "text", "text": "Now: 10:01. You are a handbook assistant."}
    got = first_divergence(req([TOOL], [old], [U1]), req([TOOL], [new], [U1, A1, U2]))
    assert got == Divergence("system", 0)


def test_new_tool_shifts_everything_after_it() -> None:
    other = {"name": "search", "input_schema": {"type": "object"}}
    got = first_divergence(req([TOOL], [SYS], [U1]), req([TOOL, other], [SYS], [U1]))
    assert got == Divergence("tools", 1)


def test_key_reorder_changes_the_bytes() -> None:
    reordered = {"input_schema": {"type": "object"}, "name": "lookup"}
    got = first_divergence(req([TOOL], [SYS], [U1]), req([reordered], [SYS], [U1]))
    assert got == Divergence("tools", 0)


def test_edited_earlier_turn_is_found() -> None:
    edited = {"role": "assistant", "content": "forty-five"}
    got = first_divergence(req([TOOL], [SYS], [U1, A1, U2]), req([TOOL], [SYS], [U1, edited, U2]))
    assert got == Divergence("messages", 1)
