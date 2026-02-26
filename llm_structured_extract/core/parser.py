# -*- coding: utf-8 -*-
import re
import time
from typing import Any, Dict, List, Optional, Type, Union
from pydantic import BaseModel
from llm_structured_extract.utils.logger import get_logger
from llm_structured_extract.core.exceptions import ParserError
from llm_structured_extract.utils.strings import normalize_title, clean_markdown_code_block

logger = get_logger(__name__)

class MarkdownParser:
    """
    将 LLM 生成的结构化 Markdown 转换回 Pydantic 模型的解析器。
    """

    def __init__(self, model_cls: Type[BaseModel]):
        self.model_cls = model_cls

    def parse(self, text: str) -> BaseModel:
        """解析 Markdown 文本并返回 Pydantic 模型实例"""
        if not text:
            logger.warning("Empty input to parser")
            return self.model_cls()

        start_time = time.time()  # 添加耗时监控
        
        # 0. 基础清洗：使用统一工具类
        text = clean_markdown_code_block(text)

        # 1. 将 Markdown 分割成层级树
        sections = self._split_sections(text)
        
        # 2. 递归映射到模型
        try:
            # 自动跳过包装标题逻辑：
            # 1. 如果模型显式定义了骨架，则按骨架跳入
            business_arch = getattr(self.model_cls, "__business_architecture__", "")
            if business_arch:
                # 清理骨架中的 ID 标记
                clean_arch = re.sub(r'\s*\[id:[a-zA-Z_][a-zA-Z0-9_]*\]', '', business_arch)
                top_headers = re.findall(r'^#\s+(.*)', clean_arch, re.MULTILINE)
                if len(top_headers) == 1:
                    root_title = top_headers[0].strip()
                    root_section = self._find_section_by_title(sections["subsections"], root_title)
                    if root_section:
                        sections = root_section
            # 2. 如果模型没定义骨架，但 Markdown 只有一个顶级标题，则自动跳入
            elif len(sections["subsections"]) == 1:
                sections = list(sections["subsections"].values())[0]
            
            data = self._map_sections_to_model(self.model_cls, sections)
            result = self.model_cls.model_validate(data)
            
            elapsed = time.time() - start_time
            if elapsed > 0.1:  # 超过 100ms 记录警告
                logger.warning(
                    f"Slow parsing: {self.model_cls.__name__} took {elapsed:.3f}s "
                    f"(len={len(text)} chars)"
                )
            return result
        except Exception as e:
            logger.error(f"Parsing failed for {self.model_cls.__name__}: {str(e)}")
            # 不再静默返回空模型，让上层捕获
            raise

    def _split_sections(self, text: str) -> Dict[str, Any]:
        """根据 Markdown 标题层级将文本分割为字典"""
        lines = text.split('\n')
        root = {"content": "", "subsections": {}}
        stack = [(0, root)]  # (level, dict)

        for line in lines:
            header_match = re.match(r'^(#{1,6})\s+(.*)', line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                
                # 找到正确的父级
                while stack and stack[-1][0] >= level:
                    stack.pop()
                
                if not stack: # 防御性编程
                    stack = [(0, root)]

                new_section = {"content": "", "subsections": {}}
                stack[-1][1]["subsections"][title] = new_section
                stack.append((level, new_section))
            else:
                if stack:
                    if stack[-1][1]["content"]:
                        stack[-1][1]["content"] += "\n" + line
                    else:
                        stack[-1][1]["content"] = line

        return root

    def _map_sections_to_model(self, model_cls: Type[BaseModel], sections: Dict[str, Any]) -> Dict[str, Any]:
        """增强映射：支持模糊标题匹配和 List 类型"""
        result = {}
        subsections = sections.get("subsections", {})
        
        for field_name, field_info in model_cls.model_fields.items():
            # 特殊字段：summary 取根 content
            if field_name == "summary" and sections.get("content"):
                result[field_name] = sections["content"].strip()
                continue

            # 获取 markdown_title（可选，缺省则使用字段名）
            markdown_title = self._get_markdown_title(field_info) or field_name

            annotation = field_info.annotation
            origin = getattr(annotation, "__origin__", None)
            args = getattr(annotation, "__args__", None)
            
            # 兼容 Optional[T] 和 T | None
            is_optional = False
            actual_type = annotation
            if origin is Union or (hasattr(annotation, "__or__") and origin is None):
                if args and type(None) in args:
                    is_optional = True
                    actual_type = next(t for t in args if t is not type(None))
                    # 更新 origin/args 以反映实际类型
                    origin = getattr(actual_type, "__origin__", None)
                    args = getattr(actual_type, "__args__", None)

            # 1. 处理 List 类型
            if origin is list:
                item_type = args[0] if args else Any
                section = self._find_section_by_title(subsections, markdown_title)
                if section:
                    content = section.get("content", "").strip()
                    # 尝试解析列表项
                    items = self._parse_markdown_list(content)
                    if issubclass(item_type, BaseModel):
                        # 如果列表项是模型，目前暂不支持从纯文本解析 List[Model]，
                        # 除非模型结构允许（例如子标题）。这里先支持 List[str]
                        result[field_name] = items if items else []
                    else:
                        result[field_name] = items if items else []
                else:
                    result[field_name] = []
                continue

            # 2. 处理嵌套模型
            if isinstance(actual_type, type) and issubclass(actual_type, BaseModel):
                # 如果嵌套模型有显式标题，则跳入该章节
                if self._get_markdown_title(field_info):
                    nested_section = self._find_section_by_title(subsections, markdown_title)
                    if nested_section is not None:
                        result[field_name] = self._map_sections_to_model(actual_type, nested_section)
                    else:
                        result[field_name] = None if is_optional else actual_type()
                else:
                    # 如果没有显式标题，则视为“透明嵌套”，继续在当前章节查找字段
                    result[field_name] = self._map_sections_to_model(actual_type, sections)
            
            # 3. 处理基础类型 (str)
            elif actual_type is str:
                section = self._find_section_by_title(subsections, markdown_title)
                if section is not None:
                    result[field_name] = section.get("content", "").strip() or None
                else:
                    result[field_name] = None
            else:
                result[field_name] = None

        return result

    def _find_section_by_title(self, subsections: Dict[str, Any], target_title: str) -> Optional[Dict[str, Any]]:
        """模糊匹配标题：使用正规化后的字符串进行查找"""
        normalized_target = normalize_title(target_title)
        
        # 1. 精确匹配
        if target_title in subsections:
            return subsections[target_title]
        
        # 2. 正规化匹配
        for title, section in subsections.items():
            if normalize_title(title) == normalized_target:
                return section
        
        # 3. 包含匹配（应对 LLM 缩减标题的情况）
        for title, section in subsections.items():
            norm_title = normalize_title(title)
            if normalized_target in norm_title or norm_title in normalized_target:
                return section
                
        return None

    def _parse_markdown_list(self, text: str) -> List[str]:
        """解析 Markdown 列表项 (- item 或 1. item)"""
        if not text:
            return []
        
        items = []
        # 匹配 - 或 * 或 1. 开头的行
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            item_match = re.match(r'^[-*+]\s+(.*)', line)
            if not item_match:
                item_match = re.match(r'^\d+\.\s+(.*)', line)
            
            if item_match:
                items.append(item_match.group(1).strip())
            elif line and not items:
                # 如果第一行不是列表格式，但有内容，视作单项
                items.append(line)
        return items

    def _get_markdown_title(self, field_info) -> Optional[str]:
        """从 FieldInfo 中提取 markdown_title"""
        if field_info.json_schema_extra and "markdown_title" in field_info.json_schema_extra:
            return field_info.json_schema_extra["markdown_title"]
        return None
