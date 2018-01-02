
help:
	@echo -------------------------------
	@echo - Makefile Target Information -
	@echo -------------------------------
	@IFS=$$'\n' ; \
	    help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	    for help_line in $${help_lines[@]}; do \
	        IFS=$$':' ; \
	        help_split=($$help_line) ; \
	        help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
	        help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
	        printf '\033[33m'; \
	        printf "%-20s %s" $$help_command ; \
	        printf '\033[0m'; \
	        printf "%s\n" $$help_info; \
	    done

build: ## Build docker image
	@echo -----------------------------
	@echo - Building country-comp app -
	@echo -----------------------------
	docker-compose build

up: ## Start the container and run the bokeh server app

	@echo ------------------------------------
	@echo - Start country-comp app container -
	@echo ------------------------------------
	docker-compose up -d
	sleep 1
	docker ps

down: ## Stop and remove the container
	@echo ----------------------------------------------
	@echo - Stop and Remove country-comp app container -
	@echo ----------------------------------------------
	docker-compose down

.PHONY: build up down