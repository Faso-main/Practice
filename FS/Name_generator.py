import fasttext
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import re, os

class SmartFastTextGrouper:
    def __init__(self, model_path=os.path.join('FS','cc.ru.300.bin')):
        self.model = fasttext.load_model(model_path)
        # Словарь для улучшения названий групп
        self.category_map = {
            'компьютер': 'Компьютеры',
            'ноутбук': 'Ноутбуки', 
            'монитор': 'Мониторы',
            'принтер': 'Принтеры',
            'картридж': 'Картриджи',
            'мышь': 'Компьютерные мыши',
            'клавиатура': 'Клавиатуры',
            'вебкамера': 'Веб-камеры',
            'стул': 'Офисные стулья',
            'стол': 'Столы',
            'мебель': 'Офисная мебель',
            'канцелярский': 'Канцелярия',
            'бумага': 'Бумага',
            'проектор': 'Проекторы',
            'роутер': 'Сетевое оборудование'
        }
    
    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^а-яё\s]', ' ', text)
        return ' '.join(text.split())
    
    def get_text_vector(self, text):
        """Улучшенное получение вектора с учетом важности слов"""
        clean_text = self.preprocess_text(text)
        words = clean_text.split()
        
        # Взвешиваем слова по важности
        word_vectors = []
        for word in words:
            if len(word) > 2 and word in self.model.words:
                vector = self.model.get_word_vector(word)
                # Увеличиваем вес специфических слов
                if word in self.category_map:
                    word_vectors.extend([vector] * 3)  # Тройной вес для ключевых слов
                else:
                    word_vectors.append(vector)
        
        if word_vectors:
            return np.mean(word_vectors, axis=0)
        return np.zeros(300)
    
    def detect_main_category(self, text):
        """Определяем основную категорию текста"""
        clean_text = self.preprocess_text(text)
        words = clean_text.split()
        
        for word in words:
            if word in self.category_map:
                return self.category_map[word]
        
        return None
    
    def group_texts_improved(self, texts):
        """
        Улучшенная группировка с предварительной категоризацией
        """
        print(f"🎯 Группируем {len(texts)} текстов...")
        
        # Шаг 1: Предварительная группировка по категориям
        categorized = {}
        uncategorized = []
        
        for text in texts:
            category = self.detect_main_category(text)
            if category:
                categorized.setdefault(category, []).append(text)
            else:
                uncategorized.append(text)
        
        print(f"   Найдено категорий: {len(categorized)}")
        print(f"   Не категоризировано: {len(uncategorized)}")
        
        # Шаг 2: Детальная группировка внутри каждой категории
        final_groups = {}
        
        for category, items in categorized.items():
            if len(items) <= 3:
                # Маленькие группы оставляем как есть
                final_groups[category] = items
            else:
                # Большие группы разбиваем на подгруппы
                subgroups = self._cluster_within_category(items)
                final_groups.update(subgroups)
        
        # Шаг 3: Обработка не категоризированных элементов
        if uncategorized:
            uncat_groups = self._cluster_uncategorized(uncategorized)
            final_groups.update(uncat_groups)
        
        return dict(sorted(final_groups.items(), key=lambda x: len(x[1]), reverse=True))
    
    def _cluster_within_category(self, items):
        """Кластеризация внутри одной категории"""
        if len(items) <= 2:
            return {self._generate_detailed_name(items): items}
        
        vectors = np.array([self.get_text_vector(text) for text in items])
        
        # Используем DBSCAN для автоматического определения кластеров
        clustering = DBSCAN(eps=0.3, min_samples=2, metric='cosine').fit(vectors)
        labels = clustering.labels_
        
        groups = {}
        for label, text in zip(labels, items):
            if label == -1:  # Выбросы
                groups.setdefault('Разное', []).append(text)
            else:
                groups.setdefault(label, []).append(text)
        
        # Создаем названия для подгрупп
        result = {}
        for group_items in groups.values():
            if len(group_items) >= 2:
                name = self._generate_detailed_name(group_items)
                result[name] = group_items
            else:
                result.setdefault('Разное', []).extend(group_items)
        
        return result
    
    def _cluster_uncategorized(self, items):
        """Кластеризация не категоризированных элементов"""
        if len(items) <= 3:
            return {'Разное': items}
        
        vectors = np.array([self.get_text_vector(text) for text in items])
        
        # Пробуем разные методы кластеризации
        n_clusters = min(4, len(items) // 2)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(vectors)
        
        groups = {}
        for label, text in zip(labels, items):
            groups.setdefault(label, []).append(text)
        
        result = {}
        for group_items in groups.values():
            name = self._generate_detailed_name(group_items)
            result[name] = group_items
        
        return result
    
    def _generate_detailed_name(self, items):
        """Генерация детального названия группы"""
        if len(items) == 1:
            words = self.preprocess_text(items[0]).split()[:3]
            return ' '.join(words).title()
        
        # Собираем все слова
        all_words = []
        for text in items:
            words = self.preprocess_text(text).split()
            all_words.extend([w for w in words if len(w) > 2])
        
        word_counts = Counter(all_words)
        
        # Ищем самые характерные слова (не стоп-слова)
        stop_words = {'для', 'и', 'в', 'на', 'с', 'из', 'от', 'до', 'по', 'за'}
        keywords = []
        
        for word, count in word_counts.most_common(10):
            if (word not in stop_words and 
                word not in keywords and
                count >= max(2, len(items) // 3)):  # Слово должно встречаться в достаточном количестве текстов
                keywords.append(word)
            
            if len(keywords) >= 2:
                break
        
        # Если не нашли хороших ключевых слов, используем первые слова
        if not keywords:
            first_text_words = self.preprocess_text(items[0]).split()
            keywords = [w for w in first_text_words if len(w) > 2][:2]
        
        name = ' '.join(keywords).title() if keywords else 'Разное'
        
        # Добавляем количество если группа не слишком маленькая
        if len(items) > 2:
            name += f' ({len(items)})'
        
        return name

# ТЕСТИРОВАНИЕ УЛУЧШЕННОГО АЛГОРИТМА
if __name__ == '__main__':
    grouper = SmartFastTextGrouper()
    
    test_data = [
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
        "Проекторы для конференц-зала",
        "Роутеры и сетевое оборудование"
    ]
    
    print("=" * 70)
    print("УЛУЧШЕННАЯ ГРУППИРОВКА С КАТЕГОРИЗАЦИЕЙ")
    print("=" * 70)
    
    groups = grouper.group_texts_improved(test_data)
    
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"Всего групп: {len(groups)}")
    
    for name, items in groups.items():
        print(f"\n🏷️  {name}:")
        for item in items:
            print(f"   • {item}")
    
    # Статистика
    group_sizes = [len(items) for items in groups.values()]
    print(f"\n📈 Статистика:")
    print(f"   Размеры групп: {group_sizes}")
    print(f"   Средний размер: {np.mean(group_sizes):.1f}")
    print(f"   Минимальный размер: {min(group_sizes)}")
    print(f"   Максимальный размер: {max(group_sizes)}")