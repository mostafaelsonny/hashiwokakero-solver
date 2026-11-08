.PHONY: install test status api frontend-install frontend-dev frontend-build
install:
	python -m pip install -r requirements.txt
test:
	python -m pytest -q
status:
	python -m pytest -q -rxX
api:
	uvicorn api.main:app --reload
frontend-install:
	cd frontend && npm install
frontend-dev:
	cd frontend && npm run dev
frontend-build:
	cd frontend && npm run build
