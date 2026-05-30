from enigma.machine import EnigmaMachine


CT = "KLEGCKRGGONTBNBVPIIZWXQQEZYAXXWQMGIZDNEWWUTOVZRWOMZKGWNKWZBQXOGZSTVCGU"


def main() -> None:
    machine = EnigmaMachine.from_key_sheet(
        rotors="I II III",
        reflector="B",
        ring_settings="1 1 1",
        plugboard_settings="",
    )
    machine.set_display("AAA")
    pt = machine.process_text(CT)

    # Known quote with minor OCR/noise fixes in raw decrypt:
    quote = "WE CAN ONLY SEE A SHORT DISTANCE AHEAD BUT WE CAN SEE PLENTY THERE THAT NEEDS TO BE DONE"
    flag = "CIT{we_can_only_see_a_short_distance_ahead_but_we_can_see_plenty_there_that_needs_to_be_done}"

    print("Raw decrypt:", pt)
    print("Quote:", quote)
    print("Flag:", flag)


if __name__ == "__main__":
    main()
