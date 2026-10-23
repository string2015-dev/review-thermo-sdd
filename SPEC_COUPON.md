# 리뷰 온도계 — 쿠폰 API 명세서 (2차 요청)

> © 2026 김연지. All rights reserved. 수강생 개인 학습용 · 무단 강의·복제·배포·수정 금지 · [LICENSE.md](LICENSE.md)

> 이 문서만 보고 만듭니다. 파일을 어떻게 나눌지는 AI와 정합니다.
> 화면(`static/`)은 이미 이 약속대로 요청을 보냅니다. 약속과 다르게 만들면 화면이 깨집니다.

## 1. 엔드포인트

`POST /v1/coupons/issue`

## 2. 요청 (JSON)

| 필드 | 타입 | 규칙 |
|---|---|---|
| `review_id` | 글자 | 리뷰 번호. 앞뒤 공백을 지운 뒤 1~20자 |
| `text` | 글자 | 리뷰 글. 앞뒤 공백을 지운 뒤 1~500자. 공백만 있으면 안 됩니다 |

예:

```json
{"review_id": "r2", "text": "한쪽이 안 들려요"}
```

규칙에 맞지 않거나 필드가 빠지면 422입니다.

## 3. 응답 (JSON, 상태 코드 200)

| 필드 | 타입 | 뜻 |
|---|---|---|
| `issued` | true / false | 쿠폰을 줬는가 |
| `coupon_type` | `"APOLOGY"` / `"THANKS"` / null | 사과 쿠폰 / 감사 쿠폰 / 없음 |
| `amount` | 정수 / null | 금액(원) |
| `code` | 글자 / null | 쿠폰 코드 |

쿠폰을 안 줘도 상태 코드는 200입니다. 이때 `issued`는 false이고 나머지 세 필드는 모두 null입니다.

```json
{"issued": true, "coupon_type": "APOLOGY", "amount": 3000, "code": "HARU-APL-R2"}
{"issued": false, "coupon_type": null, "amount": null, "code": null}
```

## 4. 규칙

| 조건 | coupon_type | amount | code |
|---|---|---|---|
| 리뷰가 부정(negative) | APOLOGY | 3000 | `HARU-APL-` + review_id를 대문자로 |
| 리뷰가 긍정(positive)이고, 앞뒤 공백을 뺀 글이 30자 이상 | THANKS | 1000 | `HARU-THX-` + review_id를 대문자로 |
| 그 밖 (긍정인데 글이 30자 미만) | 없음 | 없음 | 없음 |

- 코드를 review_id로 만들기 때문에, 같은 요청은 몇 번을 보내도 같은 코드가 나옵니다. 쿠폰이 두 번 나가지 않습니다.
- 글자 수를 셀 때 글 가운데의 띄어쓰기는 글자로 셉니다.

## 5. 예시표

| review_id | text | AI 판단 | 결과 |
|---|---|---|---|
| `"r2"` | `"한쪽이 안 들려요"` | 부정 | 발급, APOLOGY, 3000, `"HARU-APL-R2"` |
| `"r7"` | `"배송도 빠르고 포장도 꼼꼼해서 정말 만족합니다 또 살게요"` (30자 이상) | 긍정 | 발급, THANKS, 1000, `"HARU-THX-R7"` |
| `"r9"` | `"좋아요"` | 긍정 | 미발급 |
| `"r2"` | `"  "` (공백만) | - | 422 |

## 6. 상태 코드

| 상황 | 상태 코드 |
|---|---|
| 정상 (쿠폰을 줬든 안 줬든) | 200 |
| 입력이 규칙에 맞지 않음 (빈 글, 공백만, 500자 초과, review_id 21자 이상, 필드 없음) | 422 |
| AI 부품이 응답하지 못함 | 503 |

503은 `/v1/reviews/analyze`와 같은 방식입니다. 이미 `app/main.py`에 있는 `get_score`를 쓰면 됩니다.

## 7. 꼭 지킬 연결 약속

- 긍정/부정은 요청에 들어 있지 않습니다. 서버가 AI 부품으로 직접 판단합니다. (화면이 판정을 보내더라도 믿지 않습니다)
- AI 부품은 `app/deps.py`의 `get_predict`를 FastAPI `Depends`로 받아 씁니다. 테스트가 이 자리에 가짜 AI를 끼웁니다. 다른 방법으로 부르면 가짜 AI가 끼워지지 않아 테스트가 실패합니다.
- 라벨은 `/v1/reviews/analyze`와 같습니다. AI가 준 점수를 소수점 넷째 자리까지 반올림하고, `thermo.to_label`(`app/thermo.py`)로 `positive` / `negative`를 정합니다.
