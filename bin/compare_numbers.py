import re
from sys import argv, exit, stdin


def get_percentage_from_string(inpt: str) -> int:
    pattern = re.compile('\s+([0-9]{2,3})%')
    matches = pattern.findall(inpt)
    if len(matches) != 1:
        print("UNABLE TO FIND MATCH IN INPUT FOR REGEX!!!")
        print("Input:")
        print(f'"""{inpt}"""')
        exit(2)
    return int(matches[0])


if __name__ == '__main__':
    input_str = "\n".join([line for line in stdin])
    if not input_str:
        print('You must pipe input into program!')
        exit(2)

    if len(argv) == 0:
        print(f"You must supply arguments(!): {__file__} <minimum percentage> <optional success message>")
        exit(2)
    elif len(argv) > 3:
        print(f"Received too many arguments! Skipping {argv[3:]!r}")

    threshold = int(argv[1])
    percentage_coverage = get_percentage_from_string(input_str)
    if percentage_coverage < threshold:
        print(f"TOO LOW PERCENTAGE OF CODE COVERAGE!!!")
        exit(1)

    if len(argv) == 4:
        print(f"{argv[3]}")
    else:
        print(f"{percentage_coverage}% test-coverage is sufficient! =D")
    exit(0)
