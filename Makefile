###############################################
#
# Openedx Rocketchat commands.
#
###############################################

.DEFAULT_GOAL := help

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: ## delete most git-ignored files
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +

requirements: ## install environment requirements
	pip install -r requirements.txt

run-quality-test: clean ## Run quality test.
	pycodestyle ./openedx_rocketchat
	pylint ./openedx_rocketchat --rcfile=./setup.cfg
