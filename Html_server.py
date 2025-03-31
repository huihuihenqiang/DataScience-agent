import json
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP  # 确保已安装 fastmcp
from openai import OpenAI  # 需安装 openai>=1.0.0
import re

# 初始化服务器
mcp = FastMCP("Html_process")


@mcp.tool()
async def generate_html_report(messages: str,) -> Dict:
    """
    基于所有对话内容调用大模型生成html形式的报告。
    :param messages: 你和用户所有的对话内容，包括工具调用的输入输出和模型回答的输入输出
    :return 返回报告的预览
    """

    # 构建大模型提示
    system_prompt = """你是一个专业的数据科学家助手。请根据对话内容生成HTML格式的竞赛分析报告，要求包含：
1. 用<div class="section">分章节展示关键信息
2. 使用卡片式布局（metric-card类）
3. 包含以下分析维度：
   - 高频操作统计（表格展示）
   - 错误类型分布（条形图占位）
   - 代码修改趋势（时间线展示）
4. 使用Bootstrap风格的CSS（内嵌在<style>中）"""

    # 调用大模型
    try:
        client = OpenAI(
            api_key='sk-quBjWaFrfCyP8NFp75Bd90C46e96425a8756545dC5Ee386f',
            base_url="https://api.gptplus5.com/v1"
        )

        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"日志内容：\n{messages}"}
            ],
            temperature=0.3,  # 降低随机性保证结构稳定
            max_tokens=1500,  # 增加token限额
            top_p=0.9
        )

        generated_html = response.choices[0].message.content

        # 后处理确保HTML完整性
        final_html = _postprocess_html(generated_html)

        # 保存报告文件
        report_path = Path("ai_report.html")
        report_path.write_text(final_html, encoding="utf-8")

        return {
            "status": "success",
            "path": str(report_path.absolute()),
            "html_preview": final_html[:500] + "..."  # 返回部分预览
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}



def _postprocess_html(raw_html: str) -> str:
    """后处理生成的HTML确保结构完整"""
    # 添加基础HTML结构如果缺失
    if "<html>" not in raw_html:
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>AI生成报告</title>
            {{style}}
        </head>
        <body>
            {{content}}
        </body>
        </html>
        """

        # 提取内联样式
        style_content = ""
        if "<style>" in raw_html:
            style_start = raw_html.index("<style>") + 7
            style_end = raw_html.index("</style>")
            style_content = raw_html[style_start:style_end]

        # 重组文档结构
        return html_template.format(
            style=f"<style>{style_content}</style>",
            content=raw_html
        )
    return raw_html

if __name__ == "__main__":
    # 启动服务器（支持多种传输方式）
    mcp.run(transport='stdio')  # 也可以使用 'websocket' 或 'http'