#!/usr/bin/env python3
"""
Reconstruye un formulario de GitHub a partir de un HTML recién exportado de JotForm.

Uso:
    python3 herramientas/reconstruir.py RUTA_EXPORT_JOTFORM.html NOMBRE_FORMULARIO

Ejemplo:
    python3 herramientas/reconstruir.py ~/Descargas/export.html DEVOLUCION_DE_FIANZA

Qué hace:
  1. Lee el HTML actual del repo (NOMBRE_FORMULARIO.html) y saca SOLO los bloques
     añadidos a mano (autorrelleno de Airtable, GUARDA REFERENCIA y DH EXTRA).
  2. Los pega al final del HTML nuevo de JotForm (justo antes de </body>).
  3. Comprueba que el ID del formulario coincide y que todos los campos (input_XXX)
     que usan esos bloques siguen existiendo en el HTML nuevo. Si alguno falta,
     lo avisa y NO escribe nada.
  4. Si todo cuadra, sobrescribe NOMBRE_FORMULARIO.html con la versión nueva.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CUSTOM = re.compile(r'<script>(?:(?!</script>).)*?(?:AIRTABLE_TOKEN|GUARDA REFERENCIA|DH EXTRA)(?:(?!</script>).)*?</script>\r?\n?', re.S)


def form_id(html):
    m = re.search(r'<form [^>]*id="(\d+)"', html)
    return m.group(1) if m else None


def ref_id(html):
    m = re.search(r'<label[^>]*for="(input_\d+)"[^>]*>\s*REFERENCIA', html)
    return m.group(1) if m else None


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    nuevo_path, nombre = Path(sys.argv[1]), sys.argv[2].removesuffix(".html")
    actual_path = REPO / f"{nombre}.html"
    if not actual_path.exists():
        sys.exit(f"ERROR: no existe {actual_path.name} en el repo. Si es un formulario nuevo, hay que montarlo a mano (ver PERSONALIZACIONES.md).")

    actual = open(actual_path, encoding="utf-8", newline="").read()
    nuevo = open(nuevo_path, encoding="utf-8", newline="").read()
    bloques = [m.group(0) for m in CUSTOM.finditer(actual)]
    if not bloques:
        sys.exit("ERROR: el HTML actual no tiene bloques personalizados que copiar.")

    errores, avisos = [], []
    if CUSTOM.search(nuevo):
        errores.append("El HTML nuevo YA contiene bloques personalizados (¿no es un export limpio de JotForm?).")
    if form_id(actual) != form_id(nuevo):
        errores.append(f"El ID de formulario no coincide: repo={form_id(actual)} / nuevo={form_id(nuevo)}.")
    if ref_id(actual) != ref_id(nuevo):
        errores.append(f"El campo REFERENCIA ha cambiado de ID: repo={ref_id(actual)} / nuevo={ref_id(nuevo)}.")

    # Todos los input_XXX que usan los bloques, y si existen en el HTML nuevo
    usados = sorted(set(re.findall(r'"(input_\d+)"', "".join(bloques))))
    for i in usados:
        en_actual = f'id="{i}"' in actual
        en_nuevo = f'id="{i}"' in nuevo
        if en_actual and not en_nuevo:
            errores.append(f"El campo {i} lo usa el autorrelleno/bloqueo pero ya NO existe en el formulario nuevo.")
        elif not en_actual and not en_nuevo:
            avisos.append(f"{i} ya no existía antes tampoco (resto antiguo, sin efecto).")

    for a in avisos:
        print("AVISO:", a)
    if errores:
        print("\nNO se ha escrito nada. Revisa:")
        for e in errores:
            print("  -", e)
        sys.exit(2)

    nl = "\r\n" if "\r\n" in nuevo else "\n"
    pegado = "".join(b.replace("\r\n", "\n").replace("\n", nl) for b in bloques)
    i = nuevo.rfind("</body>")
    if i < 0:
        sys.exit("ERROR: el HTML nuevo no tiene </body>.")
    resultado = nuevo[:i] + pegado + nuevo[i:]
    open(actual_path, "w", encoding="utf-8", newline="").write(resultado)
    print(f"OK: {actual_path.name} reconstruido con {len(bloques)} bloque(s) personalizado(s). Campos comprobados: {len(usados)}.")


if __name__ == "__main__":
    main()
