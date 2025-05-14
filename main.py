import os

def generate_mermaid_diagram_syntax():
    """
    Генерирует Mermaid-синтаксис для диаграммы архитектуры системы.
    """
    mermaid_syntax = """
flowchart LR
    %% Определяем направление графа: слева направо (Left-to-Right)

    subgraph "System Architecture: ruT5 Classification"
        direction TB %% Направление подграфа: сверху вниз (Top-to-Bottom)

        subgraph "Training Phase"
            direction LR %% Направление этапа обучения: слева направо

            RawData[Raw JSON Data<br/>(fake_marked.json)] --> TrainingScript[Python Training Script<br/>(Your Code)]
            TrainingScript --> TrainedArtifacts(Trained ruT5 Model &<br/>Tokenizer Files)
            TrainingScript --> LabelMapping(Label Mapping<br/>label2id.json)
            TrainingScript --> TrainingResults[Training Results<br/>(CSV, Plot)]
        end

        subgraph "Inference Phase"
            direction LR %% Направление этапа инференса: слева направо

            User((User)) --> ReactFrontend[React Frontend]
            ReactFrontend --> FastAPIBackend[FastAPI Backend]
            FastAPIBackend --> |Sends Result| ReactFrontend
            ReactFrontend --> |Displays Result| User
        end

        %% Соединения между этапами (бэкенд загружает артефакты обучения)
        FastAPIBackend --> |Loads Model/Tokenizer| TrainedArtifacts
        FastAPIBackend --> |Loads Mapping| LabelMapping
    end
"""
    return mermaid_syntax.strip() # Убираем лишние пробелы по краям

# Генерируем синтаксис
diagram_syntax = generate_mermaid_diagram_syntax()

# Выводим синтаксис для копирования
print("Скопируйте текст ниже и вставьте его в онлайн-редактор Mermaid или платформу с поддержкой Mermaid (например, GitHub/GitLab Markdown, Notion):")
print("\n```mermaid") # Начало блока Mermaid для Markdown
print(diagram_syntax)
print("```") # Конец блока Mermaid для Markdown

# Optional: Сохраняем синтаксис в файл для удобства
file_path = "system_architecture.mermaid"
try:
    with open(file_path, "w", encoding="utf-8") as f:
        # Записываем синтаксис в файл, опционально с ограждениями для Markdown
        f.write("```mermaid\n")
        f.write(diagram_syntax)
        f.write("\n```")
    print(f"\nСинтаксис Mermaid также сохранен в файл: {file_path}")
    print(f"Вы можете открыть этот файл в редакторах, поддерживающих Mermaid, или скопировать содержимое в онлайн-инструменты.")
except Exception as e:
    print(f"\nОшибка при сохранении файла: {e}")