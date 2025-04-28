# 🚀 Optimización de Despliegue de Antenas en Santiago

Optimizar la infraestructura de telecomunicaciones es fundamental para garantizar una cobertura de calidad en entornos urbanos en expansión. En este proyecto desarrollamos un modelo que permite determinar dónde instalar nuevas antenas en Santiago de Chile, utilizando optimización evolutiva basada en calidad de servicio espacial.

---

🧐 **Descripción del problema**

En una región urbana dividida en cuadrantes, se busca mejorar la calidad de servicio de telecomunicaciones instalando nuevas antenas de manera óptima.

- Se dispone de un conjunto inicial de antenas en ubicaciones fijas.
- Se generan puntos aleatorios que representan clientes o áreas de evaluación.
- La calidad del servicio depende de la distancia a la antena más cercana.
- El objetivo es mejorar la calidad promedio agregando el menor número de antenas posibles.

---

🛠️ **Metodología**

En este repositorio encontrarás el desarrollo de:

- División de la Región Metropolitana en 36 cuadrantes.
- Simulación de 60 puntos de evaluación aleatorios.
- Instalación de 8 antenas iniciales de manera aleatoria.
- Cálculo de calidad basada en la distancia mínima a una antena.
- Interpolación espacial usando Radial Basis Functions (RBF).
- Algoritmo evolutivo simple que agrega antenas si mejoran el promedio de calidad.
- Visualización interactiva del mapa antes y después de la optimización.


---

🤖 **Detalles del modelo**

- **División geográfica:** Santiago se divide en 36 cuadrantes iguales.
- **Antenas:** 8 instaladas inicialmente de forma aleatoria.
- **Puntos de Evaluación:** 60 generados al azar.
- **Calidad de Servicio:** Funciona según \( \text{Calidad} = \max(0, 1 - \alpha \times \text{distancia}) \).
- **Interpolación:** Se aplica RBF para estimar calidad en todo el mapa.
- **Optimización:** Algoritmo evolutivo que agrega nuevas antenas sólo si aumentan la calidad promedio.

![01 - Segmentación de STGO](https://github.com/user-attachments/assets/8a9280b3-665c-4df8-83bd-f18f684b223e)

---

📊 **Resultados**

- Mejoría significativa en la calidad promedio global.
- Incorporación selectiva de nuevas antenas en zonas de baja cobertura.
- Visualización clara de la calidad de servicio antes y después.

**Archivo generado:**
- `mapa_completo.html` : Mapa interactivo de calidad de servicio (inicial y final) con diferenciación de antenas iniciales (azul) y nuevas (rojo).

## Calidad del servicio inicialmente
![02 - Calidad inicial](https://github.com/user-attachments/assets/0ab09ae8-f311-4468-9536-0f7515ada7c2)

## Calidad del servicio luego de optimizar la inslación de antenas
![03 - Calidad final](https://github.com/user-attachments/assets/4d773e83-3c71-461b-bb5a-eb60fd74ba08)

## Resultados
Con la adición estratégica de solo 9 antenas, se logra maximizar la calidad del servicio, evitando la necesidad de instalar antenas en todos los cuadrantes y siguiendo un proceso de optimización espacial eficiente.

![04 - tabla resumén](https://github.com/user-attachments/assets/03c27a71-2b03-4b31-9ce4-ad95188b2651)


---

🔖 **Archivos principales**

- `calcular_calidad`: Evalúa la calidad de cada punto de evaluación.
- `interpolar_rbf`: Crea una superficie de calidad continua.
- `evolucion`: Algoritmo de mejora evolutiva de infraestructura.
- `mapa_completo.html`: Visualización final de los resultados.

---

🚧 **Próximas etapas**

- Incluir un modelo de costo para ponderar el beneficio de agregar nuevas antenas.
- Optimizar no solo el promedio de calidad, sino también el percentil mínimo o la equidad del servicio.
- Usar datos reales de demanda o distribución de usuarios.
- Experimentar con distintas funciones de calidad: decay exponencial, penalizaciones por baja cobertura.
- 

 **NOTA**
Sé que en la práctica un proyecto en Telecomunicaciones involucra muchas más variables y desafíos técnicos. Esto es solo un ejemplo simplificado para ilustrar cómo podría empezar a abordarse el problema.

