import openai
import json
import logging
import dataclasses
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@dataclasses.dataclass
class GPTResponse:
    """
    The GPTResponse class is a dataclass for the GPT response
    """
    response_dict: Optional[dict] = None
    g_co2: float = 0.0
    runtime_ms: float = 0.0
    error_status: bool = True
    completion_tokens: int = 0
    prompt_tokens: int = 0

def interpret_response(response: openai.types.chat.chat_completion.ChatCompletion) -> Optional[GPTResponse]:
    """
    The interpret_response function interprets the response from the OpenAI API
    """
    res = GPTResponse()
    if type(response) != openai.types.chat.chat_completion.ChatCompletion:
        logger.warning("Response is not a chat completion, CarbonAI Failure")
        return res
    res.prompt_tokens = response.usage.prompt_tokens
    res.completion_tokens = response.usage.completion_tokens
    if len(response.choices) < 1:
        logger.warning("Response has no choices, CarbonAI Failure")
        return res
    if response.choices[0].finish_reason != "stop":
        logger.warning("Response did not finish, CarbonAI Failure")
        return res
    try:
        assert isinstance(response.choices[0].message, openai.types.chat.chat_completion_message.ChatCompletionMessage)
    except:
        logger.warning("Response message is not a chat completion message, CarbonAI Failure")
        return res
    try:
        assert isinstance(response.choices[0].message.content, str)
    except:
        logger.warning("Response content is not a string, CarbonAI Failure")
        logger.warning("Response content: " + str(response.choices[0].message.content))

        return res
    
    # interpret the message as json string
    try:
        response_dict = json.loads(response.choices[0].message.content)
    except:
        logger.warning("Response content is not a valid json string, CarbonAI Failure")
        logger.warning("Response content: " + str(response.choices[0].message.content))
        raise
        return res
    res.response_dict = response_dict
    try:
        res.g_co2 = float(response_dict["g_co2"])
    except:
        logger.warning("Response does not have g_co2, CarbonAI Failure")
        return res
    try:
        res.runtime_ms = float(response_dict["runtime_ms"])
    except:
        logger.warning("Response does not have runtime_ms, CarbonAI Failure")
        return res
    try:
        res.error_status = str(response_dict["errors"])
        if res.error_status in ["false", "False", "0", "f", "F"]:
            res.error_status = False
        else:
            res.error_status = True
    except:
        logger.warning("Response does not have error status, CarbonAI Failure")
        return res

    
    return res