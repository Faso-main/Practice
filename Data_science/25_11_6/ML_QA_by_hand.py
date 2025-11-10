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
        self.model_name=model_name
        self.tokenizer= AutoTokenizer.from_pretrained(model_name)
        self.model=None
        
        self.answer_map={} # mapping класс-ответ

    def set_data(self, hashmap : list):
        # задача метода : вернуть маппинг уникальных ответов
        logger.info("Подготовка данных...")
        questions = []
        answers = []

        for itr in hashmap:
        #{'question': 'Когда работает библиотека?',
        #  'answer': 'Библиотека работает с 9:00 до 18:00'},
            questions.append(itr['question'])
            answers.append(itr['answer'])

        unique_val=list(set(answers))
        self.answer_map = {key:val for key, val in enumerate(unique_val)} # {0: 'Библиотека работает до 18:00'}
        self.label_to_answer = {val: key for key, val in enumerate(unique_val)} # {'Библиотека работает до 18:00' : 0}

        # ответы в числовые метки
        labels = [self.label_to_answer[answer] for answer in answers]

        return questions, labels
    def train(self, hashmap):
        logger.info("Обучение модели...")
        questions, labels = self.set_data(hashmap)

        self.model=AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(self.answer_map)
        )

        def tokenizer(examples):
            return self.tokenizer(examples['text'],
                padding=True,
                trancation=True,
                max_length=128)
        
        dataset=Dataset.from_dict({
            'text': questions,
            'label': labels
        })

        tokenized_dataset=dataset.map(tokenizer, batched=True)

        set_trainer=TrainingArguments(
            output_dir='/Data_science/25_11_6/classifier',
            num_train_epochs=5,
            per_device_train_batch_size=8,
            save_steps=500,
            logging_steps=100)
        
        trainer = Trainer(
            model=self.model,
            args=set_trainer,
            train_dataset=tokenized_dataset,
            tokenizer=self.tokenizer
        )

        logger.info('Начало обучения...')
        trainer.train()
        logger.info('Конец обучения...')

        return trainer


