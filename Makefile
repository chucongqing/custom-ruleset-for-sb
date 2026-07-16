.PHONY: all setup generate update clean help

all: generate

setup:
	git submodule update --init --recursive

generate:
	python generate-rules.py

update:
	python update-ruleset.py

clean:
	rm -f rules.json

help:
	@echo "Available targets:"
	@echo "  make setup      Initialize all Git submodules"
	@echo "  make generate   Generate rules.json from template"
	@echo "  make update     Update all submodules to their tracked remote branches"
	@echo "  make clean      Remove generated rules.json"
	@echo "  make all        Run generate (default)"
	@echo "  make help       Show this help message"
