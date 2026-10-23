# 명세서 (1차 요청: 리뷰 온도계)

> © 2026 김연지. All rights reserved. 수강생 개인 학습용 · 무단 강의·복제·배포·수정 금지 · [LICENSE.md](LICENSE.md)

## 1. 이 기능은 무엇을 하나요? (한 문장)

- 리뷰 한 건과 별점을 받아 긍정/부정, 리뷰 온도(0~100℃), 별점 불일치 여부를 알려 줍니다.

## 2. 입력 (무엇을 받나요?)

| 이름 | 종류(글자/숫자) | 허용 범위 | 예 |
|---|---|---|---|
| text | 글자(문자열) | 1~500자 (앞뒤 공백 제거 후) | "배송도 빠르고 품질도 좋아요" |
| rating | 정수(숫자) | 1 ~ 5 | 5 |

## 3. 출력 (무엇을 돌려주나요?)

| 이름 | 종류 | 뜻 | 예 |
|---|---|---|---|
| label | 글자(문자열) | 리뷰 내용의 감성 판별 결과 ("positive" 또는 "negative") | "positive" |
| score | 실수(숫자) | AI 부품이 계산한 긍정 확률 (0.0~1.0, 소수점 넷째 자리) | 0.8732 |
| temperature | 실수(숫자) | 긍정적인 정도를 나타내는 리뷰 온도 (0.0~100.0℃) | 87.3 |
| mismatch | 불리언(참/거짓) | 별점과 리뷰 내용(긍정/부정)의 불일치 여부 | false |

## 4. 규칙 (어떻게 정하나요?)

- **긍정/부정 기준 (`to_label`)**: AI가 예측한 긍정 확률(`score`)이 0.5 이상이면 `"positive"`, 0.5 미만이면 `"negative"`
- **리뷰 온도 계산법 (`to_temperature`)**: `score` × 100 을 계산하여 소수점 첫째 자리까지 반올림 (0.0 ~ 100.0)
- **별점과 내용이 '반대'라는 기준 (`is_mismatch`)**:
  - 별점이 높은데(4~5점) 내용이 부정(`label == "negative"`)인 경우 `True`
  - 별점이 낮은데(1~2점) 내용이 긍정(`label == "positive"`)인 경우 `True`
  - 별점이 3점(중립)이거나, 별점과 내용이 일치하는 경우(별점 4~5 & positive, 별점 1~2 & negative)는 `False`

## 5. 예시표 (이 표가 그대로 테스트가 됩니다)

### to_label
| score | 결과 |
|---|---|
| 0.9 | "positive" |
| 0.5 | "positive" |
| 0.4999 | "negative" |
| 0.1 | "negative" |

### to_temperature
| score | 결과 |
|---|---|
| 0.8732 | 87.3 |
| 0.5 | 50.0 |
| 0.0 | 0.0 |
| 1.0 | 100.0 |

### is_mismatch
| rating | label | 결과 |
|---|---|---|
| 5 | "negative" | True |
| 4 | "negative" | True |
| 2 | "positive" | True |
| 1 | "positive" | True |
| 3 | "negative" | False |
| 5 | "positive" | False |
| 1 | "negative" | False |

## 6. 이런 입력은 거절합니다

- 빈 문자열이거나 공백만 있는 글 (앞뒤 공백 제거 후 0자) -> 422 Unprocessable Entity
- 500자를 초과하는 리뷰 글 -> 422 Unprocessable Entity
- 1 미만이거나 5 초과인 별점 (예: 0점, 6점 등) -> 422 Unprocessable Entity
- AI 부품(`app/sentiment.py`)이 오류를 내거나 응답하지 않는 경우 -> 503 Service Unavailable

## 7. AI와 대화하면서 새로 알게 된 것, 애매했던 것

- 정확히 `score == 0.5`인 경계값에서는 `"positive"`로 판정하며, 온도는 `50.0`℃가 됩니다.
- 별점 3점은 중립으로 취급되어 감성 라벨(`label`)과 상관없이 `mismatch`는 항상 `False`입니다.
- AI 점수(`score`)는 소수점 넷째 자리까지 반올림되어 제공되며, 온도는 소수점 첫째 자리까지 표시됩니다.
