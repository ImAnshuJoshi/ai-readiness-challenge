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

### 2. Run LM Studio with a model

1. Install [LM Studio](https://lmstudio.ai/) and open it.
2. Download the **google/gemma-3-4b** model (or another model) and load it.
3. Start the local server in LM Studio (e.g. **Develop → Local Server**, then Start Server). The API runs at `http://localhost:1234/v1` by default.

Optional: create a `.env` file to override defaults:

```bash
cp .env.example .env
```

Edit `.env` if needed:

```
# LM_STUDIO_BASE_URL=http://localhost:1234/v1
# LM_STUDIO_MODEL=google/gemma-3-4b
```

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

### "LM Studio API error" / connection refused
- Ensure LM Studio is running and the local server is started.
- Confirm the model (e.g. google/gemma-3-4b) is loaded in LM Studio.
- Check that the server is on `http://localhost:1234` (or set `LM_STUDIO_BASE_URL` in `.env`).

### "Module not found" errors
- Run `pip install -r requirements.txt`
- Use Python 3.7+

### Model response or JSON parse errors
- Try a different or larger model in LM Studio.
- Check the raw error in the browser or server logs.

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
│   └── analyzer.py          # LM Studio (OpenAI-compatible) integration
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
