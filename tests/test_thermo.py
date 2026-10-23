"""app/thermo.py 테스트 (정답지). 각 줄은 SPEC.md 예시표의 한 줄입니다."""

import pytest

from app.thermo import is_mismatch, to_label, to_temperature

LABEL_CASES = [  # SPEC.md 예시표 to_label: (score, 기대 결과)
    pytest.param(0.9, "positive", id="0.9"),
    pytest.param(0.5, "positive", id="0.5_boundary"),
    pytest.param(0.4999, "negative", id="0.4999"),
    pytest.param(0.1, "negative", id="0.1"),
]

TEMPERATURE_CASES = [  # SPEC.md 예시표 to_temperature: (score, 기대 결과)
    pytest.param(0.8732, 87.3, id="0.8732"),
    pytest.param(0.5, 50.0, id="0.5"),
    pytest.param(0.0, 0.0, id="0.0"),
    pytest.param(1.0, 100.0, id="1.0"),
]

MISMATCH_CASES = [  # SPEC.md 예시표 is_mismatch: (rating, label, 기대 결과)
    pytest.param(5, "negative", True, id="rating5_negative"),
    pytest.param(4, "negative", True, id="rating4_negative"),
    pytest.param(2, "positive", True, id="rating2_positive"),
    pytest.param(1, "positive", True, id="rating1_positive"),
    pytest.param(3, "negative", False, id="rating3_negative"),
    pytest.param(5, "positive", False, id="rating5_positive"),
    pytest.param(1, "negative", False, id="rating1_negative"),
]


@pytest.mark.parametrize("score, expected", LABEL_CASES)
def test_to_label(score, expected):
    assert to_label(score) == expected


@pytest.mark.parametrize("score, expected", TEMPERATURE_CASES)
def test_to_temperature(score, expected):
    assert to_temperature(score) == expected


@pytest.mark.parametrize("rating, label, expected", MISMATCH_CASES)
def test_is_mismatch(rating, label, expected):
    assert is_mismatch(rating, label) == expected

# © 2026 김연지. All rights reserved. 수강생 개인 학습용 · 무단 강의·복제·배포·수정 금지 (LICENSE.md)
