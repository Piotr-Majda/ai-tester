import os

import yaml
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI

# Path to the configuration file
CONFIG_PATH = "config/settings.yaml"

# Load .env into environment
load_dotenv()


def create_llm() -> BaseChatModel:
    """
    Factory function to create a LangChain chat model based on the configuration file.

    Reads the configuration from `config/settings.yaml` and instantiates the
    appropriate chat model (Ollama or OpenAI). It resolves environment variables
    for keys that start with '$'.
    """
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")

    llm_config = config.get("llm")
    if not llm_config:
        raise ValueError("LLM configuration is missing from settings.yaml")

    provider = llm_config.get("provider")
    model_name = llm_config.get("model")
    # Get temperature from config, default to 0 for deterministic output
    temperature = llm_config.get("temperature", 0.0)

    if provider == "ollama":
        base_url = llm_config.get("url")
        return ChatOllama(model=model_name, base_url=base_url, temperature=temperature)
    elif provider == "openai":
        api_key_value = llm_config.get("api-key")
        if api_key_value and api_key_value.startswith("$"):
            # If the value starts with '$', resolve it as an environment variable
            env_var_name = api_key_value.strip("${}")
            api_key = os.getenv(env_var_name)
            if not api_key:
                raise ValueError(f"Environment variable '{env_var_name}' not found.")
        else:
            api_key = api_key_value

        return ChatOpenAI(model=model_name, api_key=api_key, temperature=temperature)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
