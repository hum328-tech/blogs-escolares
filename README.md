# Blogs escolares — prototipo inicial

## Incluye
- 15 diseños originales importables desde el ZIP, almacenados en Firestore (no publicados como HTML individuales).
- Login con nombre de usuario y contraseña (Firebase Email/Password con alias interno `@alumnos.blogs.invalid`).
- Directorio privado de blogs, editor visual, borradores, una publicación definitiva por semana ISO.
- Panel de profesor con acceso a blogs y borradores, importación de diseños.

## Configuración necesaria
1. Crea un proyecto Firebase y una app web. Activa **Authentication > Email/Password** y **Firestore**.
2. Pega la configuración pública de Firebase en `public/firebase-config.js`.
3. Publica las reglas de `firestore.rules` en Firestore antes de añadir alumnos.
4. Descarga una **cuenta de servicio** de Firebase para uso local; nunca la subas a GitHub. Instala `firebase-admin` en Python y define `GOOGLE_APPLICATION_CREDENTIALS` apuntando a ese archivo privado.
5. Prepara los 15 diseños: `python tools/prepare_import.py "submissions (2).zip"`. El JSON resultante queda en `private/` (ignorado por Git).
6. Crea usuarios: `python tools/create_users.py`. Entrega individualmente las credenciales de `private/credentials.csv`. El script no reestablece contraseñas de cuentas ya existentes.
7. Crea tu cuenta de profesor manualmente desde Firebase Authentication (correo real y contraseña); añade documento `users/{uid}` en Firestore con `name`, `role: "teacher"`, `active: true`. El profesor usa el **nombre anterior a @** si el correo es `nombre@alumnos.blogs.invalid`; para correos reales, adapta el login o crea la cuenta del profesor con alias interno también.
8. Abre el portal con una cuenta de profesor, entra en **Administración** e importa `private/import-data.json`.
9. Publica **solo el contenido de `public/`** en GitHub Pages. Si GitHub Pages está configurado para desplegar la raíz del repositorio, mueve `public/` a la raíz de una rama de publicación separada. Nunca publiques `private/` ni la cuenta de servicio.

## Limitaciones de esta primera versión
- El editor visual admite texto, formato, listas, enlaces e imágenes mediante URL HTTPS. Aún no sube archivos de imagen directamente.
- El diseño original se muestra en un iframe restringido sin scripts. Algunos elementos interactivos originales no funcionarán, por seguridad. Enlaces e imágenes relativos al archivo original pueden requerir ajustes.
- La semana usa el calendario ISO del dispositivo para el borrador; las reglas protegen la publicación final, pero **todavía no verifican la semana desde un reloj de servidor**. Antes de uso evaluativo formal, incorporar Cloud Functions para fijar semanas, fechas límite y desbloqueos desde el servidor.
- La lectura de diseños y publicaciones exige login. Sin embargo, el código de la app es público en GitHub Pages. No coloques datos privados en ese código.
- Los estilos originales se importan sin validación CSS profunda y se aíslan en iframe sandbox. Revisar contenido HTML/CSS antes de importarlo.
- No se ha probado contra un proyecto Firebase real; faltan credenciales/configuración y despliegue.
