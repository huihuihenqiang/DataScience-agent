import asyncio
import os
import json
from typing import Optional, Dict
from contextlib import AsyncExitStack
from openai import OpenAI
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import logging
from datetime import datetime
load_dotenv()


class MultiServerMCPClient:
    def __init__(self):
        """管理多个 MCP 服务器的客户端"""
        self.exit_stack = AsyncExitStack()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("BASE_URL")
        self.model = os.getenv("MODEL")
        if not self.openai_api_key:
            raise ValueError("未找到OPENAI_API_KEY，请在.env文件中配置")
            # 初始化 OpenAI Client
        self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)

            # 存储 (server_name -> MCP ClientSession) 映射
        self.sessions: Dict[str, ClientSession] = {}
            # 存储工具信息
        self.tools_by_session: Dict[str, list] = {}  # 每个 session 的 tools 列表
        self.all_tools = []  # 合并所有工具的列表

        # 初始化日志（仅保留文件日志）
        self.logger = logging.getLogger("MCPClient")
        self.logger.setLevel(logging.INFO)

        # 创建日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 仅保留文件日志处理器
        file_handler = logging.FileHandler(
            'mcp_client.log',
            encoding='utf-8',  # 明确指定编码
            mode='w'  # 每次运行覆盖日志（如需追加可改为 'a'）
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.log_step = 1  # 用于跟踪流程步骤
    async def connect_to_servers(self, servers: dict):
        """
        同时启动多个服务器并获取工具
        servers: 形如 {"weather": "weather_server.py", "rag": "rag_server.py"}
        """
        for server_name, script_path in servers.items():
            session = await self._start_one_server(script_path)
            self.sessions[server_name] = session

                # 列出此服务器的工具
            resp = await session.list_tools()
            self.tools_by_session[server_name] = resp.tools  # 保存到self.tools_by_session
            for tool in resp.tools:
    # OpenAI Function Calling 格式修正
                function_name = f"{server_name}_{tool.name}"
                self.all_tools.append({"type": "function",
                                       "function": {
                                           "name": function_name,
                                           "description": tool.description,
                                           "input_schema": tool.inputSchema
                                       }
                                       })
            # 转化function calling格式
        self.all_tools = await self.transform_json(self.all_tools)
        print("\n已连接到下列服务器: ")
        for name in servers:
            print(f"  - {name}: {servers[name]}")
        print("\n汇总的工具:")

        for t in self.all_tools:
            print(f"  - {t['function']['name']}")

    async def transform_json(self, json2_data):
        """
       将Claude Function calling参数格式转换为OpenAI Function calling参数格式，多余字
       段会被直接删除。
        :param json2_data: 一个可被解释为列表的 Python 对象（或已解析的 JSON 数据）
        :return: 转换后的新列表
               """
        result = []

        for item in json2_data:
            # 确保有 "type" 和 "function" 两个关键字段
            if not isinstance(item, dict) or "type" not in item or "function" not in item:
                continue
            old_func = item["function"]

# 确保 function 下有我们需要的关键子字段
            if not isinstance(old_func, dict) or "name" not in old_func or "description" not in old_func:
                continue

# 处理新 function 字段
            new_func = {
    "name": old_func["name"],
    "description": old_func["description"],
    "parameters": {}
}

# 读取 input_schema 并转成 parameters
            if "input_schema" in old_func and isinstance(old_func["input_schema"], dict):
                old_schema = old_func["input_schema"]

# 新的 parameters 保留 type, properties, required 这三个字段
                new_func["parameters"]["type"] = old_schema.get("type", "object")
                new_func["parameters"]["properties"] =old_schema.get("properties", {})
                new_func["parameters"]["required"] = old_schema.get("required",
                                                    [])

            new_item = {
    "type": item["type"],
    "function": new_func
}

            result.append(new_item)

        return result

    async def _start_one_server(self, script_path: str) -> ClientSession:
        """启动单个 MCP 服务器子进程，并返回 ClientSession"""
        is_python = script_path.endswith(".py")
        is_js = script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("服务器脚本必须是 .py 或 .js 文件")
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
                command=command,
                args=[script_path],
                env=None
            )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        read_stream, write_stream = stdio_transport
        session = await self.exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        return session

    async def chat_base(self, messages: list) -> list:
        max_iterations = 30  # 最大执行次数
        iteration = 0  # 当前执行次数计数器
        # 记录LLM请求
        self._log_llm_request(messages)

        # 第一次请求
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.all_tools
        )
        # 记录LLM响应
        self._log_llm_response(response)

        # 如果模型要求调用工具，则进入循环
        if response.choices[0].finish_reason == "tool_calls":
            while True:
                iteration += 1  # 增加执行次数计数

                # 如果超过最大执行次数，强制终止循环
                if iteration > max_iterations:
                    print(f"达到最大工具调用次数 {max_iterations} 次，强制终止")
                    break

                # 处理工具调用并更新消息历史
                messages = await self.create_function_response_messages(messages, response)

                # 发送新的请求
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.all_tools
                )

                # 如果模型不需要再调用工具，退出循环
                if response.choices[0].finish_reason != "tool_calls":
                    break

        return response

    async def create_function_response_messages(self, messages, response):
        function_call_messages = response.choices[0].message.tool_calls
        messages.append(response.choices[0].message.model_dump())

        for function_call_message in function_call_messages:
            tool_name = function_call_message.function.name
            tool_args = json.loads(function_call_message.function.arguments)

            # 运行外部函数
            function_response = await self._call_mcp_tool(tool_name, tool_args)
            # 拼接消息队列
            messages.append(
                {
                    "role": "tool",
                    "content": function_response,
                    "tool_call_id": function_call_message.id,
                }
            )
        return messages

#     async def process_query(self, user_query: str) -> str:
#         """
#         OpenAI 最新 Function Calling 逻辑:
#          1. 发送用户消息 + tools 信息
#          2. 若模型 `finish_reason == "tool_calls"`，则解析 toolCalls 并执行相应 MCP
# 工具
#          3. 把调用结果返回给 OpenAI，让模型生成最终回答
#         """
#         messages = [{"role": "user", "content": user_query}]
#         # 第一次请求
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=messages,
#             tools=self.all_tools
#         )
#         content = response.choices[0]
#         print(content)
#         print(self.all_tools)
#         # 如果模型调用了 MCP 工具
#         if content.finish_reason == "tool_calls":
#             # 解析 tool_calls
#             tool_call = content.message.tool_calls[0]
#             tool_name = tool_call.function.name  # 形如 "weather_query_weather"
#             tool_args = json.loads(tool_call.function.arguments)
#             print(f"\n[ 调用工具: {tool_name}, 参数: {tool_args} ]\n")
#             # 执行MCP工具
#             result = await self._call_mcp_tool(tool_name, tool_args)
#             # 把工具调用历史写进 messages
#             messages.append(content.message.model_dump())
#             messages.append({
#                 "role": "tool",
#                 "content": result,
#                 "tool_call_id": tool_call.id,
#             })
#             # 第二次请求，让模型整合工具结果，生成最终回答
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=messages
#             )
#             return response.choices[0].message.content
#             # 如果模型没调用工具，直接返回回答
#         return content.message.content

    async def _call_mcp_tool(self, tool_full_name: str, tool_args: dict) -> str:
        """
        根据 "serverName_toolName" 调用相应的服务器工具
        """
        # 记录工具调用请求
        self.logger.info(f"[Step {self.log_step}] 调用工具请求")
        self.log_step += 1
        self.logger.info(f"工具名称: {tool_full_name}")
        self.logger.info(f"工具参数: {json.dumps(tool_args, indent=2)}")

        parts = tool_full_name.split("_", 1)
        if len(parts) != 2:
            return f"无效的工具名称: {tool_full_name}"
        server_name, tool_name = parts
        session = self.sessions.get(server_name)
        if not session:
            return f"找不到服务器: {server_name}"

    # 执行 MCP 工具
        resp = await session.call_tool(tool_name, tool_args)
        #print(resp)#这句话就是每次的显示

        # 记录工具响应
        self.logger.info(f"[Step {self.log_step}] 工具调用响应")
        self.log_step += 1
        self.logger.info(f"工具名称: {tool_full_name}")
        self.logger.info(f"响应内容: {resp.content if resp.content else '无输出'}")

        return resp.content if resp.content else "工具执行无输出"

    async def chat_loop(self):
        print("\n自动kaggle处理客户端已启动！输入'quit'退出。")
        messages = []
        while True:
            query = input("\n用户: ").strip()

            # 记录用户输入
            self.logger.info(f"\n[Step {self.log_step}]用户输入")
            self.log_step += 1
            self.logger.info(f"内容: {query}")

            if query.lower() == "quit":
                break
            try:
                messages.append({"role": "user", "content": query})
                messages = messages[-20:]
                # print(messages)
                response = await self.chat_base(messages)
                messages.append(response.choices[0].message.model_dump())
                result = response.choices[0].message.content

                print(f"\nAI: {result}")
            except Exception as e:
                print(f"\n调用过程出错: {e}")

            # 记录最终响应
            self.logger.info(f"[Step {self.log_step}] AI响应")
            self.log_step += 1
            self.logger.info(f"内容: {result}")


        # 新增日志辅助方法

    def _log_llm_request(self, messages):
        self.logger.info(f"\n[Step {self.log_step}] LLM请求")
        self.log_step += 1
        self.logger.info(f"模型: {self.model}")
        self.logger.info("消息历史:")
        for msg in messages:
            self.logger.info(f"- {msg['role'].upper()}: {msg['content']}")
        self.logger.info("可用工具:")
        for tool in self.all_tools:
            self.logger.info(f"- {tool['function']['name']}")

    def _log_llm_response(self, response):
        self.logger.info(f"\n[Step {self.log_step}] LLM响应")
        self.log_step += 1
        self.logger.info(f"响应ID: {response.id}")
        self.logger.info(f"模型: {response.model}")
        self.logger.info(f"完成原因: {response.choices[0].finish_reason}")

        if response.choices[0].message.content:
            self.logger.info(f"回复内容: {response.choices[0].message.content}")

        if response.choices[0].message.tool_calls:
            self.logger.info("工具调用:")
            for tool_call in response.choices[0].message.tool_calls:
                self.logger.info(f"- ID: {tool_call.id}")
                self.logger.info(f"  工具: {tool_call.function.name}")
                self.logger.info(f"  参数: {tool_call.function.arguments}")

    async def cleanup(self):
        # 关闭所有资源
        await self.exit_stack.aclose()

async def main():
    # 服务器脚本
    servers = {
        "SQLServer": "SQL_server.py",
        "PythonServer": "Python_server.py",
        "LocalServer": "Local_server.py",
        "WebSearch": "Web_server.py",
        "Rag_ML": "Rag_server.py",
        "Html_process": "Html_server.py",
        "FileReaderServer": "File_server.py",
    }
    client = MultiServerMCPClient()
    try:
        await client.connect_to_servers(servers)
        await client.chat_loop()
    finally:
        await client.cleanup()
if __name__ == "__main__":
        asyncio.run(main())



