# Prompt Objectivity Analyzer

Web app that detects bias in AI prompts and rewrites them objectively using NLP and AI.

## Features

<img width="800" alt="Screenshot" src="https://github.com/user-attachments/assets/2cc578ba-d984-4eb5-a12c-7b65f3201177" />

- 🔍 **Basic Mode** - Fast, rule-based pattern matching using NLP
- 🤖 **AI Mode** - Deep semantic analysis powered by Google Gemini

**Core Capabilities:**
- Detects 6 bias types: subjective language, loaded terms, absolutist language, confirmation bias, leading questions, presumptive language
- Auto-detects domain (political, science, medical, general)
- Visual bias highlighting with color-coded severity (0-100 score)
- Automatic prompt rewriting with change tracking
- Domain-specific alternative suggestions

## Tech Stack

**Backend:** Python, Flask, NLTK, Google Gemini API
**Frontend:** React, Axios
**ML/NLP:** Tokenization, pattern matching, transformer integration ready

## Quick Start

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your Gemini API key to backend/.env:
# GEMINI_API_KEY=your_key_here

python api/app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

Open http://localhost:3000

## Example

**Input:** "Why is climate change obviously fake?"

**Detected:**
- Bias score: 60
- Subjective language: "obviously"
- Presumptive language: assumes conclusion
- Leading question structure

**Rewritten:** "What evidence exists regarding climate change?"

## Use Cases

- Reduce echo chambers in LLM interactions
- Improve research queries (scientific, medical, political)
- Educational tool for critical thinking
- Combat misinformation through objective framing

## Project Structure

```
├── backend/
│   ├── models/          # Bias detection, prompt rewriting
│   ├── utils/           # Domain detection, Gemini client
│   └── api/             # Flask REST API
├── frontend/
│   ├── src/
│   │   ├── components/  # React UI components
│   │   ├── services/    # API integration
│   │   └── styles/      # CSS
└── README.md
```

## Future Enhancements

- Deep learning model training with user feedback
- RAG integration for factual verification
- Multi-language support
- Browser extension

## License

Private use only.
