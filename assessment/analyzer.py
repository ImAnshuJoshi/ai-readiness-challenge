"""
LM Studio Integration for AI Readiness Analysis
Generates personalized insights using a local model (e.g. google/gemma-3-4b)
"""

import os
import json
from openai import OpenAI


def generate_assessment(formatted_data):
    """
    Generate AI readiness insights using LM Studio (OpenAI-compatible API)

    Args:
        formatted_data: dict with scores, readiness_level, and responses

    Returns:
        dict with insights, recommendations, and risks
    """
    base_url = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
    model = os.getenv("LM_STUDIO_MODEL", "google/gemma-3-4b")

    client = OpenAI(base_url=base_url, api_key="not-needed")

    # Build the prompt
    system_prompt = """You are an expert AI readiness consultant with deep knowledge of organizational AI adoption frameworks including Gartner AI Maturity Model, McKinsey State of AI research, MIT Sloan leadership studies, and EU AI Act compliance requirements.

Your role is to provide actionable, specific insights based on an organization's assessment results. Avoid generic consulting jargon. Focus on practical, concrete next steps that reflect the organization's specific situation.

Ground your recommendations in current research and best practices from AI leaders."""

    # Format responses for the prompt
    responses_text = "\n".join([
        f"- {r['question']}\n  Answer: {r['answer']} (Score: {r['score']}/5)"
        for r in formatted_data["responses"]
    ])

    user_prompt = f"""Organization Assessment Results:

Overall Score: {formatted_data['overall_score']}/5
Preliminary Readiness Level: {formatted_data['readiness_level']}

Dimension Scores:
- Data & Infrastructure: {formatted_data['dimension_scores'].get('data_infrastructure', 0):.2f}/5
- Skills & Culture: {formatted_data['dimension_scores'].get('skills_culture', 0):.2f}/5
- Strategy & Leadership: {formatted_data['dimension_scores'].get('strategy_leadership', 0):.2f}/5

Detailed Responses:
{responses_text}

Based on this assessment, provide a comprehensive analysis in JSON format with the following structure:

{{
  "readiness_level": "Emerging|Developing|Competent|Advanced|Leading",
  "overall_insight": "2-3 sentences summarizing the organization's AI readiness and key characteristics",
  "dimension_insights": {{
    "data_infrastructure": "Specific observation about their data and infrastructure situation, highlighting strengths or gaps",
    "skills_culture": "Specific observation about their people capabilities and organizational culture",
    "strategy_leadership": "Specific observation about their strategic direction and leadership commitment"
  }},
  "top_3_recommendations": [
    "First priority action with specific steps",
    "Second priority action with specific steps",
    "Third priority action with specific steps"
  ],
  "key_risks": [
    "Primary risk or blocker to AI adoption",
    "Secondary risk or challenge to address"
  ]
}}

Make sure your insights reference specific responses and are tailored to this organization's situation. Avoid generic advice."""

    # Call LM Studio (OpenAI-compatible) API
    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=2048,
            temperature=0.7,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        response_text = response.choices[0].message.content

        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        else:
            json_text = response_text.strip()

        analysis = json.loads(json_text)

        return {
            "success": True,
            "analysis": analysis,
            "model": model,
        }

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Failed to parse model response: {str(e)}",
            "raw_response": response_text if "response_text" in locals() else None,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"LM Studio API error: {str(e)}",
        }
