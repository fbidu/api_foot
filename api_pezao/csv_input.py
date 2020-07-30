"""
Module that handles CSV import
"""
from collections import namedtuple
import csv

from pydantic import BaseModel
import pydantic

CSVToPydanticError = namedtuple(
    "CSVToPydanticError", ["csv_record", "validation_error"]
)
CSVToPydanticResult = namedtuple("CSVToPydanticResult", ["objects", "errors"])


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


def csv_to_pydantic(
    csv_reader: csv.DictReader, pydantic_schema: BaseModel, transformer: dict = None
) -> CSVToPydanticResult:
    """
    Converts the lines of a csv_reader to objects of a pydantic schema. If you
    need to rename columns, supply a `transformer` dictionary with the original
    column names as keys and their new name as values.

    Returns a tuple containing two lists -
    """
    result = []
    errors = []

    def rename_dict(dict_, transformer):
        dict_ = dict(dict_)
        for k in dict_:
            if k in transformer:
                dict_[transformer[k]] = dict_.pop(k)
        return dict_

    for record in csv_reader:
        if transformer:
            record = rename_dict(record, transformer)

        record = {k: v for k, v in record.items() if v not in ("", None)}

        try:
            object_ = pydantic_schema.parse_obj(record)
        except pydantic.ValidationError as e:
            errors.append(
                CSVToPydanticError(csv_record=record, validation_error=e.json())
            )
        else:
            result.append(object_)

    return CSVToPydanticResult(result, errors)
