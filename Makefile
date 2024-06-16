include .env

init:
	ssh $(DEPLOY_HOST) 'cd $(DEPLOY_DIR) && python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install --upgrade pip && pip install -r requirements.txt'

deploy:
	ssh $(DEPLOY_HOST) 'mkdir -p $(DEPLOY_DIR)'
	scp main.py requirements.txt .env $(DEPLOY_HOST):$(DEPLOY_DIR)

start:
	ssh $(DEPLOY_HOST) 'cd $(DEPLOY_DIR) && source .venv/bin/activate && nohup python3 main.py &'