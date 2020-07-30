# Criar usuário
curl -X POST "http://127.0.0.1:8000/users/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"cpf\":\"444.619.448-83\",\"name\":\"Ana Clara Zoppi Serpa\",\"email\":\"anaclara.zoppiserpa@gmail.com\",\"login\":\"CIPOI_ADMIN\",\"password\":\"string\"}"

curl -X POST "http://127.0.0.1:8000/users/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"cpf\":\"444.619.448-83\",\"name\":\"Ana Clara Zoppi Serpa\",\"email\":\"anaclara.zoppiserpa@gmail.com\",\"login\":null,\"password\":\"string\"}"

curl -X POST "http://127.0.0.1:8000/users/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"cpf\":\"074.761.958-17\",\"name\":\"Melissa Silva\",\"email\":\"melissa@gmail.com\",\"login\":null,\"password\":\"string\"}"

# Criar hospital

curl -X POST "http://127.0.0.1:8000/hospitals/?password=string" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"code\":\"ABCD\",\"name\":\"Hospital ABCD\",\"type\":\"H\",\"email1\":\"string\",\"email2\":\"string\",\"email3\":\"string\"}"

curl -X POST "http://127.0.0.1:8000/hospitals/?password=string" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"code\":\"EFGH\",\"name\":\"Hospital EFGH\",\"type\":\"H\",\"email1\":\"string\",\"email2\":\"string\",\"email3\":\"string\"}"

curl -X POST "http://127.0.0.1:8000/hospitals/?password=string" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"code\":\"CLAA\",\"name\":\"Clínica A\",\"type\":\"C\",\"email1\":\"string\",\"email2\":\"string\",\"email3\":\"string\"}"

curl -X POST "http://127.0.0.1:8000/hospitals/?password=string" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"code\":\"CLBB\",\"name\":\"Clínica B\",\"type\":\"C\",\"email1\":\"string\",\"email2\":\"string\",\"email3\":\"string\"}"

# Criar resultado

curl -X POST "http://127.0.0.1:8000/result_creation_just_for_test/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"id\":1,\"IDExport\":2,\"Barcode\":3,\"NumLote\":4,\"DataNasc\":\"12/05/1999\",\"HoraNasc\":\"string\",\"DataColeta\":\"16/05/1999\",\"HoraColeta\":\"string\",\"prMotherFirstname\":\"Ana Clara\",\"prMotherSurname\":\"Zoppi Serpa\",\"CPF\":\"444.619.448-83\",\"ptnFirstname\":\"Henrique\",\"ptnSurname\":\"Serpa\",\"DNV\":\"DNV do Henrique\",\"CNS\":\"CNS da Ana\",\"ptnEmail\":\"string\",\"ptnPhone1\":\"string\",\"ptnPhone2\":\"string\",\"CodLocColeta\":\"string\",\"LocalColeta\":\"string\",\"COD_LocColeta\":\"string\",\"COD_HospNasc\":\"string\",\"HospNasc\":\"string\",\"LocalNasc\":\"string\",\"PDF_Filename\":\"string\",\"Tipo_SMS\":\"string\",\"RECORD_CREATION_DATE\":\"2020-07-27T16:09:04.184Z\",\"FILE_EXPORT_DATE\":\"2020-07-27T16:09:04.184Z\",\"FILE_EXPORT_NAME\":\"string\"}"

curl -X POST "http://127.0.0.1:8000/result_creation_just_for_test/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"id\":10,\"IDExport\":20,\"Barcode\":30,\"NumLote\":40,\"DataNasc\":\"12/08/1999\",\"HoraNasc\":\"string\",\"DataColeta\":\"16/08/1999\",\"HoraColeta\":\"string\",\"prMotherFirstname\":\"Ana Clara\",\"prMotherSurname\":\"Zoppi Serpa\",\"CPF\":\"444.619.448-83\",\"ptnFirstname\":\"Alice\",\"ptnSurname\":\"Serpa\",\"DNV\":\"DNV da Alice\",\"CNS\":\"CNS da Ana\",\"ptnEmail\":\"string\",\"ptnPhone1\":\"string\",\"ptnPhone2\":\"string\",\"CodLocColeta\":\"string\",\"LocalColeta\":\"string\",\"COD_LocColeta\":\"string\",\"COD_HospNasc\":\"string\",\"HospNasc\":\"string\",\"LocalNasc\":\"string\",\"PDF_Filename\":\"string\",\"Tipo_SMS\":\"string\",\"RECORD_CREATION_DATE\":\"2020-07-27T16:09:04.184Z\",\"FILE_EXPORT_DATE\":\"2020-07-27T16:09:04.184Z\",\"FILE_EXPORT_NAME\":\"string\"}"

curl -X POST "http://127.0.0.1:8000/result_creation_just_for_test/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"id\":100,\"IDExport\":200,\"Barcode\":300,\"NumLote\":400,\"DataNasc\":\"20/08/1999\",\"HoraNasc\":\"string\",\"DataColeta\":\"26/08/1999\",\"HoraColeta\":\"string\",\"prMotherFirstname\":\"Melissa\",\"prMotherSurname\":\"Silva\",\"CPF\":\"074.761.958-17\",\"ptnFirstname\":\"Luiza\",\"ptnSurname\":\"Silva\",\"DNV\":\"DNV da Luiza\",\"CNS\":\"CNS da Melissa\",\"ptnEmail\":\"string\",\"ptnPhone1\":\"string\",\"ptnPhone2\":\"string\",\"CodLocColeta\":\"string\",\"LocalColeta\":\"string\",\"COD_LocColeta\":\"string\",\"COD_HospNasc\":\"string\",\"HospNasc\":\"string\",\"LocalNasc\":\"string\",\"PDF_Filename\":\"string\",\"Tipo_SMS\":\"string\",\"RECORD_CREATION_DATE\":\"2020-07-27T16:09:04.184Z\",\"FILE_EXPORT_DATE\":\"2020-07-27T16:09:04.184Z\",\"FILE_EXPORT_NAME\":\"string\"}"
