import aisuite as ai
from .prompts import CREATE_TOPICS
from .parser import parse_json

class LLM:
    def __init__(self, model="ollama:phi4"):
        self.model = ai.Client()
        self.model = model

    def __call__(self, messages: list):
        return self.model.chat.completions.create(
            model=self.model,
            temperature=0.75,
            messages=messages
        ).choices[0].message.content
    
    def clean_topics(self, topics: list):
        topics_str = "\n".join(topics)
        prompt = CREATE_TOPICS.format(topics=topics_str)
        results = self.__call__([
            {"role": "system", "content": prompt}
        ])
        return parse_json(results)