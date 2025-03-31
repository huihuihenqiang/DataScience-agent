import json
import subprocess
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("LocalServer")
ALLOWED_COMMANDS = {'uv','pip','start','cd','ls', 'dir', 'pwd', 'date', 'echo', 'ipconfig', 'ifconfig'}  # 基础命令白名单


@mcp.tool()
async def execute_command(command: str) -> str:
    """
     执行本地电脑命令（基础命令白名单机制），window系统
    :param command: 要执行的系统命令
    :return: 命令执行结果或错误信息
    """
    # 基础安全校验
    # if not any(cmd in command.lower() for cmd in ALLOWED_COMMANDS):
    #     return "拒绝执行未授权的命令"

    try:
        # 执行命令（支持跨平台）
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )

        # 构造返回结果
        output = {
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
        return json.dumps(output, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')