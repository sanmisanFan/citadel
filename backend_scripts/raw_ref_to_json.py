import re
import json
import requests
from time import sleep
from openai import OpenAI
import os

class ReferenceParser:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.s2_base = "https://api.semanticscholar.org/graph/v1"
        self.orcid_base = "https://pub.orcid.org/v3.0"

    def parse_reference(self, text):
        """Main parsing workflow"""
        try:
            # Step 1: Extract basic metadata with GPT
            metadata = self.extract_metadata_with_gpt(text)
            if not metadata:
                return None

            # Step 2: Search Semantic Scholar for canonical data
            s2_data = self.search_semantic_scholar(metadata['title'])
            
            # Step 3: Merge results with priority to Semantic Scholar data
            return self.merge_results(metadata, s2_data)
            
        except Exception as e:
            print(f"Parsing failed: {e}")
            return None

    def extract_metadata_with_gpt(self, text):
        """Get title, venue, and raw authors using GPT"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": """Extract JSON with: title, venue, authors (array of raw names). 
                    Example: {"title": "...", "venue": "...", "authors": ["Smith J", ...]}"""
                },
                {"role": "user", "content": text}
            ],
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)

    def search_semantic_scholar(self, title):
        """Search Semantic Scholar for paper details"""
        try:
            response = requests.get(
                f"{self.s2_base}/paper/search",
                params={
                    'query': title,
                    'fields': 'title,authors,venue,year,externalIds'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json().get('data', [])
                return self.find_best_match(title, results)
                
        except Exception as e:
            print(f"Semantic Scholar search failed: {e}")
        return None

    def find_best_match(self, target_title, results):
        """Find best title match using similarity check"""
        target = self.normalize_title(target_title)
        for paper in results:
            if self.normalize_title(paper['title']) == target:
                return {
                    'title': paper['title'],
                    'venue': paper.get('venue', ''),
                    'year': paper.get('year', ''),
                    'doi': paper.get('externalIds', {}).get('DOI', ''),
                    'authors': [self.process_s2_author(a) for a in paper.get('authors', [])]
                }
        return None

    def process_s2_author(self, author):
        """Enrich author data from Semantic Scholar"""
        enriched = {
            'name': author['name'],
            's2_id': author['authorId'],
            'hIndex': author.get('hIndex'),
            'affiliations': author.get('affiliations', [])
        }
        
        # ORCID lookup
        orcid = self.get_orcid_id(author['name'], author.get('affiliations'))
        if orcid:
            enriched['orcid'] = orcid
            
        return enriched

    def get_orcid_id(self, name, affiliations=[]):
        """Find ORCID ID with context-aware search"""
        try:
            query = f"given-names:{name.split()[0]} family-name:{name.split()[-1]}"
            if affiliations:
                query += f" affiliation-name:{affiliations[0]}"
                
            response = requests.get(
                f"{self.orcid_base}/search",
                params={'q': query},
                headers={'Accept': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json().get('result', [])
                if results:
                    return results[0]['orcid-identifier']['uri']
            sleep(0.5)
        except Exception as e:
            print(f"ORCID lookup failed: {e}")
        return None

    def normalize_title(self, title):
        """Normalize title for comparison"""
        return re.sub(r'[^a-z0-9]', '', title.lower())

    def merge_results(self, metadata, s2_data):
        """Combine GPT and Semantic Scholar results"""
        final = {
            'title': metadata['title'],
            'venue': s2_data['venue'] if s2_data else metadata['venue'],
            'year': s2_data['year'] if s2_data else None,
            'doi': s2_data['doi'] if s2_data else None,
            'authors': s2_data['authors'] if s2_data else self.enrich_gpt_authors(metadata['authors'])
        }
        return final

    def enrich_gpt_authors(self, raw_authors):
        """Fallback author enrichment"""
        return [{'name': name, 'source': 'GPT'} for name in raw_authors]

def process_references(input_file, output_file, api_key):
    with open(input_file, 'r', encoding='utf-8') as f:
        references = [line.strip() for line in f if line.strip()]
    
    parser = ReferenceParser(api_key)
    results = []
    
    for idx, ref in enumerate(references, 1):
        print(f"Processing {idx}/{len(references)}")
        parsed = parser.parse_reference(ref)
        if parsed:
            parsed['id'] = idx
            results.append(parsed)
        sleep(2)  # Rate limiting
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(results)} references")

if __name__ == "__main__":
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("API key not found. Please set OPENAI_API_KEY in your environment.")