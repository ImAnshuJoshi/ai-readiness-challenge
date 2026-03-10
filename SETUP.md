# Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

**Get your API key:** https://console.anthropic.com/settings/keys

### 3. Run the Application

```bash
python app.py
```

Visit **http://localhost:5000** in your browser.

## Testing the Assessment

Try these scenarios to demo different outcomes:

### Scenario 1: Emerging Organization
- Select mostly 1-2 scores across all questions
- Should yield "Emerging" or "Developing" readiness level
- Expect recommendations focused on foundational capabilities

### Scenario 2: Advanced Organization
- Select mostly 4-5 scores across all questions
- Should yield "Advanced" or "Leading" readiness level
- Expect recommendations focused on optimization and innovation

### Scenario 3: Mixed Profile (Most Interesting)
- Data & Infrastructure: 4-5 (strong)
- Skills & Culture: 2-3 (weak)
- Strategy & Leadership: 3-4 (moderate)
- Should highlight the skills gap as a key risk
- Recommendations should prioritize upskilling

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Make sure you created a `.env` file
- Check that the API key is correct
- Restart the Flask app after creating `.env`

### "Module not found" errors
- Make sure you ran `pip install -r requirements.txt`
- Check you're using Python 3.7+

### Claude API errors
- Verify your API key is valid
- Check you have API credits
- Review error message in browser console

## Project Structure

```
ai-readiness-challenge/
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── .env                      # API key (create this)
├── .env.example             # API key template
├── assessment/
│   ├── __init__.py
│   ├── questions.py         # 10 assessment questions
│   ├── scorer.py            # Scoring logic
│   └── analyzer.py          # Claude API integration
├── static/
│   ├── style.css            # Frontend styling
│   └── script.js            # Frontend logic
└── templates/
    └── index.html           # Main UI
```

## API Endpoints

- `GET /` - Main application
- `GET /api/questions` - Fetch all questions
- `POST /api/assess` - Submit assessment, get results
- `GET /api/health` - Health check
