"""쿠폰 API 계약 테스트 (강사 제공). SPEC_COUPON.md의 약속을 HTTP 요청과 응답만으로 확인합니다.

내부 함수 이름이나 파일 구조는 보지 않습니다. 그래서 어떻게 나눠 만들든 약속만 지키면 통과합니다.
"""

PRAISE = "배송도 빠르고 포장도 꼼꼼해서 정말 만족합니다 또 살게요"  # 30자 이상


def test_coupon_apology(make_client):
    """부정(점수 0.2) -> 사과 쿠폰 HARU-APL-R2."""
    r = make_client(0.2).post("/v1/coupons/issue", json={"review_id": "r2", "text": "한쪽이 안 들려요"})
    assert r.status_code == 200
    assert r.json() == {"issued": True, "coupon_type": "APOLOGY", "amount": 3000, "code": "HARU-APL-R2"}


def test_coupon_thanks(make_client):
    """긍정(점수 0.9) + 30자 이상 -> 감사 쿠폰."""
    r = make_client(0.9).post("/v1/coupons/issue", json={"review_id": "r7", "text": PRAISE})
    assert r.status_code == 200
    assert r.json() == {"issued": True, "coupon_type": "THANKS", "amount": 1000, "code": "HARU-THX-R7"}


def test_coupon_short_praise(make_client):
    """긍정이어도 글이 짧으면 미발급 (그래도 200)."""
    r = make_client(0.9).post("/v1/coupons/issue", json={"review_id": "r9", "text": "좋아요"})
    assert r.status_code == 200
    assert r.json() == {"issued": False, "coupon_type": None, "amount": None, "code": None}


def test_coupon_same_request_same_code(make_client):
    """같은 요청을 두 번 보내도 같은 코드 (중복 발급 없음)."""
    client = make_client(0.2)
    body = {"review_id": "r2", "text": "한쪽이 안 들려요"}
    first = client.post("/v1/coupons/issue", json=body).json()
    second = client.post("/v1/coupons/issue", json=body).json()
    assert first["code"] == second["code"] == "HARU-APL-R2"


def test_coupon_blank_text(make_client):
    """공백뿐인 글은 422."""
    r = make_client(0.2).post("/v1/coupons/issue", json={"review_id": "r2", "text": "  "})
    assert r.status_code == 422


def test_coupon_ai_down(broken_client):
    """AI 부품이 고장 나면 503 (분석 API와 같은 방식)."""
    r = broken_client.post("/v1/coupons/issue", json={"review_id": "r2", "text": "한쪽이 안 들려요"})
    assert r.status_code == 503

# © 2026 김연지. All rights reserved. 수강생 개인 학습용 · 무단 강의·복제·배포·수정 금지 (LICENSE.md)
