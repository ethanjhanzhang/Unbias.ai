# Prompt Objectivity Analyzer

A web application that uses AI and NLP to detect bias in prompts and rewrite them to be more objective. Combat echo chambers and promote better AI interactions.

## Purpose

Personal LLMs can commonly serve as self-validation chambers or echo chambers. This tool helps users:
- Identify subjective language and biases in their prompts
- Rewrite prompts to be more objective
- Combat misinformation and biased AI responses
- Reduce polarization in political, scientific, and medical queries

## Features

- **Bias Detection**: Identifies subjective language, loaded terms, absolutist language, confirmation bias, and leading questions
- **Prompt Rewriting**: Automatically rewrites prompts to be more neutral and objective
- **Visual Highlighting**: Shows detected biases highlighted in the original text
- **Domain-Specific Analysis**: Tailored suggestions for political, science, medical, or general topics
- **Bias Scoring**: Provides a numerical bias score (0-100)
- **Alternative Suggestions**: Offers multiple objective alternatives to your prompt

## Tech Stack

### Backend
- Python 3.8+
- Flask (REST API)
- NLTK (Natural Language Processing)
- Transformers (for future deep learning integration)
- spaCy (linguistic analysis)

### Frontend
- React 18
- Axios (API communication)
- CSS3 (styling)

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python api/app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Usage

1. Open the web application in your browser
2. Enter your prompt in the text area
3. Select the appropriate domain (general, political, science, or medical)
4. Click "Analyze Prompt"
5. Review the bias analysis, highlighted biases, and rewritten prompt
6. Copy the objective version to use with your AI assistant

## Example

**Original Prompt:**
"Why is climate change obviously a hoax? Everyone knows it's fake news."

**Detected Biases:**
- Subjective language: "obviously"
- Loaded terms: "fake"
- Confirmation bias: Leading question structure

**Rewritten Prompt:**
"What is the scientific evidence regarding climate change?"

## Future Enhancements

- [ ] Implement transformer-based deep learning models
- [ ] Add retrieval-augmented generation (RAG) for context
- [ ] Create model training pipeline for continuous learning
- [ ] Add user feedback mechanism to improve accuracy
- [ ] Implement feature engineering for domain-specific improvements
- [ ] Add support for multiple languages
- [ ] Create browser extension for real-time bias detection

## Architecture

```
prompt-objectivity-analyzer/
├── backend/
│   ├── models/
│   │   ├── bias_detector.py       # NLP bias detection
│   │   └── prompt_rewriter.py     # Prompt rewriting logic
│   ├── api/
│   │   └── app.py                 # Flask REST API
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── services/              # API service layer
│   │   └── styles/                # CSS styling
│   └── package.json
└── README.md
```

## License

For private use only.

## Contributing

This is a personal project. Contributions and suggestions are welcome for educational purposes.
