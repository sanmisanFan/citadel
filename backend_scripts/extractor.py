import subprocess
import re

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

import flor


def run_marker_single(pdf_path, output_dir, output_format, disable_links=True):
    """
    Runs the `marker_single` CLI command with the given arguments.
    """
    try:
        # Build the CLI command
        command = [
            "marker_single",
            pdf_path,
            "--output_dir",
            output_dir,
            "--output_format",
            output_format,
        ]

        # Add --disable_links option if specified
        if disable_links:
            command.append("--disable_links")

        # Run the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Print the output from the command
        print("Command Output:")
        print(result.stdout)

        # Print any errors (if present)
        if result.stderr:
            print("Command Error:")
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Command Output: {e.output}")
        print(f"Command Error: {e.stderr}")


if __name__ == "__main__":
    # Define arguments
    pdf_path = flor.arg("pdf_path", "test.pdf")  # Replace with the path to your PDF
    output_dir = flor.arg("output_dir", "outputs")  # Directory to save output files

    # Run with --disable_links enabled
    output_format = flor.arg("output_format", "json")
    assert output_format in ["json", "markdown"], "Invalid output format specified."
    run_marker_single(pdf_path, output_dir, output_format)

    # Optional: Run with --disable_links disabled
    # run_marker_single(pdf_path, output_dir, "json", disable_links=False)
    # run_marker_single(pdf_path, output_dir, "markdown", disable_links=False)
