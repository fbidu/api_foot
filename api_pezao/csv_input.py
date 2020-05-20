"""
Module that handles CSV import
"""
import csv


def import_csv(csv_content):
    """
    Reads a csv file and returns its line length
    """
    csv_reader = csv.reader(csv_content, delimiter=";")
    next(csv_reader)  # Skip the header
    line_count = 0

    for _ in csv_reader:
        line_count += 1

    return line_count
