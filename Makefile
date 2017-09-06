.PHONY: clean lint create_environment update_environment crontab_create 
	crontab_dir crontab_clean

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = vandyscripts
PYTHON_INTERPRETER = python
ENVIRONMENT_FILE = environment.yml
CRONTAB_OUTFILE = "$(PROJECT_DIR)/crontab_$(PROJECT_NAME).dat"
CRONTAB_MAINPATH = ~/crontab_jobs
CRONTAB_MAINFILE = $(CRONTAB_MAINPATH)/crontab_file

# Shell file
ifeq ($(uname), Darwin)
BASH_PATH = ~/.bash_profile
else
BASH_PATH = ~/.bashrc
endif

# Anaconda
ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Delete all compiled Python files
clean:
	find . -name "*.pyc" -exec rm {} \;

## Lint using flake8
lint:
	flake8 --exclude=lib/,bin/,docs/conf.py .

## Set up python interpreter environment
environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
		conda config --add channels conda-forge
		conda env create -f $(ENVIRONMENT_FILE)
endif

## Update python interpreter environment
update_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
		conda env update -f $(ENVIRONMENT_FILE)
endif

## Delte python interpreter environment
remove_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, removing conda environment"
		conda env remove -n $(PROJECT_NAME)
endif

## Create crontab file to attach
crontab_create: crontab_file
	@echo "0 7 * * * source activate $(PROJECT_NAME); python $(PROJECT_DIR)/Astroweb_post/Astroweb_updates_xmlrpc.py >> $(PROJECT_DIR)/Astroweb_post/updatelog2 2>&1 ; source deactivate;" > $(CRONTAB_OUTFILE)
	@echo "0 7 * * * source activate $(PROJECT_NAME); python $(PROJECT_DIR)/Astroweb_post/Astroweb_updates_xmlrpc.py >> $(PROJECT_DIR)/Astroweb_post/updatelog2 2>&1 ; source deactivate;" >> $(CRONTAB_MAINFILE)
	@echo "0 8 * * * source activate $(PROJECT_NAME); python $(PROJECT_DIR)/AJC_Scheduler/AJC_Reminders.py >> $(PROJECT_DIR)/AJC_Scheduler/ajc_log 2>&1 ; source deactivate;" >> $(CRONTAB_OUTFILE)
	@echo "0 8 * * * source activate $(PROJECT_NAME); python $(PROJECT_DIR)/AJC_Scheduler/AJC_Reminders.py >> $(PROJECT_DIR)/AJC_Scheduler/ajc_log 2>&1 ; source deactivate;" >> $(CRONTAB_MAINFILE)
	@crontab $(CRONTAB_MAINFILE)
	@echo ">>> CRONTAB file created! Done!"

## Checks if CRONTAB file exists
crontab_file: crontab_dir
	@if test ! -f $(CRONTAB_MAINFILE); then \
		touch $(CRONTAB_MAINFILE); \
	fi

## Checks if CRONTAB folder exits
crontab_dir:
	@if test ! -d $(CRONTAB_MAINPATH); then \
		mkdir $(CRONTAB_MAINPATH); \
	fi

## Cleans the Crontab
crontab_clean:
	rm -rf $(CRONTAB_OUTFILE)
	rm -rf $(CRONTAB_MAINFILE)
	crontab -r

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
