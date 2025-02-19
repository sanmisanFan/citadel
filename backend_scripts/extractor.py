import subprocess

def run_marker_single(pdf_path, output_dir, output_format):
    """
    Runs the `marker_single` CLI command with the given arguments.
    """
    try:
        # Build the CLI command
        command = [
            "marker_single",
            pdf_path,
            "--output_dir", output_dir,
            "--output_format", output_format,
        ]

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
    pdf_path = "test.pdf"  # Replace with the path to your PDF
    output_dir = "outputs"  # Directory to save output files
    output_format = "json"  # Desired output format

    # Run the command
    run_marker_single(pdf_path, output_dir, output_format)
