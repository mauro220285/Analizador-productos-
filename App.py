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

# CSS personalizado (sin cambios)
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

# Función para investigar mercado (OPTIMIZADA)
def investigar_mercado(datos_formulario, api_key):
    """Investiga el mercado usando Claude con web search - VERSIÓN OPTIMIZADA"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Contexto ultra-compacto
        contexto = f"{datos_formulario['tipo']}: {datos_formulario['categoria']} | Resuelve: {datos_formulario['problema']} | Target: {datos_formulario['publico']} | País: {datos_formulario['pais']}"
        
        # Agregar solo si existe
        extras = []
        if datos_formulario.get('dedicacion'):
            extras.append(f"Dedicación: {datos_formulario['dedicacion']}")
        if datos_formulario.get('titulo'):
            extras.append(f"Título: {datos_formulario['titulo']}")
        if datos_formulario.get('talento'):
            extras.append(f"Talento: {datos_formulario['talento']}")
        
        if extras:
            contexto += " | " + " | ".join(extras)
        
        # Prompt ultra-conciso (reducido 60%)
        prompt = f"""Investiga este producto digital: {contexto}

Busca en web y responde CONCISO:
1. 2 productos similares (nombre, precio exacto)
2. Demanda estimada (volumen búsquedas/mes)
3. Rango de precios del mercado
4. 1 oportunidad/gap identificado

Solo datos concretos, sin explicaciones."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1200,  # ✂️ REDUCIDO de 2500
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

# Función para generar informe (OPTIMIZADA)
def generar_informe(datos_formulario, datos_investigacion, api_key):
    """Genera el informe formateado - VERSIÓN OPTIMIZADA"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Contexto compacto
        contexto = f"{datos_formulario['tipo']}: {datos_formulario['categoria']} | {datos_formulario['problema']} | Target: {datos_formulario['publico']} | {datos_formulario['pais']}"
        
        if datos_formulario.get('dedicacion'):
            contexto += f" | {datos_formulario['dedicacion']}"
        if datos_formulario.get('titulo'):
            contexto += f" | {datos_formulario['titulo']}"
        if datos_formulario.get('talento'):
            contexto += f" | {datos_formulario['talento']}"
        
        # Prompt simplificado (reducido 50%)
        prompt = f"""Genera informe siguiendo EXACTO este formato:

DATOS: {contexto}

INVESTIGACIÓN: {datos_investigacion}

═══════════════════════════════════════════════════════════════
                    🎯 TU PRODUCTO DIGITAL
═══════════════════════════════════════════════════════════════

📦 PRODUCTO
───────────────────────────────────────────────────────────────
[Nombre pegadizo]
Formato: [Tipo]

💰 PRECIO
───────────────────────────────────────────────────────────────
$[Precio ARG]
Mercado: [Rango basado en investigación]

👥 CLIENTE IDEAL
───────────────────────────────────────────────────────────────
[Descripción específica]
Problema: [Dolor real]
Deseo: [Objetivo]

🎣 PROPUESTA DE VALOR
───────────────────────────────────────────────────────────────
"[Frase poderosa única]"

📋 QUÉ INCLUYE
───────────────────────────────────────────────────────────────
PRINCIPAL:
✓ [Componente core]

BONUS:
✓ [Bonus 1]
✓ [Bonus 2]
✓ [Bonus 3]

✅ POR QUÉ SE VENDERÁ
───────────────────────────────────────────────────────────────
[Datos mercado: volumen búsquedas, estadísticas]
- [Ventaja 1 con dato]
- [Ventaja 2 con dato]
- [Diferenciación única]

🌊 OPORTUNIDAD
───────────────────────────────────────────────────────────────
[Gap del mercado identificado]

⚡ PLAN 72 HORAS
═══════════════════════════════════════════════════════════════
DÍA 1 - [FASE]
□ [Tarea 1]
□ [Tarea 2]

DÍA 2 - [FASE]
□ [Tarea 1]
□ [Tarea 2]

DÍA 3 - [FASE]
□ [Tarea 1]
□ [Tarea 2]

🚀 PRIMER PASO (30 MIN)
═══════════════════════════════════════════════════════════════
[Acción concreta inmediata]
═══════════════════════════════════════════════════════════════

Usa datos REALES. Sé directo."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1200,  # ✂️ REDUCIDO de 2500
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

# ═══════════════════════════════════════════════════════════════
# FORMULARIO (sin cambios - mantiene las 8 preguntas)
# ═══════════════════════════════════════════════════════════════

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
