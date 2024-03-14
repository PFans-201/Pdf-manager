from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter

class RasaChatbot:
    def __init__(self, model_directory):
        self.interpreter = RasaNLUInterpreter(model_directory)
        self.agent = Agent.load(model_directory, interpreter=self.interpreter)

    def get_response(self, message):
        responses = self.agent.handle_text(message)
        return responses
