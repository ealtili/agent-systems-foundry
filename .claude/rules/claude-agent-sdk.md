---
paths:
  - "labs/30*/**"
  - "labs/31*/**"
  - "labs/32*/**"
  - "labs/33*/**"
  - "labs/35*/**"
---

# Claude Agent SDK (`claude-agent-sdk`) Rules

1. **Current Package:** Always import from `claude_agent_sdk`. Never import from legacy `claude_code_sdk`.
2. **Provenance & Ambient Authority:**
   - For developer tools: project setting sources may be enabled.
   - For automated/multi-tenant services: explicitly set `setting_sources=[]` to prevent ambient host contamination.
3. **Non-Blocking Execution:** Always supply a custom `can_use_tool` callback or configure explicit `allowed_tools` with `permission_mode="dontAsk"` in headless environments.
4. **In-Process Tools:** Use `@tool` with `create_sdk_mcp_server(name="srv", tools=[...])` and namespace in permissions as `mcp__srv__<tool_name>`.
