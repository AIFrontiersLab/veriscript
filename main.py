import re
from typing import List, Optional
from pydantic import BaseModel

class FlaggedItem(BaseModel):
    text: str
    reason: str
    suggestion: str

class AnalysisResult(BaseModel):
    score: int
    flagged_items: List[FlaggedItem]
    suggestion: Optional[str] = None

def analyze_text(text: str) -> AnalysisResult:
    if not text or not text.strip():
        return AnalysisResult(score=0, flagged_items=[])

    flagged_items = []
    words = text.split()
    total_words = len(words)
    if total_words == 0:
        return AnalysisResult(score=0, flagged_items=[])

    # 1. Repetition Check
    word_counts = {}
    for w in words:
        w_lower = w.lower()
        if len(w_lower) > 3: # Ignore short words
            word_counts[w_lower] = word_counts.get(w_lower, 0) + 1

    for word, count in word_counts.items():
        if count > 5: # Arbitrary threshold for repetition
            flagged_items.append(FlaggedItem(
                text=word,
                reason=f"Repeated {count} times",
                suggestion=f"Use synonyms for '{word}'"
            ))

    # 2. Burstiness Check (Sentence Length Variance)
    sentences = re.split(r'(?<=[.!?]) +', text)
    variance = 0 # Initialize to avoid UnboundLocalError
    if len(sentences) > 2:
        lengths = [len(s.split()) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        variance = sum((x - avg_len) ** 2 for x in lengths) / len(lengths)

        if variance < 50: # Low variance = robotic
             flagged_items.append(FlaggedItem(
                text="[Structure]",
                reason="Sentences are too uniform in length",
                suggestion="Vary sentence length for natural flow"
            ))

    # 3. Perplexity Simulation (Randomness)
    unique_ratio = len(set(words)) / total_words
    score = 100

    # Penalty for AI markers
    marker_count = sum(1 for f in flagged_items if f.text != "[Structure]")
    score -= marker_count * 10

    # Penalty for low variance
    if variance < 50:
        score -= 20

    # Penalty for low unique ratio (high repetition)
    if unique_ratio < 0.5:
        score -= 30

    score = max(0, min(100, score))

    suggestion = None
    if flagged_items:
        suggestion = flagged_items[0].suggestion

    return AnalysisResult(score=score, flagged_items=flagged_items, suggestion=suggestion)

def demo():
    result = analyze_text("This is a test. This is only a test. This is repetitive.")
    print(f"Score: {result.score}")
    print(f"Flags: {len(result.flagged_items)}")
    print(f"Suggestion: {result.suggestion}")