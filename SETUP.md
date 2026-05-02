# Reporte Orvian Colombia — Guía de Despliegue en GitHub Pages

Con esta configuración el reporte vive en internet, se actualiza solo cada noche
y tú solo necesitas editar un archivo CSV desde cualquier dispositivo.

---

## Requisitos previos

- Cuenta en **GitHub** (ya la tienes)
- El archivo `pedidos.csv` actualizado con tus pedidos
- 15 minutos la primera vez

---

## PARTE 1 — Crear el repositorio en GitHub

### Paso 1: Crear un repositorio nuevo

1. Abre [github.com](https://github.com) e inicia sesión
2. Clic en el botón verde **"New"** (esquina superior izquierda)
3. Configura así:
   - **Repository name:** `orvian-reporte` (o el nombre que prefieras)
   - **Visibility:** `Private` ← importante, mantén los datos privados
   - **NO** marques ninguna opción de inicializar (sin README, sin .gitignore)
4. Clic **"Create repository"**

---

## PARTE 2 — Subir los archivos

### Opción A: Subir desde el navegador (más fácil, sin terminal)

1. En tu nuevo repositorio vacío, verás un enlace que dice **"uploading an existing file"** — haz clic ahí
2. Arrastra y suelta TODOS los archivos de esta carpeta `GitHub_Setup/` manteniendo la estructura:
   ```
   index.html
   requirements.txt
   data/
     pedidos.csv
     pedidos.json
   scripts/
     csv_to_json.py
   .github/
     workflows/
       nightly-update.yml
       manual-update.yml
   snapshots/        ← carpeta vacía (crea un archivo .gitkeep dentro)
   ```
   > **Truco:** Si GitHub no deja subir carpetas vacías, crea un archivo llamado
   > `.gitkeep` (sin contenido) dentro de `snapshots/` antes de subir.

3. En el campo de mensaje escribe: `inicial: reporte Orvian Colombia`
4. Clic **"Commit changes"**

### Opción B: Subir con Git (si tienes Git instalado)

```bash
cd ruta/a/GitHub_Setup
git init
git add .
git commit -m "inicial: reporte Orvian Colombia"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/orvian-reporte.git
git push -u origin main
```

---

## PARTE 3 — Activar GitHub Pages

1. En tu repositorio, ve a **Settings** (pestaña con engranaje)
2. En el menú izquierdo busca **"Pages"**
3. En **"Source"** selecciona:
   - Branch: `main`
   - Folder: `/ (root)`
4. Clic **"Save"**
5. Espera 1-2 minutos y aparecerá una URL como:
   ```
   https://TU_USUARIO.github.io/orvian-reporte/
   ```
   **Guarda esa URL** — es donde vivirá tu reporte.

> **Nota de seguridad:** GitHub Pages de repositorios privados requiere GitHub Pro
> o superior para ser privadas. Con cuenta gratuita, la URL será accesible por
> cualquiera que tenga el link. Si necesitas privacidad total, considera poner
> una contraseña en el HTML o usar un repositorio público con datos ofuscados.

---

## PARTE 4 — Verificar los workflows

1. Ve a la pestaña **"Actions"** en tu repositorio
2. Deberías ver los workflows:
   - **Actualización Nocturna (11 PM Colombia)** — corre automático cada noche
   - **Actualización Manual** — para lanzar cuando quieras
3. Si ves un aviso amarillo diciendo que los workflows están desactivados, haz clic en **"Enable workflows"**

### Probar que funciona ahora mismo

1. Ve a **Actions → Actualización Manual**
2. Clic **"Run workflow"** → **"Run workflow"** (botón verde)
3. Espera 30-60 segundos
4. Si el círculo se pone verde ✅: todo funciona
5. Si se pone rojo ❌: abre el workflow y revisa el log de error (escríbeme el error)

---

## PARTE 5 — Flujo de trabajo diario

### Cómo actualizar los pedidos

**Método 1 — Desde GitHub en el navegador (sin instalar nada):**

1. Ve a tu repositorio en github.com
2. Navega a `data/pedidos.csv`
3. Clic en el ícono de lápiz ✏️ (Edit this file)
4. Edita los datos directamente
5. Clic **"Commit changes"**
6. Ve a **Actions → Actualización Manual** y lanza el workflow
7. En 1 minuto el reporte ya está actualizado

**Método 2 — Subir un CSV desde Dropi:**

1. Exporta tus pedidos desde Dropi como CSV
2. Limpia/adapta las columnas para que coincidan con el formato de `pedidos.csv`
   (ver sección "Formato del CSV" más abajo)
3. Ve a `data/pedidos.csv` en GitHub → ✏️ → reemplaza el contenido → Commit
4. Lanza el workflow manual

### El reporte se actualiza solo cada noche

No necesitas hacer nada — el workflow nocturno corre a las **11 PM Colombia** y
convierte el CSV a JSON automáticamente. Al día siguiente abres el link y los
datos ya están frescos.

---

## Formato del CSV (pedidos.csv)

El archivo tiene estas columnas. Respeta exactamente los nombres:

| Columna | Tipo | Ejemplo | Notas |
|---|---|---|---|
| `id` | texto | OC-001 | Identificador único del pedido |
| `fecha` | fecha | 2026-05-01 | Formato YYYY-MM-DD |
| `cliente` | texto | Juan Pérez | |
| `ciudad` | texto | Bogotá | |
| `dpto` | texto | Cundinamarca | |
| `producto` | texto | Faja Reductora | |
| `valor` | número | 120000 | Precio de venta (COP) |
| `costo` | número | 60000 | Costo del producto (COP) |
| `ganancia` | número | 60000 | valor - costo |
| `recaudo` | número | 0 | Lo recaudado (0 si no ha pagado) |
| `carrier` | texto | Coordinadora | Transportadora |
| `guia` | texto | 1234567890 | Número de guía (vacío si no hay) |
| `fecha_guia` | fecha | 2026-05-02 | Cuando el proveedor despachó |
| `fecha_en_oficina` | fecha | | Cuando quedó en oficina de la transp. |
| `estado_carrier` | texto | EN_RUTA | Ver valores abajo |
| `intentos_entrega` | número | 0 | Cuántas veces intentaron entregar |
| `ult_mov` | texto | | Última novedad del carrier |
| `novedad` | texto | | Descripción de la novedad |
| `nov_activa` | booleano | false | true/false |
| `estado` | texto | EN_PROCESO | Ver valores abajo |
| `caso_status` | texto | | Estado del caso si aplica |
| `proceso_dev_completo` | booleano | false | true si devolución cerrada |
| `fecha_reembolso` | fecha | | Cuando se hizo reembolso |
| `monto_reembolsado` | número | 0 | |
| `alertas_hist` | lista | [] | No editar manualmente |
| `origen` | texto | Dropi | Plataforma de origen |

**Valores válidos para `estado_carrier`:**
- `EN_RUTA` — en camino normal
- `BODEGA` — detenido en bodega del carrier
- `INTENTO_FALLIDO` — intentaron entregar pero no pudieron
- `EN_OFICINA` — dejaron aviso, esperando en oficina
- `DEVUELTO` — ya devuelto al proveedor

**Valores válidos para `estado`:**
- `EN_PROCESO` — pedido activo
- `ENTREGADO` — entregado exitosamente
- `DEVOLUCION` — en proceso de devolución
- `CANCELADO` — cancelado

---

## Snapshots mensuales

El workflow nocturno guarda automáticamente un snapshot el **día 1 de cada mes**
en la carpeta `snapshots/` con el nombre `pedidos_YYYY-MM.json`.

Esto te da un historial mes a mes de todos tus pedidos.

---

## Preguntas frecuentes

**¿Cada cuánto se actualiza el reporte?**
Automáticamente cada noche a las 11 PM Colombia. También puedes lanzarlo manualmente
en cualquier momento desde la pestaña Actions.

**¿Qué pasa si no actualizo el CSV?**
El reporte seguirá mostrando los últimos datos que tenía. El workflow corre igual
pero no cambia nada si el CSV no cambió.

**¿Puedo tener el reporte en el celular?**
Sí. Abre el link de GitHub Pages desde el navegador del celular y guárdalo en
favoritos (o como acceso directo en el escritorio del celular).

**¿Los datos del localStorage (log de trazabilidad) se pierden al cambiar de dispositivo?**
Sí, el log de acciones vive en el navegador local. Si necesitas que el log sea
compartido entre dispositivos, avisame y lo extendemos para que también se guarde
en el JSON del repositorio.

**¿Cómo cambio la hora de actualización?**
En `.github/workflows/nightly-update.yml`, la línea:
```yaml
- cron: "0 4 * * *"
```
El formato es `minuto hora día mes díaDeLaSemana` en UTC.
Colombia es UTC-5, entonces: hora_colombia + 5 = hora_UTC.
- 11 PM Colombia = 4 AM UTC = `0 4 * * *`
- 8 PM Colombia = 1 AM UTC = `0 1 * * *`
- 6 AM Colombia = 11 AM UTC = `0 11 * * *`

---

## Soporte

Si algo falla, compárteme:
1. El error exacto que aparece en la pestaña Actions (clic en el workflow rojo → ver log)
2. Las primeras líneas del error en rojo

Con eso puedo ayudarte a corregirlo rápidamente.
