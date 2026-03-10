"""
Scoring Logic for AI Readiness Assessment
Calculates dimension scores and overall readiness
"""

from collections import defaultdict


def calculate_scores(responses):
    """
    Calculate dimension scores and overall score from user responses

    Args:
        responses: dict of {question_id: selected_value}

    Returns:
        dict with dimension_scores, overall_score, and response count
    """
    # Group scores by dimension
    dimension_scores = defaultdict(list)

    for question_id, value in responses.items():
        # Extract dimension from question_id (e.g., "data_1" -> "data_infrastructure")
        if question_id.startswith("data_"):
            dimension_scores["data_infrastructure"].append(value)
        elif question_id.startswith("skills_"):
            dimension_scores["skills_culture"].append(value)
        elif question_id.startswith("strategy_"):
            dimension_scores["strategy_leadership"].append(value)

    # Calculate averages
    dimension_averages = {
        dimension: round(sum(scores) / len(scores), 2) if scores else 0
        for dimension, scores in dimension_scores.items()
    }

    # Calculate overall score (average of all dimension averages)
    overall_score = round(
        sum(dimension_averages.values()) / len(dimension_averages),
        2
    ) if dimension_averages else 0

    return {
        "dimension_scores": dimension_averages,
        "overall_score": overall_score,
        "total_responses": len(responses)
    }


def get_readiness_level(overall_score):
    """
    Convert numeric score to readiness level category
    Based on Gartner AI Maturity Model

    Args:
        overall_score: float between 1-5

    Returns:
        str: readiness level label
    """
    if overall_score < 1.5:
        return "Emerging"
    elif overall_score < 2.5:
        return "Developing"
    elif overall_score < 3.5:
        return "Competent"
    elif overall_score < 4.5:
        return "Advanced"
    else:
        return "Leading"


def format_scores_for_analysis(scores, responses, questions):
    """
    Format scores and responses for Claude API analysis

    Args:
        scores: dict from calculate_scores()
        responses: dict of {question_id: selected_value}
        questions: list of question dicts

    Returns:
        dict ready for Claude API
    """
    # Create question lookup
    question_lookup = {q["id"]: q for q in questions}

    # Format responses with context
    formatted_responses = []
    for q_id, value in responses.items():
        question = question_lookup.get(q_id)
        if question:
            selected_option = next(
                (opt for opt in question["options"] if opt["value"] == value),
                None
            )
            formatted_responses.append({
                "question": question["text"],
                "dimension": question["dimension"],
                "score": value,
                "answer": selected_option["label"] if selected_option else "Unknown"
            })

    return {
        "overall_score": scores["overall_score"],
        "dimension_scores": scores["dimension_scores"],
        "readiness_level": get_readiness_level(scores["overall_score"]),
        "responses": formatted_responses
    }
