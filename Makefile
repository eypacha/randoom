dev:
	cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000

activate:
	source venv/bin/activate

install:
	cd app && pip install -r requirements.txt

freeze:
	cd app && pip freeze > requirements.txt