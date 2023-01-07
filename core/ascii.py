from colorama import Style


def print_ascii_art():
        print(ascii_art)


ascii_art = '''
.____                                             __________
|    |      ____  _____      ____   __ __   ____  \______   \  ____  ___  ___
|    |    _/ __ \ \__  \    / ___\ |  |  \_/ __ \  |    |  _/ /  _ \ \  \/  /
|    |___ \  ___/  / __ \_ / /_/  >|  |  /\  ___/  |    |   \(  <_> ) >    <
|_______ \ \___  >(____  / \___  / |____/  \___  > |______  / \____/ /__/\_ \\
        \/     \/      \/ /_____/              \/         \/               \/'''


def colored(text: str = '', color: str = None, bg: str = None) -> None:

        if color and color[0] == '#':
                color = color[1:]
        if bg and bg[0] == '#':
                bg = bg[1:]

        fore = ''
        back = ''
        reset = '\033[0m'

        # Extract the red, green, and blue components of the colors

        if color:
                fr, fg, fb = (
                        int(color[:2], 16),
                        int(color[2:4], 16),
                        int(color[4:6], 16),
                )

                fore = f'\033[38;2;{fr};{fg};{fb}m'

        if bg:
                br, bg, bb = (
                int(bg[:2], 16),
                int(bg[2:4], 16),
                int(bg[4:6], 16)
                )
                back = f'\033[48;2;{br};{bg};{bb}m'

        print(f'{fore}{back}{text}{reset}')
