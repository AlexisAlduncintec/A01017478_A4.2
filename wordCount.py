# pylint: disable=invalid-name,duplicate-code
"""
Program to count word frequencies in a file.
"""

import sys
import time
import os


def count_words(filename):
    """Count words in file."""
    word_counts = {}
    blank_count = 0
    total_count = 0

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                stripped = line.strip()
                if not stripped:
                    blank_count += 1
                    continue
                total_count += 1
                word = stripped.lower()
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}, 0, 0
    except IOError as error:
        print(f"Error reading file: {error}")
        return {}, 0, 0

    return word_counts, blank_count, total_count


def sort_words(word_counts):
    """Sort words by frequency then alphabetically."""
    items = list(word_counts.items())
    n = len(items)

    for i in range(n):
        for j in range(0, n - i - 1):
            word1, count1 = items[j]
            word2, count2 = items[j + 1]
            swap = False
            if count1 < count2:
                swap = True
            elif count1 == count2 and word1 > word2:
                swap = True
            if swap:
                items[j], items[j + 1] = items[j + 1], items[j]

    return items


def get_base_name(filepath):
    """Get filename without extension."""
    basename = os.path.basename(filepath)
    if '.' in basename:
        return basename.rsplit('.', 1)[0]
    return basename


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        return

    filename = sys.argv[1]
    start_time = time.time()

    word_counts, blank_count, total_count = count_words(filename)
    if not word_counts and total_count == 0:
        print("Error: No valid words found in the file.")
        return

    sorted_words = sort_words(word_counts)
    elapsed = time.time() - start_time
    file_base = get_base_name(filename)

    output = [f"Row Labels\tCount of {file_base}"]
    for word, count in sorted_words:
        output.append(f"{word}\t{count}")
    if blank_count > 0:
        output.append("(blank)\t")
    output.append(f"Grand Total\t{total_count}")
    output.append(f"\nElapsed Time: {elapsed:.6f} seconds")

    for line in output:
        print(line)

    try:
        with open('WordCountResults.txt', 'w', encoding='utf-8') as file:
            for line in output:
                file.write(line + '\n')
    except IOError as error:
        print(f"Error writing results file: {error}")


if __name__ == "__main__":
    main()
