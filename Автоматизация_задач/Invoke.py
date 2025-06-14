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


"""
invoke hello --name=Alice
invoke lint
invoke deploy --env=staging
"""