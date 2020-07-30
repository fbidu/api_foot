"""
Here be awesome code!
"""
from functools import lru_cache
from pathlib import Path

from typing import List

from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import config, crud, schemas, log
from .auth import oauth2_scheme, verify_password, create_access_token
from .csv_input import import_csv
from .database import SessionLocal, engine, Base
from .pdf_input import save_pdf
from .schemas.pdf_processed import PDFProcessed
from .utils import sha256, is_valid_cpf, is_valid_email


Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)
origins = ["http://localhost:3000", "http://localhost", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache()
def get_settings():
    """
    Returns a new instance of settings
    """
    return config.Settings()


def get_db():
    """
    Returns a new DB instance
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # pylint: disable=no-member


@app.get("/")
def home():
    """
    The root of the API
    """
    return "Hello, world!"


@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Realiza o login de um usuário aceitando como input um formulário com
    `username` e `password`. O `username` pode ser o e-mail ou CPF de
    um usuário.
    """
    user = None

    username = ""

    if is_valid_email(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.email
    elif is_valid_cpf(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.cpf
    else:
        user = crud.find_user(db=db, username=form_data.username)
        username = form_data.username

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {
        "access_token": create_access_token({"sub": username}),
        "token_type": "bearer",
    }

@app.post("/token2")
def login2(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Realiza o login de um usuário aceitando como input um formulário com
    `username` e `password`. O `username` pode ser o e-mail ou CPF de
    um usuário.
    """
    user = None

    username = ""

    if is_valid_email(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.email
    elif is_valid_cpf(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.cpf
    else:
        user = crud.find_user(db=db, username=form_data.username)
        username = form_data.username

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": username})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_data": read_current_user(db, token)
    }


@app.get("/users/token")
def read_token(token: str = Depends(oauth2_scheme)):
    """
    Dado um `token` retorna informações sobre ele.
    """
    return {"token": token}


@app.get("/users/me", response_model=schemas.User)
def read_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Retorna informações do usuário logado atualmente.
    """
    user = crud.get_current_user(db, token)

    if not user:
        raise HTTPException(401, "Token inválido")

    return user


@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Receives a new user record in `user` and creates
    a new user in the current database
    """
    created_user = crud.create_user(db=db, user=user)

    # ANA: ISSO ESTÁ AQUI SÓ PARA EU FAZER TESTE, TEMOS QUE TIRAR DEPOIS
    if created_user.login == "CIPOI_ADMIN":
        created_user.is_superuser = True
    ###############################################################

    log(
        "Foi criado um usuário com os seguintes dados: cpf = %s, email = %s, login = %s"
        % (created_user.cpf, created_user.email, created_user.login),
        db,
    )

    return created_user


@app.post("/roles/", response_model=schemas.User)
def change_role(
    user: schemas.User,
    is_staff: bool = False,
    is_superuser: bool = False,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Altera o papel de um usuário no sistema
    """
    logged_user = crud.get_current_user(db, token)
    updated_user = user

    if logged_user.is_staff:
        updated_user = crud.set_staff_role(user, is_staff, db)
        log("Um usuário staff atualizou a flag staff de outro", db)
        return updated_user
    if logged_user.is_superuser:
        updated_user = crud.set_staff_role(user, is_staff, db)
        updated_user = crud.set_superuser_role(user, is_superuser, db)
        log("Um usuário superuser atualizou as flags staff e superuser de outro", db)
        return updated_user

    log("Um usuário sem privilégio tentou alterar flag de outro", db)
    raise HTTPException(
        status_code=403, detail="Um usuário sem privilégio tentou alterar flag de outro"
    )


@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Lists all users
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        user_list = crud.list_users(db)
        log(f"Usuários foram listados pelo superuser {logged_user.name}.", db)
        return user_list

    log(f"Usuário {logged_user.name}, que não é superuser, tentou listar usuários!", db)
    raise HTTPException(
        status_code=403, detail="Usuário sem permissão tentou listar usuários"
    )


@app.post("/csv/")
def read_csv(csv_file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Receives a CSV input file
    """
    with csv_file.file as file:
        content = file.read()
        content = content.decode("utf-8")
        content = content.split("\n")
        lines = import_csv(content)

    log("CSV foi importado.", db)

    return {"lines": lines}


@app.post("/pdf/", response_model=PDFProcessed)
def read_pdf(
    pdf_file: UploadFile = File(...),
    settings: config.Settings = Depends(get_settings),
    db: Session = Depends(get_db),
):
    """
    Receives and stores a PDF file. The location of the file will be determined
    by the `pdf_storage_path` config.
    """
    file = pdf_file.file
    content = file.read()

    # Builds the path
    target_path = Path(settings.pdf_storage_path)
    filename = target_path.joinpath(pdf_file.filename)

    save_pdf(content, filename)

    log("PDF foi importado.", db)

    return PDFProcessed(
        length=len(content), filename=pdf_file.filename, sha256=sha256(filename)
    )


@app.post(
    "/result_creation_just_for_test/", response_model=schemas.Result, status_code=201
)
def create_result_just_for_test(
    result: schemas.ResultCreate, db: Session = Depends(get_db)
):
    """
    Receives a new result record in `result` and creates
    a new result in the current database
    """
    created_result = crud.create_result(db=db, result=result)

    log(
        "Foi criado um resultado para fins de teste. ID do resultado: %s"
        % (created_result.id),
        db,
    )

    return created_result


# pylint: disable=too-many-arguments
@app.get("/results/", response_model=List[schemas.Result])
def read_results(
    db: Session = Depends(get_db),
    dnv: str = "",
    cns: str = "",
    cpf: str = "",
    data_nasc: str = "",
    data_coleta: str = "",
    local_coleta: str = "",
    mother_firstname: str = "",
    mother_surname: str = "",
    token: str = Depends(oauth2_scheme),
):
    """
    Lista resultados conforme os filtros: resultados cujo DNV é dado
    e o CNS também é dado e assim por diante.

    Se deixar o filtro vazio, ele não será considerado.
    Por exemplo, deixar todos os filtros vazios faz com que
    sejam listados todos os resultados existentes no banco.

    Filtros de nome da mãe e de local de coleta funcionam com operador LIKE:
        Colocar Ana fará com que apenas mães com nome = Ana apareçam.
        Colocar Ana% fará com que mães com nome que começa com Ana apareçam.
        Colocar %Ana% fará com que mães com nome que contém Ana apareçam.

    O mesmo vale pros locais de coleta.
    """

    logged_user = crud.get_current_user(db, token)
    if not (logged_user.is_superuser or logged_user.is_staff):
        cpf = logged_user.cpf

    result_list = crud.read_results(
        db,
        dnv,
        cns,
        cpf,
        data_nasc,
        data_coleta,
        local_coleta,
        mother_firstname,
        mother_surname,
    )

    log(
        "Resultados foram buscados com os seguintes filtros: DNV = %s, "
        "CNS = %s, CPF = %s, DataNasc = %s, DataColeta = %s, "
        "LocalColeta = %s, prMotherFirstname = %s, prMotherSurname = %s"
        % (
            dnv,
            cns,
            cpf,
            data_nasc,
            data_coleta,
            local_coleta,
            mother_firstname,
            mother_surname,
        ),
        db,
    )

    return result_list


# Listar hospitais para o admin, com filtros se ele desejar
@app.get("/hospitals/", response_model=List[schemas.HospitalCS])
def read_hospitals(
    db: Session = Depends(get_db),
    code: str = "",
    name: str = "",
    email: str = "",
    token: str = Depends(oauth2_scheme),
):
    """
    Lista hospitais conforme os filtros. Se o filtro estiver vazio, não é considerado.
    É possível usar operador LIKE no nome do hospital e no e-mail (%).
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        hospital_list = crud.read_hospitals(db, code=code, name=name, email=email)

        log(
            "Hospitais foram buscados com os seguintes filtros: code = %s, name = %s, email = %s"
            % (code, name, email),
            db,
        )

        return hospital_list

    log(
        f"Usuário {logged_user.name}, que não é superuser, tentou listar hospitais.", db
    )
    raise HTTPException(
        status_code=403, detail="Um usuário sem permissão tentou listar hospitais"
    )


# Criar um novo hospital, e o usuário/senha associado a ele


@app.post("/hospitals/", response_model=schemas.HospitalCS)
def create_hospital(
    hospital: schemas.HospitalCSCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Cria um novo hospital
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        created_hospital = crud.create_hospital(db, hospital)

        log(
            "Novo hospital foi criado com code = %s, type = %s, name = %s."
            % (created_hospital.code, created_hospital.type, created_hospital.name),
            db,
        )

        return created_hospital

    log("Usuário que não é superuser tentou criar hospital", db)
    raise HTTPException(
        status_code=403, detail="Um usuário sem permissão tentou criar hospital"
    )


# Alterar um hospital já existente (qualquer campo exceto id, user_id)


@app.put("/hospitals/{hospital_id}/", response_model=schemas.HospitalCS)
def update_hospital(
    hospital_id: int,
    hospital: schemas.HospitalCSUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Atualiza um hospital
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        db_hospital = crud.read_hospitals(db, id_=hospital_id)[0]

        if not db_hospital:
            raise HTTPException(status_code=404, detail="Hospital não encontrado")

        updated_hospital = crud.update_hospital(db, db_hospital, hospital)

        log(
            "Um hospital teve dados atualizados: code = %s, type = %s, name = %s."
            % (updated_hospital.code, updated_hospital.type, updated_hospital.name),
            db,
        )

        return updated_hospital

    log("Usuário que não é superuser tentou atualizar hospital", db)
    raise HTTPException(
        status_code=403, detail="Um usuário sem permissão tentou editar hospital"
    )


# Deletar um hospital existente
@app.delete("/hospitals/{hospital_id}/", response_model=bool)
def delete_hospital(
    hospital_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Deleta um hospital
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        db_hospital = crud.read_hospitals(db, id_=hospital_id)[0]

        if not db_hospital:
            raise HTTPException(status_code=404, detail="Hospital não encontrado")

        deleted = crud.delete_hospital(db, db_hospital)

        log("Tentativa de deletar hospital de ID %s: %s" % (hospital_id, deleted), db)

        return deleted

    log("Usuário que não é superuser tentou deletar hospital", db)
    raise HTTPException(
        status_code=403, detail="Um usuário sem permissão tentou apagar hospital"
    )


@app.get("/logs/", response_model=List[schemas.Log])
def read_logs(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Lista os logs
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        return crud.list_logs(db)

    raise HTTPException(
        status_code=403, detail="Um usuário sem permissão tentou ler os logs"
    )


@app.get("/test_get_hospital_user/", response_model=schemas.User)
def test_get_hospital_user(id_: int, db: Session = Depends(get_db)):
    """
    Teste do user de hospital
    """
    return crud.test_get_hospital_user(db, id_)
