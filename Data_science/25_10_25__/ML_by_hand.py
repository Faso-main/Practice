from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
from datasets import Dataset
import pandas as pd
import os, torch, logging

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


training_data = [
            ("где находится деканат", "location"),
            ("когда работает библиотека", "time"),
            ("телефон деканата", "contacts"),
            ("нужна справка об обучении", "documents"),
            ("сколько стоит обучение", "payment"),
            ("как подать заявление", "procedure"),
            ("что такое КТ", "definition"),
            ("привет", "greeting"),
            ("пока", "greeting"),
            ("какие документы нужны для поступления", "documents"),
            ("график работы столовой", "time"),
            ("адрес общежития", "location"),
]

class IntentClassfier:
    def __init__(self, hashmap:list,
                 epochs=5,model_name="DeepPavlov/rubert-base-cased"):
        self.model_name=model_name
        self.tokenizer=AutoTokenizer.from_pretrained(model_name)
        self.model=None
        self.label_map={}
        self.hashmap=hashmap
        self.epochs=epochs
        
        self._model_setup()


    def _model_setup(self): # инициализаци модели
        texts = [itr[0] for itr in self.hashmap]
        labels = [itr[1] for itr in self.hashmap]

        # Аппроксимация(mapping меток)
        unique_labels=list(set(labels))
        self.label_map={label:index for index,label in enumerate(unique_labels)}
        
        self.model=AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(unique_labels)
        )

        logger.info('Success : инициализаци')
        
    
    def tokenize_function(self, examples):
        return self.tokenizer(
                examples['text'], 
                padding=True, 
                truncation=True, 
                max_length=64,  # уменьшаем для маленького датасета
                return_tensors="pt"
            )
    
    def set_dataset(self) -> Dataset: # подготовка датасета

        texts = [itr[0] for itr in self.hashmap]
        labels = [itr[1] for itr in self.hashmap]
        
        dataset = []
        for text, label in zip(texts, labels):
            dataset.append({
                'text': text,
                'label': self.label_map[label]
            })

        set_dataset=Dataset.from_list(dataset)

        tokenized_dataset = set_dataset.map(self.tokenize_function,
                                            batched=True)
        
        logger.info('Success : подготовка датасета')
        return tokenized_dataset
        
    

    def train(self): # обучение модели

        # Настройки обучения
        training_args = TrainingArguments(
            output_dir="./intent_classifier",
            num_train_epochs=self.epochs,
            per_device_train_batch_size=8,
            save_steps=500,
            logging_steps=100,
        )

        trainer=Trainer(model=self.model,
                        args=training_args,
                        train_dataset=self.set_dataset())
        
        trainer.train()
        trainer.save_model()
        logger.info('Success : обучение модели')
        return trainer
    
    def predict(self,text): # получение и вывод результата
        request=self.tokenizer(text,
                               return_tensors='pt',
                               padding=True,
                               truncation=True)
        
        self.model.eval()
        with torch.no_grad():
                outputs = self.model(**request)
                probs = torch.softmax(outputs.logits, dim=1)
                predicted_idx = torch.argmax(probs, dim=1).item()
                confidence = probs[0][predicted_idx].item()
            
        reverse_map = {v: k for k, v in self.label_map.items()}
        predicted_label = reverse_map[predicted_idx]
        
        # Детальная информация о предсказании
        all_probs = {reverse_map[i]: float(probs[0][i]) for i in range(len(reverse_map))}
            
        return predicted_label, confidence, all_probs

    
Intent_classifier=IntentClassfier(training_data)
Intent_classifier.train()


for question in ["где столовая?", "какой график работы?", "привет!"]:
    intent, confidence, all_probs = Intent_classifier.predict(question)

    logger.info(f"'{question}' → {intent} ({confidence})")

