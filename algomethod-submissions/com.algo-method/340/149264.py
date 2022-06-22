import typing
import re
def main() -> typing.NoReturn:
    print('Yes' if re.match(r'^[a-z-]{1,100}$', input()) else 'No')
main()
