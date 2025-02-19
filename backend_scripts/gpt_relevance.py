import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def map_file_names_to_citation_keys(paper_summaries):
    mapping = {}
    for entry in paper_summaries:
        file_name = entry.get("file_name", "")
        summary = entry.get("summary", "No summary available.")
        key = f"[{file_name.split('.')[0]}]"
        mapping[key] = summary
    return mapping

def assess_citation_relevance(citation_key, context_text, summary_text):
    """Assesses relevance using GPT-4 Turbo with explicit reasoning"""
    prompt = f"""
You are an expert academic researcher. Your task is to evaluate the contextual relevance of the citation {citation_key} in the provided text excerpt, and to clearly explain your reasoning.

Here is the text excerpt where {citation_key} is mentioned:
-----------------------------
{context_text}
-----------------------------

Below is the summary of the cited paper corresponding to {citation_key}:
-----------------------------
{summary_text}
-----------------------------

Instructions:
1. First, decide if this mention is substantive (i.e., the text engages with the paper’s content, methods, or results) or if it is merely a bibliographic reference.
2. If the excerpt is only a reference list entry (just publication details with no discussion), then:
   - Output Score: 0
   - Explanation: "Reference list entry with no substantive discussion."
3. If the mention is substantive, rate its relevance on a scale from 1 to 10 using these guidelines:
   - 10: The text provides a detailed, direct discussion of the paper’s methods and results.
   - 7-9: The text contains an important contextual reference that significantly influences the discussion.
   - 4-6: The text offers general background information about the paper.
   - 1-3: The mention is peripheral or only minimally discussed.
4. In your response, first provide the Score and then give a detailed Explanation that explicitly states the evidence and reasoning behind your score. Mention key phrases or elements from both the excerpt and the paper summary that informed your judgment.

Please provide your answer in exactly the following format:
Score: [number]
Explanation: [Your detailed 2-3 sentence analysis, including key evidence and reasoning]

Now, evaluate the citation mention.
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.2,
        top_p=0.95
    )
    return response.choices[0].message.content

def process_citation_mentions(citation_mentions, paper_summary_mapping):
    """Process each citation mention individually"""
    assessments = {}
    
    for citation_key, text_excerpts in citation_mentions.items():
        print(f"Processing {len(text_excerpts)} mentions for {citation_key}...")
        summary_text = paper_summary_mapping.get(citation_key, "No summary available.")
        
        citation_assessments = []
        for idx, text in enumerate(text_excerpts, 1):
            print(f"  Assessing mention {idx}/{len(text_excerpts)}...")
            try:
                assessment = assess_citation_relevance(citation_key, text, summary_text)
                citation_assessments.append({
                    "excerpt": text,
                    "assessment": assessment
                })
            except Exception as e:
                print(f"Error processing mention {idx}: {str(e)}")
                citation_assessments.append({
                    "excerpt": text,
                    "assessment": "Assessment failed",
                    "error": str(e)
                })
        
        assessments[citation_key] = citation_assessments
    
    return assessments

def main():
    citation_mentions_file = "organized_citations.json"
    paper_summaries_file = "pdf_summaries.json"

    citation_mentions = load_json(citation_mentions_file)
    paper_summaries = load_json(paper_summaries_file)
    paper_summary_mapping = map_file_names_to_citation_keys(paper_summaries)

    # Process all citations with individual text excerpts
    citation_assessments = process_citation_mentions(citation_mentions, paper_summary_mapping)

    # Save results
    output_file = "detailed_citation_assessments.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(citation_assessments, f, indent=2, ensure_ascii=False)

    print(f"Detailed assessments saved to {output_file}")

if __name__ == "__main__":
    main()