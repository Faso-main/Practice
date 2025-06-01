import pandas as pd
import re
from bs4 import BeautifulSoup
import PyPDF2  # для PDF

def load_text_data(file_path: str) -> list[str]:
    """Загрузка текста из файла (поддержка CSV, JSON, PDF и др.)."""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        return df['text'].tolist()
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return [page.extract_text() for page in reader.pages]
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    else:
        raise ValueError(f"Unsupported format: {file_path}")

def clean_text(text: str) -> str:
    """Очистка текста."""
    text = BeautifulSoup(text, 'html.parser').get_text()  # удаление HTML
    text = re.sub(r'[^\w\s]', '', text)  # только буквы и пробелы
    return text.strip()

def create_dataframe(texts: list[str]) -> pd.DataFrame:
    """Формирование DataFrame с NLP-признаками."""
    df = pd.DataFrame({'raw_text': texts})
    df['cleaned_text'] = df['raw_text'].apply(clean_text)
    df['token_count'] = df['cleaned_text'].apply(lambda x: len(x.split()))
    df = df[df['token_count'] > 5]  # фильтрация слишком коротких текстов
    return df

# Пример использования
texts = load_text_data("data.pdf")  # или data.csv, data.json
df = create_dataframe(texts)
print(df.head())