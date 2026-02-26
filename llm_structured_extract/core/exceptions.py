# llm_structured_extract/core/exceptions.py

class LLMExtractError(Exception):
    """项目基础异常类"""
    pass

class ConfigurationError(LLMExtractError):
    """配置错误（如缺少 API Key）"""
    pass

class SchemaError(LLMExtractError):
    """Schema 相关错误（加载失败、校验失败）"""
    pass

class PromptError(LLMExtractError):
    """提示词构建错误"""
    pass

class ProviderError(LLMExtractError):
    """LLM 服务提供商相关错误"""
    pass

class LLMCallError(ProviderError):
    """LLM API 调用失败"""
    pass

class ParserError(LLMExtractError):
    """解析 Markdown 结果失败"""
    pass
