"""
Flask API for Prompt Objectivity Analyzer
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.bias_detector import BiasDetector
from models.prompt_rewriter import PromptRewriter

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize models
bias_detector = BiasDetector()
prompt_rewriter = PromptRewriter()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_prompt():
    """
    Main endpoint to analyze and rewrite prompts
    Expects JSON: { "prompt": "text", "domain": "general|political|science|medical" }
    """
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400

        prompt = data['prompt']
        domain = data.get('domain', 'general')

        # Detect biases
        biases = bias_detector.detect_biases(prompt)
        bias_score = bias_detector.get_bias_score(biases)

        # Rewrite prompt
        rewrite_result = prompt_rewriter.rewrite_prompt(prompt, biases)

        # Get domain-specific alternatives
        alternatives = prompt_rewriter.suggest_alternatives(prompt, domain)

        # Prepare response
        response = {
            'original_prompt': prompt,
            'rewritten_prompt': rewrite_result['rewritten'],
            'bias_score': bias_score,
            'biases_detected': biases,
            'changes_made': rewrite_result['changes'],
            'alternative_suggestions': alternatives,
            'domain': domain
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/detect', methods=['POST'])
def detect_only():
    """
    Endpoint to only detect biases without rewriting
    Expects JSON: { "prompt": "text" }
    """
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400

        prompt = data['prompt']

        # Detect biases
        biases = bias_detector.detect_biases(prompt)
        bias_score = bias_detector.get_bias_score(biases)

        response = {
            'prompt': prompt,
            'bias_score': bias_score,
            'biases_detected': biases
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
