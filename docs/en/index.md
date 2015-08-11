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
