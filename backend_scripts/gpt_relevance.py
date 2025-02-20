import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def map_references_to_summaries(paper_summaries):
    """Map reference numbers from pdf_summaries.json to citation keys (e.g., '[1]') and their summaries."""
    mapping = {}
    for entry in paper_summaries:
        ref_number = entry.get("reference")  # String like "1", "2", etc.
        summary = entry.get("summary", "")
        key = f"[{ref_number}]"  # Convert to citation key format like "[1]"
        mapping[key] = summary
    return mapping

def assess_citation_relevance(citation_key, context_text, summary_text):
    """Assesses relevance using GPT-4 Turbo with explicit reasoning."""
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
    """Process each citation mention individually, skipping if no summary is available."""
    assessments = {}
    
    for entry in citation_mentions:
        ref_number = entry.get("reference")  # Integer like 1, 2, etc.
        citation_key = f"[{ref_number}]"  # Convert to string format like "[1]"
        text_excerpts = entry.get("texts", [])
        
        # Check if a summary exists for this citation key
        summary_text = paper_summary_mapping.get(citation_key)
        if not summary_text:
            print(f"Skipping {citation_key}: No summary available in pdf_summaries.json.")
            continue
        
        print(f"Processing {len(text_excerpts)} mentions for {citation_key}...")
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

def assign_scores_to_enriched_papers(enriched_papers, citation_assessments):
    """Assign relevance scores to the reference_mentions in enriched_papers.json."""
    # Create a lookup dictionary for assessments by excerpt text
    assessment_lookup = {}
    for citation_key, assessments in citation_assessments.items():
        for assessment in assessments:
            excerpt = assessment["excerpt"]
            assessment_lookup[excerpt] = assessment["assessment"]

    # Update enriched_papers with assessments
    for paper in enriched_papers:
        ref_id = paper.get("ref_id")
        if ref_id is None:
            print(f"Warning: Paper with title '{paper.get('title')}' has no ref_id. Skipping.")
            continue
        
        # Convert ref_id to citation key format for consistency
        citation_key = f"[{ref_id}]"
        
        if "reference_mentions" in paper and paper["reference_mentions"]:
            updated_mentions = []
            for mention in paper["reference_mentions"]:
                if mention in assessment_lookup:
                    # Parse the assessment to extract the score
                    assessment_text = assessment_lookup[mention]
                    try:
                        score_line = assessment_text.split('\n')[0]  # "Score: [number]"
                        score = int(score_line.split(': ')[1])
                    except (IndexError, ValueError) as e:
                        print(f"Error parsing score for mention in {citation_key}: {assessment_text}. Setting score to None.")
                        score = None
                    
                    updated_mentions.append({
                        "text": mention,
                        "relevance_score": score,
                        "assessment": assessment_text
                    })
                else:
                    # If no assessment exists (e.g., skipped due to no summary), keep original text
                    updated_mentions.append({
                        "text": mention,
                        "relevance_score": None,
                        "assessment": "No assessment available"
                    })
            paper["reference_mentions"] = updated_mentions
        else:
            print(f"No reference_mentions found for {citation_key} in enriched_papers.json.")
    
    return enriched_papers

def main():
    citation_mentions_file = "outputs/reference_mentions.json"
    paper_summaries_file = "outputs/pdf_summaries.json"
    enriched_papers_file = "outputs/enriched_papers.json"
    output_assessments_file = "outputs/detailed_citation_assessments.json"
    output_enriched_papers_file = "outputs/enriched_papers_with_scores.json"

    # Load data
    citation_mentions = load_json(citation_mentions_file)
    paper_summaries = load_json(paper_summaries_file)
    enriched_papers = load_json(enriched_papers_file)
    
    # Map reference numbers to summaries
    paper_summary_mapping = map_references_to_summaries(paper_summaries)

    # Process all citations with individual text excerpts
    citation_assessments = process_citation_mentions(citation_mentions, paper_summary_mapping)

    # Save detailed assessments
    with open(output_assessments_file, "w", encoding="utf-8") as f:
        json.dump(citation_assessments, f, indent=2, ensure_ascii=False)
    print(f"Detailed assessments saved to {output_assessments_file}")

    # Assign scores to enriched_papers
    updated_enriched_papers = assign_scores_to_enriched_papers(enriched_papers, citation_assessments)

    # Save updated enriched_papers
    with open(output_enriched_papers_file, "w", encoding="utf-8") as f:
        json.dump(updated_enriched_papers, f, indent=2, ensure_ascii=False)
    print(f"Updated enriched papers with scores saved to {output_enriched_papers_file}")

if __name__ == "__main__":
    main()