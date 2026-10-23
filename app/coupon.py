"""쿠폰 규칙 (SPEC_COUPON.md)."""


def decide_coupon(review_id: str, text: str, label: str) -> dict:
    """negative면 사과 쿠폰 3000원, positive이고 글이 30자 이상이면 감사 쿠폰 1000원.

    코드는 "HARU-APL-" 또는 "HARU-THX-" + review_id 대문자. 그 외는 미발급.
    """
    code_id = review_id.upper()
    if label == "negative":
        return {"issued": True, "coupon_type": "APOLOGY", "amount": 3000, "code": f"HARU-APL-{code_id}"}
    if label == "positive" and len(text.strip()) >= 30:
        return {"issued": True, "coupon_type": "THANKS", "amount": 1000, "code": f"HARU-THX-{code_id}"}
    return {"issued": False, "coupon_type": None, "amount": None, "code": None}

# © 2026 김연지. All rights reserved. 수강생 개인 학습용 · 무단 강의·복제·배포·수정 금지 (LICENSE.md)
