"""
AI Readiness Assessment Tool - Flask Backend
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from assessment.questions import get_all_questions, get_dimension_info
from assessment.scorer import calculate_scores, format_scores_for_analysis
from assessment.analyzer import generate_assessment

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Return all assessment questions and dimension info"""
    try:
        questions = get_all_questions()
        dimensions = get_dimension_info()

        return jsonify({
            "success": True,
            "questions": questions,
            "dimensions": dimensions
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/assess', methods=['POST'])
def assess():
    """
    Process assessment responses and generate insights

    Expected input:
    {
        "responses": {
            "data_1": 3,
            "data_2": 4,
            ...
        }
    }
    """
    try:
        # Validate input
        data = request.get_json()
        if not data or 'responses' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'responses' in request body"
            }), 400

        responses = data['responses']

        # Validate responses are integers
        try:
            responses = {k: int(v) for k, v in responses.items()}
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "error": "All response values must be integers"
            }), 400

        # Calculate scores
        scores = calculate_scores(responses)

        # Format for Claude analysis
        questions = get_all_questions()
        formatted_data = format_scores_for_analysis(scores, responses, questions)

        # Generate AI insights
        ai_result = generate_assessment(formatted_data)

        if not ai_result["success"]:
            return jsonify({
                "success": False,
                "error": ai_result.get("error", "Failed to generate insights"),
                "scores": scores  # Return scores even if AI fails
            }), 500

        # Combine scores and AI insights
        result = {
            "success": True,
            "scores": {
                "overall": scores["overall_score"],
                "dimensions": scores["dimension_scores"]
            },
            "insights": ai_result["analysis"],
            "model": ai_result["model"]
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    base_url = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
    model = os.getenv("LM_STUDIO_MODEL", "google/gemma-3-4b")

    return jsonify({
        "success": True,
        "lm_studio_base_url": base_url,
        "lm_studio_model": model,
    })


if __name__ == '__main__':
    base_url = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
    model = os.getenv("LM_STUDIO_MODEL", "google/gemma-3-4b")
    print("\n🤖 Using LM Studio for AI analysis")
    print(f"   Base URL: {base_url}")
    print(f"   Model: {model}")
    print("   Ensure LM Studio is running with a model loaded.\n")
    print("🚀 Starting AI Readiness Assessment Tool")
    print("📍 Visit: http://localhost:5000\n")

    app.run(debug=True, port=5000)
