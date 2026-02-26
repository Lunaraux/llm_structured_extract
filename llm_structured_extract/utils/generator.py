# -*- coding: utf-8 -*-
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class MarkdownNode:
    level: int
    title: str
    raw_title: str
    ident: str
    children: List['MarkdownNode'] = field(default_factory=list)
    parent: Optional['MarkdownNode'] = None

    def is_leaf(self) -> bool:
        return len(self.children) == 0

class ModelGenerator:
    def __init__(self, indent: str = "    "):
        self.indent = indent

    def _to_camel_case(self, snake_str: str) -> str:
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)

    def _normalize_name(self, title: str) -> str:
        # 移除 Markdown 符号和前面的序号
        clean = re.sub(r'^[#\s\d\.]+', '', title).strip()
        # 移除非字母数字字符并转换为下划线
        clean = re.sub(r'[^\w\s]', '', clean)
        clean = re.sub(r'\s+', '_', clean).lower()
        return clean.strip('_')

    def _extract_id_and_title(self, line_title: str) -> tuple[str, str]:
        # 匹配 ... [id:some_name]
        match = re.search(r'\[id:([a-zA-Z_][a-zA-Z0-9_]*)\]\s*$', line_title)
        if match:
            ident = match.group(1)
            # 标题需要去掉前面的 # 符号
            clean_title = line_title[:match.start()].strip().lstrip('#').strip()
            return ident, clean_title
        else:
            # 回退到自动 snake_case
            clean_title = line_title.lstrip('#').strip()
            ident = self._normalize_name(clean_title)
            return ident, clean_title

    def parse_markdown(self, md_content: str) -> List[MarkdownNode]:
        lines = md_content.strip().split('\n')
        root_nodes = []
        stack: List[MarkdownNode] = []

        for line in lines:
            line = line.strip()
            if not line.startswith('#'):
                continue
            
            level = len(re.match(r'^#+', line).group())
            ident, title = self._extract_id_and_title(line)
            
            node = MarkdownNode(
                level=level,
                title=title,
                raw_title=line,
                ident=ident
            )

            while stack and stack[-1].level >= level:
                stack.pop()
            
            if stack:
                node.parent = stack[-1]
                stack[-1].children.append(node)
            else:
                root_nodes.append(node)
            
            stack.append(node)
            
        return root_nodes

    def _generate_class_name(self, node: MarkdownNode) -> str:
        suffix = "View" if node.level <= 2 else "SubView"
        return f"{self._to_camel_case(node.ident)}{suffix}"

    def _generate_model_code(self, node: MarkdownNode, generated_classes: List[str]) -> str:
        if node.is_leaf():
            return ""

        # 先生成子节点的类
        child_codes = []
        for child in node.children:
            if not child.is_leaf():
                child_codes.append(self._generate_model_code(child, generated_classes))

        # 生成当前类
        class_name = self._generate_class_name(node)
        if class_name in generated_classes:
            return "\n".join(filter(None, child_codes))
            
        lines = [f"class {class_name}(BaseModel):", f'{self.indent}"""{node.raw_title}"""']
        
        # 只有当模型有子节点时才生成字段
        for child in node.children:
            field_name = child.ident
            markdown_title = child.title
            
            if child.is_leaf():
                lines.append(f"{self.indent}{field_name}: Optional[str] = Field(")
                lines.append(f"{self.indent}{self.indent}None,")
                lines.append(f'{self.indent}{self.indent}json_schema_extra={{"markdown_title": "{markdown_title}"}}')
                lines.append(f"{self.indent})")
            else:
                child_class = self._generate_class_name(child)
                lines.append(f"{self.indent}{field_name}: {child_class} = Field(")
                lines.append(f"{self.indent}{self.indent}default_factory={child_class},")
                lines.append(f'{self.indent}{self.indent}json_schema_extra={{"markdown_title": "{markdown_title}"}}')
                lines.append(f"{self.indent})")

        generated_classes.append(class_name)
        current_class_code = "\n".join(lines)
        return "\n".join(filter(None, child_codes + [current_class_code]))

    def generate_python_code(self, md_content: str, root_class_name: str = "MasterView") -> str:
        root_nodes = self.parse_markdown(md_content)
        if not root_nodes:
            return ""

        output = [
            "# -*- coding: utf-8 -*-",
            "from typing import Optional",
            "from pydantic import BaseModel, Field",
            "from llm_structured_extract.core.schema_registry import register_schema",
            "\n"
        ]

        generated_classes = []
        all_model_codes = []
        
        # 顶层类特殊处理
        top_node = root_nodes[0]
        
        # 递归生成所有子模型
        model_code = self._generate_model_code(top_node, generated_classes)
        all_model_codes.append(model_code)
        
        output.append("\n\n".join(all_model_codes))
        
        # 加上顶层注册装饰器（假设最后一个生成的是顶层类，或者我们需要手动指定）
        # 实际上上面的递归会最后生成 top_node 的类
        
        # 修正：我们需要把最后一个类（顶层类）加上装饰器和骨架
        last_class_name = generated_classes[-1]
        
        # 寻找代码中对应的类并插入装饰器和骨架
        code = "\n\n".join(all_model_codes)
        
        # 插入骨架
        skeleton = f'    __business_architecture__: str = """\n{md_content.strip()}\n""".strip()'
        
        # 使用正则替换
        code = re.sub(
            f"class {last_class_name}\(BaseModel\):",
            f"@register_schema\nclass {last_class_name}(BaseModel):\n{skeleton}\n",
            code
        )
        
        # 移除类定义中的 Markdown 标题 docstring（因为已经有骨架了）
        code = re.sub(f'class {last_class_name}\(BaseModel\):\n{self.indent}""".*?"""', f"class {last_class_name}(BaseModel):", code, flags=re.DOTALL)
        
        output = [output[0], output[1], output[2], output[3], "\n", code]
        
        return "\n".join(output)

if __name__ == "__main__":
    example_md = """
# 二、公司创始人和团队 [id:founder_and_team]

## 1. 公司是否具有清晰且共享的愿景及价值观？ [id:vision_and_values]

### 公司团队对公司的长期愿景和价值观是否有统一的认识和认同？ [id:team_recognition]

#### 公司从上到下是否都充分了解公司的价值观和愿景？是否都十分认可公司的价值观和愿景？ [id:awareness_and_endorsement]
"""
    gen = ModelGenerator()
    print(gen.generate_python_code(example_md))
