# PDFS := $(wildcard input/*.pdf)
PDFS ?= test.pdf
OUTPUT_DIR := outputs/

JSONS := $(patsubst %.pdf,$(OUTPUT_DIR)%/%.json,$(PDFS))
MARKDOWNS := $(patsubst %.pdf,$(OUTPUT_DIR)%/%.md,$(PDFS))

.PHONY: all extract clean

all: extract

$(OUTPUT_DIR)%/%.json: %.pdf
	marker_single --output_dir $(OUTPUT_DIR) --output_format json $<
	@echo "Extraction complete. JSON file created at $(OUTPUT_DIR)%/%.json"

$(OUTPUT_DIR)%/%.md: %.pdf
	marker_single --output_dir $(OUTPUT_DIR) --output_format markdown $<
	@echo "Extraction complete. Markdown file created at $(OUTPUT_DIR)%/%.md"

extract: $(JSONS) $(MARKDOWNS)
	@echo "All files extracted successfully."

clean:
	rm -rf $(OUTPUT_DIR)
	@echo "Cleaned up generated files."