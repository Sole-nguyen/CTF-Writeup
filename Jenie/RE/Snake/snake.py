import sys
import base64

def check_flag(code):
    # SSSssuper SSssecure!!!
    return base64.b64encode(''.join(chr((ord(c) + 2) ^ 0x23) for c in code)[::-1].swapcase().encode()).decode() == "dhpEd2YWFGJxRGRuYlIaYlpyaWJaclNOYlUKcxFlYlZETkFTVmIAUUBXZg=="

print(r"""

                                    __
                      ---_ ...... _/_ -
                     /  .      ./ .'*\ \
                     : '         /__-'   \.
                    /                      ) 
                  _/                  >   .' 
                /   .   .       _.-" /  .' 
                \           __/"     /.'/| 
                  \ '--  .-" /     //' |\| 
                   \|  \ | /     //_ _ |/| 
                    `.  \:     //|_ _ _|\|
                    | \/.    //  | _ _ |/| ASH
                     \_ | \/ /    \ _ _ \\\
                         \__/      \ _ _ \|\
         ------------------------------------------------
    
    ___________________________________     _______________________________
    7     77     77  _  77  7  77     7     7     77  _  77        77     7
    |  ___!|  _  ||  _  ||   __!|  ___!     |   __!|  _  ||  _  _  ||  ___!
    !__   7|  7  ||  7  ||     ||  __|_     |  !  7|  7  ||  7  7  ||  __|_
    7     ||  |  ||  |  ||  7  ||     7     |     ||  |  ||  |  |  ||     7
    !_____!!__!__!!__!__!!__!__!!_____!     !_____!!__!__!!__!__!__!!_____!

""")
print("Welcome to Snake Game! Enter the SSSSSsssecret code to get your flag Ssss.")

flag = input(">>> ")
if check_flag(flag):
    print("Ssss Congratulations! You found the Sssecret flag! You can validate with: ")
    print("JDHACK{" + flag + "}")
else:
    print("\nGame Over! Try again.")
    print(r"""
                          _  /)
                         mo / )
                         |/)\)
                          /\_
                          \__|=
                         (    )
                         __)(__
                   _____/      \\_____
                  |  _     ___   _   ||
                  | | \     |   | \  ||
                  | |  |    |   |  | ||
                  | |_/     |   |_/  ||
                  | | \     |   |    ||
                  | |  \    |   |    ||
                  | |   \. _|_. | .  ||
                  |                  ||
                  |       You        ||
                  |  Eaten by Snake  ||
          *       | *   **    * **   |**      **
           \))ejm97/.,(//,,..,,\||(,,.,\\,.((//
    """)
    sys.exit(1) 
