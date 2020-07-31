"""
Module that handles CSV import
"""
from collections import namedtuple
import csv

from pydantic import BaseModel
import pydantic

from .models import Result, TemplatesResult
from .schemas import ResultCreate, TemplatesResultCreate


CSVToPydanticError = namedtuple(
    "CSVToPydanticError", ["csv_record", "validation_error"]
)
CSVToPydanticResult = namedtuple("CSVToPydanticResult", ["objects", "errors"])


def import_results_csv(csv_content, db):
    """
    Reads a csv file and returns its line length
    """
    csv_reader = csv.DictReader(csv_content, delimiter=",")

    transform = {
        "id_reportedPatientsExport": "IDExport",
        "SpcCode1_Barcode": "Barcode",
        "SpcCode2_LotNumber": "LotNumber",
        "BirthDate": "DataNasc",
        "BirthTime": "HoraNasc",
        "sd2ColTimePart_DataHoraColeta": "DataColeta",
        "MotherName": "prMotherFirstname",
        "MotherSurname": "prMotherSurname",
        "MotherSSN_CPF": "CPF",
        "PatientName": "ptnFirstName",
        "PatientSurname": "ptnSurname",
        "PatientSSN_DNV": "DNV",
        "PatientMedRec2_CNS": "CNS",
        "PatientEmail": "ptnEmail",
        "PatientPhone1": "ptnPhone1",
        "PatientPhone2": "ptnPhone2",
        "cntCode1_LocalColeta": "COD_LocalColeta",
        "cntFacility_LocalColeta": "LocalColeta",
        "cntCode1_HospitalNasc": "COD_HospitalNasc",
        "cntFacility_HospitalNasc": "HospitalNasc",
        "rqsCity_LocalNasc": "LocalNasc",
        "PDF_ImageFileName": "PDF_Filename",
        "PDF_ImageDate": "PDF_ImageDate",
        "FILE_EXPORT_DATE": "FILE_EXPORT_DATE",
        "FILE_EXPORT_NAME": "FILE_EXPORT_NAME",
    }

    results = csv_to_pydantic(csv_reader, ResultCreate, transform)

    for result in results.objects:
        db_result = Result(**result.dict())
        db.add(db_result)

    db.commit()
    return results.objects


def import_templates_results_csv(csv_content, db):
    """
    Importa um csv que liga resultados à templates
    """
    csv_reader = csv.DictReader(csv_content, delimiter=",")

    transform = {"id_reportedPatientsExport": "IDExport", "SMS_Code": "template_id"}

    converted = csv_to_pydantic(csv_reader, TemplatesResultCreate, transform)

    for template_result in converted.objects:
        db_template_result = TemplatesResult(**template_result.dict())
        db.add(db_template_result)

    db.commit()
    return converted.objects


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
        new_dict = {}
        for k, v in dict_.items():
            if k in transformer:
                new_dict[transformer[k]] = dict_[k]
            else:
                new_dict[k] = v
        return new_dict

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
