from backend.app.config import USE_MOCK_AI

if USE_MOCK_AI:
    from backend.analyzers.mock_ai_reviewer import analyze_code
else:
    from backend.analyzers.openai_reviewer import analyze_code
