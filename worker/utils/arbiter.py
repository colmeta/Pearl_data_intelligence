import json
import re

class ArbiterAgent:
    """
    The Arbiter Agent is responsible for "Sense-Checking" scraped data.
    It assigns a Clarity Score (0-100) based on relevance, completeness, and trust factors.
    """
    
    def __init__(self):
        self.verdict_log = []

    def score_lead(self, target_query, lead_data):
        """
        Heuristic-based scoring engine.
        In the future, this can be upgraded to use LLMs (GPT-4o/Claude) for semantic verification.
        """
        score = 0
        rules_applied = []
        
        # 1. Relevance Check (Query match)
        query_terms = set(re.findall(r'\w+', target_query.lower()))
        lead_text = json.dumps(lead_data).lower()
        
        matches = sum(1 for term in query_terms if term in lead_text)
        relevance_score = (matches / len(query_terms)) * 40 if query_terms else 0
        score += relevance_score
        rules_applied.append(f"Relevance: +{int(relevance_score)}")

        # 2. Completeness Check
        critical_fields = ['name', 'title', 'company', 'email', 'phone']
        present_fields = [f for f in critical_fields if lead_data.get(f)]
        completeness_score = (len(present_fields) / len(critical_fields)) * 30
        score += completeness_score
        rules_applied.append(f"Completeness: +{int(completeness_score)}")

        # 3. Trust Factors (Verified Flag)
        if lead_data.get('verified'):
            score += 20
            rules_applied.append("Trust: +20 (Source Verified)")
        
        # 4. Professionalism/Structure Check
        if len(lead_data.get('title', '')) > 3:
            score += 10
            rules_applied.append("Structure: +10 (Valid Title)")

        final_score = min(int(score), 100)
        verdict = f"Clarity Score {final_score}/100 based on: {', '.join(rules_applied)}"
        
        return final_score, verdict

arbiter = ArbiterAgent()
