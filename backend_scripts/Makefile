# PDFS := $(wildcard input/*.pdf)
PDFS ?= test.pdf

# Convert to .json files, .md files
OUTPUT_DIR := outputs/
JSONS := $(patsubst %.pdf,$(OUTPUT_DIR)%/%.json,$(PDFS))
MARKDOWNS := $(patsubst %.pdf,$(OUTPUT_DIR)%/%.md,$(PDFS))

.PHONY: all
all: $(MARKDOWNS) $(JSONS)

# python extractor.py --kwargs pdf_path=$< output_dir=$(OUTPUT_DIR) output_format=json
$(OUTPUT_DIR)%/%.json: %.pdf
	@echo "Running extraction with marker-pdf..."
	marker_single --output_dir $(OUTPUT_DIR) --output_format json $<
	@echo "Extraction complete. JSON file created at $(OUTPUT_DIR)%/%.json"

# python extractor.py --kwargs pdf_path=$< output_dir=$(OUTPUT_DIR) output_format=markdown
$(OUTPUT_DIR)%/%.md: %.pdf
	@echo "Running extraction with marker-pdf..."
	marker_single --output_dir $(OUTPUT_DIR) --output_format markdown $<
	@echo "Extraction complete. Markdown file created at $(OUTPUT_DIR)%/%.md"


.PHONY: clean
clean:
	$(RM) $(JSONS)
	$(RM) $(MARKDOWNS)
	rm -rf $(OUTPUT_DIR)
	@echo "Cleaned up generated files."