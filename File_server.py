import os
#import json
from mcp.server.fastmcp import FastMCP
import pandas as pd

mcp = FastMCP("FileReaderServer")


@mcp.tool()
async def read_question_files(folder_path: str = None):
    """
    读取指定文件夹下的文件内容
    :param folder_path: (可选) 自定义路径，默认使用内置路径
    :return 文件的所有内容
    """
    # 设置默认路径（建议使用原始字符串处理Windows路径）
    default_path = r"D:\桌面\投递\mcp\pythonProject\datas\question"
    target_path = folder_path or default_path



    result = {}

    try:
        for filename in os.listdir(target_path):
            file_path = os.path.join(target_path, filename)

            if not os.path.isfile(file_path):
                continue

            file_info = {"filename": filename, "type": "", "content": ""}

            try:
                if filename.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_info.update({
                            "type": "text",
                            "content": f.read()
                        })

                elif filename.endswith(".xlsx"):
                    df = pd.read_excel(file_path, nrows=5, engine="openpyxl")
                    file_info.update({
                        "type": "excel",
                        "content": df.fillna("").to_dict(orient="records")
                    })
                elif filename.endswith(".csv"):
                    df = pd.read_csv(file_path, nrows=5)
                    file_info.update({
                        "type": "csv",
                        "content": df.fillna("").to_dict(orient="records")
                    })

                elif filename.endswith(".py"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_info.update({
                            "type": "code",
                            "content": f.read()
                        })

                result[filename] = file_info

            except Exception as e:
                result[filename] = {"error": f"读取失败: {str(e)}"}

        return result
    except PermissionError:
        return {"error": "没有文件夹访问权限"}


if __name__ == "__main__":
    mcp.run(transport='stdio')