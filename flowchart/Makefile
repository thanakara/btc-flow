.DEFAULT_GOAL: help

CONFIG			:= kind-config.yaml
CLUSTER_NAME	:= btcflow

.PHONY: help \
		generate-config

help:
	@echo "-------------------------------+"
	@echo "|[DEPENDENCY] generate-config  |"
	@echo "|[KIND]       create-cluster   |"
	@echo "|[KIND]       delete-cluster   |"
	@echo "--------------------------------+"

generate-config:
	@ABS_PATH=$(PWD) envsubst < $(CONFIG).TEMPLATE > $(CONFIG)

create-cluster: generate-config
	@kind create cluster --name $(CLUSTER_NAME) --config $(CONFIG)

delete-cluster:
	@kind delete cluster --name $(CLUSTER_NAME)
