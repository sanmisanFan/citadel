# PDFS := $(wildcard input/*.pdf)
PDFS ?= test.pdf
OUTPUT_DIR := outputs/

OUTPUTS := $(patsubst %.pdf,$(OUTPUT_DIR)%/marker.done,$(PDFS))

.PHONY: all extract clean

all: extract

$(OUTPUT_DIR)%/marker.done: %.pdf
	mkdir -p $(dir $@)
	marker_single --output_dir $(OUTPUT_DIR) --output_format json $<
	marker_single --output_dir $(OUTPUT_DIR) --output_format markdown $<
	touch $@
	@echo "Extraction complete. JSON and Markdown files created for $<"

extract: $(OUTPUTS)
	@echo "All files extracted successfully."

clean:
	rm -rf $(OUTPUT_DIR)
	@echo "Cleaned up generated files."