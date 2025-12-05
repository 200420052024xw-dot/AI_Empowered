from service.file_to_url import pdf_to_url, ppt_to_url, word_to_url, excel_to_url
from API.api_siliconflow import view_llm
from log.core.logger import get_logger
import asyncio
import time

logger=get_logger()

def url_to_text(file_path, file_type, max_work=10):

    # 判断文件类型,采用不同的方法转化为图片
    if file_type == "pdf":
        image_results, page_count = pdf_to_url(file_path, max_work)
        logger.info("已经处理完PDF文件！")
    elif file_type == "pptx":
        image_results, page_count = ppt_to_url(file_path, max_work)
        logger.info("已经处理完PPT文件！")
    elif file_type in ["doc", "docx"]:
        image_results, page_count = word_to_url(file_path, max_work)
        logger.info("已经处理完WORD文件！")
    elif file_type in ["xls", "xlsx"]:
        logger.info("已经处理完EXCEL！")
        image_results, page_count = excel_to_url(file_path, max_work)
    else:
        return f"文件格式不支持！{{文件类型：{file_type}}}"

    brief_content = [None] * len(image_results)
    completed_count = 0

    # 读取图片的内容
    def image_to_text(idx, url):
        start_time = time.perf_counter()
        read_result = view_llm(url)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        return idx, read_result, elapsed

    overall_start = time.perf_counter()

    # 顺序处理，不用 asyncio
    for i, url in enumerate(image_results):
        idx, read_result, elapsed = image_to_text(i, url)

        brief_content[idx] = read_result

        completed_count += 1
        logger.info(f"进度: {completed_count}/{page_count} 页完成, 耗时 {elapsed:.3f} 秒")

    overall_end = time.perf_counter()

    overall_time = overall_end - overall_start

    # 拼接字符串
    content_parts = []
    for i in range(page_count):
        if brief_content[i] is not None:
            content_parts.append(f"============第{i + 1}页============\n{brief_content[i]}")
    content = "\n".join(content_parts)

    # 保存brief内容测试用
    # with open("F:\\document_interpret\\test\\test_content.txt","r+",encoding="utf-8") as pd:
    #     pd.write(content)


    logger.info(f"模型读取总耗时: {overall_time:.2f} 秒")

    if not content or not content.strip():
        logger.error("提取的文字内容为空！")

    logger.info("文字提取全部完成!")

    return content
