import re
import sys
import pandas as pd
from rapidfuzz import fuzz
import pymorphy3

CSV_PATH = "result_itr4.csv"  # поменяй путь, если нужно

# ---------- 1. Исправление раскладки EN → RU ----------

EN_TO_RU = str.maketrans({
    'q':'й', 'w':'ц', 'e':'у', 'r':'к', 't':'е', 'y':'н', 'u':'г', 'i':'ш', 'o':'щ', 'p':'з', '[':'х', ']':'ъ',
    'a':'ф', 's':'ы', 'd':'в', 'f':'а', 'g':'п', 'h':'р', 'j':'о', 'k':'л', 'l':'д', ';':'ж', '\'':'э',
    'z':'я', 'x':'ч', 'c':'с', 'v':'м', 'b':'и', 'n':'т', 'm':'ь', ',':'б', '.':'ю', '`':'ё'
})

def fix_layout_en_to_ru(text: str) -> str:
    return text.translate(EN_TO_RU)

# ---------- 2. Нормализация + лемматизация ----------

morph = pymorphy3.MorphAnalyzer(lang="ru")
WORD_RE = re.compile(r"[a-zа-я0-9]+", re.IGNORECASE)

def normalize_and_lemmatize(text: str) -> str:
    """
    - lower
    - заменить ё → е
    - вытащить токены
    - для русских слов взять normal_form
    """
    text = str(text).lower()
    text = text.replace("ё", "е")
    words = WORD_RE.findall(text)

    lemmas = []
    for w in words:
        if re.search("[а-я]", w):
            p = morph.parse(w)[0]
            lemmas.append(p.normal_form)
        else:
            # латиница / цифры — оставляем как есть
            lemmas.append(w)
    return " ".join(lemmas)

# ---------- 3. Загрузка CSV и построение индекса ----------

def build_index(csv_path: str) -> pd.DataFrame:
    print(f"Загружаю CSV: {csv_path}")
    df = pd.read_csv(csv_path, low_memory=False)

    # колонки-спеки (описание)
    spec_cols = [c for c in df.columns if c.startswith("spec")]

    def join_specs(row):
        texts = [str(row[c]) for c in spec_cols if pd.notna(row[c])]
        return " ".join(texts)

    df["category_desc_raw"] = df.apply(join_specs, axis=1)

    # Группируем по id_категории + названию (на случай дублей по товарам)
    cat_df = (
        df.groupby(["id_категории", "название_категории"], as_index=False)
          .agg({"category_desc_raw": lambda x: " ".join(set(x))})
    )

    print(f"Всего уникальных категорий: {len(cat_df)}")

    # Нормализуем и лемматизируем заранее
    print("Лемматизирую названия категорий...")
    cat_df["name_norm"] = cat_df["название_категории"].apply(normalize_and_lemmatize)

    print("Лемматизирую описания категорий...")
    cat_df["desc_norm"] = cat_df["category_desc_raw"].apply(normalize_and_lemmatize)

    print("Индекс готов.")
    return cat_df

# ---------- 4. Функция умного поиска ----------

def smart_search(cat_df: pd.DataFrame, query: str, top_k: int = 10, min_score: int = 40):
    # варианты запроса: как есть и с исправленной раскладкой
    q_orig = normalize_and_lemmatize(query)
    q_fixed = normalize_and_lemmatize(fix_layout_en_to_ru(query))

    queries = [q_orig]
    if q_fixed != q_orig:
        queries.append(q_fixed)

    results = []

    for _, row in cat_df.iterrows():
        best_score_name = 0
        best_score_desc = 0

        for q in queries:
            # приоритет имени категории — короткий текст
            score_name = fuzz.partial_ratio(q, row["name_norm"])
            # описание длинное, тоже partial_ratio
            score_desc = fuzz.partial_ratio(q, row["desc_norm"])

            if score_name > best_score_name:
                best_score_name = score_name
            if score_desc > best_score_desc:
                best_score_desc = score_desc

        final_score = 0.8 * best_score_name + 0.2 * best_score_desc

        if final_score >= min_score:
            results.append({
                "id_категории": row["id_категории"],
                "название_категории": row["название_категории"],
                "score": final_score,
                "score_name": best_score_name,
                "score_desc": best_score_desc,
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

# ---------- 5. Простой CLI для обкатки ----------

def main():
    cat_df = build_index(CSV_PATH)

    print()
    print("=== УМНЫЙ ПОИСК ПО КАТЕГОРИЯМ ===")
    print("Пиши запрос, пустая строка — выход.")
    print()

    while True:
        try:
            q = input("Запрос> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        if not q:
            print("Выход.")
            break

        res = smart_search(cat_df, q, top_k=10, min_score=40)

        if not res:
            print("Ничего не найдено (score < 40).")
            continue

        for r in res:
            print(
                f"[{r['score']:.1f}] id={r['id_категории']} | "
                f"{r['название_категории']} "
                f"(name={r['score_name']:.1f}, desc={r['score_desc']:.1f})"
            )

        print()

if __name__ == "__main__":
    main()
