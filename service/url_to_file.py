from log.core.logger import get_logger
import requests
import hashlib
import os

logger = get_logger()

def save_file(file_path):
    # 确保Document文件夹存在
    file_folder = "./Document"
    os.makedirs(file_folder, exist_ok=True)

    file_type = os.path.splitext(file_path)[1].lower().split(".")[1]

    # 判断是否是 URL
    if file_path.startswith("http://") or file_path.startswith("https://"):
        response = requests.get(file_path, stream=True)

        if response.status_code != 200:
            logger.error(f"无法下载文件: {file_path}", exc_info=True)
            raise FileNotFoundError(f"无法下载文件: {file_path}")

        # 获取文件类型
        file_type = os.path.splitext(file_path)[1].lower().split(".")[1]

        # 使用 URL 的 MD5 生成安全文件名
        url_hash = hashlib.md5(file_path.encode("utf-8")).hexdigest()
        filename = f"{url_hash}.{file_type}"
        tmp_path = os.path.join(file_folder, filename)

        # 保存文件
        with open(tmp_path, "wb") as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
        file_path = tmp_path
        logger.info(f"已经成功保存文件:{filename}！")

    # 本地文件不存在报错
    elif not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        raise FileNotFoundError(f"文件不存在: {file_path}")

    return file_path,file_type