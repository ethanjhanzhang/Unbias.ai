"""
Bias Detection Module
Uses NLP techniques to identify subjective language and biases in prompts
"""

import re
from typing import List, Dict, Tuple
import nltk
import ssl
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

class BiasDetector:
    def __init__(self):
        # Fix SSL certificate issue for NLTK downloads
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')

        # Subjective language indicators
        self.subjective_words = {
            'obviously', 'clearly', 'everyone knows', 'it is obvious',
            'undoubtedly', 'certainly', 'always', 'never', 'definitely',
            'surely', 'of course', 'naturally', 'without a doubt'
        }

        # Loaded language (emotional/biased terms)
        self.loaded_terms = {
            'terrible', 'awful', 'horrible', 'amazing', 'perfect',
            'disgusting', 'brilliant', 'stupid', 'idiotic', 'genius',
            'catastrophic', 'disaster', 'evil', 'corrupt', 'fake'
        }

        # Absolutist language
        self.absolutist_patterns = [
            r'\ball\b', r'\bevery\b', r'\bnone\b', r'\bno one\b',
            r'\beveryone\b', r'\balways\b', r'\bnever\b'
        ]

        # Confirmation bias phrases
        self.confirmation_phrases = [
            'prove that', 'show that', 'confirm that', 'verify that',
            'demonstrate that', 'evidence that', 'support the idea',
            'back up the claim'
        ]

        # Presumptive language patterns (assumes unproven facts)
        self.presumption_patterns = [
            r'show (?:me )?why (.+?) (?:exist|is real|works|happened)',
            r'explain why (.+?) (?:exist|is real|works|happened)',
            r'tell me why (.+?) (?:exist|is real|works|happened)',
            r'why does (.+?) exist',
            r'how does (.+?) work',  # Can assume something works when it might not
            r'when did (.+?) happen',  # Assumes event occurred
            r'prove (.+?) exists',
            r'show (.+?) is real'
        ]

    def detect_biases(self, text: str) -> Dict[str, List[Dict]]:
        """
        Analyze text for various types of biases
        Returns dict with bias types and their locations
        """
        biases = {
            'subjective_language': [],
            'loaded_terms': [],
            'absolutist_language': [],
            'confirmation_bias': [],
            'leading_questions': [],
            'presumptive_language': []
        }

        text_lower = text.lower()

        # Detect subjective language
        for word in self.subjective_words:
            if word in text_lower:
                start = text_lower.find(word)
                biases['subjective_language'].append({
                    'term': word,
                    'position': start,
                    'length': len(word)
                })

        # Detect loaded terms
        tokens = word_tokenize(text_lower)
        for token in tokens:
            if token in self.loaded_terms:
                start = text_lower.find(token)
                biases['loaded_terms'].append({
                    'term': token,
                    'position': start,
                    'length': len(token)
                })

        # Detect absolutist language
        for pattern in self.absolutist_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                biases['absolutist_language'].append({
                    'term': match.group(),
                    'position': match.start(),
                    'length': len(match.group())
                })

        # Detect confirmation bias phrases
        for phrase in self.confirmation_phrases:
            if phrase in text_lower:
                start = text_lower.find(phrase)
                biases['confirmation_bias'].append({
                    'term': phrase,
                    'position': start,
                    'length': len(phrase)
                })

        # Detect leading questions
        if '?' in text and any(q in text_lower for q in ['why is', 'why are', "isn't it", "aren't they", "don't you think"]):
            biases['leading_questions'].append({
                'term': 'Leading question detected',
                'position': 0,
                'length': len(text)
            })

        # Detect presumptive language (assumes unproven facts)
        for pattern in self.presumption_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                biases['presumptive_language'].append({
                    'term': match.group(),
                    'position': match.start(),
                    'length': len(match.group())
                })

        return biases

    def get_bias_score(self, biases: Dict[str, List[Dict]]) -> float:
        """
        Calculate overall bias score (0-100, higher = more biased)
        """
        total_biases = sum(len(v) for v in biases.values())
        # Weight different bias types
        weights = {
            'subjective_language': 10,
            'loaded_terms': 15,
            'absolutist_language': 12,
            'confirmation_bias': 20,
            'leading_questions': 25,
            'presumptive_language': 30  # High weight for assuming unproven facts
        }

        weighted_score = sum(
            len(biases[bias_type]) * weights[bias_type]
            for bias_type in biases.keys()
            if bias_type in weights
        )

        # Cap at 100
        return min(weighted_score, 100)
