# Carbon-AI

Welcome to **Carbon-AI**, an open-source tool designed to estimate the carbon impact of software functions in real-time. This fantastic tool empowers developers to make environmentally conscious decisions by providing insights into the carbon footprint of their code.

Nothing says "caring about your environmental impact" like using the latest in LLM technology to evaluate
the impact of your code!

## Features

- ⏱️ **Real-Time Analysis**: Get immediate feedback on the carbon impact of your software functions, at run-time!  No valuable time needs to be wasted during development, everything happens in real-time when the code is executed.
- 👩‍💻 **Easy Integration**: Seamlessly integrate Carbon-AI into your existing development workflow.
- 🌎 **Open Source**: Modified MIT License for flexibility in deploying this in your own software.
- 🤖 **Large Language Model Integration**: Use the power of the latest and greatest AI tools available to evaluate your software's carbon footprint.
- ☁️ **Cloud-Based Technology**: Do you have any components of your tech stack which aren't utilizing the power of the cloud?  Just import this library and you can make any function use cloud resources!

## How It Works

Once you've installed the carbon_ai library, and provided a correct API token for OpenAI, then you can use the class to add an
`evaluate_impact` decorator onto any of your functions.  This causes your function, upon being run, to send a copy of itself (the code and the 
arguments) to the OpenAI LLM, where it will handle the heavy lifting of computing the carbon dioxide emissions, in grams CO2, 
that would be generated by that function.  This information will be logged with the logger library, at `INFO` level.

Functionality is provided to choose different GPT agents, to balance expense and accuracy.

## Getting Started

To get started with Carbon-AI, follow these steps:

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/chefmayhem/carbon-ai.git
    ```
2. **Install Package**:
    We recommend using a virtual environment manager, such as venv or conda.
    From the base carbon-ai directory
    ```sh
    pip install .
    ```

3. **Configuration**:
    Utilizing the OpenAI tools requires a working API key.  You can find yours at
    `https://platform.openai.com/api-keys`.  Then, there are several ways of providing the key to
    the CarbonAI software.

    * Create a file named login_info.json, in the proper json format, looking something like...
    ```json
    {
        "key": "<your key here>"
    }
    ```
    * Save the key in an environment variable `"OPENAI_API_KEY"`
    * Save the key in another environment variable, and specify it using the `reset_login` function.
    * Specify the key directly using the `reset_login` function.

    If a valid key is not provided, the function may fall back to a back-of-the-envelope estimation
    based on the length of time it takes to run the function.  This method loses all of the benefits of
    the LLM technology which powers Carbon AI.

4. **Run the Tool**:
    See the `examples/find_primes.py` for a nice example of using this.  Effectively, it goes like...

    ```python
    from carbon_ai import CarbonAI

    cai_instance = CarbonAI()

    @cai_instance.evaluate_impact
    def your_function_here(arg1, arg2):
        # do the thing
        pass
        return True
    ```

    After this, any time the function is called, it will perform an evaluation of the function's
    carbon emissions impact.  A message will be returned via logging at the `INFO` level, like...

    ```
    INFO:carbon_ai.carbon_ai:Estimated CO2 emissions: 0.05 grams
    ```

## License

This project is licensed under a modified MIT License. See the [LICENSE](LICENSE.txt) file for details.

## Contact

For questions or feedback... discuss with your friends!

Join us in making software development more sustainable with Carbon-AI!  You can be a 10x developer with 1000x the impact using Carbon-AI!
