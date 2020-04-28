lint:
	poetry run isort --check-only --settings-path=.config/isort.cfg
	poetry run flake8 --config=.config/.flake8 .
	poetry run mypy --config-file=.config/mypy.ini .
	poetry run black --check .

test:
	poetry run pytest -c .config/pytest.ini --cov=web_api --cov-config=.config/.coveragerc --cov-report=term-missing
