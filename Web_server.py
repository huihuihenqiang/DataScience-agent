import json
from duckduckgo_search import DDGS
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WebSearch")


@mcp.tool()
async def web_search(query: str, max_results: int = 5) -> str:
    """
     使用互联网搜索，搜索用户想联网检索的内容,获取用户搜索关键词内容，然后返回结果，最大返回结果数量（默认5）。
    :param query: 搜索关键词,用户的搜索关键词。
    :param max_results: 最大返回结果数量（默认5）
    """
    try:
        with DDGS(headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }) as ddgs:
            # 获取文本结果（新版API接3口）
            results = []
            for r in ddgs.text(query, max_results=max_results, timelimit='60'):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "content": r.get("body")
                })

            return json.dumps(results, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run(transport='stdio')