"""
Natural Language Query Parser
Extracts intent and parameters from user questions
"""

import re


class QueryParser:
    """
    Parse user questions to determine intent and extract parameters
    """
    
    def __init__(self, ai_helper=None):
        """
        Args:
            ai_helper: Optional AI helper for advanced parsing
        """
        self.ai = ai_helper
    
    def parse_question(self, question: str):
        """
        Extract intent and parameters from question
        
        Returns:
            {
                "intent": "calculate_incentive" | "show_top" | "what_if" | "compare",
                "employee_name": str or None,
                "metric": "mrr" | "total" | "renewal" etc,
                "additional_params": dict
            }
        """
        
        question_lower = question.lower()
        
        # Simple keyword matching (fast)
        intent = self._classify_intent(question_lower)
        
        # Extract employee name if mentioned
        employee_name = self._extract_name(question)
        
        # Extract metric type
        metric = self._extract_metric(question_lower)
        
        # Extract numbers for "what if" scenarios
        additional_amount = self._extract_number(question_lower)
        
        return {
            "intent": intent,
            "employee_name": employee_name,
            "metric": metric,
            "additional_amount": additional_amount
        }
    
    def _classify_intent(self, question: str):
        """Classify question type based on keywords"""
        if any(word in question for word in ["what if", "scenario", "suppose", "add", "close"]):
            return "what_if"
        elif any(word in question for word in ["top", "best", "highest", "rank", "leader"]):
            return "show_top"
        elif any(word in question for word in ["compare", "vs", "versus", "difference"]):
            return "compare"
        else:
            return "calculate_incentive"
    
    def _extract_name(self, question: str):
        """
        Extract person's name (simple version)
        Better approach: maintain a list of known employees
        """
        # Look for capitalized words (likely names)
        words = question.split()
        for i, word in enumerate(words):
            if word and word[0].isupper() and i < len(words) - 1:
                if words[i+1] and words[i+1][0].isupper():
                    return f"{word} {words[i+1]}"
        return None
    
    def _extract_metric(self, question: str):
        """Extract which metric user is asking about"""
        if "mrr" in question:
            return "mrr"
        elif "renewal" in question:
            return "renewal"
        elif "tcv" in question:
            return "tcv"
        elif "total" in question or "overall" in question:
            return "total"
        else:
            return "total"  # default
    
    def _extract_number(self, question: str):
        """Extract dollar amounts from question"""
        # Match patterns like $50K, $50,000, 50000
        patterns = [
            r'\$?([\d,]+)k',  # $50K
            r'\$?([\d,]+)',   # $50,000
        ]
        
        for pattern in patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                num_str = match.group(1).replace(',', '')
                num = float(num_str)
                if 'k' in question.lower():
                    num *= 1000
                return num
        return None

