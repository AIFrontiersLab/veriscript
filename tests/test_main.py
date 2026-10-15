import pytest
from main import analyze_text, AnalysisResult, FlaggedItem

def test_empty_input():
    result = analyze_text("")
    assert result.score == 0
    assert len(result.flagged_items) == 0

def test_short_text():
    result = analyze_text("Hi.")
    assert result.score >= 0
    assert isinstance(result, AnalysisResult)

def test_happy_path_ai_detection():
    # Text with high repetition and low variance
    text = "The cat sat. The cat sat. The cat sat. The cat sat. The cat sat. The cat sat."
    result = analyze_text(text)
    assert result.score < 100
    assert len(result.flagged_items) > 0
    # Ensure no UnboundLocalError occurs
    assert result.suggestion is not None or len(result.flagged_items) > 0

def test_revised_text_contains_suggestions():
    text = "This is boring. This is boring. This is boring. This is boring. This is boring. This is boring. This is boring."
    result = analyze_text(text)
    # Should flag repetition
    assert any(f.text != "[Structure]" for f in result.flagged_items)

def test_normal_text_high_score():
    text = "The weather is nice today. I went for a walk in the park. It was very relaxing."
    result = analyze_text(text)
    # Should have fewer flags than repetitive text
    assert result.score > 50