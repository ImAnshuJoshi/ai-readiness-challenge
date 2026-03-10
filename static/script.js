// AI Readiness Assessment - Frontend Logic

let questions = [];
let dimensions = {};
let currentQuestionIndex = 0;
let responses = {};

// Initialize the app
document.addEventListener('DOMContentLoaded', async () => {
    await loadQuestions();
    displayQuestion();

    // Event listeners
    document.getElementById('next-btn').addEventListener('click', handleNext);
    document.getElementById('prev-btn').addEventListener('click', handlePrevious);
    document.getElementById('restart-btn').addEventListener('click', restartAssessment);
});

// Load questions from API
async function loadQuestions() {
    try {
        const response = await fetch('/api/questions');
        const data = await response.json();

        if (data.success) {
            questions = data.questions;
            dimensions = data.dimensions;
        } else {
            showError('Failed to load questions');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

// Display current question
function displayQuestion() {
    const question = questions[currentQuestionIndex];
    const dimension = dimensions[question.dimension];

    // Update dimension header
    const dimensionHeader = document.getElementById('dimension-header');
    dimensionHeader.innerHTML = `
        <div class="dimension-badge" style="background-color: ${dimension.color}20; border-left: 4px solid ${dimension.color}">
            <strong>${dimension.name}</strong>
            <p>${dimension.description}</p>
        </div>
    `;

    // Update question container
    const questionContainer = document.getElementById('question-container');
    questionContainer.innerHTML = `
        <h3 class="question-text">${question.text}</h3>
        <div class="options-container">
            ${question.options.map(option => `
                <label class="option-label ${responses[question.id] === option.value ? 'selected' : ''}">
                    <input
                        type="radio"
                        name="question-${question.id}"
                        value="${option.value}"
                        ${responses[question.id] === option.value ? 'checked' : ''}
                    >
                    <span class="option-text">${option.label}</span>
                </label>
            `).join('')}
        </div>
    `;

    // Add event listeners to options
    const optionLabels = questionContainer.querySelectorAll('.option-label');
    optionLabels.forEach(label => {
        label.addEventListener('click', () => {
            const input = label.querySelector('input');
            responses[question.id] = parseInt(input.value);

            // Update UI
            optionLabels.forEach(l => l.classList.remove('selected'));
            label.classList.add('selected');

            // Enable next button
            updateNavigationButtons();
        });
    });

    // Update progress
    updateProgress();
    updateNavigationButtons();
}

// Update progress bar
function updateProgress() {
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    document.getElementById('progress-fill').style.width = progress + '%';
    document.getElementById('progress-text').textContent =
        `Question ${currentQuestionIndex + 1} of ${questions.length}`;
}

// Update navigation buttons
function updateNavigationButtons() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const currentQuestion = questions[currentQuestionIndex];

    // Enable/disable previous button
    prevBtn.disabled = currentQuestionIndex === 0;

    // Update next button
    const isAnswered = responses[currentQuestion.id] !== undefined;
    const isLastQuestion = currentQuestionIndex === questions.length - 1;

    if (isLastQuestion) {
        nextBtn.textContent = 'Submit Assessment';
        nextBtn.disabled = !isAnswered;
    } else {
        nextBtn.textContent = 'Next';
        nextBtn.disabled = !isAnswered;
    }
}

// Handle next button
function handleNext() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    } else {
        // Submit assessment
        submitAssessment();
    }
}

// Handle previous button
function handlePrevious() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

// Submit assessment
async function submitAssessment() {
    // Show loading state
    document.getElementById('assessment-form').style.display = 'none';
    document.getElementById('progress-container').style.display = 'none';
    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch('/api/assess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ responses })
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data);
        } else {
            showError('Assessment failed: ' + data.error);
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

// Dimension chart instance (destroy before re-creating on restart)
let dimensionsChart = null;

// Display results
function displayResults(data) {
    // Hide loading, show results
    document.getElementById('loading').style.display = 'none';
    document.getElementById('results').style.display = 'block';

    // Overall score
    document.getElementById('overall-score').textContent = data.scores.overall.toFixed(1);
    document.getElementById('readiness-level').textContent = data.insights.readiness_level;

    // Dimension scores
    const dimensionScores = data.scores.dimensions;
    updateDimensionScore('data', dimensionScores.data_infrastructure);
    updateDimensionScore('skills', dimensionScores.skills_culture);
    updateDimensionScore('strategy', dimensionScores.strategy_leadership);

    // Draw dimensions bar chart
    drawDimensionsChart(dimensionScores);

    // Overall insight
    document.getElementById('overall-insight').textContent = data.insights.overall_insight;

    // Dimension insights
    const dimensionInsights = data.insights.dimension_insights;
    const dimensionInsightsContainer = document.getElementById('dimension-insights');
    dimensionInsightsContainer.innerHTML = `
        <div class="dimension-insight">
            <strong>Data & Infrastructure:</strong> ${dimensionInsights.data_infrastructure}
        </div>
        <div class="dimension-insight">
            <strong>Skills & Culture:</strong> ${dimensionInsights.skills_culture}
        </div>
        <div class="dimension-insight">
            <strong>Strategy & Leadership:</strong> ${dimensionInsights.strategy_leadership}
        </div>
    `;

    // Recommendations
    const recommendationsList = document.getElementById('recommendations');
    recommendationsList.innerHTML = data.insights.top_3_recommendations
        .map(rec => `<li>${rec}</li>`)
        .join('');

    // Risks
    const risksList = document.getElementById('risks');
    risksList.innerHTML = data.insights.key_risks
        .map(risk => `<li>${risk}</li>`)
        .join('');

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Draw radar chart of dimension scores
function drawDimensionsChart(dimensionScores) {
    const canvas = document.getElementById('dimensions-chart');
    if (!canvas || typeof Chart === 'undefined') return;

    if (dimensionsChart) {
        dimensionsChart.destroy();
        dimensionsChart = null;
    }

    const labels = ['Data & Infrastructure', 'Skills & Culture', 'Strategy & Leadership'];
    const values = [
        dimensionScores.data_infrastructure ?? 0,
        dimensionScores.skills_culture ?? 0,
        dimensionScores.strategy_leadership ?? 0
    ];

    const ctx = canvas.getContext('2d');
    dimensionsChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels,
            datasets: [{
                label: 'Score (1–5)',
                data: values,
                backgroundColor: 'rgba(59, 130, 246, 0.25)',
                borderColor: '#3B82F6',
                borderWidth: 2,
                pointBackgroundColor: '#3B82F6',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#3B82F6'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    min: 0,
                    max: 5,
                    ticks: { stepSize: 1 }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.label}: ${ctx.raw.toFixed(1)} / 5`
                    }
                }
            }
        }
    });
}

// Update dimension score display
function updateDimensionScore(prefix, score) {
    const percentage = (score / 5) * 100;
    document.getElementById(`${prefix}-score-fill`).style.width = percentage + '%';
    document.getElementById(`${prefix}-score-value`).textContent = score.toFixed(1);
}

// Restart assessment
function restartAssessment() {
    if (dimensionsChart) {
        dimensionsChart.destroy();
        dimensionsChart = null;
    }
    currentQuestionIndex = 0;
    responses = {};

    document.getElementById('results').style.display = 'none';
    document.getElementById('assessment-form').style.display = 'block';
    document.getElementById('progress-container').style.display = 'block';

    displayQuestion();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show error message
function showError(message) {
    document.getElementById('loading').style.display = 'none';
    alert('Error: ' + message);

    // Return to form
    document.getElementById('assessment-form').style.display = 'block';
    document.getElementById('progress-container').style.display = 'block';
}
