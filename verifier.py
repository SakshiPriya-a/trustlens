import json
from gemini_api import gemini_generate
from serpapi_api import search_google, search_news


def extract_claim(user_input):
    prompt = f"""
You are the claim extraction component of a digital
content verification system.

Analyze this user input:

{user_input}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "claim": "main factual claim",
  "category": "news/general/government/finance/shopping/science/other",
  "search_queries": [
    "search query 1",
    "search query 2",
    "search query 3"
  ]
}}

Do not add markdown.
Do not add explanation.
"""

    response = gemini_generate(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        cleaned = response.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)


def collect_evidence(search_queries, category):
    all_results = []

    for query in search_queries[:3]:
        try:
            web_results = search_google(query, 5)
            all_results.extend(web_results)
        except Exception:
            pass

    if category == "news":
        for query in search_queries[:2]:
            try:
                news_results = search_news(query, 5)
                all_results.extend(news_results)
            except Exception:
                pass

    return all_results


def analyze_evidence(claim, evidence):
    evidence_text = ""

    for index, item in enumerate(evidence[:20], start=1):
        evidence_text += f"""
SOURCE {index}
Title: {item.get("title", "")}
Source: {item.get("source", "")}
Date: {item.get("date", "")}
Snippet: {item.get("snippet", "")}
URL: {item.get("link", "")}

"""

    prompt = f"""
You are the final evidence-analysis component of TrustLens.

Claim:
{claim}

Retrieved evidence:
{evidence_text}

Analyze the evidence carefully.

IMPORTANT:
- Do not treat absence of evidence as proof that a claim is false.
- Do not say a claim is definitely true only because many websites repeat it.
- Prefer official or primary sources when available.
- Identify contradictions.
- Distinguish supporting evidence from merely similar information.
- Be transparent about uncertainty.

Return ONLY valid JSON in this exact structure:

{{
  "status": "Strongly Supported / Contradicted / Verification Needed / No Reliable Evidence Found",
  "claim": "{claim}",
  "why": "short explanation",
  "evidence_summary": "summary of the strongest evidence",
  "same_similar_information": [
    "..."
  ],
  "conflicts": [
    "..."
  ],
  "sources": [
    {{
      "title": "...",
      "url": "...",
      "supports": true
    }}
  ]
}}

Do not add markdown.
"""

    response = gemini_generate(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        cleaned = response.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)


def verify_claim(user_input):
    claim_data = extract_claim(user_input)

    claim = claim_data["claim"]
    category = claim_data["category"]
    queries = claim_data["search_queries"]

    evidence = collect_evidence(
        queries,
        category
    )

    if not evidence:
        return {
            "status": "No Reliable Evidence Found",
            "claim": claim,
            "why": "No reliable search evidence was retrieved.",
            "evidence_summary": "",
            "same_similar_information": [],
            "conflicts": [],
            "sources": []
        }

    return analyze_evidence(
        claim,
        evidence
    )