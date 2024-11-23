from fastapi.testclient import TestClient
from src.backend.script import app

client = TestClient(app)

# Casos de prueba para el endpoint POST /validar-formulario/
def test_validar_formulario_valido():
    response = client.post(
        "/validar-formulario/",
        json={
            "nombre": "Juan",
            "apellido": "Pérez",
            "contrasena": "Contrasena1",
            "correo": "juan.perez@example.com",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Formulario válido"}

def test_validar_formulario_nombre_invalido():
    response = client.post(
        "/validar-formulario/",
        json={
            "nombre": "J",
            "apellido": "Pérez",
            "contrasena": "Contrasena1",
            "correo": "juan.perez@example.com",
        },
    )
    assert response.status_code == 400
    assert "El nombre debe tener al menos 2 caracteres" in response.json()["detail"]

def test_validar_formulario_apellido_invalido():
    response = client.post(
        "/validar-formulario/",
        json={
            "nombre": "Juan",
            "apellido": "P",
            "contrasena": "Contrasena1",
            "correo": "juan.perez@example.com",
        },
    )
    assert response.status_code == 400
    assert "El apellido debe tener al menos 2 caracteres" in response.json()["detail"]

def test_validar_formulario_contrasena_corta():
    response = client.post(
        "/validar-formulario/",
        json={
            "nombre": "Juan",
            "apellido": "Pérez",
            "contrasena": "Short1",
            "correo": "juan.perez@example.com",
        },
    )
    assert response.status_code == 400
    assert "La contraseña debe tener al menos 8 caracteres" in response.json()["detail"]

def test_validar_formulario_contrasena_sin_numero():
    response = client.post(
        "/validar-formulario/",
        json={
            "nombre": "Juan",
            "apellido": "Pérez",
            "contrasena": "SinNumero",
            "correo": "juan.perez@example.com",
        },
    )
    assert response.status_code == 400
    assert "La contraseña debe incluir al menos un número" in response.json()["detail"]

def test_validar_formulario_contrasena_sin_mayuscula():
    response = client.post(
        "/validar-formulario/",
        json={
            "nombre": "Juan",
            "apellido": "Pérez",
            "contrasena": "nouppercase1",
            "correo": "juan.perez@example.com",
        },
    )
    assert response.status_code == 400
    assert "La contraseña debe incluir al menos una letra mayúscula" in response.json()["detail"]

def test_validar_formulario_correo_invalido():
    response = client.post(
        "/validar-formulario/",
        json={
            "nombre": "Juan",
            "apellido": "Pérez",
            "contrasena": "Contrasena1",
            "correo": "correo-invalido",  # Correo no válido
        },
    )
    assert response.status_code == 422  # La validación de Pydantic devuelve 422
    assert response.json()["detail"][0]["msg"].startswith("value is not a valid email address")



def test_validar_formulario_datos_faltantes():
    response = client.post("/validar-formulario/", json={})
    assert response.status_code == 422  # La validación de Pydantic devuelve 422
    # Comprobamos que todos los campos faltantes están incluidos en el detalle de errores
    errores = response.json()["detail"]
    campos_faltantes = [error["loc"][-1] for error in errores]
    assert "nombre" in campos_faltantes
    assert "apellido" in campos_faltantes
    assert "contrasena" in campos_faltantes
    assert "correo" in campos_faltantes


# Casos de prueba para el endpoint GET /validar-formulario/
def test_obtener_formulario():
    response = client.get("/validar-formulario/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Envía un formulario usando POST con datos JSON"}
