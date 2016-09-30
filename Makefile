BE := bundle exec

JEKYLL := $(BE) jekyll
HTMLPROOF := $(BE) htmlproofer

# MAIN TASKS ###################################################################

.PHONY: all
all: install

.PHONY: ci
ci: check test

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: doctor
doctor:  ## Confirm system dependencies are available
	@ echo "Checking Ruby version:"
	@ ruby --version | tee /dev/stderr | grep -q `cat .ruby-version`

# PROJECT DEPENDENCIES #########################################################

GEMS := vendor/bundler

.PHONY: install
install: $(GEMS) ## Install all project dependnecies

$(GEMS): Gemfile*
	bundle install --path $@
	@ touch $@

.PHONY: update
update: ## Update all project dependnecies
	bundle update

# SERVER TARGETS ###############################################################

PORT ?= 3000

.PHONY: run
run: install
	$(JEKYLL) serve  --future --drafts --port $(PORT)

.PHONY: launch
launch: install
	eval "sleep 3; open http://localhost:$(PORT)" &
	make run

# BUILD ########################################################################

URL := jacebrowning.info

.PHONY: build
build: install
	$(JEKYLL) build --quiet
	echo $(URL) > _site/CNAME

# CHECKS #######################################################################

.PHONY: check
check: install build ## Run linters and static analysis
	$(JEKYLL) doctor
	$(HTMLPROOF) _site --allow-hash-href --only-4xx --enforce-https

# TESTS ########################################################################

.PHONY: test
test: install ## Run unit and integration tests
	@ echo "TODO: add 'test' task"

# DOCUMENTATION ################################################################

.PHONY: doc
doc: install ## Run documentation generators
	@ echo "TODO: add 'doc' task"

# CLEANUP ######################################################################

.PHONY: clean
clean: ## Delete all generated and temporary files
	rm -rf $(GEMS)

# HELP #########################################################################

.PHONY: help
help: all
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
