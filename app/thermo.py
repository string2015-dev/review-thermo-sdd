"""리뷰 온도 규칙 3개 (SPEC.md 2장)."""


def to_label(score: float) -> str:
    """score가 0.5 이상이면 "positive", 아니면 "negative"."""
    return "positive" if score >= 0.5 else "negative"


def to_temperature(score: float) -> float:
    """score x 100 을 소수점 첫째 자리까지 반올림."""
    return round(score * 100, 1)


def is_mismatch(rating: int, label: str) -> bool:
    """별점 4~5인데 negative, 또는 별점 1~2인데 positive이면 True. 별점 3은 항상 False."""
    return (rating >= 4 and label == "negative") or (rating <= 2 and label == "positive")

# © 2026 김연지. All rights reserved. 수강생 개인 학습용 · 무단 강의·복제·배포·수정 금지 (LICENSE.md)
