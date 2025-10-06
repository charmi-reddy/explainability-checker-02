import ast
def compute_explainability_score(tree):
    score = 0
    max_score = 100
    issues = []
    has_docstring = any(
        isinstance(node, ast.FunctionDef) and ast.get_docstring(node)
        for node in ast.walk(tree)
    )
    if has_docstring:
        score += 10    
    else:
        issues.append("Missing function docstrings")
    short_names = []
    allowed_short = {'i', 'j', 'x', 'y', '_'}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if len(node.id) < 3 and node.id not in allowed_short:
                short_names.append((node.id, node.lineno))
    if short_names:
        issues += [f"Short variable name '{name}' at line {line}" for name, line in short_names]
    else:
        score += 10

    # Heuristic 3: Modularity
    has_functions = any(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
    if has_functions:
        score += 10
    else:
        issues.append("No functions found — code is not modular.")

    # ✅ Heuristic 4: Deep nesting
    def get_max_depth(node, current_depth=0):
        if not isinstance(node, (ast.If, ast.For, ast.While, ast.FunctionDef, ast.With, ast.Try)):
            return current_depth
        return max(
            [get_max_depth(child, current_depth + 1) for child in ast.iter_child_nodes(node)] + [current_depth]
        )

    nesting_depths = [get_max_depth(node) for node in ast.walk(tree)]
    max_nesting = max(nesting_depths, default=0)

    if max_nesting > 2:
        deduction = min((max_nesting - 2) * 5, 20)
        score -= deduction
        issues.append(f"Deep nesting detected — max depth {max_nesting}, penalized {deduction} points.")
    else:
        score += 10

    final_score = max(min(score, max_score), 0)
    return round(final_score, 2), issues
