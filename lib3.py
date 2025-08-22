# libreria3.py

errores_comunes = {
    "teclado": "teclado",
    "tecllado": "teclado",
    "programasion": "programación",
    "holaa": "hola"
}

def corrector(texto):
    palabras = texto.split()
    corregidas = []
    for p in palabras:
        if p.lower() in errores_comunes:
            corregidas.append(errores_comunes[p.lower()])
        else:
            corregidas.append(p)
    return " ".join(corregidas)
