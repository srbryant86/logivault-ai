from difflib import SequenceMatcher

def compute_metrics(original: str, optimized: str) -> dict:
    def similarity(a, b):
        return round(SequenceMatcher(None, a, b).ratio() * 100)

    def word_count(text):
        return len(text.split())

    clarity_boost = similarity(optimized, original)
    brevity = round((word_count(original) - word_count(optimized)) / word_count(original) * 100, 2)
    engagement_score = min(100, round((clarity_boost + brevity) / 2 + 20))  # fudge factor

    time_saved = round(word_count(original) / 200 * 1.4, 2)  # avg edit time multiplier
    money_saved = round(time_saved * 75, 2)  # freelance editing cost/hour

    return {
        "clarity": clarity_boost,
        "brevity": brevity,
        "engagement": engagement_score,
        "timeSavedHours": time_saved,
        "moneySaved": money_saved
    }