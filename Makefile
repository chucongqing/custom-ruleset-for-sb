.PHONY: all generate update clean help

all: generate

generate:
	python generate-rules.py

update:
	python update-ruleset.py

clean:
	rm -f rules.json

help:
	@echo "Available targets:"
	@echo "  make generate   Generate rules.json from template"
	@echo "  make update     Update sing-geosite submodule to latest rule-set"
	@echo "  make clean      Remove generated rules.json"
	@echo "  make all        Run generate (default)"
	@echo "  make help       Show this help message"
