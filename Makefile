BE := bundle exec

JEKYLL := $(BE) jekyll
HTMLPROOF := $(BE) htmlproofer

# MAIN TASKS ###################################################################

.PHONY: all
all: test ## Run all tasks that determine CI status

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: doctor
doctor:  ## Confirm system dependencies are available
	bin/verchew

# PROJECT DEPENDENCIES #########################################################

GEMS := vendor/bundler/.flag

.PHONY: install
install: $(GEMS) ## Install all project dependencies

$(GEMS): Gemfile*
	@ bundle config set path vendor/bundler
	bundle install
	@ touch $@

.PHONY: update
update: ## Update all project dependnecies
	bundle update

# SERVER TARGETS ###############################################################

PORT ?= 3000

.PHONY: run
run: install
	$(JEKYLL) serve --port=$(PORT) --livereload --future --drafts

.PHONY: launch
launch: install
	eval "sleep 4 && open http://localhost:$(PORT)" &
	make run

# BUILD ########################################################################

URL := jacebrowning.info

.PHONY: build
build: install music.md
	$(JEKYLL) build
	echo $(URL) > _site/CNAME

music.md: scripts/music.py
	python $<

# TEST ########################################################################

.PHONY: test
test: install build ## Check site content
	$(JEKYLL) doctor
	$(HTMLPROOF) _site --no-enforce-http --ignore-status-codes 0,301,403,999 --ignore-urls "https://www.meetup.com/PyLadiesGrandRapids/"

# CLEANUP ######################################################################

.PHONY: clean
clean: ## Delete all generated and temporary files
	rm -rf $(GEMS)

# HELP #########################################################################

.PHONY: help
help: install
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
