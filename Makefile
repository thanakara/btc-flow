.DEFAULT_GOAL: help

SHA	:= $(shell git rev-parse HEAD)
TAG	:= $(shell git describe --tags --abbrev=0)

.PHONY: help \
		latest \
		remove-cache \
		test-suite \
		pre-commit \
		docker-container-prune



help:
	@echo "--------------------------+"
	@echo "|remove-cache             |"
	@echo "|test-suite               |"
	@echo "|pre-commit               |"
	@echo "|docker-container-prune   |"
	@echo "--------------------------+"

latest:
	@echo ""
	@echo "SHA: $(SHA)"
	@echo "TAG: $(TAG)"
	@echo ""

remove-cache:
	@echo "Ponding while removing..."
	@find . -type d -name "__pycache__" | xargs rm -rf 2>/dev/null || true
	@find . -type d -name ".ruff_cache" | xargs rm -rf 2>/dev/null || true
	@find . -type d -name ".pytest_cache" | xargs rm -rf 2>/dev/null || true
	@sleep 0.33

test-suite:
	@uv run pytest tests/* -x

pre-commit:
	@uv run pre-commit run --all-files

docker-container-prune:
	@docker stop $(shell docker ps -aq) 2>/dev/null || true
	@docker rm $(shell docker ps -aq) 2>/dev/null || true
