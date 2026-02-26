# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, Type, Union, get_origin, get_args
from pydantic import BaseModel
from pydantic.fields import FieldInfo

def resolve_actual_type(annotation: Any) -> Any:
    """
    解析实际类型，剥离 Optional, Union 和 List。
    返回 (actual_type, is_list, is_optional)
    """
    origin = get_origin(annotation)
    args = get_args(annotation)
    
    is_optional = False
    is_list = False
    actual_type = annotation

    # 处理 Union (包括 Optional[T] = Union[T, None])
    if origin is Union:
        if type(None) in args:
            is_optional = True
            # 取出非 None 的类型
            actual_type = next(t for t in args if t is not type(None))
            # 递归处理实际类型（可能是 List）
            actual_type, nested_is_list, _ = resolve_actual_type(actual_type)
            is_list = nested_is_list
        else:
            # 普通的 Union，取第一个
            actual_type = args[0]
    
    # 处理 List
    elif origin is list or origin is List:
        is_list = True
        if args:
            actual_type = args[0]
            # 递归处理 List 内部类型
            actual_type, _, nested_is_optional = resolve_actual_type(actual_type)
            is_optional = nested_is_optional
            
    return actual_type, is_list, is_optional

def print_markdown_structure(model_cls: Type[BaseModel], depth: int = 1, prefix: str = "", show_meta: bool = False, parent_title: str = ""):
    """
    递归打印模型的 Markdown 结构，使用 # 标题格式。
    
    :param model_cls: Pydantic 模型类
    :param depth: 当前 Markdown 标题层级 (1 为 #, 2 为 ##)
    :param prefix: 字段路径前缀
    :param show_meta: 是否显示字段名和类型等元数据
    :param parent_title: 父级字段的标题，用于去重
    """
    # 获取模型的字段
    for field_name, field_info in model_cls.model_fields.items():
        # 1. 提取 markdown_title
        markdown_title = "Unnamed"
        if field_info.json_schema_extra and "markdown_title" in field_info.json_schema_extra:
            markdown_title = field_info.json_schema_extra["markdown_title"]
        elif field_name == "summary":
            # 如果是 summary，且没有定义 markdown_title，默认为“概要说明”
            markdown_title = "概要说明"
            
        # 2. 如果当前标题与父级标题完全一致（常见于嵌套模型的 summary 或中间层），
        # 在可视化时跳过，以匹配骨架中的简洁表示。
        if markdown_title == parent_title:
            # 但如果它有子字段，我们还是需要递归
            actual_type, _, _ = resolve_actual_type(field_info.annotation)
            if isinstance(actual_type, type) and issubclass(actual_type, BaseModel):
                print_markdown_structure(actual_type, depth, prefix=f"{prefix}.{field_name}", show_meta=show_meta, parent_title=markdown_title)
            continue
            
        # 3. 解析类型信息
        actual_type, is_list, is_optional = resolve_actual_type(field_info.annotation)
        
        # 4. 构建元数据标记 (可选)
        meta_str = ""
        if show_meta:
            meta = []
            if is_list:
                meta.append("List")
            if is_optional:
                meta.append("Optional")
            
            meta_tags = f" [{', '.join(meta)}]" if meta else ""
            type_name = actual_type.__name__ if hasattr(actual_type, "__name__") else str(actual_type)
            meta_str = f" <!-- field: `{field_name}`, type: `{type_name}`{meta_tags} -->"
        
        # 5. 打印当前标题
        header_prefix = "#" * depth
        print(f"{header_prefix} {markdown_title}{meta_str}")

        # 6. 递归处理嵌套模型
        if isinstance(actual_type, type) and issubclass(actual_type, BaseModel):
            full_path = f"{prefix}.{field_name}" if prefix else field_name
            # 嵌套模型增加一级标题深度
            print_markdown_structure(actual_type, depth + 1, prefix=full_path, show_meta=show_meta, parent_title=markdown_title)

def visualize_model(model_cls: Type[BaseModel], show_meta: bool = False):
    """
    高层入口，对比生成的结构和定义的骨架。
    """
    print("\n" + "=" * 80)
    print(f" Model: {model_cls.__name__}")
    print("=" * 80)
    
    # 1. 打印生成的结构
    print("\n### [Generated Markdown Structure]")
    print("```markdown")
    
    # 提取顶层标题
    top_title = "Root Model"
    if model_cls.__doc__:
        # 优先使用 docstring 的第一行作为标题
        top_title = model_cls.__doc__.strip().split('\n')[0].strip('# ')
    
    # 如果有骨架，尝试从骨架中提取一级标题
    if hasattr(model_cls, "__business_architecture__"):
        arch = getattr(model_cls, "__business_architecture__")
        import re
        # 清理骨架中的 ID 标记
        clean_arch = re.sub(r'\s*\[id:[a-zA-Z_][a-zA-Z0-9_]*\]', '', arch)
        first_header = re.search(r'^#\s+(.*)', clean_arch, re.MULTILINE)
        if first_header:
            top_title = first_header.group(1).strip()

    print(f"# {top_title}")
    print_markdown_structure(model_cls, depth=2, show_meta=show_meta, parent_title=top_title)
    print("```")
    
    # 2. 打印定义的骨架
    if hasattr(model_cls, "__business_architecture__"):
        print("\n### [Original Business Architecture]")
        print("```markdown")
        print(getattr(model_cls, "__business_architecture__"))
        print("```")
    
    print("=" * 80 + "\n")

if __name__ == "__main__":
    # 简单的本地测试
    from pydantic import Field
    from typing import List
    
    class Sub(BaseModel):
        summary: str = Field(..., json_schema_extra={"markdown_title": "细节标题"})
        item: str = Field(..., json_schema_extra={"markdown_title": "具体项"})
        
    class TestModel(BaseModel):
        __business_architecture__ = "# 顶层标题\n## 模块1\n### 细节标题\n### 具体项"
        module1: Sub = Field(..., json_schema_extra={"markdown_title": "模块1"})
        
    visualize_model(TestModel, show_meta=True)
