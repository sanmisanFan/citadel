import openai
import os
import json
from .utils import pdf_to_str


def chunk_text(text, chunk_size=1500):
    """
    Splits text into chunks of approximately `chunk_size` characters.
    Adjust chunk_size as needed, mindful of token limits.
    """
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def summarize_text(text_chunk):
    """
    Summarizes a chunk of text using OpenAI ChatCompletion.
    """
    prompt = (
        "Summarize the following text in one concise paragraph:\n\n"
        f"{text_chunk}\n\n"
        "Summary:"
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content.strip()


def summarize_pdf(pdf_path):
    """
    Extracts text from a PDF, summarizes it chunk by chunk, and then
    combines those summaries into an overall summary.
    """
    # Step 1: Extract text from the PDF.
    full_text = pdf_to_str(pdf_path)

    # Step 2: Break the text into manageable chunks.
    chunks = chunk_text(full_text)

    # Step 3: Summarize each chunk. is this necessary?
    chunk_summaries = []
    for chunk in chunks:
        summary = summarize_text(chunk)
        chunk_summaries.append(summary)

    # Step 4: Combine the chunk summaries into one text.
    combined_summary_text = "\n".join(chunk_summaries)

    # Step 5: Optionally summarize that combined text for a final overview.
    overall_summary = summarize_text(combined_summary_text)

    return overall_summary


def main():
    pdf_folder = "reference_papers"
    output_file = "outputs/pdf_summaries.json"

    # Gather all PDF files in the folder.
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    results = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"Summarizing '{pdf_file}'...")

        summary = summarize_pdf(pdf_path)

        # Remove .pdf extension for reference name
        reference_name = os.path.splitext(pdf_file)[0]

        results.append({"reference": reference_name, "summary": summary})

    # Save all summaries to JSON.
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Summaries saved to {output_file}")


if __name__ == "__main__":
    main()
