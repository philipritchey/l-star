.PHONY: test

test:
	@PYTHONPATH=. pytest --cov-report term-missing --cov-branch --cov-fail-under=90 --cov=. tests
