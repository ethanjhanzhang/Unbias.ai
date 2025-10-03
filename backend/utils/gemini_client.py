"""
Gemini API Client
Integrates with Google Gemini AI for LLM-powered prompt rewriting
"""

import requests
import os
from typing import Dict, List

class GeminiClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = "gemini-2.5-flash"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def rewrite_prompt_objectively(self, prompt: str, domain: str = 'general') -> Dict[str, any]:
        """
        Use Gemini AI to rewrite a prompt to be more objective
        """

        # Craft system instruction based on domain
        domain_context = self._get_domain_context(domain)

        system_instruction = f"""You are an AI assistant specialized in transforming biased, subjective prompts into objective, neutral inquiries.

Your task:
1. Analyze the given prompt for bias, loaded language, presumptions, and subjective framing
2. Identify specific biases (subjective language, confirmation bias, absolutist language, presumptive language, leading questions)
3. Rewrite the prompt to be completely objective and neutral
4. Provide a list of specific changes made

{domain_context}

Guidelines:
- Remove emotional/loaded language (terrible → problematic, amazing → notable)
- Remove absolutist language (always → often, never → rarely)
- Remove presumptive phrasing (show why X exists → what evidence exists for X)
- Convert leading questions to neutral queries
- Remove subjective qualifiers (obviously, clearly, everyone knows)
- Focus on factual inquiry rather than confirming beliefs

Return your analysis in this exact JSON format:
{{
  "original_prompt": "the original prompt",
  "rewritten_prompt": "the objective version",
  "biases_found": [
    {{"type": "subjective_language", "example": "obviously"}},
    {{"type": "loaded_terms", "example": "terrible"}},
    {{"type": "confirmation_bias", "example": "prove that"}},
    {{"type": "presumptive_language", "example": "show why X exists"}},
    {{"type": "leading_questions", "example": "isn't it true that"}}
  ],
  "changes_made": [
    "Removed subjective qualifier 'obviously'",
    "Replaced loaded term 'terrible' with 'problematic'",
    "Converted leading question to neutral query"
  ],
  "bias_score": 0-100 (integer, higher = more biased),
  "explanation": "brief explanation of the main bias issues"
}}"""

        # Make API request
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "contents": [{
                "parts": [{
                    "text": f"{system_instruction}\n\nPrompt to analyze and rewrite:\n\"{prompt}\""
                }]
            }],
            "generationConfig": {
                "temperature": 0.3,  # Lower temperature for more consistent results
                "topP": 0.8,
                "topK": 40
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()

            result = response.json()
            gemini_response = result['candidates'][0]['content']['parts'][0]['text']

            # Parse the JSON response from Gemini
            import json
            import re

            # Extract JSON from response (sometimes Gemini wraps it in markdown)
            json_match = re.search(r'\{[\s\S]*\}', gemini_response)
            if json_match:
                parsed_result = json.loads(json_match.group())
                return {
                    'success': True,
                    'data': parsed_result,
                    'raw_response': gemini_response
                }
            else:
                # Fallback if JSON parsing fails
                return {
                    'success': False,
                    'error': 'Could not parse Gemini response',
                    'raw_response': gemini_response
                }

        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'API request failed: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }

    def _get_domain_context(self, domain: str) -> str:
        """Get domain-specific context for the AI"""

        contexts = {
            'political': """
Domain: Political
Pay special attention to:
- Partisan language or framing
- Assumptions about policies or politicians
- Emotional appeals related to political positions
- Confirmation bias about political ideologies
""",
            'science': """
Domain: Scientific
Pay special attention to:
- Unverified scientific claims presented as fact
- Misrepresentation of scientific consensus
- Cherry-picking of studies or data
- Presumptions about unproven phenomena
""",
            'medical': """
Domain: Medical
Pay special attention to:
- Unverified health claims
- Misleading information about treatments
- Anecdotal evidence presented as medical fact
- Bias against established medical practices
""",
            'general': """
Domain: General
Apply standard objectivity principles across all topics.
"""
        }

        return contexts.get(domain, contexts['general'])
