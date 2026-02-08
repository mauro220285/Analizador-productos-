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

# Sidebar para configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Obtener API Key desde secrets
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    st.error("⚠️ No se encontró la API Key en los secrets. Configúrala en Settings > Secrets")
    st.stop()
    
    st.markdown("---")
    
    st.markdown("""
    ### 📚 Cómo obtener tu API Key:
    1. Ve a [console.anthropic.com](https://console.anthropic.com)
    2. Crea una cuenta o inicia sesión
    3. Ve a "API Keys"
    4. Crea una nueva key
    5. Cópiala y pégala aquí
    
    **Nota:** Tu API key nunca se guarda, solo se usa en esta sesión.
    """)

# Función para investigar mercado
def investigar_mercado(idea_producto, pais, api_key):
    """Investiga el mercado usando Claude con web search"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""Necesito que investigues el mercado para esta idea de producto digital:

IDEA: {idea_producto}
PAÍS: {pais}

Investiga en la web y proporciona información sobre:
1. Productos similares que existen (nombres, precios, características)
2. Demanda del mercado (búsquedas en Google, tendencias)
3. Competencia directa e indirecta
4. Rangos de precios en el mercado
5. Público objetivo y segmentación
6. Gaps en el mercado (qué no existe o está mal resuelto)
7. Oportunidades únicas

Usa búsqueda web para obtener datos reales y actualizados. Sé específico con números, nombres de productos y precios cuando los encuentres."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
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
def generar_informe(idea_producto, datos_investigacion, pais, api_key):
    """Genera el informe formateado"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""Basándote en esta investigación de mercado, genera un informe COMPLETO siguiendo EXACTAMENTE este formato:

INVESTIGACIÓN REALIZADA:
{datos_investigacion}

IDEA DEL PRODUCTO:
{idea_producto}

PAÍS:
{pais}

---

Genera el informe siguiendo EXACTAMENTE esta estructura y formato (respeta los símbolos, líneas y emojis):

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

[Conexión personal con la idea, por qué tiene sentido para el creador]


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

IMPORTANTE:
- Usa datos REALES de la investigación
- Sé específico con precios, números, estadísticas
- El tono debe ser motivador pero realista
- Incluye al menos 5 bonus creativos y útiles
- El plan de acción debe ser ejecutable en 72 horas
"""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
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

# Interfaz principal
if not api_key:
    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Necesitas configurar tu API Key</strong><br>
        Ingresa tu API Key de Anthropic en el panel izquierdo para comenzar.
    </div>
    """, unsafe_allow_html=True)
else:
    # Formulario principal
    with st.form("analisis_form"):
        st.subheader("💡 Cuéntame tu idea")
        
        idea_producto = st.text_area(
            "¿Qué producto digital quieres crear?",
            placeholder="Ejemplo: Plantillas de Excel para freelancers",
            height=100
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            pais = st.text_input(
                "¿Para qué país/mercado?",
                value="Argentina"
            )
        
        with col2:
            st.write("")
            st.write("")
            submit = st.form_submit_button(
                "🚀 Generar Análisis",
                use_container_width=True
            )
    
    # Procesar cuando se envía el formulario
    if submit:
        if not idea_producto:
            st.error("❌ Por favor ingresa una idea de producto")
        else:
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
            
            investigacion, error = investigar_mercado(idea_producto, pais, api_key)
            
            if error:
                st.error(f"❌ Error en la investigación: {error}")
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
            
            informe, error = generar_informe(idea_producto, investigacion, pais, api_key)
            
            # Limpiar contenedores de progreso
            progress_container.empty()
            status_container.empty()
            
            if error:
                st.error(f"❌ Error generando el informe: {error}")
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
            nombre_archivo = f"informe_{timestamp}.txt"
            
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
