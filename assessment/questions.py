"""
AI Readiness Assessment Questions
Based on research from Gartner, McKinsey, MIT Sloan, HBR, and EU frameworks
"""

DIMENSIONS = {
    "data_infrastructure": {
        "name": "Data & Infrastructure Readiness",
        "description": "Technical foundation and data maturity for AI adoption",
        "color": "#3B82F6"
    },
    "skills_culture": {
        "name": "Skills & Culture",
        "description": "Digital competence, learning culture, and change readiness",
        "color": "#8B5CF6"
    },
    "strategy_leadership": {
        "name": "Strategy & Leadership",
        "description": "AI vision, commitment, and strategic alignment",
        "color": "#EC4899"
    }
}

QUESTIONS = [
    # Data & Infrastructure (4 questions)
    {
        "id": "data_1",
        "dimension": "data_infrastructure",
        "text": "How would you describe your organization's data quality and accessibility?",
        "options": [
            {"value": 1, "label": "Fragmented across silos, poor quality"},
            {"value": 2, "label": "Basic collection, some quality issues"},
            {"value": 3, "label": "Centralized but inconsistent quality"},
            {"value": 4, "label": "Well-maintained, mostly accessible"},
            {"value": 5, "label": "Enterprise-grade, real-time accessible"}
        ]
    },
    {
        "id": "data_2",
        "dimension": "data_infrastructure",
        "text": "What is your current cloud infrastructure and computing capacity?",
        "options": [
            {"value": 1, "label": "On-premise only, limited capacity"},
            {"value": 2, "label": "Hybrid, basic cloud presence"},
            {"value": 3, "label": "Cloud-first, standard compute resources"},
            {"value": 4, "label": "Multi-cloud, scalable infrastructure"},
            {"value": 5, "label": "Advanced cloud-native with GPU/TPU access"}
        ]
    },
    {
        "id": "data_3",
        "dimension": "data_infrastructure",
        "text": "How integrated are your current systems and data sources?",
        "options": [
            {"value": 1, "label": "Isolated systems, manual data transfer"},
            {"value": 2, "label": "Some APIs, limited integration"},
            {"value": 3, "label": "Moderate integration via middleware"},
            {"value": 4, "label": "Well-integrated with API-first approach"},
            {"value": 5, "label": "Fully integrated, real-time data flows"}
        ]
    },
    {
        "id": "data_4",
        "dimension": "data_infrastructure",
        "text": "What level of data governance and compliance measures do you have?",
        "options": [
            {"value": 1, "label": "Ad-hoc, no formal policies"},
            {"value": 2, "label": "Basic policies, limited enforcement"},
            {"value": 3, "label": "Documented governance, partial compliance"},
            {"value": 4, "label": "Strong governance, GDPR/regulatory compliant"},
            {"value": 5, "label": "Comprehensive governance aligned with EU AI Act"}
        ]
    },

    # Skills & Culture (3 questions)
    {
        "id": "skills_1",
        "dimension": "skills_culture",
        "text": "What is the general level of digital competence across your organization?",
        "options": [
            {"value": 1, "label": "Limited digital skills, resistance to change"},
            {"value": 2, "label": "Basic digital literacy, some resistance"},
            {"value": 3, "label": "Competent users, mixed adoption rates"},
            {"value": 4, "label": "Strong digital skills, open to innovation"},
            {"value": 5, "label": "Advanced digital natives, innovation-driven culture"}
        ]
    },
    {
        "id": "skills_2",
        "dimension": "skills_culture",
        "text": "How does your organization approach learning and upskilling?",
        "options": [
            {"value": 1, "label": "No formal training programs"},
            {"value": 2, "label": "Occasional training, low participation"},
            {"value": 3, "label": "Regular training programs available"},
            {"value": 4, "label": "Continuous learning culture, good uptake"},
            {"value": 5, "label": "Strategic learning initiatives, AI/tech focus"}
        ]
    },
    {
        "id": "skills_3",
        "dimension": "skills_culture",
        "text": "How open is your organization to experimenting with new technologies?",
        "options": [
            {"value": 1, "label": "Risk-averse, avoid experimentation"},
            {"value": 2, "label": "Cautious, limited pilot projects"},
            {"value": 3, "label": "Moderate openness, some innovation initiatives"},
            {"value": 4, "label": "Encourages experimentation, innovation budget"},
            {"value": 5, "label": "Innovation-first mindset, dedicated labs/teams"}
        ]
    },

    # Strategy & Leadership (3 questions)
    {
        "id": "strategy_1",
        "dimension": "strategy_leadership",
        "text": "Does your leadership have a clear AI vision and strategy?",
        "options": [
            {"value": 1, "label": "No AI strategy or discussion"},
            {"value": 2, "label": "Awareness but no concrete plans"},
            {"value": 3, "label": "Draft strategy under development"},
            {"value": 4, "label": "Clear AI strategy with roadmap"},
            {"value": 5, "label": "Integrated AI strategy, board-level commitment"}
        ]
    },
    {
        "id": "strategy_2",
        "dimension": "strategy_leadership",
        "text": "What resources are allocated to AI and digital transformation?",
        "options": [
            {"value": 1, "label": "No dedicated budget or resources"},
            {"value": 2, "label": "Minimal budget, shared resources"},
            {"value": 3, "label": "Moderate budget, part-time team"},
            {"value": 4, "label": "Significant investment, dedicated team"},
            {"value": 5, "label": "Strategic priority, substantial budget & talent"}
        ]
    },
    {
        "id": "strategy_3",
        "dimension": "strategy_leadership",
        "text": "How aligned are your AI initiatives with business objectives?",
        "options": [
            {"value": 1, "label": "No alignment or AI initiatives"},
            {"value": 2, "label": "Isolated projects, unclear ROI"},
            {"value": 3, "label": "Some alignment, ad-hoc initiatives"},
            {"value": 4, "label": "Well-aligned with strategic goals"},
            {"value": 5, "label": "Fully integrated, measurable business impact"}
        ]
    }
]


def get_all_questions():
    """Return all assessment questions"""
    return QUESTIONS


def get_questions_by_dimension(dimension):
    """Return questions for a specific dimension"""
    return [q for q in QUESTIONS if q["dimension"] == dimension]


def get_dimension_info():
    """Return information about all dimensions"""
    return DIMENSIONS
