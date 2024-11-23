from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, EmailStr, ValidationError
import aspectlib

app = FastAPI()

# Aspecto para validación dinámica
@aspectlib.Aspect
def validar_campo(cutpoint, *args, **kwargs):
    # print(f"Validando campo: {cutpoint.__name__}")
    try:
        resultado = yield  # Pasa la ejecución al método original
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return resultado

# Modelo base para los datos
class FormularioUsuario(BaseModel):
    nombre: str
    apellido: str
    contrasena: str
    correo: EmailStr

    @staticmethod
    @validar_campo
    def validar_nombre(nombre: str):
        if len(nombre) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        return nombre

    @staticmethod
    @validar_campo
    def validar_apellido(apellido: str):
        if len(apellido) < 2:
            raise ValueError("El apellido debe tener al menos 2 caracteres")
        return apellido

    @staticmethod
    @validar_campo
    def validar_contrasena(contrasena: str):
        if len(contrasena) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not any(char.isdigit() for char in contrasena):
            raise ValueError("La contraseña debe incluir al menos un número")
        if not any(char.isupper() for char in contrasena):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula")
        return contrasena

    @staticmethod
    @validar_campo
    def validar_correo(correo: str):
        return correo

# Endpoint para obtener el formulario (Método GET)
@app.get("/validar-formulario/")
def obtener_formulario():
    return {"mensaje": "Envía un formulario usando POST con datos JSON"}

# Endpoint para validar el formulario (Método POST)
@app.post("/validar-formulario/")
def validar_formulario(datos_formulario: FormularioUsuario = Body(...)):
    try:
        # Aplicar las validaciones dinámicas a los campos recibidos
        FormularioUsuario.validar_nombre(datos_formulario.nombre)
        FormularioUsuario.validar_apellido(datos_formulario.apellido)
        FormularioUsuario.validar_contrasena(datos_formulario.contrasena)
        FormularioUsuario.validar_correo(datos_formulario.correo)

        # Si todas las validaciones pasan, se devuelve una respuesta de éxito
        return {"mensaje": "Formulario válido"}
    except HTTPException as e:
        raise e
    except Exception as e:
        # Si ocurre un error inesperado, se devuelve un error general
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

# Ejecutar el servidor con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
