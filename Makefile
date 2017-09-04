.PHONY: clean lint create_environment update_environment autoenv_create

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = vandyscripts
PYTHON_INTERPRETER = python
ENVIRONMENT_FILE = environment.yml
BASHRC_PATH = ~/.bashrc
AUTOENV_PATH = "https://github.com/kennethreitz/autoenv"

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

# AUTOENV
ifeq (,$(shell which activate.sh))
HAS_AUTOENV=False
else
HAS_AUTOENV=True
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
create_environment:
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

## Creates environment file to use with autoenv
autoenv_create:
ifeq (True,$(HAS_AUTOENV))
		@echo ">>> Detected autoenv, creating .env file"
		echo "source activate $(PROJECT_NAME)" >> $(PROJECT_DIR)/$(PROJECT_NAME).env
		@echo ">>> $(PROJECT_NAME).env file created!"
else
		@echo ">>> autoenv not detected...Installing"
		git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv
		echo "" >> $(BASH_PATH)
		echo "# AUTOENV ($(AUTOENV_PATH))" >> $(BASH_PATH)
		echo 'source ~/.autoenv/activate.sh' >> $(BASH_PATH)
		echo "" >> $(BASH_PATH)
		@echo ">>> Detected autoenv, creating .env file"
		echo "source activate $(PROJECT_NAME)" >> $(PROJECT_DIR)/$(PROJECT_NAME).env
		@echo ">>> $(PROJECT_NAME).env file created!"
endif



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
