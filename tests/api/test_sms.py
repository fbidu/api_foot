"""
Testes funcionais para envio de SMS
"""
from datetime import datetime
from typing import List
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm.session import Session

from api_pezao.crud import (
    create_result,
    read_results,
    lists_unsent_sms,
    sms_sweep,
    confirm_sms,
)
from api_pezao.models import HospitalCS, User, TemplateSMS, TemplatesResult, Result
from api_pezao.schemas import ResultCreate
from ..utils import auth_header, create_demo_hospital, create_demo_user


class TestSMS:
    """
    Classe para testes funcionais de sms
    """

    test_user: User
    client: TestClient
    db: Session
    payload: dict
    test_hospital: HospitalCS
    results: List[ResultCreate]

    @fixture(autouse=True)
    def __test_user(self, client):
        """
        Oferece um usuário de teste
        """
        self.test_user = create_demo_user(client, password="secret")

    @fixture(autouse=True)
    def _test_client(self, client: TestClient):
        """
        Oferece um cliente de teste da API
        """
        self.client = client
        self.client.headers = auth_header(self.client)

    @fixture(autouse=True)
    def _db(self, db: Session):
        """
        Banco de testes
        """
        self.db = db

    @fixture(autouse=True)
    def _test_hospital(self):
        self.payload = {
            "code": "TEST_HC",
            "name": "test hosp",
            "type_": "CS",
            "email1": "testhosp1@test.com",
            "email2": "testhosp2@test.com",
            "email3": "testhosp3@test.com",
        }
        response = create_demo_hospital(self.client, **self.payload)

        id_ = response.json()["id"]
        self.payload["type"] = self.payload.pop("type_")

        self.test_hospital = (
            self.db.query(HospitalCS).filter(HospitalCS.id == id_).first()
        )

    @fixture(autouse=True)
    def _test_results(self):

        template_sms = TemplateSMS(msg="hello, world!")
        self.db.add(template_sms)
        self.db.commit()
        self.db.refresh(template_sms)

        self.results = [
            ResultCreate(
                IDExport=123,
                Barcode=4345,
                NumLote=123,
                DataNasc="08/01/2020",
                HoraNasc="13h45",
                DataColeta="30/07/2020",
                HoraColeta="15h",
                prMotherFirstname="Fulana 1",
                prMotherSurname="de tal",
                CPF="00000000000",
                ptnFirstname="Paciente",
                ptnSurname="um",
                DNV="123456",
                CNS="0000",
                ptnEmail="test1@test1.com",
                ptnPhone1="19 99532-2524",
                ptnPhone2="19995322525",
                CodLocColeta=self.payload["code"],
                LocalColeta=self.payload["code"],
                COD_LocColeta=self.payload["code"],
                COD_HospNasc=self.payload["code"],
                HospNasc=self.payload["code"],
                LocalNasc=self.payload["code"],
                PDF_Filename="resultado.pdf",
                Tipo_SMS="1234",
                RECORD_CREATION_DATE=datetime.now(),
                FILE_EXPORT_DATE=datetime.now(),
                FILE_EXPORT_NAME="teste.pdf",
            ),
            ResultCreate(
                IDExport=1234,
                Barcode=43451,
                NumLote=1231,
                DataNasc="08/02/2020",
                HoraNasc="13h45",
                DataColeta="30/07/2020",
                HoraColeta="15h",
                prMotherFirstname="Fulana 2",
                prMotherSurname="de tal",
                CPF="00000000002",
                ptnFirstname="Paciente",
                ptnSurname="dois",
                DNV="123456",
                CNS="0000",
                ptnEmail="test1@test1.com",
                ptnPhone1="00000000002",
                ptnPhone2="00000000022",
                CodLocColeta="outro_hospital",
                LocalColeta="outro_hospital",
                COD_LocColeta="outro_hospital",
                COD_HospNasc="outro_hospital",
                HospNasc="outro_hospital",
                LocalNasc="outro_hospital",
                PDF_Filename="resultado.pdf",
                Tipo_SMS="1234",
                RECORD_CREATION_DATE=datetime.now(),
                FILE_EXPORT_DATE=datetime.now(),
                FILE_EXPORT_NAME="teste.pdf",
            ),
            ResultCreate(
                IDExport=1235,
                Barcode=4345,
                NumLote=123,
                DataNasc="08/01/2020",
                HoraNasc="13h45",
                DataColeta="30/07/2020",
                HoraColeta="15h",
                prMotherFirstname="Fulana 1",
                prMotherSurname="de tal",
                CPF="00000000003",
                ptnFirstname="Paciente",
                ptnSurname="um",
                DNV="123456",
                CNS="0000",
                ptnEmail="test1@test1.com",
                ptnPhone1="00000000003",
                ptnPhone2="00000000033",
                CodLocColeta=self.payload["code"],
                LocalColeta=self.payload["code"],
                COD_LocColeta=self.payload["code"],
                COD_HospNasc=self.payload["code"],
                HospNasc=self.payload["code"],
                LocalNasc=self.payload["code"],
                PDF_Filename="resultado.pdf",
                Tipo_SMS="1234",
                RECORD_CREATION_DATE=datetime.now(),
                FILE_EXPORT_DATE=datetime.now(),
                FILE_EXPORT_NAME="teste.pdf",
                sms_sent=True,
            ),
        ]

        for result in self.results:
            db_result = create_result(self.db, result)
            self.db.add(
                TemplatesResult(
                    IDExport=db_result.IDExport, template_id=template_sms.id
                )
            )
            self.db.commit()

    def test_results_ok(self):
        """
        Testa se a criação dos resultados funcionou
        """
        assert len(read_results(self.db)) == 3

    def test_lists_unsent_sms(self):
        """
        Testa se listagem de SMS por hospital funciona
        """
        assert len(lists_unsent_sms(self.db)) == 2
        assert len(lists_unsent_sms(self.db, [self.payload["code"]])) == 1

    def test_sms_sweep(self):
        """
        Verifica se o sweep de sms performa de acordo
        """
        all_to_sent = sms_sweep(self.db)
        assert len(all_to_sent) == 3
        assert all_to_sent == [
            ("19995322524", "hello, world!", 1),
            ("19995322525", "hello, world!", 1),
            ("1", None, 2),
        ]

        to_be_sent = sms_sweep(self.db, [self.payload["code"]])
        assert len(to_be_sent) == 2
        assert to_be_sent == [
            ("19995322524", "hello, world!", 1),
            ("19995322525", "hello, world!", 1),
        ]

    def test_confirm_sms(self):
        """
        Testa se o registro de sms enviado funciona
        """
        db_result = self.db.query(Result).filter(Result.id == 1).first()
        assert not db_result.sms_sent
        confirm_sms(self.db, 1)
        self.db.refresh(db_result)
        assert db_result.sms_sent
