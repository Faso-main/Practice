from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import torch
import logging
from data import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealQA:
    def __init__(self, model_name="DeepPavlov/rubert-base-cased"):
        self.model_name = model_name
        self.qa_pipeline = pipeline(
            "question-answering",
            model=model_name,
            tokenizer=model_name
        )
        
    def add_context(self, context: str):
        self.context = context
    
    def ask(self, question: str):

        result = self.qa_pipeline(question=question, context=self.context)
        return result['answer'], result['score']

if __name__ == "__main__":
    qa_system = RealQA()
    qa_system.add_context(university_knowledge)
    
    
    for question in questions:
        answer, confidence = qa_system.ask(question)
        logger.info(f"Вопрос: {question}")
        logger.info(f"Ответ: {answer} (уверенность: {confidence:.3f})")
        print()