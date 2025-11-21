# filename: generate_categories_fixed.py
import pandas as pd
import os, logging
import json
import re
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ------------------- ПУТИ -------------------
DATA_PATH = os.path.join('Data_science','TenderHack','data', 'split.csv')
OUTPUT_JSON = os.path.join('Data_science','TenderHack', 'auto_categories_bertopic.json')

# ------------------- ЧТЕНИЕ ДАННЫХ -------------------
logger.info("Читаем данные...")
df = pd.read_csv(DATA_PATH, on_bad_lines='skip', dtype=str)  # всё как строки

# Главное: берём specification, а не id2!
if 'specification' in df.columns:
    texts = df['specification'].fillna('').astype(str)
else:
    logger.info("Колонки specification нет! Используем id2 как fallback (плохой вариант)")
    texts = df['id2'].fillna('').astype(str)

logger.info(f"Всего строк: {len(texts)}")

# ------------------- ОЧИСТКА ТЕКСТА -------------------
def clean_text(t):
    t = str(t).lower()
    t = re.sub(r'[^а-яa-z0-9\s]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t if len(t) > 3 else "пусто"

texts_clean = texts.apply(clean_text)
valid_texts = [t for t in texts_clean if t != "пусто"]

logger.info(f"После очистки используем: {len(valid_texts)} строк")

# ------------------- BERTopic (РАБОЧАЯ ВЕРСИЯ) -------------------
logger.info("Запускаем BERTopic...")

vectorizer = CountVectorizer(
    ngram_range=(1, 2),
    min_df=3,
    max_df=0.8,
    stop_words=[]  # не убираем "для", "и" — они важны!
)

ctfidf = ClassTfidfTransformer(reduce_frequent_words=True)

topic_model = BERTopic(
    language="russian",
    vectorizer_model=vectorizer,
    ctfidf_model=ctfidf,
    nr_topics="auto",           # автообъединение похожих тем
    calculate_probabilities=False,
    verbose=True
)

logger.info("Фитим модель...")
topics, _ = topic_model.fit_transform(valid_texts)

# ------------------- ИЕРАРХИЯ -------------------
logger.info("Строим иерархию...")
hierarchical_topics = topic_model.hierarchical_topics(valid_texts)

# ------------------- ФОРМИРОВАНИЕ РЕЗУЛЬТАТА -------------------
result = []
seen = set()

for i, row in hierarchical_topics.iterrows():
    # Уровень: чем больше расстояние — тем выше (грубее) кластер
    distance = row.get('Distance', 0)
    level = 0 if distance > 0.6 else 1  # подбери под свои данные

    # Ключевые слова — из Parent_Name или из топиков
    parent_name = str(row['Parent_Name']).strip()
    if parent_name == "nan" or not parent_name:
        parent_name = "другое"

    # Собираем слова из дочерних топиков
    child_topics = row['Topics']
    keywords = set()
    for topic_id in child_topics:
        if topic_id == -1:
            continue
        try:
            words = topic_model.get_topic(topic_id)
            keywords.update([w[0] for w in words[:10] if w[1] > 0.01])
        except:
            continue

    keywords = list(keywords)[:15]
    if not keywords:
        keywords = parent_name.split()[:3]

    # Формируем путь
    if level == 0:
        path = parent_name.title()
    else:
        # Ищем родителя уровня 0
        parent_level0 = next((r["category_path"] for r in result if r["level"] == 0), None)
        if parent_level0:
            path = f"{parent_level0} -> {parent_name.title()}"
        else:
            path = f"Общее -> {parent_name.title()}"

    if path in seen:
        continue
    seen.add(path)

    result.append({
        "category_path": path,
        "keywords": keywords,
        "level": level
    })

# ------------------- ДОБАВЛЯЕМ ОСНОВНЫЕ КАТЕГОРИИ, если их нет -------------------
main_cats = ["техника", "мебель", "канцелярия", "расходные материалы", "хозяйственные товары", "спецодежда", "оборудование"]
for cat in main_cats:
    if not any(cat.lower() in r["category_path"].lower() for r in result):
        result.insert(0, {
            "category_path": cat,
            "keywords": [cat.split()[-1], cat.replace(" ", "_")],
            "level": 0
        })

# ------------------- СОХРАНЕНИЕ -------------------
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

logger.info(f"\nГОТОВО! Сохранено {len(result)} категорий в:")
logger.info(OUTPUT_JSON)

# ------------------- ВЫВОД ТОП-ТЕМ -------------------
logger.info("\nТоп-15 тем:")
info = topic_model.get_topic_info().head(15)
for _, row in info.iterrows():
    if row.Topic == -1:
        logger.info(f"  Шум: {row.Count} элементов")
        continue
    words = [w[0] for w in topic_model.get_topic(row.Topic)[:6]]
    logger.info(f"  {row.Topic:2d} | {row.Count:5d} | {', '.join(words)}")