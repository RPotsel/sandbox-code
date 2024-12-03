WORKSPASE?=example
CODE?=gitlab

compose-pull:
	@docker compose --project-directory ./$(CODE) \
		--env-file ./$(CODE)/.env.$(WORKSPASE) pull

compose-up:
	@docker compose --project-directory ./$(CODE) \
		--env-file ./$(CODE)/.env.$(WORKSPASE) up -d

compose-down:
	@docker compose --project-directory ./$(CODE) \
		--env-file ./$(CODE)/.env.$(WORKSPASE) down

compose-log:
	@docker compose --project-directory ./$(CODE) \
		--env-file ./$(CODE)/.env.$(WORKSPASE) logs
