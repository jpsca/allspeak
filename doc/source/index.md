title: API de internacionalización (i18n)
template: page.html
index: 1

<div class="header" markdown=1>

# API de internacionalización (i18n)

El módulo de i18n (abreviación de internacionalización) que viene con Shake (a partir de la versión 1.2) provee una plataforma fácil de usar para darle soporte multi-lenguaje a tu aplicación.

El proceso de “internacionalización” normalmente significa abstraer todos los textos y otros detalles locales (como fechas y formatos de moneda) fuera de tu aplicación para poder “localizarlos”.

En resumen, para internacionalizar tu aplicación tienes que:

* Extraer tus textos en archivos externos, separados por idioma.
* Decirle a Shake donde buscar estos textos.
* Indicar a tu aplicación que idioma usar al mostar una página.

Esta guía te muestra como trabajar con el API de i18n y contiene un tutorial para internacionalizar tu aplicación desde cero.

</div>


## 1. Como funciona la i18n en Shake

La internacionalización es un problema complejo. Los lenguajes naturales difieren de tantas formas (por ejemplo en sus reglas de como formar plurales) que es dificil crear una herramienta para solucionar todos los problemas de una vez.

Por eso el API de i18n de Shake se enfoca en dar soporte al Inglés y leguajes similares (como el Español) y ser personalizable para otros lenguajes.  Para la localizacion de nombres, números y fechas, se apoya en las excelentes bibliotecas _Babel_ y _pytz_.


### 1.1 Arquitectura general

La API de i18n tiene dos partes:

- traducir textos
- “localizar” valores (nombres, números, fechas, etc.)

Así que los métodos más importantes del API de i18n de Shake son:

```python
translate   # Encuentra la traducción de un texto
format      # Localiza un valor
```

En las plantillas están definidas como la variable global `t` y el filtro `format`, para que puedas usarlas de esta forma:

```jinja
{{ t('store.title') }}
{{ now|format }}
```

`'format'` intenta localizar el valor usando las opciones por defecto según el tipo de dato detectado. Sin embargo, puedes ser más específico y usar estos otros filtros:

```jinja
{{ val|datetimeformat }}
{{ val|dateformat }}
{{ val|timeformat }}
{{ val|timedeltaformat }}
{{ val|numberformat }}
{{ val|decimalformat }}
{{ val|currencyformat }}
{{ val|percentformat }}
{{ val|scientificformat }}
```

Todos ellos admiten parámetros opcionales para sobreescribir el formato y el locale específico a usar, que veremos más adelante.

Ahora, internacionalizemos una aplicación Shake desde cero!


## 2 Eligiendo el idioma y la zona horaria

En cada request, Shake busca el idioma a utilizar de las siguientes fuentes, en orden:

- Un atributo `locale` del objeto `request`.
- Un parámetro `locale` en la URL. Ej: `http://example.com/foo/?locale=es`.
- Las información que envía el navegador sobre los lenguajes soportados.
- El idioma de `DEFAULT_LOCALE`, en la configuración de tu aplicación.
- El idioma por defecto de Shake ('en').

El truco, entonces, para forzar un lenguaje específico, es definir el `locale` directamente en cada request.  Puedes hacer esto fácilmente registrando una función con el decorador `before_request`:

```python
@app.before_request
def set_locale(request, **kwargs):
    request.locale = app.settings.DEFAULT_LOCALE
```

De forma similar, la zona horaria - que se usa para dar formato a fechas - se busca en:

- Un atributo `tzinfo` del objeto `request`.
- Un parámetro `tzinfo` en la URL. Ej: `http://example.com/foo/?tzinfo=UTC`.
- El valor de `DEFAULT_TIMEZONE`, en la configuración de tu aplicación.
- La zona horaria por defecto ('UTC').

Si tu aplicación usa una sola zona horaria, basta definir `DEFAULT_TIMEZONE` en su configuración.  Si no, seimpre puede asignarse a `request.tzinfo` de la misma forma que el idioma, más arriba.

### 2.1 Idioma como parte de la URL



```python
urls = [
    Subdomain('<locale>', [
        Rule('/', index),
    ])
]

...

@app.before_request
def set_locale(request, **kwargs):
    request.locale = kwargs.pop('locale', app.settings.DEFAULT_LOCALE)
```

### 2.2 Idioma según las preferencias del usuario

```python
@app.before_request
def set_locale(request, **kwargs):
    if request.user:
        request.locale = request.user.locale or app.settings.DEFAULT_LOCALE
```


## 3. Añadiendo traducciones

Ahora que el idioma se elige corréctamente, el siguiente paso es mostrar los textos de la página traducidos a ese idioma.

Para esto, hay que reemplazar todas los textos de tus plantillas por constantes.  Por ejemplo, si tienes el texto:

```html
<p>Bienvenido al sitio</p>
```

podrías reemplazarlo por:

```jinja
<p>{{ t('welcome') }}</p>
```

y poner el el texto original, junto a los otros, en un archivo llamado `es.yml` que contenga, entre otras cosas:

```yaml
welcome: Bienvenido al sitio
```



### 3.1 Donde buscar las traducciones

Shake por defecto configurará tu aplicación para buscar los archivos con traducciones en la carpeta _`locales`_.  Si necesitas una configuración diferente puedes cambiarla fácilmente agregando un `LOCALES_DIR` a la configuración de tu aplicación.

Dentro de esta carpeta , Shake cargara automáticamente el archivo `*.yml` del idioma.

<div class=note markdown=1>
El `.yml` es por que el archivo está en format _YAML_. Este es un formato de texto perfecto para escribir cualquier cosa `llave: valor` de forma muy legible.  ¡Si quisieras, podrías trabajar con él sin haber visto nunca sus reglas! Pero [aquí están](http://wikipedia.org/wiki/YAML#Basic_components_of_YAML){target=_blank} de todos modos.
</div>

El `en.yml` por defecto contiene un ejemplo de texto traducido:

```yaml
hello: Hello world
```

Esto quiere decir que, cuando el idioma sea inglés (`en`), la llave _hello_ mostrará el texto _Hello World_.  Es decir, si tu plantillas es así:

```jinja
<p>{{ t('hello') }}</p>
```

el HTML generado será:

```html
<p>Hello world</p>
```

El idioma por defecto es inglés (en), así que si no eliges uno diferente, en ese archivo se buscarán las traducciones.

<div class=note markdown=1>
Si el idioma que elijes contiene una parte “regional”, como `en_US` o `es_PE`, el módulo de i18n intentará cargar un archivo con ese nombre primero (ej: `es_PE.yml`) y solo si no existe, buscará otro solo del lenguaje (`es.yml`).
</div>

### 3.2 Pasando variables a las traducciones



### 3.3 Plurales



### 3.5 Organización de los archivos en `locales`




## 4. Dando formato a fechas y números




## 5. Plantillas localizadas




## 6. Conclusión
