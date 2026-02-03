# pylint: disable=invalid-name,duplicate-code
"""
Program to convert numbers to binary and hexadecimal.
"""

import sys
import time


def to_binary(number):
    """Convert to binary."""
    if number == 0:
        return "0"

    digits = []
    temp = number
    while temp > 0:
        digits.append(str(temp % 2))
        temp = temp // 2
    digits.reverse()
    return ''.join(digits)


def to_hex(number):
    """Convert to hexadecimal."""
    if number == 0:
        return "0"

    hex_chars = "0123456789ABCDEF"
    digits = []
    temp = number
    while temp > 0:
        digits.append(hex_chars[temp % 16])
        temp = temp // 16
    digits.reverse()
    return ''.join(digits)


def convert_negative_bin(number):
    """Convert negative number to binary (10-bit two's complement)."""
    twos_comp = (1 << 10) + number
    return to_binary(twos_comp)


def convert_negative_hex(number):
    """Convert negative number to hex with FFFFFFFF prefix."""
    twos_comp = (1 << 32) + number
    hex_val = to_hex(twos_comp)
    while len(hex_val) < 8:
        hex_val = "0" + hex_val
    return "FFFFFFFF" + hex_val[6:]


def convert_number(number):
    """Convert number to binary and hex."""
    if number == 0:
        return ("0", "0")
    if number > 0:
        return (to_binary(number), to_hex(number))
    # Negative
    return (convert_negative_bin(number), convert_negative_hex(number))


def read_and_convert(filename):
    """Read file and convert numbers."""
    results = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            item_num = 0
            for line in file:
                line = line.strip()
                if not line:
                    continue
                item_num += 1
                try:
                    number = int(line)
                    bin_str, hex_str = convert_number(number)
                    results.append((item_num, line, bin_str, hex_str))
                except ValueError:
                    print(f"Error: Invalid data at item {item_num}: '{line}'")
                    results.append((item_num, line, "#VALUE!", "#VALUE!"))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except IOError as error:
        print(f"Error reading file: {error}")
        return []
    return results


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        return

    filename = sys.argv[1]
    start_time = time.time()

    results = read_and_convert(filename)
    if not results:
        print("Error: No data found in the file.")
        return

    elapsed = time.time() - start_time

    output = ["ITEM\tNUMBER\tBIN\tHEX"]
    for item_num, original, bin_str, hex_str in results:
        output.append(f"{item_num}\t{original}\t{bin_str}\t{hex_str}")
    output.append(f"\nElapsed Time: {elapsed:.6f} seconds")

    for line in output:
        print(line)

    try:
        with open('ConvertionResults.txt', 'w', encoding='utf-8') as file:
            for line in output:
                file.write(line + '\n')
    except IOError as error:
        print(f"Error writing results file: {error}")


if __name__ == "__main__":
    main()
