"""
Flask API for Prompt Objectivity Analyzer
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.bias_detector import BiasDetector
from models.prompt_rewriter import PromptRewriter
from utils.domain_detector import DomainDetector
from utils.gemini_client import GeminiClient

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize models
bias_detector = BiasDetector()
prompt_rewriter = PromptRewriter()
domain_detector = DomainDetector()
gemini_client = GeminiClient()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_prompt():
    """
    Main endpoint to analyze and rewrite prompts
    Expects JSON: { "prompt": "text", "mode": "nlp"|"ai" }
    Supports both NLP and AI modes
    """
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400

        prompt = data['prompt']
        mode = data.get('mode', 'nlp')  # Default to NLP mode

        # Automatically detect domain
        domain_result = domain_detector.detect_domain(prompt)
        domain = domain_result['domain']

        if mode == 'ai':
            # AI Mode: Use Gemini to analyze and rewrite
            gemini_result = gemini_client.rewrite_prompt_objectively(prompt, domain)

            if gemini_result['success']:
                gemini_data = gemini_result['data']

                # Convert Gemini's bias format to match our format
                biases_detected = {
                    'subjective_language': [],
                    'loaded_terms': [],
                    'absolutist_language': [],
                    'confirmation_bias': [],
                    'leading_questions': [],
                    'presumptive_language': []
                }

                for bias in gemini_data.get('biases_found', []):
                    bias_type = bias.get('type', 'subjective_language')
                    if bias_type in biases_detected:
                        biases_detected[bias_type].append({
                            'term': bias.get('example', ''),
                            'position': 0,
                            'length': len(bias.get('example', ''))
                        })

                response = {
                    'original_prompt': prompt,
                    'rewritten_prompt': gemini_data.get('rewritten_prompt', prompt),
                    'bias_score': gemini_data.get('bias_score', 0),
                    'biases_detected': biases_detected,
                    'changes_made': gemini_data.get('changes_made', []),
                    'alternative_suggestions': [],
                    'domain': domain,
                    'domain_confidence': domain_result['confidence'],
                    'domain_scores': domain_result['scores'],
                    'mode': 'ai',
                    'ai_explanation': gemini_data.get('explanation', '')
                }
            else:
                return jsonify({'error': gemini_result.get('error', 'AI analysis failed')}), 500

        else:
            # NLP Mode: Use rule-based analysis
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
                'domain': domain,
                'domain_confidence': domain_result['confidence'],
                'domain_scores': domain_result['scores'],
                'mode': 'nlp'
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
