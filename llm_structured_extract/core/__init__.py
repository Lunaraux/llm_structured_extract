try:
    from .llm_adapters.dashscope_adapter import DashScopeAdapter
except ImportError as e:
    import warnings
    warnings.warn(f"DashScopeAdapter未注册: {e}")