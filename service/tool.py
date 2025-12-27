try:
    import tomllib  # py>=3.11
except ImportError:  # py<=3.10
    import tomli as tomllib

from log.core.logger import get_logger

import shutil
import time
import glob
import json
import os
import re

logger=get_logger()

# 删除图片
def clean_images(folder: str = "./"):
    """删除指定目录下的 png/jpg/jpeg 图片"""
    for ext in ["*.png", "*.jpg", "*.jpeg"]:
        for file in glob.glob(os.path.join(folder, ext)):
            try:
                os.remove(file)
                logger.debug(f"已删除临时图片: {file}")
            except Exception as e:
                logger.warning(f"删除失败 {file}: {e}")

# 删除临时文件
def clean_file(folder_path: str):
    """删除指定文件夹下的所有内容（文件 + 子文件夹），但保留文件夹本身"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # 删除文件或符号链接
                logger.info(f"已删除文件: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                logger.info(f"已删除文件夹: {file_path}")
        except Exception as e:
            logger.warning(f"删除失败 {file_path}: {e}")

# 数字提取
def data_cleaning(content,clean_rule,default_value):
    match = re.search(clean_rule, content)
    if match:
        clean_result = match.group(1).strip()
    else:
        logger.warning(f"未匹配相关信息，使用默认值{default_value}")
        clean_result = default_value
    return clean_result

async def llm_time(function_name,content,prompt,name):
    start_time = time.perf_counter()
    result = await function_name(content,prompt)
    end_time = time.perf_counter()
    elapsed =  end_time - start_time
    logger.info(f"{name}处理耗时: {elapsed:.2f} 秒")
    return result


def get_prompt(file_path,**kwargs):
    with open(file_path,"r+",encoding="utf-8") as pd:
        prompt_template = pd.read()
    prompt_result = prompt_template.format(**kwargs)
    return prompt_result

def load_toml(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        data = tomllib.load(f)
    result = {
        "model": data["llm"]["model"],
        "prompt": data["prompt"]["path"]
    }
    return result


def clean_result(raw_output: str) -> dict:
    try:
        # 1. 去掉前后的 ```json ``` 和 ``` 标记
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_output.strip())
        cleaned = re.sub(r"\n?```$", "", cleaned)

        # 2. 去除多余的空格和换行
        cleaned = cleaned.strip()

        # 3. 转换为字典
        result = json.loads(cleaned)
        return result

    except Exception:
        return raw_output
