import ast
import tokenize
from io import BytesIO
from heuristics import compute_explainability_score  # you already wrote this

class CodeAnalyzer:
    def __init__(self, code: str):
        self.code = code
        self.ast_tree = ast.parse(code)
        self.tokens = list(tokenize.tokenize(BytesIO(code.encode()).readline))

    def get_score_and_issues(self):
        return compute_explainability_score(self.ast_tree)

# This is the function used in app.py after file upload
def analyze_code(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    analyzer = CodeAnalyzer(code)
    score, issues = analyzer.get_score_and_issues()
    return score, issues
