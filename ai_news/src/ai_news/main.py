#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import AiNews

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # inputs = {
    #     'topic': 'AI LLMs',
    #     'date': datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # }

    inputs_array = [
        {
            'topic': 'AI LLMs',
            'current_year': str(datetime.now().year)
        },
        {
            'topic': 'openai',
            'current_year': str(datetime.now().year)
        },
        {
            'topic': 'huggingface',
            'current_year': str(datetime.now().year)
        }
    ]
    
    try:
        for inputs in inputs_array:

            inputs['date'] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            AiNews().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()