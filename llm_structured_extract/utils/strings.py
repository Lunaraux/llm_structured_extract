# llm_structured_extract/utils/strings.py
import re
import unicodedata

def normalize_title(text: str) -> str:
    """
    正规化标题，用于增强匹配的鲁棒性。
    1. 移除首尾空格
    2. 统一全角/半角字符
    3. 移除末尾的标点符号（如 ：: ? ？ . 。）
    4. 统一转为小写
    """
    if not text:
        return ""
    
    # 统一全角转半角
    text = unicodedata.normalize('NFKC', text)
    
    # 移除末尾标点
    text = re.sub(r'[:：?？.。!！\s]+$', '', text)
    
    # 移除多余空白并转小写
    return text.strip().lower()

def clean_markdown_code_block(text: str) -> str:
    """
    剥离 Markdown 代码块标记
    """
    text = text.strip()
    if text.startswith("```markdown"):
        text = re.sub(r'^```markdown\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
    elif text.startswith("```"):
        text = re.sub(r'^```\w*\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
    return text.strip()
