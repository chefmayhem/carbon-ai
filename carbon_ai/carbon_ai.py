# carbon_ai.py
# Main file for the Carbon AI package
# Author: chefmayhem

import time
import inspect
import json
from functools import wraps
from openai import OpenAI
from openai import types as openaitypes
import logging
import dataclasses
from typing import Optional
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CarbonAI:
    """
    The CarbonAI class is the main class for the Carbon AI package
    We track important login information for 10x convenience and efficiency
    We also provide the functions here for true power users who want to achieve
    the most out of their coding experience.
    We also 10x some other things that you probably haven't even thought of yet!
    Coders who don't use this class are probably not 10xing their code.
    """
    # class parameters
    def __init__(self):
        self.login_secret = None
        self.login_org = None
        self.login_proj = None
        self._debug_mode = False
        self._model_name = "gpt-4o-mini"
        self.load_secret("./login_info.json")
        self.client = OpenAI(api_key=self.login_secret)
        #self.client = OpenAI(organization=self.login_org, project=self.login_proj)

    def set_model_name(self, model_name):
        """
        Set the OpenAI model name, examples include "gpt-4o", "gpt-4o-mini", "gpt-4o-turbo", and "gpt-3.5-turbo"
        """
        self._model_name = model_name

    def set_debug_mode(self, debug_mode):
        """
        Set the debug mode for the CarbonAI class
        """
        self._debug_mode = debug_mode

    def load_secret(self, secret_file):
        """
        The load_secret function loads the secret from a file

        """
        try:
            with open(secret_file, "r") as f:
                login_dict = json.load(f)
                if "key" in login_dict:
                    self.login_secret = login_dict["key"]
                if "org" in login_dict:
                    self.login_org = login_dict["org"]
                if "proj" in login_dict:
                    self.login_proj = login_dict["proj"]
        except: 
            logger.warning("Could not load secret file")
            self.login_secret = None
            self.login_org = None
            self.login_proj = None

    def prepare_input_content(self, func, args, kwargs)->str:
        """
        The prepare_input_content function prepares the input content for the chatbot
        """
        func_lines = inspect.getsource(func)
        input_content = {
                "function_code": func_lines,
                "function_args": json.dumps({"args": args, "kwargs": kwargs})
        }

        return json.dumps(input_content)

    # We create the decorator to process any function brought in
    def evaluate_impact(self, func):
        # We use wraps to preserve the metadata of the original function
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Let's be verbose while we learn
            logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")

            func_lines = inspect.getsource(func)
            logger.debug("Function code:")
            logger.debug(f"Function code: {func_lines}")

            # We start by getting the time before the function is called
            start_time = time.perf_counter()

            # We call the function
            result = func(*args, **kwargs)

            # We get the time after the function is called
            end_time = time.perf_counter()

            # Here's the ChatGPT messsage
            if self.client is not None:
                response = self.client.chat.completions.create(
                    response_format={"type": "json_object"},
                    messages=[
                        {
                            "role": "system",
                            "content": ("Your job is to estimate the climate impact of running this function.  You will be provided with the function code, and the function arguments, in json format.  "
                                    + "You will return results in json format, with keys g_co2, runtime_ms, and errors.  The errors response is a boolean, and should be true if you are unable to estimate the impact.  "
                                    + "The g_co2 value should be an estimate of the total grams of CO2 emitted by running this function.  The runtime_ms value should be the estimated runtime of the function in milliseconds.  "
                                    + "Assume the function is running on an x86 consumer desktop computer, and do not consider the impact of this evaluation request.  "
                                    + "If you choose to run the function to estimate the impact, feel free to add in any imports you might need.  "
                                    + "If you are unable to estimate the impact, please set the errors value to true, and do not provide the g_co2 or runtime_ms values.")
                        },
                        {
                            "role": "user",
                            "content": self.prepare_input_content(func, args, kwargs)
                        }
                    ],
                    model=self._model_name
                )
                res = interpret_response(response)

                if res.error_status:
                    logger.warning("Error status in response, CarbonAI Failure")
                else:
                    logger.info(f"Estimated CO2 emissions: {res.g_co2} grams")

            else:
                raise ValueError("OpenAI client not initialized")

            # We calculate the time taken
            time_taken = end_time - start_time

            # We print the time taken
            logger.debug(f"Time taken to run {func.__name__}: {time_taken}")

            # We return the result
            if not self._debug_mode:
                return result
            else:
                return result, response
        return wrapper
    
    def back_of_envelope_estimate(self, runtime_s: float):
        """
        Use the following very rough assumptions:
        1. An typical averaged desktop or laptop uses around 60 Watts of power
        2. The carbon intensity of the US grid is around 0.42 kg CO2 per kWh
        3. Approximately half of the computer's power is used for the function
           to be measured, the rest may be OS tasks, other programs, etc.
        Thus, we estimate the CO2 as 3.5 mg/s * runtime_s
        """
        return 0.0035 * runtime_s
    
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

def interpret_response(response: openaitypes.chat.chat_completion.ChatCompletion) -> Optional[GPTResponse]:
    """
    The interpret_response function interprets the response from the OpenAI API
    """
    res = GPTResponse()
    if type(response) != openaitypes.chat.chat_completion.ChatCompletion:
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
        assert isinstance(response.choices[0].message, openaitypes.chat.chat_completion_message.ChatCompletionMessage)
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