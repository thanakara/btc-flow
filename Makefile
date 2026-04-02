.DEFAULT_GOAL: help

SHA	:= $(shell git rev-parse HEAD)
TAG	:= $(shell git describe --tags --abbrev=0)

.PHONY: help \
		latest \
		rm-cache \
		test-suite \
		pre-commit \
		docker-container-prune



help:
	@echo "-------------------------------+"
	@echo "|[UTIL] rm-cache               |"
	@echo "|[UTIL] docker-container-prune |"
	@echo "|[TEST] test-suite             |"
	@echo "|[TEST] pre-commit             |"
	@echo "-------------------------------+"

latest:
	@echo ""
	@echo "SHA: $(SHA)"
	@echo "TAG: $(TAG)"
	@echo ""

rm-cache:
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
