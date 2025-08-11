from typing import Dict, Optional

import chainlit as cl
import jwt

from modules.ai.main import get_agent, get_all_base_tools, get_all_custom_tools
from modules.ai.prompts import PROMPT_GENERAL
from settings import SECRET, JWT_ALGORITHM

agent = get_agent(
    system_prompt=PROMPT_GENERAL,
    base_tools=get_all_base_tools(),
    custom_tools=get_all_custom_tools()
)


@cl.header_auth_callback
def header_auth_callback(headers: Dict) -> Optional[cl.User]:
    if headers.get("x-user-jwt"):
        jwt_token = headers.get("x-user-jwt")
        try:
            decoded_payload = jwt.decode(jwt_token, SECRET, algorithms=[JWT_ALGORITHM])
            return cl.User(
                identifier=decoded_payload['user'],
                display_name=decoded_payload['display_name'],
                metadata={"role": 'user', "provider": "header"})
        except jwt.ExpiredSignatureError:
            cl.logger.error("Token has expired.")
            return None
    else:
        return None


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Is going to rain today?",
            message="Is going to rain today?",
        ),
        cl.Starter(
            label="Is going to rain tomorrow?",
            message="Is going to rain tomorrow?",
        ),
        cl.Starter(
            label="tomorrow's weather",
            message="What will the weather be like tomorrow?",
        ),
        cl.Starter(
            label="Next 7 days weather",
            message="Make a weather forecast for the next 7 days. One sentence per day.",
        )
    ]


@cl.on_chat_start
async def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )


@cl.on_message
async def handle_message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()
    app_user = cl.user_session.get("user")
    question = f"user: {app_user.display_name} Content: {message.content}"
    async for event in agent.stream_async(question):
        if "data" in event:
            await msg.stream_token(str(event["data"]))
        elif "message" in event:
            await msg.stream_token("\n")
            message_history.append(event["message"])
        else:
            ...

    await msg.update()
