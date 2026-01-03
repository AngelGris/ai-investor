import json
import time

import diskcache
from agents import FunctionTool


def cached_function_tool(tool, ttl: int):
    """
    Wrap a FunctionTool (or async function) and cache its results for TTL seconds.
    """
    original_on_invoke = tool.on_invoke_tool

    _cache = diskcache.Cache("./function_tool_cache")

    async def cached_on_invoke(tool_context, tool_arguments):
        # Normalize tool_arguments into a hashable key
        if isinstance(tool_arguments, dict):
            # Multiple named arguments
            args_key = tuple(sorted(tool_arguments.items()))
        elif isinstance(tool_arguments, str):
            try:
                parsed = json.loads(tool_arguments)
                if isinstance(parsed, dict):
                    args_key = tuple(sorted(parsed.items()))
                else:
                    args_key = (tool_arguments,)
            except json.JSONDecodeError:
                args_key = (tool_arguments,)
        else:
            # Single argument (string, int, etc.)
            args_key = (tool_arguments,)

        key = (tool.name, args_key)
        now = time.time()

        if key in _cache:
            value, ts = _cache[key]
            if now - ts < ttl:
                return value

        # Call the actual tool
        result = await original_on_invoke(tool_context, tool_arguments)

        _cache[key] = (result, time.time())

        return result

    # Construct a new FunctionTool with cached_on_invoke
    return FunctionTool(
        name=tool.name,
        params_json_schema=getattr(tool, "params_json_schema", None),
        on_invoke_tool=cached_on_invoke,
        description=getattr(tool, "description", None),
    )
