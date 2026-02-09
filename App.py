import streamlit as st
import anthropic
import time
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Productos Digitales",
    page_icon="🎯",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Analizador de Productos Digitales</h1>
    <p>Genera informes profesionales de mercado en minutos</p>
</div>
""", unsafe_allow_html=True)

# Obtener API Key desde secrets
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    st.error("⚠️ No se encontró la API Key en los secrets. Configúrala en Settings > Secrets")
    st.stop()

# Función para investigar mercado
def investigar_mercado(datos_formulario, api_key):
    """Investiga el mercado usando Claude con web search"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Construir el contexto del prompt con los datos del formulario
        contexto = f"""
TIPO: {datos_formulario['tipo']}
CATEGORÍA: {datos_formulario['categoria']}
PROBLEMA QUE RESUELVE: {datos_formulario['problema']}
PÚBLICO OBJETIVO: {datos_formulario['publico']}
PAÍS: {datos_formulario['pais']}
"""
        
        # Agregar datos opcionales si existen
        if datos_formulario.get('dedicacion'):
            contexto += f"DEDICACIÓN ACTUAL: {datos_formulario['dedicacion']}\n"
        if datos_formulario.get('titulo'):
            contexto += f"ESPECIALIDAD/TÍTULO: {datos_formulario['titulo']}\n"
        if datos_formulario.get('talento'):
            contexto += f"TALENTO/FORTALEZA: {datos_formulario['talento']}\n"
        
        prompt = f"""Necesito que investigues el mercado para esta idea de producto/servicio digital:

{contexto}

Investiga en la web y proporciona información CONCRETA sobre:
1. 3-5 productos/servicios similares que existen (nombres, precios, características)
2. Demanda del mercado (volumen de búsquedas, tendencias)
3. Competidores principales
4. Rangos de precios específicos
5. Gaps en el mercado (oportunidades)

Usa búsqueda web para datos reales. Sé específico con números y nombres."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search"
            }],
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extraer contenido
        contenido = ""
        for bloque in response.content:
            if bloque.type == "text":
                contenido += bloque.text + "\n"
        
        return contenido, None
        
    except Exception as e:
        return None, str(e)

# Función para generar informe
def generar_informe(datos_formulario, datos_investigacion, api_key):
    """Genera el informe formateado"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Construir contexto del formulario
        contexto = f"""
TIPO: {datos_formulario['tipo']}
CATEGORÍA: {datos_formulario['categoria']}
PROBLEMA QUE RESUELVE: {datos_formulario['problema']}
PÚBLICO OBJETIVO: {datos_formulario['publico']}
PAÍS: {datos_formulario['pais']}
"""
        
        if datos_formulario.get('dedicacion'):
            contexto += f"DEDICACIÓN ACTUAL: {datos_formulario['dedicacion']}\n"
        if datos_formulario.get('titulo'):
            contexto += f"ESPECIALIDAD/TÍTULO: {datos_formulario['titulo']}\n"
        if datos_formulario.get('talento'):
            contexto += f"TALENTO/FORTALEZA: {datos_formulario['talento']}\n"
        
        prompt = f"""Basándote en esta investigación de mercado, genera un informe profesional siguiendo EXACTAMENTE este formato:

DATOS DEL PRODUCTO/SERVICIO:
{contexto}

INVESTIGACIÓN REALIZADA:
{datos_investigacion}

---

Genera el informe siguiendo EXACTAMENTE esta estructura:

═══════════════════════════════════════════════════════════════
                    🎯 TU PRODUCTO DIGITAL
═══════════════════════════════════════════════════════════════


📦 PRODUCTO
───────────────────────────────────────────────────────────────

[Nombre del producto pegadizo y descriptivo]

Formato: [Tipo de producto digital]


💰 PRECIO
───────────────────────────────────────────────────────────────

$[Precio sugerido en pesos argentinos]

Rango de mercado: [Basado en la investigación real]


👥 QUIÉN LO COMPRA
───────────────────────────────────────────────────────────────

[Descripción específica del cliente ideal]

Su problema: [El dolor real que tienen]
Su deseo: [Lo que realmente quieren lograr]
Por qué compra: [La razón emocional de compra]


🎣 TU GANCHO DE VENTA
───────────────────────────────────────────────────────────────

"[Propuesta única de valor - una frase poderosa]"

Versión corta: "[Slogan pegadizo]"


📋 QUÉ INCLUYE
───────────────────────────────────────────────────────────────

PRODUCTO PRINCIPAL:
✓ [Componente principal con descripción]

BONUS INCLUIDOS:
✓ [Bonus 1]
✓ [Bonus 2]
✓ [Bonus 3]
✓ [Bonus 4]
✓ [Bonus 5]

───────────────────────────────────────────────────────────────
Valor total percibido: $[Precio alto]    →    Precio: $[Precio real]
───────────────────────────────────────────────────────────────


✅ POR QUÉ SE VA A VENDER
───────────────────────────────────────────────────────────────

[Datos concretos del mercado, estadísticas, números de búsquedas]

- [Punto 1 con datos específicos]
- [Punto 2 con datos específicos]
- [Punto 3 - ventaja competitiva única]


🌊 NICHO AZUL
───────────────────────────────────────────────────────────────

[Explicación de por qué este es un océano azul - combinación única que no existe]


🧠 POR QUÉ ESTE PRODUCTO PARA VOS
───────────────────────────────────────────────────────────────

[Conexión personal con la idea, considerando tu experiencia, título o talento mencionado]


⚡ TU PLAN DE ACCIÓN (72 HORAS)
═══════════════════════════════════════════════════════════════

DÍA 1 - [TÍTULO DE LA FASE]
─────────────────────────────────
□ [Tarea específica 1]
□ [Tarea específica 2]

DÍA 2 - [TÍTULO DE LA FASE]
─────────────────────────────────
□ [Tarea específica 1]
□ [Tarea específica 2]

DÍA 3 - [TÍTULO DE LA FASE]
─────────────────────────────────
□ [Tarea específica 1]
□ [Tarea específica 2]

═══════════════════════════════════════════════════════════════


🚀 TU PRIMER PASO (AHORA MISMO)
═══════════════════════════════════════════════════════════════

[Acción concreta y específica que puede hacer en 30 minutos]

═══════════════════════════════════════════════════════════════

Usa datos REALES de la investigación. Sé específico con precios y números."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extraer informe
        informe = ""
        for bloque in response.content:
            if bloque.type == "text":
                informe += bloque.text
        
        return informe, None
        
    except Exception as e:
        return None, str(e)

# Interfaz principal - Formulario mejorado con 8 preguntas
with st.form("analisis_form"):
    st.subheader("💡 Cuéntame sobre tu producto/servicio")
    
    st.markdown("**Campos obligatorios (5)** marcados con *")
    
    # PREGUNTA 1: Servicio o Producto (OBLIGATORIA)
    tipo = st.radio(
        "1. ¿Es un servicio o un producto? *",
        options=["Producto", "Servicio"],
        horizontal=True
    )
    
    # PREGUNTA 2: Tipo/Categoría (OBLIGATORIA)
    st.markdown("**2. ¿Qué tipo específicamente? ***")
    col1, col2 = st.columns(2)
    
    with col1:
        if tipo == "Producto":
            categoria_opciones = [
                "Ebook / Libro digital",
                "Curso online",
                "Plantillas / Templates",
                "Software / App",
                "Membresía / Suscripción",
                "Paquete de recursos",
                "Otro"
            ]
        else:
            categoria_opciones = [
                "Consultoría",
                "Coaching / Mentoría",
                "Servicios de diseño",
                "Servicios de marketing",
                "Servicios de desarrollo",
                "Servicios de redacción",
                "Otro"
            ]
        
        categoria = st.selectbox(
            "Selecciona la categoría:",
            options=categoria_opciones
        )
    
    with col2:
        if categoria == "Otro":
            categoria_custom = st.text_input("Especifica el tipo:")
            if categoria_custom:
                categoria = categoria_custom
    
    # PREGUNTA 3: Problema que resuelve (OBLIGATORIA)
    problema = st.text_area(
        "3. ¿Qué problema específico resuelve tu producto/servicio? *",
        placeholder="Ejemplo: Ayuda a freelancers a organizar sus finanzas y evitar problemas de impuestos",
        height=80
    )
    
    # PREGUNTA 4: Público objetivo (OBLIGATORIA)
    publico = st.text_input(
        "4. ¿Cuál es tu público objetivo? *",
        placeholder="Ejemplo: Diseñadores freelance de 25-40 años"
    )
    
    # PREGUNTA 5: País (OBLIGATORIA)
    pais = st.text_input(
        "5. ¿Para qué país/mercado? *",
        value="Argentina"
    )
    
    st.markdown("---")
    st.markdown("**Campos opcionales (completa al menos uno para mejores resultados)**")
    
    # PREGUNTA 6: A qué te dedicas (OPCIONAL)
    dedicacion = st.text_input(
        "6. ¿A qué te dedicas actualmente? (opcional)",
        placeholder="Ejemplo: Soy diseñador gráfico freelance"
    )
    
    # PREGUNTA 7: Título/Especialidad (OPCIONAL)
    titulo = st.text_input(
        "7. ¿En qué especialidad tienes un título o certificación? (opcional)",
        placeholder="Ejemplo: Licenciado en Psicología"
    )
    
    # PREGUNTA 8: Talento (OPCIONAL)
    talento = st.text_input(
        "8. ¿En qué eres bueno o tienes un talento especial? (opcional)",
        placeholder="Ejemplo: Soy bueno explicando conceptos complejos de forma simple"
    )
    
    st.markdown("---")
    
    submit = st.form_submit_button(
        "🚀 Generar Análisis Completo",
        use_container_width=True
    )

# Procesar cuando se envía el formulario
if submit:
    # Validar campos obligatorios
    campos_vacios = []
    if not tipo:
        campos_vacios.append("Tipo (Servicio/Producto)")
    if not categoria:
        campos_vacios.append("Categoría")
    if not problema:
        campos_vacios.append("Problema que resuelve")
    if not publico:
        campos_vacios.append("Público objetivo")
    if not pais:
        campos_vacios.append("País")
    
    if campos_vacios:
        st.error(f"❌ Por favor completa los siguientes campos obligatorios: {', '.join(campos_vacios)}")
    else:
        # Verificar que al menos un campo opcional esté completo
        campos_opcionales_completos = sum([
            bool(dedicacion),
            bool(titulo),
            bool(talento)
        ])
        
        # Preparar datos del formulario
        datos_formulario = {
            'tipo': tipo,
            'categoria': categoria,
            'problema': problema,
            'publico': publico,
            'pais': pais,
            'dedicacion': dedicacion,
            'titulo': titulo,
            'talento': talento
        }
        
        # Crear contenedor para el progreso
        progress_container = st.empty()
        status_container = st.empty()
        
        # Fase 1: Investigación
        with status_container:
            st.markdown("""
            <div class="info-box">
                🔍 <strong>Fase 1/2:</strong> Investigando el mercado...<br>
                Esto puede tomar 1-2 minutos mientras busco información en internet.
            </div>
            """, unsafe_allow_html=True)
        
        with progress_container:
            progress_bar = st.progress(0)
            for i in range(50):
                time.sleep(0.02)
                progress_bar.progress(i)
        
        investigacion, error = investigar_mercado(datos_formulario, api_key)
        
        if error:
            st.error(f"❌ Error en la investigación: {error}")
            st.info("💡 Intenta de nuevo en unos segundos o verifica tu conexión.")
            st.stop()
        
        # Fase 2: Generar informe
        with status_container:
            st.markdown("""
            <div class="info-box">
                📝 <strong>Fase 2/2:</strong> Generando tu informe profesional...<br>
                Analizando datos y creando el documento.
            </div>
            """, unsafe_allow_html=True)
        
        for i in range(50, 100):
            time.sleep(0.02)
            progress_bar.progress(i)
        
        informe, error = generar_informe(datos_formulario, investigacion, api_key)
        
        # Limpiar contenedores de progreso
        progress_container.empty()
        status_container.empty()
        
        if error:
            st.error(f"❌ Error generando el informe: {error}")
            st.info("💡 Intenta de nuevo en unos segundos.")
            st.stop()
        
        # Mostrar resultado exitoso
        st.markdown("""
        <div class="success-box">
            ✅ <strong>¡Informe generado exitosamente!</strong><br>
            Tu análisis de mercado está listo.
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar el informe
        st.markdown("---")
        st.subheader("📄 Tu Informe de Mercado")
        
        # Botón de descarga
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_{datos_formulario['categoria']}_{timestamp}.txt"
        
        st.download_button(
            label="💾 Descargar Informe",
            data=informe,
            file_name=nombre_archivo,
            mime="text/plain",
            use_container_width=True
        )
        
        # Mostrar informe con scroll
        st.text_area(
            "Informe completo:",
            value=informe,
            height=600,
            disabled=True
        )
        
        # Opción para generar otro
        st.markdown("---")
        if st.button("🔄 Generar otro análisis", use_container_width=True):
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>🎯 <strong>Analizador de Productos Digitales</strong></p>
    <p style="font-size: 0.9em;">Powered by Claude AI | Datos obtenidos mediante búsqueda web en tiempo real</p>
</div>
""", unsafe_allow_html=True)
