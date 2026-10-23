"""app/coupon.py 테스트 (정답지). 각 줄은 SPEC_COUPON.md 예시표의 한 줄입니다."""

import pytest

from app.coupon import decide_coupon

# r7의 글: "배송도 빠르고 포장도 꼼꼼해서 정말 만족합니다 또 살게요" (공백 포함 30자 이상)
PRAISE = "배송도 빠르고 포장도 꼼꼼해서 정말 만족합니다 또 살게요"

NOT_ISSUED = {"issued": False, "coupon_type": None, "amount": None, "code": None}

COUPON_CASES = [  # SPEC_COUPON.md 예시표: (review_id, text, label, 기대 결과)
    pytest.param(
        "r2", "한쪽이 안 들려요", "negative",
        {"issued": True, "coupon_type": "APOLOGY", "amount": 3000, "code": "HARU-APL-R2"},
        id="r2_negative_apology",
    ),
    pytest.param(
        "r7", PRAISE, "positive",
        {"issued": True, "coupon_type": "THANKS", "amount": 1000, "code": "HARU-THX-R7"},
        id="r7_long_praise_thanks",
    ),
    pytest.param("r9", "좋아요", "positive", NOT_ISSUED, id="r9_short_praise_none"),
]


@pytest.mark.parametrize("review_id, text, label, expected", COUPON_CASES)
def test_decide_coupon(review_id, text, label, expected):
    assert decide_coupon(review_id, text, label) == expected

# © 2026 김연지. All rights reserved. 수강생 개인 학습용 · 무단 강의·복제·배포·수정 금지 (LICENSE.md)
