SHELL: /bin/bash

.DEFAULT_GOAL := install
.PHONY : install run

VENV_NAME?=.venv
PYTHON=${VENV_NAME}/bin/python

install: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements.txt
#	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	test -d $(VENV_NAME) || python3 -m venv $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(VENV_NAME)/bin/activate;\

	ifeq ($(OS),Windows_NT)
		pyinstaller.exe --onefile --windowed app.py
	else
		pyinstaller app.py
	endif


run: install
	@cp input.csv ./dist/translator/
	@./dist/translator/translator
