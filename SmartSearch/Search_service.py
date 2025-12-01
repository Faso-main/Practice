#!/usr/bin/env python
import re
from typing import List, Dict, Any

import pandas as pd
from rapidfuzz import fuzz
import pymorphy3
from fastapi import FastAPI, Query
from pydantic import BaseModel

# ==========================
#   НАСТРОЙКИ
# ==========================

# Путь к CSV с товарами и категориями
# Можешь поменять на абсолютный, если будешь запускать из другой директории:
# CSV_PATH = "/root/TH3/py_back/rexexp/data/result_itr4.csv"
CSV_PATH = "py_back/rexexp/data/result_itr4.csv"

# Сколько результатов возвращаем
DEFAULT_TOP_K = 10
DEFAULT_MIN_SCORE = 40.0

# Сколько СТЕ/строк спецификаций использовать при сборке описания категории
MAX_PRODUCTS_PER_CAT = 50   # чтобы сильно не раздувать текст
MAX_TOTAL_SPEC_LINES = 200  # на всякий случай, ограничение объёма


# ==========================
#   ИСПРАВЛЕНИЕ РАСКЛАДКИ EN→RU
# ==========================

EN_TO_RU = str.maketrans({
    'q':'й', 'w':'ц', 'e':'у', 'r':'к', 't':'е', 'y':'н', 'u':'г', 'i':'ш', 'o':'щ', 'p':'з', '[':'х', ']':'ъ',
    'a':'ф', 's':'ы', 'd':'в', 'f':'а', 'g':'п', 'h':'р', 'j':'о', 'k':'л', 'l':'д', ';':'ж', '\'':'э',
    'z':'я', 'x':'ч', 'c':'с', 'v':'м', 'b':'и', 'n':'т', 'm':'ь', ',':'б', '.':'ю', '`':'ё'
})


def correct_keyboard_layout(text: str) -> str:
    """Пытаемся починить, если пользователь набрал русский на EN-раскладке."""
    if not text:
        return text
    return text.translate(EN_TO_RU)


# ==========================
#   НОРМАЛИЗАЦИЯ + ЛЕММАТИЗАЦИЯ
# ==========================

_morph = pymorphy3.MorphAnalyzer()

_clear_re = re.compile(r"[^a-zA-Zа-яА-ЯёЁ0-9%/.,\-\s]+")


def normalize_text(text: str) -> str:
    """
    Приводим текст к нижнему регистру, чистим мусор,
    заменяем ё→е, сжимаем пробелы.
    """
    if not text:
        return ""
    text = text.lower()
    text = text.replace("ё", "е")
    text = _clear_re.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def lemmatize_text(text: str) -> str:
    """
    Лемматизация русских слов через pymorphy3.
    Для смешанного текста (русский+цифры) работает нормально.
    """
    text = normalize_text(text)
    if not text:
        return ""

    tokens = text.split()
    lemmas = []

    for token in tokens:
        # если чисто цифры/проценты — оставляем как есть
        if re.fullmatch(r"[0-9%/.\-]+", token):
            lemmas.append(token)
            continue

        parsed = _morph.parse(token)
        if not parsed:
            lemmas.append(token)
        else:
            lemmas.append(parsed[0].normal_form)

    return " ".join(lemmas)


# ==========================
#   СБОРКА КАТЕГОРИЙ ИЗ CSV
# ==========================

def load_categories_from_csv() -> pd.DataFrame:
    """
    Читаем result_itr4.csv (СТЕ) и агрегируем всё до уровня категории.

    Ожидаемые колонки в CSV:
      - id_сте
      - название_сте
      - id_категории
      - название_категории
      - производитель
      - страна_происхождения
      - spec1..spec31 (строки вида "Ключ: Значение")
    """
    df = pd.read_csv(CSV_PATH)

    # Приводим названия колонок к ожидаемым (на случай, если pandas подтянул NaN и т.п.)
    required_cols = ["id_категории", "название_категории"]
    for col in required_cols:
        if col not in df.columns:
            raise RuntimeError(f"В CSV нет обязательной колонки '{col}'")

    # Собираем текст по каждой строке СТЕ: название + спец-строки
    spec_cols = [c for c in df.columns if c.startswith("spec")]

    def build_ste_text(row) -> str:
        parts = []
        ste_name = str(row.get("название_сте") or "").strip()
        if ste_name:
            parts.append(ste_name)

        for col in spec_cols:
            val = row.get(col)
            if isinstance(val, float) and pd.isna(val):
                continue
            val = str(val or "").strip()
            if val:
                parts.append(val)

        return "; ".join(parts)

    df["ste_text"] = df.apply(build_ste_text, axis=1)

    # Агрегируем до уровня категории
    # Берем первые N товаров на категорию, чтобы не раздувать описания до безумия
    df_sorted = df.sort_values(["id_категории", "id_сте"])

    grouped_rows = []
    for cat_id, group in df_sorted.groupby("id_категории"):
        cat_name = str(group["название_категории"].iloc[0] or "").strip()

        # берем ограниченное число строк
        g = group.head(MAX_PRODUCTS_PER_CAT)

        # берем ste_text и склеиваем
        texts = []
        for _, row in g.iterrows():
            t = str(row["ste_text"] or "").strip()
            if t:
                texts.append(t)
            if len(texts) >= MAX_TOTAL_SPEC_LINES:
                break

        category_desc = " | ".join(texts)

        grouped_rows.append(
            {
                "id_категории": int(cat_id),
                "название_категории": cat_name,
                "category_desc_raw": category_desc,
            }
        )

    cat_df = pd.DataFrame(grouped_rows)
    return cat_df


def build_index_from_csv() -> pd.DataFrame:
    """
    Строим индекс: нормализованные / лемматизированные поля для поиска.
    """
    df = load_categories_from_csv()

    df["name_norm"] = df["название_категории"].fillna("").astype(str).apply(
        lambda s: lemmatize_text(correct_keyboard_layout(s))
    )
    df["desc_norm"] = df["category_desc_raw"].fillna("").astype(str).apply(
        lambda s: lemmatize_text(correct_keyboard_layout(s))
    )

    df["full_norm"] = (df["name_norm"] + " " + df["desc_norm"]).str.strip()

    return df


# ==========================
#   ПОИСК
# ==========================

def smart_search(
    cat_df: pd.DataFrame,
    query: str,
    top_k: int = DEFAULT_TOP_K,
    min_score: float = DEFAULT_MIN_SCORE,
) -> List[Dict[str, Any]]:
    """
    Умный поиск по DataFrame категорий:
    - исправление раскладки
    - нормализация и лемматизация запроса
    - fuzzy по названию и описанию
    """
    query = (query or "").strip()
    if not query:
        return []

    query_fixed = correct_keyboard_layout(query)
    query_lem = lemmatize_text(query_fixed)

    if not query_lem:
        return []

    results: List[Dict[str, Any]] = []

    for _, row in cat_df.iterrows():
        name_norm = row["name_norm"]
        desc_norm = row["desc_norm"]

        score_name = fuzz.WRatio(query_lem, name_norm) if name_norm else 0.0
        score_desc = fuzz.WRatio(query_lem, desc_norm) if desc_norm else 0.0

        final_score = max(score_name, score_desc * 0.7)

        if final_score < min_score:
            continue

        results.append(
            {
                "id": int(row["id_категории"]),
                "name": row["название_категории"],
                "description": row["category_desc_raw"],
                "score": float(final_score),
                "score_name": float(score_name),
                "score_desc": float(score_desc),
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# ==========================
#   FASTAPI СЕРВИС
# ==========================

app = FastAPI(title="TH3 Smart Search (CSV-based)")

cat_index: pd.DataFrame | None = None


class SearchResult(BaseModel):
    id: int
    name: str
    description: str | None = None
    score: float
    score_name: float
    score_desc: float


@app.on_event("startup")
def on_startup():
    global cat_index
    print(f"Загрузка категорий из CSV: {CSV_PATH}")
    cat_index = build_index_from_csv()
    print(f"Индекс готов, категорий: {len(cat_index)}")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "categories_indexed": 0 if cat_index is None else len(cat_index),
        "csv_path": CSV_PATH,
    }


@app.post("/reload")
def reload_index():
    """
    Пересобрать индекс (можно дергать после обновления CSV).
    """
    global cat_index
    cat_index = build_index_from_csv()
    return {"status": "reloaded", "categories_indexed": len(cat_index)}


@app.get("/search/categories", response_model=List[SearchResult])
def search_categories(
    q: str = Query(..., min_length=1),
    top_k: int = Query(DEFAULT_TOP_K, ge=1, le=50),
    min_score: float = Query(DEFAULT_MIN_SCORE, ge=0.0, le=100.0),
):
    global cat_index
    if cat_index is None or cat_index.empty:
        return []

    results = smart_search(cat_index, q, top_k=top_k, min_score=min_score)
    return [SearchResult(**r) for r in results]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "search_service:app",
        host="127.0.0.1",
        port=8001,
        reload=False,
        workers=1,
    )