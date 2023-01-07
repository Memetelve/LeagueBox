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

def color_print(str='Empty string', color_fore='', color_back=''):
        print(f'{color_fore}{color_back}{str}{Style.RESET_ALL}')