from transformers import AutoTokenizer, AutoModelForQuestionAnswering, Trainer, TrainingArguments
import torch

# Get data
raw_data=[
    {
        'context': 'Библиотека работает с 9 утра до 6 вечера.',
        'question': 'Когда работает библиотека?',
        'answer': 'с 9 утра до 6 вечера'  
    },
    {
        'context': 'Деканат находится на третьем этаже.',
        'question': 'Где находится деканат?', 
        'answers': 'на третьем этаже'
    }
]

# Initialize model
model_name='bert-base-multilingual-cased'
tokenizer=AutoTokenizer.from_pretrained(model_name)
model=AutoModelForQuestionAnswering.from_pretrained(model_name)

# Data preparation
def prepare_train_feature(examples):
    tokenized = tokenizer(
        examples['context'],
        examples['question'], 
        truncation=True,
        padding=True,
        max_length=256,
        return_offsets_mapping=True
    )
