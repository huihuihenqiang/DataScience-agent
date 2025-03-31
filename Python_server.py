import json
from typing import Any
import csv
import numpy as np
import pandas as pd
import random
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("PythonServer")
USER_AGENT = "Pythonserver-app/1.0"

@mcp.tool()
async def python_inter(py_code):
    """
    运行用户提供的 Python 代码，并返回执行结果。
   :param py_code: 字符串形式的 Python 代码
   :return: 代码运行的最终结果
   """


    g = globals()

    try:
    # 若是表达式，直接运行并返回
        result = eval(py_code, g)
        return json.dumps(str(result), ensure_ascii=False)

    except Exception:
        global_vars_before = set(g.keys())
        try:
            exec(py_code, g)
        except Exception as e:
            return json.dumps(f"代码执行时报错: {e}", ensure_ascii=False)
        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        if new_vars:
        # 只返回可序列化的变量值
            safe_result = {}
            for var in new_vars:
                try:
                    json.dumps(g[var])  # 尝试序列化，确保可以转换为 JSON
                    safe_result[var] = g[var]
                except (TypeError, OverflowError):
                    safe_result[var] = str(g[var])  # 如果不能序列化，则转换为字符串
            return json.dumps(safe_result, ensure_ascii=False)

        else:
            return json.dumps("已经顺利执行代码", ensure_ascii=False)
if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')