poetry init                 # interactively create pyproject.toml in an existing project
poetry new myproject        # scaffold a brand-new project with folders + pyproject

poetry add django           # add a dependency (resolves + updates lock + installs)
poetry add pytest --group dev   # add a dev-only dependency
poetry remove django        # remove one

poetry install              # install everything from the lock (reproducible)
poetry update               # re-resolve to newer allowed versions + update lock
poetry lock                 # re-resolve the lock without installing

poetry run python manage.py runserver   # run a command inside the managed venv
poetry shell                # drop into a shell with the venv activated
poetry show --tree          # see the full dependency tree

poetry build                # build wheel/sdist for distribution
poetry publish              # upload to PyPI

poetry add --group dev pytest black mypy
poetry install --without dev     # production: skip dev tools
poetry install --only dev        # CI lint step: just the dev tools

pipx install poetry          # or: pip install poetry
poetry new typing_demo       # scaffold a project
cd typing_demo
poetry add requests          # watch it create the venv + lock
poetry add --group dev pytest
poetry show --tree           # inspect the tree
poetry run python -c "import requests; print(requests.__version__)"
