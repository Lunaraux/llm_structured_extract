"""
统一配置系统
将环境变量配置与YAML配置合并到一个统一的配置入口
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class ModelConfig(BaseModel):
    """模型配置"""
    name: str = ""
    temperature: float = 0.1
    max_tokens: int = 4096
    timeout: int = 60


class LLMConfig(BaseModel):
    """LLM 配置"""
    provider: str = "dashscope"
    models: Dict[str, ModelConfig] = Field(default_factory=dict)


class PromptConfig(BaseModel):
    """提示词配置"""
    system_instruction: str = ""
    few_shot_example_path: Optional[str] = None


class ServiceConfig(BaseModel):
    """服务配置"""
    default_schema: str = ""
    task_queue: str = "extract"
    default_timeout: int = 30


class YAMLConfig(BaseModel):
    """YAML配置文件结构"""
    llm: LLMConfig = Field(default_factory=LLMConfig)
    prompts: PromptConfig = Field(default_factory=PromptConfig)
    service: ServiceConfig = Field(default_factory=ServiceConfig)


class Settings(BaseSettings):
    """统一配置类 - 合并环境变量和YAML配置"""
    # 环境变量配置（优先级最高）
    DASHSCOPE_API_KEY: str = ""
    LLM_PROVIDER: str = ""
    REDIS_URL: str = ""
    OLLAMA_HOST: str = ""
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
    PROMPT_TEMPLATE_PATH: Optional[str] = None
    CONFIG_PATH: Optional[str] = None  # YAML配置文件路径
    
    # 内部YAML配置缓存
    _yaml_config: Optional[YAMLConfig] = None

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 加载YAML配置
        self._load_yaml_config()
        # 设置默认值
        self._set_defaults()

    def _load_yaml_config(self) -> None:
        """加载YAML配置文件"""
        config_path = self.CONFIG_PATH or os.getenv("CONFIG_PATH", "")
        if not config_path:
            # 使用默认路径：项目根目录/config.yaml
            config_path = str(self.PROJECT_ROOT / "config.yaml")
        
        config_file = Path(config_path)
        
        # 如果配置文件不存在，创建默认配置
        if not config_file.exists():
            self._yaml_config = YAMLConfig()
            self._save_yaml_config(config_path)
        else:
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                self._yaml_config = YAMLConfig(**data)
            except Exception as e:
                # 如果加载失败，使用默认配置
                self._yaml_config = YAMLConfig()
                print(f"Warning: Failed to load config from {config_path}: {str(e)}")

    def _save_yaml_config(self, config_path: str) -> None:
        """保存YAML配置到文件"""
        try:
            config_file = Path(config_path)
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(self._yaml_config.model_dump(), f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Warning: Failed to save config to {config_path}: {str(e)}")

    def _set_defaults(self) -> None:
        """设置默认值（环境变量优先，YAML配置次之）"""
        if not self.LLM_PROVIDER:
            self.LLM_PROVIDER = self._yaml_config.llm.provider
        if not self.REDIS_URL:
            self.REDIS_URL = "redis://localhost:6379/0"
        if not self.OLLAMA_HOST:
            self.OLLAMA_HOST = "http://127.0.0.1:11434"

    # YAML配置访问方法
    @property
    def yaml_config(self) -> YAMLConfig:
        """获取YAML配置"""
        return self._yaml_config or YAMLConfig()

    def get_model_config(self, provider: str = "dashscope") -> ModelConfig:
        """获取指定提供商的模型配置"""
        return self.yaml_config.llm.models.get(provider, ModelConfig())

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return self.yaml_config.prompts.system_instruction

    def get_few_shot_example(self) -> str:
        """获取Few-shot示例"""
        example_path = self.yaml_config.prompts.few_shot_example_path
        
        # 1. 尝试使用配置文件指定的路径
        if example_path and Path(example_path).exists():
            try:
                return Path(example_path).read_text(encoding="utf-8")
            except Exception as e:
                raise RuntimeError(f"Failed to load few-shot example from {example_path}: {str(e)}") from e
        
        # 2. 尝试使用默认路径：templates/examples/company_extract_example.txt
        default_path = self.PROJECT_ROOT / "llm_structured_extract" / "templates" / "examples" / "company_extract_example.txt"
        if default_path.exists():
            try:
                return default_path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"Warning: Failed to load default example from {default_path}: {str(e)}")
        
        # 3. 如果都失败，返回空字符串或最简示例
        return "No example provided."

    @property
    def service_config(self) -> ServiceConfig:
        """获取服务配置"""
        return self.yaml_config.service


# 全局配置实例
settings = Settings()