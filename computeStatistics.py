# pylint: disable=invalid-name,duplicate-code
"""
Program to compute descriptive statistics from a file.
Calculates: COUNT, MEAN, MEDIAN, MODE, SD, VARIANCE
"""

import sys
import time


def sqrt(number):
    """Calculate square root."""
    if number < 0:
        return None
    if number == 0:
        return 0.0

    guess = number
    for _ in range(1000):
        next_guess = (guess + number / guess) / 2
        if abs(guess - next_guess) < 1e-15:
            return next_guess
        guess = next_guess
    return guess


def sort_list(data):
    """Sort a list of numbers."""
    result = list(data)
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


def compute_mean(data):
    """Calculate mean."""
    total = 0.0
    for value in data:
        total += value
    return total / len(data)


def compute_median(data):
    """Calculate median."""
    sorted_data = sort_list(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def compute_mode(data):
    """Calculate mode."""
    frequency = {}
    for value in data:
        if value in frequency:
            frequency[value] += 1
        else:
            frequency[value] = 1

    max_count = 0
    mode_value = None
    for value, count in frequency.items():
        if count > max_count:
            max_count = count
            mode_value = value

    if max_count == 1:
        return None
    return mode_value


def compute_variance(data, mean, population=True):
    """Calculate variance."""
    sum_sq = 0.0
    for value in data:
        diff = value - mean
        sum_sq += diff * diff
    if population:
        return sum_sq / len(data)
    return sum_sq / (len(data) - 1)


def try_parse_float(text):
    """Attempt to parse text as float."""
    try:
        return float(text), True
    except ValueError:
        return None, False


def extract_number(text):
    """Try to get a number from text."""
    text = text.strip()
    if not text:
        return None, False

    # Try direct, then comma/semicolon as decimal
    for attempt in [text, text.replace(',', '.'), text.replace(';', '.')]:
        result, success = try_parse_float(attempt)
        if success:
            return result, success

    # Try extracting leading numeric part
    numeric = ""
    for i, c in enumerate(text):
        if c in "0123456789.eE":
            numeric += c
        elif c in "+-" and (i == 0 or text[i-1] in "eE"):
            numeric += c
        else:
            break

    return try_parse_float(numeric) if numeric else (None, False)


def read_numbers(filename):
    """Read numbers from file."""
    numbers = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                number, success = extract_number(line)
                if success:
                    numbers.append(number)
                else:
                    print(f"Error: Invalid data at line {line_num}: '{line}'")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except IOError as error:
        print(f"Error reading file: {error}")
        return []
    return numbers


def format_num(value):
    """Format number for output."""
    if value is None:
        return "#N/A"
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value)


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        return

    filename = sys.argv[1]
    start_time = time.time()

    numbers = read_numbers(filename)
    if not numbers:
        print("Error: No valid numbers found in the file.")
        return

    count = len(numbers)
    mean = compute_mean(numbers)
    median = compute_median(numbers)
    mode = compute_mode(numbers)
    pop_var = compute_variance(numbers, mean, population=True)
    variance = compute_variance(numbers, mean, population=False)
    std_dev = sqrt(pop_var)

    elapsed = time.time() - start_time

    output = [
        f"COUNT: {count}",
        f"MEAN: {format_num(mean)}",
        f"MEDIAN: {format_num(median)}",
        f"MODE: {format_num(mode)}",
        f"SD: {format_num(std_dev)}",
        f"VARIANCE: {format_num(variance)}",
        f"Elapsed Time: {elapsed:.6f} seconds"
    ]

    for line in output:
        print(line)

    try:
        with open('StatisticsResults.txt', 'w', encoding='utf-8') as file:
            for line in output:
                file.write(line + '\n')
    except IOError as error:
        print(f"Error writing results file: {error}")


if __name__ == "__main__":
    main()
