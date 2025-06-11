# PDFS := $(wildcard input/*.pdf)
PDFS ?= test.pdf
OUTPUT_DIR := outputs/
DOCS_DIR := documents/

MARKDOWNS := $(patsubst %.pdf,$(OUTPUT_DIR)%/%.md,$(PDFS))

.PHONY: all extract clean process_references

all: extract process_references
	@echo "All tasks completed successfully."

$(OUTPUT_DIR)/references_processed: $(MARKDOWNS)
	@echo "Processing references..."
	python process_references.py --kwargs read_dir=$(OUTPUT_DIR)
	@touch $@

process_references: $(OUTPUT_DIR)/references_processed
	
$(OUTPUT_DIR)%/%.md: %.pdf
	marker_single --output_dir $(OUTPUT_DIR) --output_format markdown $<
	@echo "Extraction complete. JSON and Markdown files created for $<"

extract: $(MARKDOWNS)


clean:
	rm -rf $(OUTPUT_DIR)
	@echo "Cleaned up generated files."