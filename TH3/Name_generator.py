import fasttext
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import re
import string
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class TextGrouper:
    def __init__(self):
        # если уже есть скачанная модель — берём её, иначе качаем стандартную русскую
        try:
            self.model = fasttext.load_model('cc.ru.300.bin')
        except:
            log.info('Модели нет — качаю русскую fasttext...')
            fasttext.util.download_model('ru', if_exists='ignore')
            self.model = fasttext.load_model('cc.ru.300.bin')

    def clean(self, s):
        s = s.lower()
        s = re.sub(f'[{string.punctuation}0-9]', ' ', s)
        return ' '.join(s.split())

    def get_vectors(self, texts):
        vectors = []
        for text in texts:
            words = self.clean(text).split()
            vecs = [self.model.get_word_vector(w) for w in words if w in self.model.words]
            if vecs:
                vectors.append(np.mean(vecs, axis=0))
            else:
                vectors.append(np.zeros(300))
        return np.array(vectors)

    def best_k(self, vectors, max_k=10):
        if len(vectors) <= 1:
            return 1
        inertias = []
        for k in range(1, min(max_k, len(vectors)) + 1):
            inertias.append(KMeans(n_clusters=k, random_state=42, n_init=10).fit(vectors).inertia_)

        # простенький локоть
        diffs = [inertias[i-1] - inertias[i] for i in range(1, len(inertias))]
        return diffs.index(max(diffs)) + 2 if diffs else 1

    def keywords(self, texts, n=3):
        words = []
        for t in texts:
            words += [w for w in self.clean(t).split() if len(w) > 2]
        return [w for w, _ in Counter(words).most_common(n)]

    def make_name(self, texts):
        if not texts:
            return 'Без названия'

        if len(texts) == 1:
            return ' '.join(self.clean(texts[0]).split()[:4]).title()

        kw = self.keywords(texts, 2)
        name = ' '.join(kw).title()
        if len(texts) > 5:
            name += f' ({len(texts)} шт)'
        return name or f'Группа из {len(texts)}'

    def group(self, texts, clusters=None):
        if not texts:
            return {}

        vecs = self.get_vectors(texts)

        if clusters is None:
            clusters = self.best_k(vecs)
            log.info(f'Сам выбрал кластеров: {clusters}')

        if clusters <= 1:
            return {self.make_name(texts): texts}

        labels = KMeans(n_clusters=clusters, random_state=42, n_init=10).fit_predict(vecs)

        groups = {}
        for label, text in zip(labels, texts):
            groups.setdefault(label, []).append(text)

        result = {}
        for lst in groups.values():
            result[self.make_name(lst)] = lst
        return result

    # вариант через простое косинусное сходство — иногда работает лучше кластеров
    def group_by_sim(self, texts, threshold=0.65):
        if not texts:
            return {}

        vecs = self.get_vectors(texts)
        used = set()
        result = []

        for i in range(len(texts)):
            if i in used:
                continue
            group = [i]
            used.add(i)
            for j in range(i+1, len(texts)):
                if j in used:
                    continue
                if cosine_similarity([vecs[i]], [vecs[j]])[0][0] >= threshold:
                    group.append(j)
                    used.add(j)
            result.append(group)

        out = {}
        for idxs in result:
            grp_texts = [texts[k] for k in idxs]
            out[self.make_name(grp_texts)] = grp_texts
        return out


# ==================== тест =====================
if __name__ == '__main__':
    data = [
        "Закупка компьютеров и оргтехники для офиса",
        "Ноутбуки Dell Latitude для сотрудников",
        "Мониторы Samsung 24 дюйма",
        "Офисные стулья эргономичные",
        "Столы компьютерные регулируемые",
        "Канцелярские товары для отдела",
        "Бумага для принтера А4",
        "Принтеры лазерные HP",
        "Мыши и клавиатуры беспроводные",
        "Веб-камеры для видеоконференций",
        "Системные блоки для рабочего места",
        "Компьютерные мыши Logitech",
        "Картриджи для принтера",
        "Офисная мебель для переговорной",
        "Проекторы для конференц-зала"
    ]

    g = TextGrouper()

    print('K-means (авто):')
    for name, items in g.group(data).items():
        print(f'\n{name} — {len(items)} шт')
        for x in items:
            print('  •', x)

    print('\n' + '='*60 + '\n')

    print('По косинусному сходству (threshold 0.65):')
    for name, items in g.group_by_sim(data, 0.65).items():
        print(f'\n{name} — {len(items)} шт')
        for x in items:
            print('  •', x)