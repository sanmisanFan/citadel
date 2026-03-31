def assess_citation_relevance(citation_key, context_text, summary_text, client):
    """Assesses relevance using GPT-4 Turbo with explicit reasoning."""
    prompt = f"""
You are an expert academic researcher. Your task is to evaluate the contextual relevance of citation [{citation_key}] in the provided text excerpt.

IMPORTANT: Focus ONLY on citation [{citation_key}]. The text may contain other citation numbers - ignore them completely. Only evaluate how [{citation_key}] is used.

Here is the text excerpt where [{citation_key}] is mentioned:
-----------------------------
{context_text}
-----------------------------

Below is the summary/abstract of the cited paper corresponding to [{citation_key}]:
-----------------------------
{summary_text}
-----------------------------

Instructions:
1. First, decide if the mention of [{citation_key}] is substantive (i.e., the text engages with that paper's content, methods, or results) or if it is merely a bibliographic reference.
2. A "reference list entry" is ONLY text that appears in the References/Bibliography section, containing just publication metadata like:
   "[19] Smith, J. (2020). Paper Title. Journal Name, 10(2), 123-456."

   If the text contains ANY discussion, description, or context about what the cited work does or claims, it is NOT a reference list entry - even if the description is brief.

   Only output Score: 0 for actual bibliography entries. If in doubt, give a low score (1-3) instead of 0.

   If the excerpt is a true reference list entry (just publication details, no discussion), then:
   - Output Score: 0
   - Explanation: "Reference list entry with no substantive discussion."
3. If the mention of [{citation_key}] is substantive, rate its relevance on a scale from 1 to 10 using these guidelines:
   - 10: The text provides a detailed, direct discussion of [{citation_key}]'s methods and results.
   - 7-9: The text contains an important contextual reference to [{citation_key}] that significantly influences the discussion.
   - 4-6: The text offers general background information referencing [{citation_key}].
   - 1-3: The mention of [{citation_key}] is peripheral or only minimally discussed.
4. In your response, first provide the Score and then give a detailed Explanation. Only discuss citation [{citation_key}], not other citations in the text.

Please provide your answer in exactly the following format:
Score: [number]
Explanation: [Your detailed 2-3 sentence analysis about citation [{citation_key}] only]
"""
    # why not return the data as a json or something to make parsing easier later?
    response = client.chat.completions.create(
        #model="gpt-4-turbo-preview",
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.2,
        top_p=0.95,
    )
    return response.choices[0].message.content


def process_citation_mentions(citation_mentions, enriched, client):
    """Process each citation mention individually, skipping if no summary is available."""
    assessments = {}

    for ref_number, text_excerpts in citation_mentions.items():
        citation_key = f"{ref_number}"  # Convert to string format like "[1]"

        # Check if a summary exists for this citation key
        # sometimes the OCR freaks out and finds citations that don't exist...
        # Try both string and int keys since enriched may use either
        enriched_data = enriched.get(citation_key) or enriched.get(int(ref_number))

        if enriched_data:
            summary_text = enriched_data.get("abstract", None)
            if not summary_text:
                print(f"Skipping {citation_key}: No abstract available.")
                continue

            print(f"Processing {len(text_excerpts)} mentions for {citation_key}...")
            citation_assessments = []

            for idx, mention in enumerate(text_excerpts, 1):
                # Handle both old format (string) and new format (dict with text/page)
                if isinstance(mention, dict):
                    text = mention.get("text", "")
                    page = mention.get("page", 1)
                else:
                    text = mention
                    page = 1

                print(f"  Assessing mention {idx}/{len(text_excerpts)}...")
                try:
                    assessment = assess_citation_relevance(
                        citation_key, text, summary_text, client
                    )
                    citation_assessments.append(
                        {"excerpt": text, "page": page, "assessment": assessment}
                    )
                except Exception as e:
                    print(f"Error processing mention {idx}: {str(e)}")
                    citation_assessments.append(
                        {
                            "excerpt": text,
                            "page": page,
                            "assessment": "Assessment failed",
                            "error": str(e),
                        }
                    )

            assessments[citation_key] = citation_assessments

    return assessments


def assign_scores_to_enriched_papers(enriched_papers, citation_assessments):
    """Assign relevance scores to the reference_mentions in enriched_papers.json."""
    # Create a lookup dictionary for assessments by (citation_key, excerpt) tuple
    # This prevents overwriting when multiple citations share the same excerpt text
    assessment_lookup = {}
    for citation_key, assessments in citation_assessments.items():
        for assessment in assessments:
            excerpt = assessment["excerpt"]
            # Key by both citation_key and excerpt to avoid collisions
            lookup_key = (str(citation_key), excerpt)
            assessment_lookup[lookup_key] = {
                "assessment": assessment["assessment"],
                "page": assessment.get("page", 1)
            }

    # Update enriched_papers with assessments
    for ref_id, paper in enriched_papers.items():
        # Convert ref_id to citation key format for consistency
        citation_key = str(ref_id)

        if "reference_mentions" in paper and paper["reference_mentions"]:
            updated_mentions = []
            for mention in paper["reference_mentions"]:
                # Handle both old format (string) and new format (dict with text/page)
                if isinstance(mention, dict):
                    mention_text = mention.get("text", "")
                    mention_page = mention.get("page", 1)
                else:
                    mention_text = mention
                    mention_page = 1

                # Look up by both citation_key and excerpt
                lookup_key = (citation_key, mention_text)
                if lookup_key in assessment_lookup:
                    # Parse the assessment to extract the score
                    assessment_data = assessment_lookup[lookup_key]
                    assessment_text = assessment_data["assessment"]
                    page = assessment_data.get("page", mention_page)
                    try:
                        score_line = assessment_text.split("\n")[0]  # "Score: [number]"
                        score = int(score_line.split(": ")[1])
                    except (IndexError, ValueError) as e:
                        print(
                            f"Error parsing score for mention in {citation_key}: {assessment_text}. Setting score to None."
                        )
                        score = None

                    updated_mentions.append(
                        {
                            "text": mention_text,
                            "page": page,
                            "relevance_score": score,
                            "assessment": assessment_text,
                        }
                    )
                else:
                    # If no assessment exists (e.g., skipped due to no summary), keep original text
                    updated_mentions.append(
                        {
                            "text": mention_text,
                            "page": mention_page,
                            "relevance_score": None,
                            "assessment": "No assessment available",
                        }
                    )
            paper["reference_mentions"] = updated_mentions
        else:
            print(
                f"No reference_mentions found for {citation_key} in enriched_papers.json."
            )

    return enriched_papers
