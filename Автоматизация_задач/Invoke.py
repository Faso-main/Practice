from invoke import task

@task
def hello(c, name="World"):
    """Приветствие."""
    print(f"Hello, {name}!")

@task
def lint(c):
    """Проверка кода с flake8."""
    c.run("flake8 .")

@task
def deploy(c, env="prod"):
    """Деплой на сервер."""
    print(f"Deploying to {env}...")
    c.run(f"git push {env} main")
    c.run(f"ssh user@server 'cd /app && git pull && docker-compose up -d'")
from datetime import datetime

print(str(datetime.now().strftime("%Y_%m_%d")))  # Вывод: "2025-06-15" (строка в формате ГГГГ-ММ-ДД)

"""
invoke hello --name=Alice
invoke lint
invoke deploy --env=staging
"""