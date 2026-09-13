# basic imports

import json
from dataclasses import asdict
from google import genai
from google.genai import types
import os

# custom imports

from database import *
from messages import geminiPrompts

class Gemini:
    def __init__(self, batteryThreshold : int):
        # Load Gemini API Token
        self.geminiToken = os.getenv("GEMINI_API_KEY")
        # Load Gemini model name
        self.modelName = os.getenv("GEMINI_MODEL_NAME")
        if self.modelName is None:
            self.modelName = "gemini-3.5-flash-lite"
        # define Gemini client instance
        self.client = genai.Client(api_key = self.geminiToken)
        # initializing HADBData class instance and load data from db
        self.db = HADBData()
        self.batteryPercentList = self.db.getLatestBatteryPercentEntries()
        self.lqiList = self.db.getLatestLQIEntries()
        self.rssiList = self.db.getLatestRSSIEntries()
        self.batteryThreshold = batteryThreshold

        # set payload data
        self.payloadData = {
            "batteriespercent": [asdict(item) for item in self.batteryPercentList],
            "deviseslqi": [asdict(item) for item in self.lqiList ],
            "devicesrssi": [asdict(item) for item in self.rssiList ]
        }
        self.jsonData = json.dumps(self.payloadData, ensure_ascii=False, indent=4, default=str)

        # define precise system instructions
        self.system_instruction = geminiPrompts["plSystemPrompt"].replace("THRESHOLD_MARKER", str(self.batteryThreshold)) # You can add a system prompt in other language - messages.py
        self.promptStart = geminiPrompts["plPromptStart"] # You can add a prompt start in other language - messages.py
        self.promptFull = self.promptStart + self.jsonData

    # method of sending a prompt and returning Gemini response

    def askGemini(self) -> list[str]:
        """
        Sends full request with JSON to Gemini and returns a Markdown response.
        Returns simple string with an error message if something goes
        wrong with an HTTP/API request.
        """
        if self.modelName is None:
            self.modelName = "gemini-3.5-flash-lite"
        tokenCount = self.client.models.count_tokens(
            model=self.modelName, contents=self.promptFull
        )
        print(f"Tokens number in prompt: {str(cast(int, tokenCount.total_tokens))}")
        try:
            response = self.client.models.generate_content(
                model=self.modelName,
                contents=self.promptFull,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.2,  # Low temperature for strict data analysis without hallucinations
                    # Wyłączenie automatycznego wywoływania narzędzi (AFC):
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True)
                )
            )
            # Returning plain text as a response (Markdown format)
            result: str | None = response.text
            if result is None:
                return ["Error in communication with Gemini API\n\nPlease try again later."]
            else:
                return [result, str(cast(int, tokenCount.total_tokens))]
        except Exception as e:
            print(f"Error in communication with Gemini API: {e}")
            return [f"Error in communication with Gemini API: {e}"]