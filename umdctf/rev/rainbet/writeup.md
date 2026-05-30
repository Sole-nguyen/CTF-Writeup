# rainbet

Bài này hở toàn bộ RNG backend qua `rainbet_gen.wasm`, nên có thể chơi perfect 25 round liên tiếp.

## Điểm mấu chốt

- Frontend (`/static/app.js`) cho biết:
  - lấy `session_id`, `secret` từ `GET /api/sessioninfo`
  - chơi qua websocket `/ws`
  - mỗi move phải kèm:
    - `view` canonical
    - `sig = HMAC_SHA256(secret, view)`
- `rainbet.py` local đã wrap thẳng wasm generator:
  - `generate_game(session_id, round_idx)` cho map mines / cars đúng y hệt server.

=> Ta không cần đoán: mỗi round tính trước full hidden state rồi gửi move max-win.

## Luồng solve

1. `GET /api/sessioninfo` lấy `sid` cookie + `session_id` + `secret`.
2. Mở WS với cookie `sid`.
3. Với mỗi round:
   - gọi `generate_game(session_id, streak)` để biết game thật.
   - **mines**: reveal toàn bộ ô safe.
   - **chicken**: cross đến `max_safe_steps(cars)`, rồi cashout đúng bước đó.
4. Mỗi action đều ký `view` đúng format frontend.
5. Lặp đến khi server trả `flag`.

## Chạy

```bash
python3 solve.py
```

Flag thu được:

```text
UMDCTF{one_might_argue_that_gambling_is_the_best_vice_but_they_would_be_wrong}
```
