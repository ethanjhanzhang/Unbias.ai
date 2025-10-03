"""
Domain Detection Module
Automatically detects the domain/category of a prompt
"""

import re
from typing import Dict

class DomainDetector:
    def __init__(self):
        # Keywords for different domains
        self.domain_keywords = {
            'political': {
                'keywords': [
                    'government', 'politics', 'politician', 'election', 'vote', 'voting',
                    'congress', 'senate', 'president', 'mayor', 'governor', 'law',
                    'legislation', 'policy', 'democrat', 'republican', 'liberal', 'conservative',
                    'party', 'campaign', 'immigration', 'taxes', 'regulation', 'rights',
                    'democracy', 'socialism', 'capitalism', 'freedom', 'liberty'
                ],
                'patterns': [
                    r'\b(?:biden|trump|obama|harris|pence)\b',
                    r'\b(?:white house|capitol|supreme court)\b',
                    r'\b(?:left-wing|right-wing)\b'
                ]
            },
            'science': {
                'keywords': [
                    'research', 'study', 'experiment', 'theory', 'hypothesis', 'data',
                    'scientist', 'laboratory', 'climate', 'evolution', 'physics', 'chemistry',
                    'biology', 'astronomy', 'geology', 'scientific', 'evidence', 'peer-reviewed',
                    'quantum', 'atom', 'molecule', 'species', 'ecosystem', 'energy',
                    'gravity', 'space', 'universe', 'planet', 'DNA', 'gene'
                ],
                'patterns': [
                    r'\b(?:climate change|global warming)\b',
                    r'\b(?:big bang|black hole)\b',
                    r'\b(?:peer.?reviewed)\b'
                ]
            },
            'medical': {
                'keywords': [
                    'doctor', 'hospital', 'patient', 'disease', 'illness', 'diagnosis',
                    'treatment', 'medicine', 'medication', 'surgery', 'therapy', 'vaccine',
                    'symptoms', 'health', 'healthcare', 'medical', 'clinical', 'drug',
                    'virus', 'bacteria', 'infection', 'cancer', 'diabetes', 'heart',
                    'blood', 'pharmaceutical', 'prescription', 'dosage', 'side effects'
                ],
                'patterns': [
                    r'\b(?:covid|coronavirus|pandemic)\b',
                    r'\b(?:FDA|CDC|WHO)\b',
                    r'\b(?:clinical trial|clinical study)\b'
                ]
            }
        }

    def detect_domain(self, text: str) -> Dict[str, any]:
        """
        Detect the domain of the given text
        Returns the domain name and confidence score
        """
        text_lower = text.lower()
        scores = {
            'political': 0,
            'science': 0,
            'medical': 0,
            'general': 0
        }

        # Score each domain based on keyword matches
        for domain, data in self.domain_keywords.items():
            # Check keywords
            for keyword in data['keywords']:
                if keyword in text_lower:
                    scores[domain] += 1

            # Check regex patterns (worth more points)
            for pattern in data['patterns']:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                scores[domain] += len(matches) * 2

        # Determine the domain with highest score
        max_score = max(scores.values())

        if max_score == 0:
            detected_domain = 'general'
            confidence = 'high'
        else:
            detected_domain = max(scores, key=scores.get)

            # Calculate confidence based on score difference
            sorted_scores = sorted(scores.values(), reverse=True)
            if len(sorted_scores) > 1:
                score_diff = sorted_scores[0] - sorted_scores[1]
                if score_diff >= 3:
                    confidence = 'high'
                elif score_diff >= 1:
                    confidence = 'medium'
                else:
                    confidence = 'low'
            else:
                confidence = 'high'

        return {
            'domain': detected_domain,
            'confidence': confidence,
            'scores': scores
        }
