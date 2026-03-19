# App de Portafolio para Fotógrafos (Cloud App)

## Autores
Rogelio Sosa Luna - 751476
David Vela -751183
Manuel Lopez - 753353

---

## Descripción

Desarrollamos una aplicación en la nube para facilitar a fotógrafos la entrega segura de su trabajo. La plataforma permite organizar sesiones por cliente, compartir galerías privadas y gestionar la selección y compra de imágenes.

Con esto buscamos resolver problemas de seguridad y logística, evitando el uso de medios informales y reduciendo el riesgo de uso no autorizado de las fotografías.

---

## Tecnologías

- AWS EC2: Hosting de la aplicación
- AWS S3: Almacenamiento de imágenes
- AWS RDS: Base de datos relacional
- AWS Lambda: Procesamiento de imágenes (marca de agua)
- AWS SQS: Manejo de tareas asíncronas
- AWS Cognito: Autenticación de usuarios

---

## Arquitectura

- EC2 ejecuta la aplicación, expone endpoints y gestiona la lógica del sistema.
- S3 almacena imágenes originales y procesadas.
- RDS guarda usuarios, portafolios y registros de compra.
- SQS gestiona solicitudes de procesamiento.
- Lambda genera imágenes con marca de agua.

---

## Flujo

1. El fotógrafo crea un cliente y sube imágenes.
2. Las imágenes se almacenan en S3.
3. Se envía una tarea a SQS.
4. Lambda procesa las imágenes.
5. El cliente accede a su galería.
6. Selecciona y compra imágenes.
7. Descarga versiones sin marca de agua.

---

## Funcionalidades

Fotógrafos:
- Gestión de clientes
- Carga de sesiones
- Administración de portafolios

Clientes:
- Acceso a galerías privadas
- Selección de imágenes
- Compra y descarga

---
