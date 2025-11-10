"""
вход: ворпос пользователя (как жить?)
выход: ответ от обученой пониманию модели(жить нужно правильно)

анализ: 
ML
fine-tuning OR SS
id(300-1000)

токенизация: контекст - вопрос, ответ - последоватльно
требования к базе знаний: 

"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch, logging
from data import qa_data

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger=logging.getLogger(__name__)

class QAClassifier:
    def __init__(self, model_name="DeepPavlov/rubert-base-cased"):
        self.model=model_name
        self.tokenizer= AutoTokenizer.from_pretrained(model_name)
        self.model=None
        
        self.answer_map={} # mapping класс-ответ
        self.is_trained = False

    def set_data(self, hashmap : list):
        # задача метода : вернуть маппинг уникальных ответов
        questions = []
        answers = []

        for itr in hashmap:
        #{'question': 'Когда работает библиотека?',
        #  'answer': 'Библиотека работает с 9:00 до 18:00'},
            questions.append(itr['question'])
            answers.append(itr['answer'])

        unique_val=list(set(answers))
        self.answer_map = {key:val for key, val in enumerate(unique_val)}
        self.label_to_answer = {val: key for key, val in enumerate(unique_val)}

        # ответы в числовые метки
        labels = [self.label_to_answer[answer] for answer in answers]

        return questions, labels


