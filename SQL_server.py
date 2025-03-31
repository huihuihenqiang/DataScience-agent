import json
import sqlite3
import csv
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import pandas as pd  # 需要安装 pandas 和 openpyxl

# 初始化 MCP 服务器
mcp = FastMCP("SQLiteServer")
USER_AGENT = "SQLite-app/1.0"


@mcp.tool()
async def sql_inter(sql_query: str):
    """
    查询本地 SQLite 数据库,通过运行一段SQL代码来进行数据库查询。\
    :param sql_query: 字符串形式的SQL查询语句，用于执行对本地文件中mydatabase.db数据库中各张表进行查
询，并获得各表中的各类相关信息
    :return: ：sql_query在sqlite中的运行结果。
    """
    # 连接到 SQLite 数据库
    connection = sqlite3.connect('mydatabase.db')

    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)

        # 获取查询结果
        results = cursor.fetchall()

        # 获取列名（增强结果可读性）
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            # 将结果转换为字典列表
            dict_results = [dict(zip(columns, row)) for row in results]
            return json.dumps(dict_results, ensure_ascii=False)

        return json.dumps(results)
    finally:
        connection.close()






if __name__ == "__main__":

    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')