import openai
import json
import re


class RhinoModelingAssistant:
    """
    A helper class to interact with OpenAI for Rhino 3D modeling tasks:
      - suggest_parameters: get modeling parameters as JSON
      - generate_steps: obtain script modeling steps
      - generate_code: generate Rhino Python script
      - fix_code_with_feedback: adjust code based on Rhino python error or user feedback

      Attributes:
        client (OpenAI): OpenAI API client instance
        model (str): Name of the OpenAI model to use (default: 'gpt-4o')
    """

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initialize the OpenAI client with API credentials.
        
        Args:
            api_key (str): OpenAI API key for authentication
            model (str, optional): Which OpenAI model to use. Defaults to "gpt-4o".
        """
        self.client = openai.OpenAI(api_key = api_key)
        self.model = model

    def suggest_parameters(self, user_input: str) -> dict:
        """
        Generate geometric parameters for architectural modeling based on user description.
    
        Args:
            user_input (str): User's description of desired structure

        Returns:
            dict: Parameters dictionary with nested configuration objects
        """

        # Design the prompt to focus on geometric parameters
        prompt = (
            "You are a proficient Rhino 3D modeling architectual specialist. "
            "Concentrate solely on the geometric construction of the single building's shape." 
            "while maintaining the overall integrity and aesthetic appeal of the architectural model."
            "excluding any considerations of color, texture, or material attributes. "
            f"Provide a set of quantitative parameters essential for the accurate modeling of the specified geometry: \"{user_input}\"\n"
            "RETURN ONLY a single JSON object—nothing else. It must start with '{' and end with '}'.\n"
            "Example format:\n"
            "{\n"
            "  \"height\": { \"default\": 50, \"min\": 20, \"max\": 100, \"step\": 5 },\n"
            "  \"radius\": { \"default\": 10, \"min\": 1, \"max\": 20, \"step\": 1 }\n"
            "}\n"
        )
        # Call the OpenAI API to get the parameters
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        # Extract the JSON response and parse it
        raw = resp.choices[0].message.content.strip()
        return self._parse_json(raw)

    def generate_steps(self, parameters: dict) -> str:
        """
        Create beginner-friendly modeling instructions based on generated parameters.
        
        Provides step-by-step guidance for Rhino novices, including:
        - How to access Python editor
        - Basic workflow instructions
        - Error handling recommendations

        Args:
            parameters (dict): Parameters dictionary from suggest_parameters()

        Returns:
            str: Plaintext instructions with numbered steps and command shortcuts
        """
         
        params_json = json.dumps(parameters)
        prompt = (
            "Describe the step-by-step how to use generated Rhino python script to model for those without experience with Rhino 3D."
            "Provide short cut to command line  to open editor in Rhino."
            "If there are any errors in the code, return here to provide feedback below and adjust through a conversation with the AI."
            "Keep it simple and clear in 5 steps and make sure they know how to use after read."
            f"for these parameters (in JSON):\n{params_json}"
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return resp.choices[0].message.content

    def generate_code(self, parameters: dict) -> str:
        """
        Generate executable Rhino Python script using RhinoScriptSyntax.
        Creates a complete, self-contained script.
    
        Args:
            parameters (dict): Parameters dictionary from suggest_parameters()

        Returns:
            str: Plain Python code without markdown formatting
        """

        params_json = json.dumps(parameters)
        prompt = (
            "Generate runnable Rhino Python code using RhinoScriptSyntax. "
            "Return ONLY the Python function definition (no markdown fences). "
            "The code should be a complete script that can be run in Rhino Python editor. "
            "Remember to call the function with user selected parameters"
            f"given these parameters:\n{params_json}"
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return resp.choices[0].message.content

    def fix_code_with_feedback(self, code: str, feedback: str) -> str:
        """
        Adjust the given Rhino Python script based on error feedback.

        Args:
            code (str): Original problematic code
            feedback (str): Error message/user feedback about issues

        Returns:
            str:Corrected Python code extracted from response.
        """

        prompt = (
            f"Given this Rhino error feedback: {feedback}\n"
            f"Adjust and fix the following Rhino Python script to make it work correctly:\n```python\n{code}\n```"
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        # Extract the content from the response
        raw = response.choices[0].message.content

        # Attempt to extract code between python fences
        match = re.search(r"```python(.*?)```", raw, re.DOTALL)

        print(f"Raw response: {raw}")
        if match:
            return match.group(1).strip()
        return raw

    def _parse_json(self, raw: str) -> dict:
        """
        Internal method to handle JSON parsing from API responses.
        Implements error recovery.

        Args:
            raw (str): Raw text response from API

        Returns:
            dict: Parsed JSON data or empty dict on failure
        """

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            m = re.search(r"(\{[\s\S]*\})", raw)
            if not m:
                return {}
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                return {}
            

    def summarize_code_changes(self, original_code: str, modified_code: str) -> str:
        """
        Summarizes changes made between the original and modified Rhino Python scripts.

        Args:
            original_code (str): The original version of the code.
            modified_code (str): The updated version after applying feedback.

        Returns:
            str: Bullet-point summary of code changes.
        """

        prompt = ("You are a Rhino 3D coding assistant. The user asked for a modification."
        f"Original code: {original_code}"
        f"Modified code: {modified_code}"
        "Please describe what was changed, in clear and concise 3 bullet points."
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content

