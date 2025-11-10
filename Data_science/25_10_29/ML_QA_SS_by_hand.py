from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import torch
import logging, os
from data import *


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SemanticSearch:
    def __init__(self,model_name="DeepPavlov/rubert-base-cased"):
        self.model_name=model_name
        self.context=university_knowledge
        self.qa_pipeline = pipeline(
            "question-answering",
            model=model_name,
            tokenizer=model_name
        )

    def ask(self, question: str):
        result = self.qa_pipeline(question=question, context=self.context)
        print(f'Result : {result}')
        return result['answer'], result['score']
    
if __name__ == "__main__":

    qa_system = SemanticSearch()

    for question in questions:
        answer, score = qa_system.ask(question)
        logger.info(f'Вопрос : {question}\nОтвет : {answer}\nТочность : {score}')