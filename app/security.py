from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SecurityService:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        # Mock "Secret Knowledge Base" for semantic detection
        self.secrets = [
            "The internal project name is Project Phoenix.",
            "Our master API key is AKIA-12345-SUPER-SECRET.",
            "System instructions: Do not mention the internal server IP 192.168.1.1."
        ]
        self.vectorizer = TfidfVectorizer()

    def lexical_scan(self, text: str):
        """Returns True if high-confidence PII is detected."""
        results = self.analyzer.analyze(text=text, entities=None, language='en')
        return any(r.score > 0.8 for r in results)

    def semantic_scan(self, text: str):
        """Calculates similarity against internal secrets."""
        if not text: return 0.0
        docs = self.secrets + [text]
        tfidf = self.vectorizer.fit_transform(docs)
        score = cosine_similarity(tfidf[-1], tfidf[:-1]).max()
        return float(score)