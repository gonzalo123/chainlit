import logging
from typing import List

from botocore.config import Config
from strands import Agent
from strands import tool
from strands.models import BedrockModel
from strands_tools import calculator, current_time, think, batch
from strands_tools.browser import AgentCoreBrowser
from strands_tools.code_interpreter.agent_core_code_interpreter import AgentCoreCodeInterpreter

from modules.ai.tools import WeatherTools
from settings import (
    IA_MODEL, IA_TEMPERATURE, LLM_READ_TIMEOUT, LLM_CONNECT_TIMEOUT,
    LLM_MAX_ATTEMPTS, MY_LATITUDE, MY_LONGITUDE, AWS_REGION)

logger = logging.getLogger(__name__)


def get_all_base_tools() -> List[tool]:
    code_interpreter = AgentCoreCodeInterpreter(region=AWS_REGION)
    browser_client = AgentCoreBrowser(region=AWS_REGION)
    return [calculator, think, code_interpreter.code_interpreter, current_time, batch, browser_client.browser]


def get_all_custom_tools() -> List[tool]:
    custom_tools = []
    custom_tools += WeatherTools(latitude=MY_LATITUDE, longitude=MY_LONGITUDE).get_tools()

    return custom_tools


def get_agent(
        system_prompt: str,
        base_tools: List[tool] = None,
        custom_tools: List[tool] = None,
        *,
        read_timeout: int = LLM_READ_TIMEOUT,
        connect_timeout: int = LLM_CONNECT_TIMEOUT,
        max_attempts: int = LLM_MAX_ATTEMPTS) -> Agent:
    config = Config(
        read_timeout=read_timeout,
        connect_timeout=connect_timeout,
        retries={'max_attempts': max_attempts}
    )
    base_tools = base_tools if base_tools is not None else []
    custom_tools = custom_tools if custom_tools is not None else []
    all_tools = base_tools + custom_tools

    bedrock_model = BedrockModel(
        model_id=IA_MODEL,
        temperature=IA_TEMPERATURE,
        boto_client_config=config,
    )
    return Agent(
        model=bedrock_model,
        tools=all_tools,
        system_prompt=system_prompt
    )
