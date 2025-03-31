from pathlib import Path
from pprint import pprint
import pandas as pd
import graphrag.api as api
from graphrag.config.load_config import load_config
from graphrag.index.typing.pipeline_run_result import PipelineRunResult
from typing import Any
from mcp.server.fastmcp import FastMCP
 # 初始化 MCP 服务器
mcp = FastMCP("Rag_ML")
USER_AGENT = "rag_ML-app/1.0"

@mcp.tool()
async def rag_ML(query: str) -> str:
    """
    用于查询数据科学相关信息。比如说回归，分类，聚类，做nlp，时间序列等任务。
    :param query: 用户提出的具体问题
    :return: 最终获得的答案
    """
    PROJECT_DIRECTORY = r"D:\桌面\投递\mcp\pythonProject\datas\graphrag"
    graphrag_config = load_config(Path(PROJECT_DIRECTORY))
    # 加载实体
    entities = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/entities.parquet")
 # 加载社区
    communities = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/communities.parquet")
 # 加载社区报告
    community_reports = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/community_reports.parquet")
 # 进行全局搜索
    response, context = await api.global_search(
    config=graphrag_config,
    entities=entities,
    communities=communities,
    community_reports=community_reports,
    community_level=2,
    dynamic_community_selection=False,
    response_type="Multiple Paragraphs",
    query=query,
)
    return response
if __name__ == "__main__":
# 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')