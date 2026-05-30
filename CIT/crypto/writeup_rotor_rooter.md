# rotor_rooter

Ciphertext:

`KLEGCKRGGONTBNBVPIIZWXQQEZYAXXWQMGIZDNEWWUTOVZRWOMZKGWNKWZBQXOGZSTVCGU`

Hint: `Spin it till it drains`

## Ý tưởng

- Tên challenge + hint gợi ý rotor machine.
- Brute-force Enigma-I (rotor order / reflector / start position) cho ra plaintext gần đúng của quote nổi tiếng.
- Cấu hình đúng:
  - Rotors: `I II III`
  - Reflector: `B`
  - Ring: `1 1 1`
  - Start: `AAA`

Raw plaintext:

`WECANONLYSEEASHORTDNHTANCEAHEADBUTWECANSEEPLEIGYTHERETHATNEEDSTOBEDONE`

Chuẩn hoá lỗi ký tự nhỏ thành:

`WE CAN ONLY SEE A SHORT DISTANCE AHEAD BUT WE CAN SEE PLENTY THERE THAT NEEDS TO BE DONE`

## Flag

`CIT{we_can_only_see_a_short_distance_ahead_but_we_can_see_plenty_there_that_needs_to_be_done}`
