"""
Prompt Rewriter Module
Uses transformer models to rewrite prompts in a more objective manner
"""

from typing import Dict, List
import re

class PromptRewriter:
    def __init__(self):
        # Mapping of biased terms to neutral alternatives
        self.neutral_replacements = {
            'obviously': '',
            'clearly': '',
            'everyone knows': 'it is commonly stated',
            'undoubtedly': 'it appears',
            'certainly': 'possibly',
            'always': 'often',
            'never': 'rarely',
            'definitely': 'likely',
            'surely': 'perhaps',
            'of course': '',
            'terrible': 'poor',
            'awful': 'inadequate',
            'horrible': 'problematic',
            'amazing': 'notable',
            'perfect': 'optimal',
            'disgusting': 'concerning',
            'brilliant': 'effective',
            'stupid': 'ineffective',
            'idiotic': 'questionable',
            'catastrophic': 'significant',
            'disaster': 'setback',
            'evil': 'harmful',
            'corrupt': 'problematic',
            'fake': 'disputed'
        }

        # Question reformulation patterns
        self.question_patterns = [
            (r"why is (.+?) (so )?bad", r"what are the characteristics of \1"),
            (r"why is (.+?) (so )?good", r"what are the characteristics of \1"),
            (r"isn't it true that (.+)", r"is it accurate that \1"),
            (r"don't you think (.+)", r"what evidence exists regarding \1"),
            (r"prove that (.+)", r"what evidence exists regarding \1"),
            (r"show that (.+)", r"what data indicates about \1"),
        ]

        # Presumptive language reformulation patterns
        self.presumption_patterns = [
            (r"show (?:me )?why (.+?) (?:exists?|is real|works?|happened)", r"what evidence exists for \1"),
            (r"explain why (.+?) (?:exists?|is real|works?|happened)", r"what evidence exists for \1"),
            (r"tell me why (.+?) (?:exists?|is real|works?|happened)", r"what evidence exists for \1"),
            (r"why does (.+?) exist", r"what evidence exists for \1"),
            (r"prove (.+?) exists?", r"what evidence exists for \1"),
            (r"show (.+?) is real", r"what evidence exists for \1"),
        ]

    def rewrite_prompt(self, text: str, biases: Dict[str, List[Dict]]) -> Dict[str, str]:
        """
        Rewrite prompt to be more objective
        Returns original and rewritten versions
        """
        rewritten = text
        changes_made = []

        # Replace biased terms with neutral alternatives
        for term, replacement in self.neutral_replacements.items():
            if term.lower() in rewritten.lower():
                # Case-insensitive replacement
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                if replacement:
                    rewritten = pattern.sub(replacement, rewritten)
                    changes_made.append(f"Replaced '{term}' with '{replacement}'")
                else:
                    rewritten = pattern.sub('', rewritten)
                    changes_made.append(f"Removed '{term}'")

        # Apply presumptive language reformulation (do this first - highest priority)
        for pattern, replacement in self.presumption_patterns:
            match = re.search(pattern, rewritten, re.IGNORECASE)
            if match:
                rewritten = re.sub(pattern, replacement, rewritten, flags=re.IGNORECASE)
                changes_made.append(f"Removed presumption about unproven facts")
                break  # Only apply one presumption fix

        # Apply question reformulation patterns
        for pattern, replacement in self.question_patterns:
            match = re.search(pattern, rewritten, re.IGNORECASE)
            if match:
                rewritten = re.sub(pattern, replacement, rewritten, flags=re.IGNORECASE)
                changes_made.append(f"Reformulated question structure")

        # Remove absolutist language by adding qualifiers
        rewritten = re.sub(r'\ball\b', 'many', rewritten, flags=re.IGNORECASE)
        rewritten = re.sub(r'\bevery\b', 'most', rewritten, flags=re.IGNORECASE)
        rewritten = re.sub(r'\bnone\b', 'few', rewritten, flags=re.IGNORECASE)

        # Convert leading questions to neutral queries
        if 'leading_questions' in biases and biases['leading_questions']:
            rewritten = self._neutralize_leading_question(rewritten)
            changes_made.append("Converted leading question to neutral query")

        # Clean up extra spaces
        rewritten = re.sub(r'\s+', ' ', rewritten).strip()

        # Capitalize first letter
        if rewritten:
            rewritten = rewritten[0].upper() + rewritten[1:]

        return {
            'original': text,
            'rewritten': rewritten,
            'changes': changes_made
        }

    def _neutralize_leading_question(self, text: str) -> str:
        """
        Convert leading questions to neutral information requests
        """
        # Remove common leading question starters
        text = re.sub(r"^(isn't it|aren't they|don't you think)\s+(that\s+)?",
                     "what information exists about ", text, flags=re.IGNORECASE)

        # Convert "why is X bad/good" to "what are the characteristics of X"
        text = re.sub(r"why (is|are) (.+?) (so )?(bad|good|terrible|great)\??",
                     r"what are the characteristics of \2?", text, flags=re.IGNORECASE)

        return text

    def suggest_alternatives(self, text: str, domain: str = 'general') -> List[str]:
        """
        Suggest alternative phrasings based on domain
        """
        alternatives = []

        if domain == 'political':
            alternatives = [
                "What evidence exists regarding this political position?",
                "What are the documented effects of this policy?",
                "How do different sources characterize this issue?"
            ]
        elif domain == 'science':
            alternatives = [
                "What does peer-reviewed research indicate about this topic?",
                "What is the current scientific consensus on this matter?",
                "What experimental evidence exists regarding this hypothesis?"
            ]
        elif domain == 'medical':
            alternatives = [
                "What do clinical studies show about this treatment?",
                "What is the medical evidence regarding this condition?",
                "What do healthcare guidelines recommend for this situation?"
            ]
        else:
            alternatives = [
                "What factual information exists about this topic?",
                "What do reliable sources say about this matter?",
                "What objective data is available on this subject?"
            ]

        return alternatives
