from transformers import AutoTokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer
import torch


# 1. Данные для обучения (строго вопрос-ответ)
train_data = [
    {
        'context': 'Библиотека работает с 9 утра до 6 вечера.',
        'question': 'Когда работает библиотека?',
        'answers': {'text': ['с 9 утра до 6 вечера'], 'answer_start': [16]}
    },
    {
        'context': 'Деканат находится на третьем этаже.',
        'question': 'Где находится деканат?', 
        'answers': {'text': ['на третьем этаже'], 'answer_start': [16]}
    }
]

# 2. Инициализация модели
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
model = AutoModelForQuestionAnswering.from_pretrained("bert-base-multilingual-cased")

# 3. Подготовка данных
def prepare_train_features(examples):
    tokenized = tokenizer(
        examples['question'],
        examples['context'], 
        truncation=True,
        padding=True,
        max_length=256
    )
    
    start_positions = []
    end_positions = []
    
    for i, answers in enumerate(examples['answers']):
        start_char = answers['answer_start'][0]
        end_char = start_char + len(answers['text'][0])
        
        start_positions.append(start_char)
        end_positions.append(end_char)
    
    tokenized['start_positions'] = start_positions
    tokenized['end_positions'] = end_positions
    
    return tokenized

from datasets import Dataset
dataset = Dataset.from_list(train_data)
tokenized_dataset = dataset.map(prepare_train_features, batched=True)

# 4. Обучение
training_args = TrainingArguments(
    output_dir="./qa_model",
    num_train_epochs=3,
    per_device_train_batch_size=8
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

trainer.train()

# 5. Использование
def answer_question(context, question):
    inputs = tokenizer(question, context, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model(**inputs)
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits
        
        start_idx = torch.argmax(start_logits)
        end_idx = torch.argmax(end_logits)
        
        answer_tokens = inputs['input_ids'][0][start_idx:end_idx+1]
        answer = tokenizer.decode(answer_tokens)
        
    return answer

# Тест
context = "Библиотека работает с 9 утра до 6 вечера."
question = "Когда работает библиотека?"
print(answer_question(context, question))  # → "с 9 утра до 6 вечера"