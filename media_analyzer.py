import json
from gemini_api import gemini_generate, gemini_analyze_video


def analyze_image(image_bytes, image_mime):
    prompt = """
You are analyzing a screenshot or image for TrustLens.

Tasks:

1. Read visible text.
2. Identify the main factual claim.
3. Identify names, organizations, dates and numbers.
4. Explain what the image appears to claim.
5. Mention visible signs that may require verification.

Do NOT declare the image authentic or fake solely from appearance.

Return ONLY JSON:

{
  "extracted_text": "...",
  "claim": "...",
  "entities": ["..."],
  "verification_notes": ["..."]
}
"""

    response = gemini_generate(
        prompt,
        image_bytes=image_bytes,
        image_mime=image_mime
    )

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        cleaned = response.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)


def analyze_video(video_bytes, video_mime):
    prompt = """
You are the video-analysis component of TrustLens.

Analyze this video carefully.

Your tasks:

1. Describe what is visibly happening in the video.
2. Identify whether a human/person appears in the video.
3. Identify the main factual claim or message, if any.
4. Look for observable signs that may indicate digital manipulation,
   synthetic generation, or AI-generated content.
5. Look for visual inconsistencies, unnatural facial movement,
   lip-sync problems, strange motion, lighting inconsistencies,
   frame artifacts, or other suspicious signals.
6. Do NOT claim with certainty that a video is AI-generated
   based only on visual appearance.
7. Clearly state uncertainty and limitations.

Return ONLY valid JSON:

{
  "description": "...",
  "human_present": true,
  "claim": "...",
  "manipulation_signals": [
    "..."
  ],
  "assessment": "Potential manipulation signals detected / No strong manipulation signals detected / Inconclusive",
  "limitations": "..."
}

Do not add markdown.
"""

    return gemini_analyze_video(
        video_bytes,
        video_mime,
        prompt
    )