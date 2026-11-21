# Personalizaciones de los formularios (GitHub vs JotForm)

Este documento recoge **todo lo que tienen los HTML de este repo que NO viene de JotForm**.
Sirve para que, cuando cambies un formulario en JotForm y lo vuelvas a exportar, se pueda
rehacer la versión de GitHub sin perder nada.

## 1. Qué se añade a mano (no es configurable en JotForm)

JotForm no permite meter código propio en sus formularios, así que todo esto vive **solo** en GitHub.
En los 32 formularios son bloques `<script>` pegados **al final del HTML, después del formulario**.
El contenido del formulario (campos, textos, diseño, lógica condicional) **no se ha tocado**: eso sigue
saliendo tal cual de JotForm.

| Bloque | Qué hace | Dónde está |
|---|---|---|
| **Autorrelleno Airtable** | Al escribir la REFERENCIA, busca en Airtable (base DH, tabla CARTERA INMUEBLES) y rellena los campos del formulario según una tabla «columna de Airtable → campo de JotForm» (sección 4). En la mayoría también bloquea el botón y los campos hasta confirmar la referencia y muestra ✅/❌. | Bloque con `AIRTABLE_TOKEN` |
| **DH EXTRA** (solo algunos formularios) | Lógica propia de un formulario concreto (DATOS_RESERVA y PAGO_RESERVA). En DATOS_RESERVA: no deja pulsar «IR A PAGO RESERVA» si falta algún campo obligatorio visible (excepto la firma, que se hace después en JotForm Sign) y lista lo que falta; y ajusta la altura de los textos 1)–5) para que se lean enteros sin scroll. | Bloque que empieza por `/* DH EXTRA` |
| **GUARDA REFERENCIA** | Quita todos los espacios y pone MAYÚSCULAS en la REFERENCIA mientras se escribe. Si no coincide **exactamente** con Airtable: vacía los datos rellenados, bloquea el envío y muestra ❌. Repite la comprobación al pulsar enviar. | Último bloque, empieza por `/* GUARDA REFERENCIA (DH)` |

Lo que **sí** puedes hacer en JotForm sin perder nada en GitHub: cambiar textos, diseño, añadir o quitar campos
que **no** estén en la tabla de autorrelleno, cambiar condiciones, notificaciones, etc.

Lo que **rompe** la versión de GitHub si lo haces en JotForm: borrar o volver a crear un campo que aparece en
la sección 4 (su `input_XXX` cambia), borrar o recrear el campo REFERENCIA, o duplicar el formulario
(cambia el ID del formulario).

## 2. Cómo actualizar un formulario después de cambiarlo en JotForm

1. En JotForm: **Publicar → Plataformas → Código fuente → descargar HTML**.
2. Pásame ese HTML y dime de qué formulario es (y si quieres, qué has cambiado).
3. Yo ejecuto `herramientas/reconstruir.py`, que:
   - copia los bloques personalizados del HTML actual del repo al HTML nuevo;
   - comprueba que el ID del formulario y el campo REFERENCIA son los mismos;
   - comprueba que **todos** los campos que usa el autorrelleno siguen existiendo;
   - si algo no cuadra, **no escribe nada** y dice exactamente qué campo falta.
4. Si has añadido un campo nuevo que quieres que se rellene desde Airtable, dime qué columna
   de Airtable va en qué campo y lo añado a su tabla.

```
python3 herramientas/reconstruir.py RUTA_DEL_HTML_NUEVO.html NOMBRE_FORMULARIO
```

**Diseño (CSS):** el diseño visual va en el CSS personalizado de JotForm (Diseñador → Estilos → Inyectar CSS), así viene ya dentro del export.
La copia de cada CSS está en `herramientas/css/`. Si un export llega SIN el bloque «DH DISEÑO…» que tenía la versión del repo,
`reconstruir.py` se para y avisa (para no perder el diseño por accidente).

**Formulario totalmente nuevo:** dime qué campo es la REFERENCIA, si debe bloquear el envío cuando no
existe en Airtable, y qué columnas de Airtable van en qué campos.

## 3. Resumen por formulario y excepciones

Lo estándar en todos: botón de envío `input_81`, la REFERENCIA se limpia y, si no existe en Airtable, se bloquea el envío.
La columna «Excepciones» indica lo que se sale de eso.

| Formulario | ID JotForm | Campo REFERENCIA | Campos que rellena | Excepciones |
|---|---|---|---|---|
| AGENCIA_AL_INQUILINO | 260466908725365 | `input_414` | 10 | — |
| AGENCIA_AL_PROPIETARIO | 260747140199360 | `input_416` | 8 | — |
| ALBARAN_FINALIZACION_ALQUILER | 261296771911362 | `input_486` | 8 | — |
| ALTA_PROPIEDAD | 253353585653363 | `input_135` | 0 | NO bloquea el envío (solo limpia la referencia) |
| AUTORIZACION_COMERCIALIZACION | 263225564982061 | `input_2` | 14 | botón de JotForm Sign; el autorrelleno localiza los campos por ETIQUETA (no por input_XXX); oculta Propietario 2/3 si no existen; lee `?ref=` del enlace; diseño y orden en el CSS personalizado de JotForm (bloque «DH DISEÑO») |
| VERIFICACION_PERFIL_SOLVENCIA | 262793349901062 | `input_3` | 0 | lo rellena Juan; autorrelleno por número de pregunta (Q en el script) desde DOCUMENTACION INQUILINOS (tblDEOgGd0gJ1sFGb, alimentada por el escenario Make «12.JF-AT. DOCUMENTACIÓN CONTRATO…») + DIRECCIÓN de CARTERA; pone Nº de inquilinos y dispara las condiciones; lee `?ref=` |
| CALCULAR_DEVOLUCION_FIANZA | 261166944755366 | `input_440` | 9 | — |
| CAMBIO_SUMINISTROS | 261265033882356 | `input_317` | 3 | CUPS rellenados con retardo según el desplegable input_316 |
| CHECK-IN | 253224147452351 | `input_351` | 18 | — |
| CHECK-OUT | 253274824796369 | `input_414` | 11 | — |
| COMUNICAR_INCIDENCIA | 253325706428357 | `input_420` | 8 | — |
| CONFIRMAR_FECHA_ENTRADA | 261462969334365 | `input_351` | 8 | — |
| CONFIRMAR_FECHA_SALIDA | 260404957152355 | `input_378` | 3 | botón de envío input_408; fechas de Airtable convertidas a DD/MM/AAAA |
| CONTACTO_PROPIEDAD | 253393126842358 | `input_306` | 1 | — |
| DATOS_CONTRATO | 252986821301357 | `input_357` | 31 | — |
| DATOS_RESERVA | 252701841871356 | `input_298` | 13 | botón de JotForm Sign; bloque DH EXTRA (campos obligatorios completos + altura de los textos 1–5); diseño en el CSS personalizado de JotForm (bloque «DH DISEÑO RESERVA», copia en `herramientas/css/DATOS_RESERVA.css`) |
| DATOS_SUMINISTROS | 260874819333364 | `input_317` | 1 | — |
| DEVOLUCION_DE_FIANZA | 261116538998369 | `input_455` | 10 | fechas de Airtable convertidas a DD/MM/AAAA |
| DOCUMENTACION_CONTRATO | 253184377345362 | `input_345` | 1 | — |
| ENVIAR_INCIDENCIA | 253332405677357 | `input_411` | 8 | — |
| ENVIO_SUMINISTROS | 253313682276358 | `input_407` | 9 | — |
| FINALIZAR_INCIDENCIA | 253337261889367 | `input_410` | 9 | — |
| INFORMAR_INQUILINO | 253396425090358 | `input_417` | 10 | — |
| INFORMAR_PROPIETARIO | 260036857117356 | `input_416` | 8 | — |
| INQUILINO_A_LA_AGENCIA | 260466528141355 | `input_416` | 8 | — |
| LIQUIDACION | 253404784219359 | `input_368` | 8 | — |
| MODIFICAR_DATOS | 260076834888370 | `input_135` | 0 | NO bloquea el envío (solo limpia la referencia) |
| PAGO_RESERVA | 253172214183349 | `input_296` | 18 | bloque DH EXTRA (no deja enviar si faltan campos obligatorios visibles; el adjunto lo valida JotForm); bloque DH EXTRA CONFIANZA (pasos, ficha del piso con FOTO ANUNCIO y URL ANUNCIO de Airtable, a quién pagas, botones Copiar, aviso antiestafa, qué pasa después, contacto y pie; textos editables en el objeto `TXT` al principio del bloque); diseño en el CSS personalizado de JotForm (bloque «DH DISEÑO PAGO RESERVA», copia en `herramientas/css/PAGO_RESERVA.css`) |
| RESCISION | 253421851530349 | `input_408` | 14 | botón de JotForm Sign |
| RESOLVEMOS_TUS_DUDAS | 261755783472367 | `input_416` | 2 | — |
| RESOLVER_INCIDENCIA | 253336812383357 | `input_405` | 8 | — |
| RESUELVE_TUS_DUDAS | 261755390907364 | `input_416` | 2 | — |
| REVISION_Y_LIMPIEZA | 253404965104353 | `input_399` | 8 | — |
| SOLICITUD_SUMINISTROS | 253294271940358 | `input_387` | 8 | — |

## 4. Problemas encontrados en la revisión (no afectan al envío)

- **ALTA_PROPIEDAD**: contiene un bloque de autorrelleno copiado de otra plantilla que apunta a `input_378` (no existe aquí). No hace nada; se puede borrar.
- **CONFIRMAR_FECHA_SALIDA**: la columna «Fecha prevista de salida» apunta a `input_377`, que no existe en el formulario (ese dato no se rellena).
- **CONTACTO_PROPIEDAD**: contiene un bloque de autorrelleno copiado de otra plantilla que apunta a `input_378` (no existe aquí). No hace nada; se puede borrar.
- **DATOS_SUMINISTROS**: contiene un bloque de autorrelleno copiado de otra plantilla que apunta a `input_378` (no existe aquí). No hace nada; se puede borrar.
- **DEVOLUCION_DE_FIANZA**: contiene un bloque de autorrelleno copiado de otra plantilla que apunta a `input_378` (no existe aquí). No hace nada; se puede borrar.
- **MODIFICAR_DATOS**: contiene un bloque de autorrelleno copiado de otra plantilla que apunta a `input_378` (no existe aquí). No hace nada; se puede borrar.

## 5. Tabla de autorrelleno de cada formulario

### AGENCIA_AL_INQUILINO

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |
| EMAIL INQUILINO | `input_410` | EMAIL INQUILINO |
| EMAIL INQUILINO ANTERIOR | `input_416` | EMAIL INQUILINO ANTERIOR |

### AGENCIA_AL_PROPIETARIO

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### ALBARAN_FINALIZACION_ALQUILER

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_437` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### ALTA_PROPIEDAD

No rellena datos desde Airtable.

### AUTORIZACION_COMERCIALIZACION

El autorrelleno busca cada campo por su etiqueta, así que no se rompe si cambian los `input_XXX`; solo hay que mantener las etiquetas.
El orden de los campos, los textos y el diseño están en JotForm (CSS personalizado, bloque «DH DISEÑO»). Enlace para el email: `AUTORIZACION_COMERCIALIZACION.html?ref=REFERENCIA`.

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_23` | DIRECCIÓN |
| NOMBRE P1 | `input_26` | NOMBRE P1 |
| DNI P1 | `input_27` | DNI P1 |
| EMAIL P1 | `input_29` | EMAIL P1 |
| NOMBRE P2 | `input_32` | NOMBRE P2 |
| DNI P2 | `input_33` | DNI P2 |
| EMAIL P2 | `input_35` | EMAIL P2 |
| NOMBRE P3 | `input_38` | NOMBRE P3 |
| DNI P3 | `input_39` | DNI P3 |
| EMAIL P3 | `input_41` | EMAIL P3 |
| TITULAR PROPIEDAD | `input_16` | TITULAR PROPIEDAD |
| BANCO | `input_17` | BANCO |
| IBAN | `input_18` | IBAN |
| SWIFT/BIC | `input_19` | SWIFT/BIC |

### VERIFICACION_PERFIL_SOLVENCIA
Al escribir la REFERENCIA (o con `?ref=`):
| Campo | Origen |
|---|---|
| DIRECCIÓN (`input_4`) | CARTERA INMUEBLES · DIRECCIÓN |
| Nº de inquilinos (`input_32`) | nº de inquilinos distintos en DOCUMENTACION INQUILINOS (máx. 4) |
| Inquilino N – Nombre / Motivo del alquiler / Centro / Empresa / Especificar / Documento aportado / Solvencia / Avalista nombre y relación | DOCUMENTACION INQUILINOS: filas con esa REFERENCIA, enviadas en los últimos 60 días (variable DIAS del script) y sin «USADO EN INFORME», orden FECHA ENVÍO; si un inquilino envió varias veces, su último envío |
Si no hay documentación recibida solo carga la dirección y lo avisa. Todo queda editable.

### CALCULAR_DEVOLUCION_FIANZA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_437` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |
| EMAIL INQUILINO ANTERIOR | `input_436` | EMAIL INQUILINO ANTERIOR |

### CAMBIO_SUMINISTROS

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_300` | DIRECCIÓN |
| Nº CUPS LUZ | `input_321` | Nº CUPS LUZ |
| Nº CUPS GAS | `input_322` | Nº CUPS GAS |

### CHECK-IN

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_331` | EMAIL P1 |
| NAME P1 | `input_335` | NAME P1 |
| EMAIL P2 | `input_332` | EMAIL P2 |
| NAME P2 | `input_336` | NAME P2 |
| EMAIL P3 | `input_333` | EMAIL P3 |
| NAME P3 | `input_337` | NAME P3 |
| COMPAÑIA SUMINISTRADORA LUZ | `input_334` | COMPAÑIA SUMINISTRADORA LUZ |
| COMPAÑIA SUMINISTRADORA GAS | `input_362` | COMPAÑIA SUMINISTRADORA GAS |
| Nº CUPS LUZ | `input_358` | Nº CUPS LUZ |
| Nº CUPS GAS | `input_363` | Nº CUPS GAS |
| NOMBRE TITULAR LUZ | `input_359` | NOMBRE TITULAR LUZ |
| NOMBRE TITULAR GAS | `input_364` | NOMBRE TITULAR GAS |
| DNI TITULAR LUZ | `input_360` | DNI TITULAR LUZ |
| DNI TITULAR GAS | `input_365` | DNI TITULAR GAS |
| FACTURA LUZ | `input_371` | FACTURA LUZ |
| FACTURA GAS | `input_372` | FACTURA GAS |
| NOMBRE AGENTE | `input_361` | NOMBRE AGENTE |

### CHECK-OUT

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| Nº CUPS LUZ | `input_403` | Nº CUPS LUZ |
| Nº CUPS GAS | `input_404` | Nº CUPS GAS |
| EMAIL INQUILINO | `input_402` | EMAIL INQUILINO |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### COMUNICAR_INCIDENCIA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### CONFIRMAR_FECHA_ENTRADA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_331` | EMAIL P1 |
| NAME P1 | `input_335` | NAME P1 |
| EMAIL P2 | `input_332` | EMAIL P2 |
| NAME P2 | `input_336` | NAME P2 |
| EMAIL P3 | `input_333` | EMAIL P3 |
| NAME P3 | `input_337` | NAME P3 |
| NOMBRE AGENTE | `input_361` | NOMBRE AGENTE |

### CONFIRMAR_FECHA_SALIDA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| Fecha prevista de salida | `input_377` | ⚠️ NO EXISTE |
| DIRECCIÓN | `input_135` | DIRECCIÓN |

### CONTACTO_PROPIEDAD

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_300` | DIRECCIÓN |

### DATOS_CONTRATO

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| REF. CATASTRAL | `input_258` | REF. CATASTRAL |
| NOMBRE P1 | `input_136` | NOMBRE P1 |
| DNI P1 | `input_137` | DNI P1 |
| DIRECCIÓN P1 | `input_332` | DIRECCIÓN P1 |
| TELÉFONO P1 | `input_299` | TELÉFONO P1 |
| EMAIL P1 | `input_300` | EMAIL P1 |
| NOMBRE P2 | `input_293` | NOMBRE P2 |
| DNI P2 | `input_296` | DNI P2 |
| DIRECCIÓN P2 | `input_333` | DIRECCIÓN P2 |
| TELÉFONO P2 | `input_301` | TELÉFONO P2 |
| EMAIL P2 | `input_302` | EMAIL P2 |
| NOMBRE P3 | `input_295` | NOMBRE P3 |
| DNI P3 | `input_294` | DNI P3 |
| DIRECCIÓN P3 | `input_334` | DIRECCIÓN P3 |
| TELÉFONO P3 | `input_303` | TELÉFONO P3 |
| EMAIL P3 | `input_304` | EMAIL P3 |
| IBAN | `input_138` | IBAN |
| TITULAR PROPIEDAD | `input_356` | TITULAR PROPIEDAD |
| BANCO | `input_139` | BANCO |
| SWIFT/BIC | `input_298` | SWIFT/BIC |
| Nº CUPS LUZ | `input_350` | Nº CUPS LUZ |
| Nº CUPS GAS | `input_353` | Nº CUPS GAS |
| COMPAÑIA SUMINISTRADORA LUZ | `input_361` | COMPAÑIA SUMINISTRADORA LUZ |
| COMPAÑIA SUMINISTRADORA GAS | `input_362` | COMPAÑIA SUMINISTRADORA GAS |
| NOMBRE TITULAR LUZ | `input_351` | NOMBRE TITULAR LUZ |
| NOMBRE TITULAR GAS | `input_354` | NOMBRE TITULAR GAS |
| DNI TITULAR LUZ | `input_352` | DNI TITULAR LUZ |
| DNI TITULAR GAS | `input_355` | DNI TITULAR GAS |
| ALQUILER | `input_140` | ALQUILER |
| ALQUILER LETRA | `input_297` | ALQUILER LETRA |

### DATOS_RESERVA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| ALQUILER | `input_140` | ALQUILER |
| REF. CATASTRAL | `input_258` | REF. CATASTRAL |
| TITULAR PROPIEDAD | `input_302` | TITULAR PROPIEDAD |
| NOMBRE P1 | `input_136` | NOMBRE P1 |
| DNI P1 | `input_137` | DNI P1 |
| EMAIL P1 | `input_295` | EMAIL P1 |
| EMAIL P2 | `input_296` | EMAIL P2 |
| EMAIL P3 | `input_297` | EMAIL P3 |
| AGENTE | `input_210` | AGENTE |
| BANCO | `input_139` | BANCO |
| IBAN | `input_138` | IBAN |
| SWIFT/BIC | `input_259` | SWIFT/BIC |

### DATOS_SUMINISTROS

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_300` | DIRECCIÓN |

### DEVOLUCION_DE_FIANZA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_415` | DIRECCIÓN |
| EMAIL P1 | `input_416` | EMAIL P1 |
| EMAIL P2 | `input_417` | EMAIL P2 |
| EMAIL P3 | `input_418` | EMAIL P3 |
| NAME P1 | `input_419` | NAME P1 |
| NAME P2 | `input_420` | NAME P2 |
| NAME P3 | `input_421` | NAME P3 |
| NOMBRE AGENTE | `input_422` | NOMBRE AGENTE |
| EMAIL INQUILINO | `input_423` | EMAIL INQUILINO |
| Fecha CHECK OUT | `input_453` | Fecha CHECK OUT |

### DOCUMENTACION_CONTRATO

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |

### ENVIAR_INCIDENCIA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### ENVIO_SUMINISTROS

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL INQUILINO | `input_380` | EMAIL INQUILINO |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### FINALIZAR_INCIDENCIA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| EMAIL INQUILINO | `input_407` | EMAIL INQUILINO |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### INFORMAR_INQUILINO

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |
| EMAIL INQUILINO | `input_410` | EMAIL INQUILINO |
| EMAIL INQUILINO ANTERIOR | `input_418` | EMAIL INQUILINO ANTERIOR |

### INFORMAR_PROPIETARIO

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### INQUILINO_A_LA_AGENCIA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### LIQUIDACION

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### MODIFICAR_DATOS

No rellena datos desde Airtable.

### PAGO_RESERVA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| ALQUILER | `input_285` | ALQUILER |
| NOMBRE P1 | `input_136` | NOMBRE P1 |
| TITULAR PROPIEDAD | `input_308` | TITULAR PROPIEDAD |
| IBAN | `input_138` | IBAN |
| SWIFT/BIC | `input_262` | SWIFT/BIC |
| BANCO | `input_139` | BANCO |
| AGENTE | `input_289` | AGENTE |
| IBAN AGENCIA | `input_290` | IBAN AGENCIA |
| SWIFT/BIC AGENCIA | `input_291` | SWIFT/BIC AGENCIA |
| BANCO AGENCIA | `input_292` | BANCO AGENCIA |
| EMAIL P1 | `input_278` | EMAIL P1 |
| NAME P1 | `input_279` | NAME P1 |
| EMAIL P2 | `input_280` | EMAIL P2 |
| NAME P2 | `input_281` | NAME P2 |
| EMAIL P3 | `input_282` | EMAIL P3 |
| NAME P3 | `input_283` | NAME P3 |
| NOMBRE AGENTE | `input_284` | NOMBRE AGENTE |

### RESCISION

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE P1 | `input_379` | NOMBRE P1 |
| DNI P1 | `input_380` | DNI P1 |
| NOMBRE P2 | `input_387` | NOMBRE P2 |
| DNI P2 | `input_389` | DNI P2 |
| NOMBRE P3 | `input_390` | NOMBRE P3 |
| DNI P3 | `input_392` | DNI P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### RESOLVEMOS_TUS_DUDAS

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL HASTA CHECK IN | `input_360` | EMAIL HASTA CHECK IN |

### RESOLVER_INCIDENCIA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### RESUELVE_TUS_DUDAS

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL HASTA CHECK IN | `input_360` | EMAIL HASTA CHECK IN |

### REVISION_Y_LIMPIEZA

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

### SOLICITUD_SUMINISTROS

| Columna de Airtable | Campo JotForm | Etiqueta en JotForm |
|---|---|---|
| DIRECCIÓN | `input_135` | DIRECCIÓN |
| EMAIL P1 | `input_354` | EMAIL P1 |
| NAME P1 | `input_355` | NAME P1 |
| EMAIL P2 | `input_356` | EMAIL P2 |
| NAME P2 | `input_357` | NAME P2 |
| EMAIL P3 | `input_358` | EMAIL P3 |
| NAME P3 | `input_359` | NAME P3 |
| NOMBRE AGENTE | `input_360` | NOMBRE AGENTE |

## 6. INFORME_SOLVENCIA.html (informe para el propietario)

No es un formulario de JotForm: es la página que ve el propietario con el informe de solvencia.

- Flujo: la agencia envía el formulario **VERIFICACIÓN PERFIL DE SOLVENCIA** (JotForm 262793349901062) →
  webhook de Make → escenario **20.- Enviar informe de solvencia** (carpeta CONTRATOS): busca los emails
  P1/P2/P3 en CARTERA INMUEBLES por la REFERENCIA, guarda el envío en el Data Store **INFORMES SOLVENCIA**
  con un código aleatorio y envía el email (desde reservas@) con el enlace `INFORME_SOLVENCIA.html?id=CÓDIGO`.
- La página pide los datos al escenario **21.- Mostrar informe de solvencia** (webhook en `WEBHOOK_INFORME`),
  que devuelve solo el registro de ese código. La página no lleva claves de JotForm ni de Airtable.
- Lee las respuestas por número de pregunta (`q17_`, `q34_`…): si se cambian textos en JotForm no pasa nada;
  si se borra y se recrea una pregunta, cambia su número y hay que actualizar la tabla `Q` del script.
- `INFORME_SOLVENCIA.html?ejemplo` muestra el diseño con datos de muestra.


### DATOS_RESERVA — DH EXTRA CONFIANZA
Igual que en PAGO_RESERVA: barra de pasos (paso 1 activo), ficha del piso debajo de la REFERENCIA (foto y anuncio desde Airtable: FOTO ANUNCIO / URL ANUNCIO; dirección input_135, entrada lite_mode_260, salida lite_mode_261, alquiler input_140), caja del agente (input_210) con WhatsApp/llamar, universidades y Telemadrid, y pie. Estilos en la sección «Bloque de confianza» de herramientas/css/DATOS_RESERVA.css.
