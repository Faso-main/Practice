from transformers import AutoTokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer
import torch
from datasets import Dataset

# 1. Данные для обучения (упрощенная структура)
raw_data = [
    {
        'context': 'Библиотека работает с 9 утра до 6 вечера.',
        'question': 'Когда работает библиотека?',
        'answer': 'с 9 утра до 6 вечера'  
    },
    {
        'context': 'Деканат находится на третьем этаже.',
        'question': 'Где находится деканат?', 
        'answer': 'на третьем этаже'
    }
]

# 2. Инициализация модели
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
model = AutoModelForQuestionAnswering.from_pretrained("bert-base-multilingual-cased")

# 3. Подготовка данных с автоматическим вычислением позиций
def prepare_train_features(examples):
    # Добавляем answer_start автоматически
    for i in range(len(examples['context'])):
        context = examples['context'][i]
        answer = examples['answer'][i]
        start_char = context.find(answer)
        if start_char == -1:
            raise ValueError(f"Ответ '{answer}' не найден в контексте: '{context}'")
        examples.setdefault('answer_start', []).append(start_char)
    
    # Токенизация
    tokenized = tokenizer(
        examples['question'],
        examples['context'], 
        truncation=True,
        padding=True,
        max_length=256,
        return_offsets_mapping=True  # для корректного mapping токенов
    )
    
    # Конвертируем символьные позиции в токенные
    start_positions = []
    end_positions = []
    
    for i, offset_mapping in enumerate(tokenized['offset_mapping']):
        start_char = examples['answer_start'][i]
        end_char = start_char + len(examples['answer'][i])
        
        # Ищем start и end токены
        start_token = None
        end_token = None
        
        for token_idx, (start, end) in enumerate(offset_mapping):
            if start <= start_char < end:
                start_token = token_idx
            if start < end_char <= end:
                end_token = token_idx
                break
        
        # Если не нашли, используем первый/последний токен
        start_positions.append(start_token if start_token is not None else 0)
        end_positions.append(end_token if end_token is not None else len(offset_mapping)-1)
    
    tokenized['start_positions'] = start_positions
    tokenized['end_positions'] = end_positions
    
    # Убираем offsets_mapping т.к. он не нужен для обучения
    tokenized.pop('offset_mapping')
    
    return tokenized

# 4. Создаем датасет и обрабатываем
dataset = Dataset.from_list(raw_data)
tokenized_dataset = dataset.map(prepare_train_features, batched=True)

# 5. Обучение
training_args = TrainingArguments(
    output_dir="./qa_model",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    logging_steps=10,
    save_steps=100
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

trainer.train()

# 6. Использование
def answer_question(context, question):
    inputs = tokenizer(question, context, return_tensors='pt', truncation=True, max_length=256)
    
    with torch.no_grad():
        outputs = model(**inputs)
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits
        
        start_idx = torch.argmax(start_logits)
        end_idx = torch.argmax(end_logits)
        
        answer_tokens = inputs['input_ids'][0][start_idx:end_idx+1]
        answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)
        
    return answer

# Тест
context = "Библиотека работает с 9 утра до 6 вечера."
question = "Когда работает библиотека?"
result = answer_question(context, question)
print(f"Вопрос: {question}")
print(f"Ответ: {result}")