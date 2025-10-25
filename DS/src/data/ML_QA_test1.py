from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
from datasets import Dataset
import torch
import os

# Добавляем if __name__ для multiprocessing
if __name__ == "__main__":
    
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
        ("где столовая", "location"),  # Добавим больше примеров
        ("время работы столовой", "time"),
        ("как связаться с деканатом", "contacts"),
    ]

    class IntentClassifier:
        def __init__(self, hashmap: list, epochs=10, model_name="cointegrated/rubert-tiny2"):  # Используем легкую модель
            self.model_name = model_name
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = None
            self.label_map = {}
            self.hashmap = hashmap
            self.epochs = epochs
            self.is_trained = False
            self._initialize_model()
        
        def _initialize_model(self):
            """Инициализация модели"""
            print("🔧 Инициализируем модель...")
            texts = [itr[0] for itr in self.hashmap]
            labels = [itr[1] for itr in self.hashmap]
            
            # Анализ данных
            unique_labels = sorted(list(set(labels)))
            self.label_map = {label: index for index, label in enumerate(unique_labels)}
            
            print(f"📊 Статистика данных:")
            print(f"   Всего примеров: {len(texts)}")
            print(f"   Уникальные классы: {unique_labels}")
            print(f"   Распределение классов:")
            for label in unique_labels:
                count = labels.count(label)
                print(f"     {label}: {count} примеров ({count/len(labels)*100:.1f}%)")
            
            # Используем легкую модель для быстрого тестирования
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=len(unique_labels)
            )
            print("✅ Модель инициализирована")
        
        def tokenize_function(self, examples):
            """Функция токенизации"""
            return self.tokenizer(
                examples['text'], 
                padding=True, 
                truncation=True, 
                max_length=64,  # Уменьшаем для маленького датасета
                return_tensors="pt"
            )
        
        def prepare_data(self):
            """Подготовка данных"""
            texts = [itr[0] for itr in self.hashmap]
            labels = [itr[1] for itr in self.hashmap]
            numeric_labels = [self.label_map[label] for label in labels]
            
            dataset = Dataset.from_dict({
                'text': texts,
                'label': numeric_labels
            })
            
            tokenized_dataset = dataset.map(self.tokenize_function, batched=True)
            print(f"✅ Данные подготовлены: {len(tokenized_dataset)} примеров")
            return tokenized_dataset
        
        def train(self):
            """Обучение модели с улучшенными настройками"""
            tokenized_dataset = self.prepare_data()
            
            # Улучшенные настройки для маленького датасета
            training_args = TrainingArguments(
                output_dir="./intent_classifier",
                num_train_epochs=self.epochs,
                per_device_train_batch_size=4,  # Уменьшаем batch size
                per_device_eval_batch_size=4,
                learning_rate=1e-4,  # Увеличиваем learning rate
                warmup_steps=20,
                weight_decay=0.01,
                logging_dir="./logs",
                logging_steps=10,
                save_steps=100,
                evaluation_strategy="no",
                save_total_limit=1,
                report_to=None,  # Отключаем отчеты
                dataloader_pin_memory=False,  # Для Windows
            )
            
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=tokenized_dataset,
            )
            
            print("🚀 Начинаем обучение...")
            train_result = trainer.train()
            trainer.save_model()
            self.is_trained = True
            
            print("📈 Результаты обучения:")
            print(f"   Final loss: {train_result.metrics['train_loss']:.4f}")
            print("✅ Обучение завершено!")
            return trainer
        
        def predict(self, text):
            """Предсказание с детальной диагностикой"""
            if not self.is_trained:
                raise ValueError("Сначала обучите модель!")
            
            inputs = self.tokenizer(
                text,
                return_tensors='pt',
                padding=True,
                truncation=True,
                max_length=64
            )
            
            self.model.eval()
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.softmax(outputs.logits, dim=1)
                predicted_idx = torch.argmax(probs, dim=1).item()
                confidence = probs[0][predicted_idx].item()
            
            reverse_map = {v: k for k, v in self.label_map.items()}
            predicted_label = reverse_map[predicted_idx]
            
            # Детальная информация о предсказании
            all_probs = {reverse_map[i]: float(probs[0][i]) for i in range(len(reverse_map))}
            
            return predicted_label, confidence, all_probs

    # Использование
    print("🎯 ЗАПУСК КЛАССИФИКАТОРА НАМЕРЕНИЙ")
    print("=" * 50)
    
    classifier = IntentClassifier(training_data, epochs=15)  # Увеличиваем эпохи
    classifier.train()
    
    print("\n🧪 ТЕСТИРУЕМ МОДЕЛЬ:")
    print("=" * 50)
    
    test_questions = [
        "где столовая?", 
        "какой график работы?", 
        "привет!",
        "мне нужна справка",
        "адрес деканата",
        "телефон библиотеки"
    ]
    
    for question in test_questions:
        try:
            intent, confidence, all_probs = classifier.predict(question)
            print(f"\n📝 Вопрос: '{question}'")
            print(f"🎯 Предсказание: {intent} (уверенность: {confidence:.3f})")
            print(f"📊 Все вероятности:")
            for label, prob in sorted(all_probs.items(), key=lambda x: x[1], reverse=True):
                print(f"   {label}: {prob:.3f}")
        except Exception as e:
            print(f"❌ Ошибка для '{question}': {e}")