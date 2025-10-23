from transformers import AutoTokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer
from transformers import pipeline
import torch
from datasets import Dataset
import pandas as pd

class QAFineTuner:
    def __init__(self):
        self.model_name = "DeepPavlov/rubert-base-cased"  # Лучшая русская модель
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
    
    def prepare_data(self, qa_pairs):
        """Подготовка данных для fine-tuning"""
        formatted_data = []
        
        for question, answer in qa_pairs:
            # Форматируем в формат для QA
            context = answer  # В нашем случае контекст = ответ
            start_pos = 0
            end_pos = len(answer)
            
            formatted_data.append({
                'question': question,
                'context': context,
                'answers': {
                    'text': [answer],
                    'answer_start': [start_pos],
                    'answer_end': [end_pos]
                }
            })
        
        return Dataset.from_list(formatted_data)
    
    def fine_tune(self, train_dataset, epochs=3):
        """Fine-tuning модели"""
        training_args = TrainingArguments(
            output_dir='./qa_model',
            num_train_epochs=epochs,
            per_device_train_batch_size=8,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir='./logs',
            save_steps=500,
            save_total_limit=2,
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
        )
        
        trainer.train()
        trainer.save_model()
        return trainer

# Пример использования
qa_pairs = [
    ("где находится деканат", "Деканат расположен на улице Ленина, этаж 2"),
    ("когда работает библиотека", "Библиотека работает с 9:00 до 18:00"),
    # ... ваши 1000 пар вопрос-ответ
]

tuner = QAFineTuner()
dataset = tuner.prepare_data(qa_pairs)
trainer = tuner.fine_tune(dataset, epochs=3)