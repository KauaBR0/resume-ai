import sys
import os
import unittest

# Add project root to path
sys.path.append(os.getcwd())

from app.services.pdf_service import extract_text_from_pdf
from app.models.schemas import CandidateAnalysis

class TestResumeProcessing(unittest.TestCase):
    def test_pdf_extraction(self):
        pdf_path = os.path.join("Docs", "Curriculo_Bruno_Silva.pdf")
        if not os.path.exists(pdf_path):
            self.skipTest(f"File {pdf_path} not found")
            
        with open(pdf_path, "rb") as f:
            content = f.read()
        
        text = extract_text_from_pdf(content)
        print(f"\nExtracted {len(text)} characters from PDF.")
        
        self.assertTrue(len(text) > 0, "Text extraction failed")
        self.assertIn("Bruno", text, "Could not find expected name in text")
        self.assertIn("Python", text, "Could not find expected skill in text")

    def test_schema_validation(self):
        # Test if Pydantic model accepts valid data
        data = {
            "full_name": "Test User",
            "years_of_experience": 5.5,
            "skills": ["Python", "FastAPI"],
            "seniority": "SENIOR",
            "companies": ["Corp A"],
            "summary": "Expert dev",
            "strengths": ["Fast learner"],
            "weaknesses": ["None"]
        }
        model = CandidateAnalysis(**data)
        self.assertEqual(model.seniority, "SENIOR")
        self.assertEqual(model.match_score, 0.0) # Default

if __name__ == '__main__':
    unittest.main()

