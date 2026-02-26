# -*- coding: utf-8 -*-
import unittest
from pydantic import BaseModel, Field
from typing import Optional
from llm_structured_extract.core.parser import MarkdownParser

class SubModel(BaseModel):
    summary: Optional[str] = Field(None, json_schema_extra={"markdown_title": "子模块标题"})
    detail: Optional[str] = Field(None, json_schema_extra={"markdown_title": "详细内容"})

class RootModel(BaseModel):
    __business_architecture__ = """
# 根标题
## 模块A
### 子模块标题
### 详细内容
""".strip()
    
    module_a: SubModel = Field(default_factory=SubModel, json_schema_extra={"markdown_title": "模块A"})

class TestRefactoredParser(unittest.TestCase):
    def test_minimalist_parsing(self):
        md = """
# 根标题
## 模块A
### 子模块标题
这是模块A的概要内容。
### 详细内容
这是模块A的详细内容。
● 列表项1
● 列表项2
"""
        parser = MarkdownParser(RootModel)
        result = parser.parse(md)
        
        self.assertEqual(result.module_a.summary, "这是模块A的概要内容。")
        self.assertEqual(result.module_a.detail, "这是模块A的详细内容。\n● 列表项1\n● 列表项2")

    def test_missing_optional_field(self):
        md = """
# 根标题
## 模块A
### 子模块标题
只有概要。
"""
        parser = MarkdownParser(RootModel)
        result = parser.parse(md)
        
        self.assertEqual(result.module_a.summary, "只有概要。")
        self.assertIsNone(result.module_a.detail)

if __name__ == "__main__":
    unittest.main()
