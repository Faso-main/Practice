from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch
import logging
from data import qa_data

logging.basicConfig(level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuestionClassifier:
    def __init__(self, model_name="DeepPavlov/rubert-base-cased"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = None
        self.answer_map = {}  # маппинг: класс -> ответ
        self.is_trained = False
    
    def prepare_data(self, qa_data):
        questions = []
        answers = []
        
        for item in qa_data:
            questions.append(item['question'])
            answers.append(item['answer'])
        
        # Создаем маппинг уникальных ответов
        unique_answers = list(set(answers))
        self.answer_map = {i: answer for i, answer in enumerate(unique_answers)}
        self.label_to_answer = {answer: i for i, answer in enumerate(unique_answers)}
        
        # Конвертируем ответы в числовые метки
        labels = [self.label_to_answer[answer] for answer in answers]
        
        return questions, labels
    
    def train(self, qa_data, epochs=5):
        logger.info("Подготовка данных...")
        questions, labels = self.prepare_data(qa_data)
        
        # Создаем модель
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(self.answer_map)
        )
        
        # Токенизация
        def tokenize_function(examples):
            return self.tokenizer(examples['text'],
                                   padding=True,
                                    truncation=True,
                                      max_length=128)
        
        dataset = Dataset.from_dict({
            'text': questions,
            'label': labels
        })
        
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        # Обучение
        training_args = TrainingArguments(
            output_dir="./classifier",
            num_train_epochs=epochs,
            per_device_train_batch_size=8,
            save_steps=500,
            logging_steps=100,
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
        )
        
        logger.info("Начало обучения...")
        trainer.train()
        self.is_trained = True
        logger.info("Обучение завершено!")
        
        return trainer
    
    def get_answer(self, question):
        """Получить ответ на вопрос"""
        if not self.is_trained:
            return "Модель не обучена"
        
        inputs = self.tokenizer(question, return_tensors='pt', padding=True, truncation=True, max_length=128)
        
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            predicted_idx = torch.argmax(probs, dim=1).item()
            confidence = probs[0][predicted_idx].item()
        
        answer = self.answer_map[predicted_idx]
        return answer, confidence


if __name__ == "__main__":

    logger.info(f"Загружено {len(qa_data)} примеров для обучения")
    
    # Инициализация и обучение
    classifier = QuestionClassifier()
    classifier.train(qa_data, epochs=5)
    
    # Тестирование
    test_questions = [
        "Когда работает библиотека?",
        "Где находится деканат?", 
        "Сколько стоит учеба?",
        "В какое время открыта библиотека?",
        "Какой график работы библиотеки?",
        "Где общежитие?",
        "Какая стипендия?",
        "Где посмотреть расписание?",
        "Какой телефон деканата?",
        "Сколько составляет стипендия?"
    ]
    
    logger.info("ТЕСТИРОВАНИЕ МОДЕЛИ")
    
    for question in test_questions:
        answer, confidence = classifier.get_answer(question)
        logger.info(f"ВОПРОС: {question}")
        logger.info(f"ОТВЕТ: {answer}")
        logger.info(f"УВЕРЕННОСТЬ: {confidence:.3f}")
