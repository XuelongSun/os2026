import sys
import colorama
colorama.init()

if len(sys.argv) != 2:
    # limit is infinite
    limit = float('inf')
else:
    limit = int(sys.argv[1])
count = 0
n = 0
strings = ''
while True:
    ch = sys.stdin.read(1)
    if not ch:
        sys.exit(0)
        # continue
    else:
        n += 1
        strings += ch
        if ch == '{': count += 1
        elif ch == '}': count -= 1
        elif ch == '\n':
            print(f'{n-1} OK.')
            sys.exit(0)
        else:
            print(f'Error: invalid character {ch!r}')
            break
        if not (0 <= count <= limit):
            print(f'Error: {strings[:n-1]}' + colorama.Fore.RED + strings[n-1] + colorama.Style.RESET_ALL + strings[n:])
            print(colorama.Fore.RED + ' '*(n+6) + '^' + colorama.Style.RESET_ALL)
            break
