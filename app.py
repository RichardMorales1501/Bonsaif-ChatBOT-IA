from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)
port = int(os.environ.get('PORT', 2000))  # Usa 2000 si la variable PORT no está definida



# Cargar el modelo entrenado
MODEL_PATH = "modelo_entrenado.pkl"
if os.path.exists(MODEL_PATH):
    clf = joblib.load(MODEL_PATH)
    print("Modelo cargado exitosamente.")
else:
    clf = None
    print("Error: Modelo no encontrado. Asegúrate de que 'modelo_entrenado.pkl' exista.")

user_states = {}


respuestas = {
    "Abono a capital" : "Puedes hacer abonos a capital y tienes dos opciones:\n1. Reducir el monto de tus pagos mensuales: Esto te permitirá tener cuotas más bajas cada mes 📉\n2. Reducir el plazo de tu crédito: De esta manera, terminarás de pagar tu crédito en menos tiempo ⏳\nPara hacer tu pago o conocer más información contacta a atención a clientes al\n- Teléfono: 5540407940\n- WhatsApp: 5593036268\n- Correo: atencion@laudex.mx",
    "Adeudos con universidad": "Si tienes adeudos de algún periodo, no te preocupes.\n\nPuedes realizar una renovación y contemplar esa cantidad dentro del monto solicitado, siempre y cuando tu crédito tenga línea suficiente para cubrirlo 💵",
    "Atencion al cliente": "Por favor, para esta solicitud debes comunicarte con atención al cliente:\n\n- Teléfono: 5540407940\n- WhatsApp: 5593036268\n- Correo: atencion@laudex.mx\n\n_Mis compañeras están disponibles de lunes a viernes de 8 hrs a 20 hrs y sábados de p a 14 hrs_\n\n_Por favor, contáctalas lo antes posible para que puedan ayudarte_.",
    "Calculadora un pago":"La calculadora 🧮 en un solo pago (100) es:\n\nUn documento que indica el costo total de tus estudios cuando decides pagar el periodo completo de una sola vez, en lugar de hacerlo en mensualidades.\n\nPor lo general, pagar de esta manera resulta más económico, ya que en pagos crecientes o mensuales las colegiaturas suelen incrementar. 🚨\n\nRecuerda que Laudex realiza el pago del periodo completo y no pagos parcializados. 📈\n\nPuedes descargar tu calculadora en:\n*ventanilla-enlinea.unitec.mx*\n\n_En caso de que la plataforma de UNITEC no te deje descargarla, debes acudir con respaldo económico._",
    "Calculo mensualidades" : "Para determinar el monto exacto de tus mensualidades, primero necesitamos iniciar el proceso de renovación💸\n\nEste cálculo se realiza con base en el monto que solicites y el plazo de tu crédito 🕦\n\n_Si al final las mensualidades resultan por encima de tu presupuesto, no te preocupes. Solo asegúrate de no firmar el documento; *si no lo firmas, no te compromete a nada*_.\n\nSi deseas continuar, por favor responde “*Quiero iniciar mi renovación*” para que podamos iniciar con tu proceso de renovación y brindarte toda la información que necesitas. 😊",
    "Cambio de OS" : "Lamentablemente, *solo podemos realizar el trámite* para cambiar al obligado solidario *en caso de fallecimiento o incapacidad permanente* del actual obligado solidario.\n\nPero si este no es tu caso, podríamos tratar ayudarte, pero debes saber que este proceso se somete a validación.\n\nPara proceder, necesitas proponer a un candidato que cumpla con los siguientes requisitos:\n1. INE (identificación oficial)🪪\n2. Comprobante de domicilio reciente🏡\n3. Comprobante de ingresos de los últimos 3 meses💶",
    "Como firmar": "Sigue estos pasos para firmar tu pagaré 📝:\n\n*Paso 1*:\nBusca en tu bandeja de entrada un correo de Firmamex.\n(_No olvides revisar también tu carpeta de spam o correos no deseados_).\n\n*Paso 2*:\nIngresa al enlace proporcionado en el correo y firma el documento. ✍🏻\n_Recuerda que cada participante (tú y tu obligado solidario, si aplica) recibirá un documento para firmar_.\n\nSi tienes algún problema durante el proceso, ¡avísanos para ayudarte! 😊",
    "Conceptos renovacion": "Sí, es posible incluir otros conceptos adicional a tus colegiaturas en tu financiamiento con Laudex\n\nSiempre y cuando tu universidad lo permita\n\nDe esta manera, podrás utilizar tu crédito Laudex para cubrir los conceptos que necesites💰",
    "Cuando pago" : "El nuevo monto que debes pagar se activa a partir del primer día hábil del mes siguiente. 🗓️\n\nEsto significa que si el primer día del mes no es un día laboral 🏖️, tu pago se procesará el siguiente día hábil 👷🏻.\n\nPor ejemplo, si el primero de enero cae en un domingo, tu pago se moverá al lunes 2 de enero 📅",
    "Depositos a universidades": "Una vez que firmas tu pagaré ✍🏻 ... hacemos unas ultimas validaciones y si todo esta bien, programamos el pago de forma inmediata.\n\nEl tiempo en que se refleje dependerá de tu universidad, pero puedes estar tranquilo(a) 🧘🏻 ... \n\nLaudex enviará el comprobante el día habil siguiente a la firma del pagaré.\n\nSi aún no se refleja coloca *quiero hablar con un ejecutivo* para poder ser atendido por un especialista",
    "Desconocido": "Lo siento, no estoy seguro de cómo responder a eso. ¿Podrías proporcionar más detalles?",
    "Documentos academicos": "Para renovar necesitas de tu historial académico, ya que es un documento oficial emitido por tu escuela que resume tu desempeño académico 📑\n\nEn este documento, encontrarás tus calificaciones, el promedio general de tus materias, tu nombre completo y la fecha de emisión 📆",
    "Domi no aplicada" : "*Recuerda que las domiciliaciones se procesan el primer día hábil del mes*.\n\nSi el primer día del mes es inhábil, el cargo se realizará el siguiente día hábil 🗓️\n\nEjemplo:\n\n- Si el primer día del mes es domingo, la domiciliación se realizará el lunes (si no es festivo).\n- Si el lunes es festivo, se hará el martes.\n\nPara más información o realizar tu pago contacta a atención a clientes al\n- Teléfono: 5540407940\n- WhatsApp: 5593036268\n- Correo: atencion@laudex.mx",
    "Domiciliar" : "Domiciliar 💳 es muy fácil y puedes hacerlo directamente en\nportal.laudex.mx\n\n*Beneficios de domiciliar*:\n- No hay comisión por forma de pago.\n- Evitas ir al banco a pagar en caja.\n- No necesitas ingresar a tu app móvil bancaria cada mes.\n- El cargo se genera automáticamente el primer día hábil del mes.\n- La confirmación de tu pago se procesa en un máximo de 24 horas hábiles\n- Puedes domiciliar cualquier cuentay/o tarjeta de de debito.\n\nPara más información contacta a atención a clientes al\n- Teléfono: 5540407940\n- WhatsApp: 5593036268\n- Correo: atencion@laudex.mx",
    "Donde HA": "*El proceso puede variar según tu universidad* 👨🏻‍💻\n\nGeneralmente, puedes descargarlo directamente desde la plataforma en línea de la universidad.\n\nEn caso de que no sea posible, deberás acudir al campus y solicitarlo personalmente 😊",
    "Dudas pago": "El ajuste en tu pago mensual se realiza para simplificar tu experiencia y evitar que tengas que hacer pagos dobles. Esto significa que, con tu nuevo pago mensual, estás cubriendo tanto la cantidad pendiente de tu crédito anterior como el nuevo monto que solicitaste en la renovación 💶",
    "Fecha virtual": "La fecha de depósito es el día en que deseas que se realice el pago a tu universidad. 🎓\n\nPor ejemplo, si tu periodo comienza el 1 de enero, puedes colocar una fecha cercana como referencia.🚨\n\nRecuerda: Laudex programa los pagos con base en esta fecha, pero la confirmación también depende de tu universidad. Si tienes dudas o necesitas ayuda escribe *quiero hablar con un ejecutivo* para poder ser atendido por un especialista 😊",
    "Informacion comercial" : "",
    "Informacion del pago" : "El monto que debes pagar se encuentra en el pagaré que se te envía a ti y a tu obligado solidario por correo electrónico💶\nEl monto del pago mensual está resaltado en amarillo, y también encontrarás el mes específico en el que debes realizar el pago.\nPara hacer tu pago o conocer más información contacta a atención a clientes al\n- Teléfono: 5540407940\n- WhatsApp: 5593036268\n- Correo: atencion@laudex.mx",
    "Informacion financiera": "Puedes consultar tus montos, saldos y movimientos en tu portal de cliente: https://portal.laudex.mx/login.",
    "Informacion sobre renovaciones": "Puedes obtener información sobre renovaciones en nuestro portal: https://laudex.mx/renovaciones/ o escribiendo a renovaciones@laudex.mx.",
    "Liquidar" : "💚 ¡Gracias por dejarnos ser parte de tu camino y permitirnos apoyarte en tus metas! 💚\n\nPor favor, para esta solicitud debes comunicarte con atención al cliente:\n\n- Teléfono: 5540407940\n- WhatsApp: 5593036268\n- Correo: atencion@laudex.mx\n\n_Mis compañeras están disponibles de lunes a viernes de 8 hrs a 20 hrs y sábados de p a 14 hrs_\n\n_Por favor, contáctalas lo antes posible para que puedan ayudarte_.",
    "Lugar laudex" : "Bosque de Radiatas 42 – PH-02\nCol. Bosques de las Lomas, CDMX, C.P. 05120\n\nhttps://maps.app.goo.gl/sazpAQV6sNmLCJNw6",
    "Monto que necesitas": "El monto que necesitas solicitar *dependerá totalmente de tus necesidades y de los costos de tu universidad* 📚\n\nTe recomiendo considerar lo siguiente:\n\nSolicita el monto que cubra el total de tu periodo actual o el nuevo periodo.\nRecuerda que *Laudex no realiza pagos mensuales, sino que cubre el pago total del periodo*.\n\nPor ejemplo, si tu periodo es semestral, el crédito cubrirá todas las mensualidades juntas 💸",
    "Politica de pagos": "Todos los pagos se realizan únicamente el primer día de cada mes. Esta política nos ayuda a mantener un proceso de gestión eficiente. Te recomendamos que planifiques tus pagos en función de esta fecha. ¡Gracias por tu comprensión!",
    "Portal" : "¡Conoce el nuevo portal del cliente! 📱\nEn portal.laudex.mx puedes acceder a toda la información de tu crédito en un solo lugar:\n- Fecha de tus pagos 📅\n- Cómo y dónde realizar tus pagos 💳\n- Estados de cuenta detallados 📂\n- Historial de tus últimos pagos 🧾\n- Y mucho más.\n\n¿Tienes dudas o necesitas ayuda? Estamos aquí para apoyarte:\n- Teléfono: 5540407940\n- WhatsApp: 5593036268\n- Correo: atencion@laudex.mx\n\n💡 _Estamos disponibles de lunes a viernes de 8:00 a 20:00 hrs y sábados de 9:00 a 14:00 hrs_.",
    "Postventa" : "Para poder brindar acceso por favor, envíanos un correo a\n\npostventa@laudex.mx\n\nIndicando tu nombre completo y nuestro equipo te asistirá para que recuperes tus credenciales y puedas acceder al portal 🔐",
    "Problemas con documentos": "Si no encuentras tu pagaré, busca un correo con el asunto 'FIRMAMEX' en tu bandeja de entrada o spam. Si no lo encuentras, contáctanos.",
    "Problemas con firmamex" : "*¿Has buscado el documento como “FIRMAMEX” en tu bandeja de entrada y en la carpeta de spam?*\n\nEl pagaré se envía primero al alumno(a) y, una vez firmado, se enviará al obligado solidario.\nA veces, por razones de seguridad, el correo puede terminar en la bandeja de spam o en correos no deseados o spam ✍🏻",
    "Puedo ayudarte mas": "¿Existe algo más en lo que pueda ayudarte? 🦌",
    "Que es OS":" Un *Obligado solidario* es:\n\nUn co-acreditado y co-responsable con el estudiante en su crédito educativo 👥\n\nParticipa en el crédito educativo, desde el proceso de solicitud y al igual que el estudiante, en la apertura firma el contrato de crédito y en cada disposición subsecuente firma un nuevo pagaré 📝",
    "Que es": "Una renovación en Laudex es *cuando solicitas acceder a una parte de tu línea de crédito disponible*\n\n Piensa en ello como cuando usas una tarjeta de crédito (TDC)\n\n Por ejemplo, si tienes una TDC 💳 con un límite de $10,000 y ya has utilizado $6,000, te quedan $4,000 disponibles para gastar\n\nSi decides hacer una renovación, puedes solicitar parte de esos $4,000 para financiar un nuevo periodo de estudios💶",
    "Reflejo de pagos": "Tu pago se refleja en un plazo de 24 horas hábiles ⏳\n\nPara más información contacta a atención a clientes al\n- Teléfono: 5540407940\n- WhatsApp: 5593036268\n- Correo: atencion@laudex.mx",
    "Se necesta reenviarlo": "¡Entendido! Para ayudarte mejor, ¿podrías por favor hacer lo siguiente?\n\n1. Escríbeme tu correo electrónico aquí en el chat.\n2. Tómale una captura de pantalla a tu bandeja de spam y correos no deseados y compártela conmigo.\n3. Ayúdame enviando un correo de prueba a renovaciones@laudex.mx con el asunto: PRUEBA y tu nombre completo.\n\nSi tienes un obligado solidario, pídele que haga lo mismo:\n\n4. Comparte su correo y una captura de pantalla de su bandeja de entrada, spam y/o no deseados.\n5. Pídeles que también envíen un correo de prueba al mismo correo electrónico.\n\nCon esta información, podremos ayudarte a resolverlo lo antes posible 😊",
    "Saludo inicial": "Hola soy *Reno* 🦌\n\nTu asistente virtual de Renovaciones Laudex\n\n*¿Cómo puedo ayudarte?*",
    "Tiempo de respuesta renovaciones": "La respuesta a tu trámite será enviada a tu correo electrónico en un plazo máximo de 72 horas.\n\nTe pedimos, por favor, estar pendiente de tu bandeja de entrada y también revisar tu carpeta de spam o correos no deseados. ✉️\n\nSi después de este tiempo no has recibido respuesta, por favor responde *Pasaron más de 72 horas*, y con gusto revisaremos tu solicitud a detalle. 🕵",
    "Que duda": "Con gusto puedo ayudarte, aquí estamos para resolver tus dudas. 😊\n\nPara poder ayudarte mejor, ¿me puedes contar un poquito más? Por ejemplo: ¿es sobre pagos, renovaciones, documentos, o algo más? 🎓💰",
}

# Función para procesar el mensaje con el modelo de IA
def procesar_mensaje(msg, from_number):
    if clf is None:
        return {
            "msg_response": respuestas["Desconocido"],
            "asignar": True,
            "fin": False
        }
    try:
        # Clasificar el mensaje
        categoria = clf.predict([msg])[0]
        print(f"Categoria: {categoria}")

        # Crear la respuesta según la categoría
        if categoria == "Canalizar con asesor":
            if from_number in user_states:
                del user_states[from_number]  # Eliminar al usuario de la lista de estados
            return {
                "msg_response": "Te estamos transferido con un asesor... ",
                "asignar": True,  # Se asigna a un agente
                "fin": False      # La conversación sigue activa
            }
        elif categoria == "Despedida":
            if from_number in user_states:
                del user_states[from_number]  # Eliminar al usuario de la lista de estados
            return {
                "msg_response": "Gracias por comunicarte con nosotros, hasta pronto 👋🏻.",
                "asignar": False, # No se asigna a un agente
                "fin": True       # La conversación debe finalizar
            }
        elif categoria == "Iniciar renovacion":
            user_states[from_number]["step"] = 2
            return {
                "msg_response": "¿En qué universidad estudias? \n1. UNITEC\n2. UVM\n3. UPAEP\n4. UNIVA\n5. Otra",
                "asignar": False,
                "fin": False
            }
        elif categoria == "Cambiar correo":
            return {
                "msg_response": "Para actualizar tu correo 📧 sigue estos pasos:\n\n1. Graba un video: Menciona tu *nombre completo*, el número de *contrato* y si eres estudiante u obligado solidario, tambien menciona *el correo anterior y el nuevo*.\n2. Envíanos tu video por este medio.\n\n⏳ En un plazo máximo de 48 horas hábiles, recibirás el pagaré en tu nuevo correo.😊",
                "asignar": True,
                "fin": False
            }
        else:
            # Respuesta para categorías desconocidas
            return {
                "msg_response": respuestas.get(categoria, "No entiendo tu mensaje, ¿podrías reformularlo?"),
                "asignar": False,
                "fin": False
            }

    except Exception as e:
        print(f"Error procesando el mensaje con el modelo de IA: {e}")
        return {
            "msg_response": respuestas["Desconocido"],
            "asignar": False,
            "fin": False
        }
    
# Ruta para la raíz del servidor
@app.route("/")
def home():
    print(f"Encabezados de la solicitud: {dict(request.headers)}")
    return "Bienvenido a la API de chatbot de renovaciones Laudex. Todo está funcionando correctamente."
# Endpoint para recibir datos de Bonsaif
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        print(f"Encabezados de la solicitud: {dict(request.headers)}")

        # Obtener los datos enviados por Bonsai
        data = request.json
        if not data or "data" not in data:
            return jsonify({"error": "Datos inválidos"}), 400

        print(f"Datos recibidos: {data}")
        msg = data.get('data', {}).get('msg', '')
        name = data.get('data', {}).get('name', '')
        first_name = name.split()[0] if name else ''  # Toma el primer nombre

        from_number = data.get('data', {}).get('phone', '')

        print(f"Mensaje recibido: {msg}")
        print(f"Primer nombre recibido: {first_name}")
        print(f"Telefono: {from_number}")

        # Inicializar el estado del usuario si es necesario
        if from_number not in user_states:
            user_states[from_number] = {"step": 0}

        step = user_states[from_number]["step"]

        # Flujo de pasos
        if step == 0:
            user_states[from_number]["step"] = 1
            return jsonify({
                "msg_response": f"Hola *{first_name}*\n\nBienvenido a Renovaciones Laudex 💚\n\n*¿En qué podemos ayudarte?*\n\n1. Iniciar renovación\n2. Seguimiento a solicitud\n3. Dudas sobre pagos\n4. Otra consulta",
                "asignar": False,
                "fin": False
            }), 200

        elif step == 1:
            if msg in {"1", "Iniciar renovación", "Iniciar mi renovación", "Quiero renovar"}:
                user_states[from_number]["step"] = 2
                return jsonify({
                    "msg_response": "¿En qué universidad estudias? \n1. UNITEC\n2. UVM\n3. UPAEP\n4. UNIVA\n5. Otra",
                    "asignar": False,
                    "fin": False
                }), 200
            elif msg == "2" or msg == "3" or msg == "4" or msg == "2. Seguimiento a solicitud" or msg == "3. Dudas sobre pagos" or msg == "4. Otra consulta" or msg == "Seguimiento a solicitud" or msg == "Dudas sobre pagos" or msg == "Otra consulta":                
                user_states[from_number]["step"] = 9
                return jsonify({
                    "msg_response": "Hola soy *Reno* 🦌\n\nTu asistente virtual de Renovaciones Laudex\n\n*¿Cómo puedo ayudarte?*",
                    "asignar": False,
                    "fin": False
                }), 200
            else:
                return jsonify({
                    "msg_response": "Responde con una opción válida:\n1. Iniciar renovación\n2. Seguimiento a solicitud\n3. Dudas sobre pagos\n4. Otra consulta",
                    "asignar": False,
                    "fin": False
                }), 200
        elif step == 2:
            if msg == "1" or msg == "UNITEC" or msg == "unitec" or msg == "Unitec" or msg == "1. UNITEC":                
                user_states[from_number]["step"] = 9
                return jsonify({
                    "msg_response": "Ok, para vamos a iniciar.\n\nPor favor ayudame a subir tus documentos y llenar algunos unos datos en el iguiente link:\n\nhttps://bit.ly/4e4Zn1r\n\nNecesitaras de *tu historial académico* 📝 y tu *calculadora en un solo pago (100)* 🔢 en PDF\n\nSi no lo tienes puedes descargarlo desde:\nventanilla-enlinea.unitec.mx/login",
                    "asignar": False,
                    "fin": False
                }), 200
            elif msg == "2" or msg == "UVM" or msg == "uvm" or msg == "Uvm" or msg == "2. UVM":
                return jsonify({
                    "msg_response": "Ok, para vamos a iniciar.\n\nPor favor indicame el monto total que necesitas para cubrir el costo total de tu nuevo periodo",
                    "asignar": True,
                    "fin": False
                }), 200
            elif msg == "3" or msg == "UPAEP" or msg == "upaep" or msg == "Upaep" or msg == "3. UPAEP":
                return jsonify({
                    "msg_response": "Ok, para vamos a iniciar.\n\nPor favor compárteme tu kardex con fecha de este mes y estado de cuenta (UNISOF)",
                    "asignar": True,
                    "fin": False
                }), 200
            elif msg == "4" or msg == "UNIVA" or msg == "univa" or msg == "Univa" or msg == "4. UNIVA":
                user_states[from_number]["step"] = 9
                return jsonify({
                    "msg_response": "Para realizar tu inscripción debes visitar las oficinas de cobranza en tu campus UNIVA y firmar tu carga académica con Pedro Hernández.\n\nEstará disponible de lunes a viernes, de 9:00 a 14:00 HRS y de 16:00 a 19:00 HRS. ⏰",
                    "asignar": False,
                    "fin": False
                }), 200
            elif msg == "5" or msg == "OTRA" or msg == "otra" or msg == "Otra" or msg == "5. Otra":
                return jsonify({
                    "msg_response": "Por favor, indícame el monto total que necesitas para cubrir este periodo (o el próximo) 💰 y comparte tu historial académico 📝.",
                    "asignar": True,
                    "fin": False
                }), 200
            elif msg == "Atras" or msg == "atras" or msg == "0" or msg == "inicio":
                user_states[from_number]["step"] = 0
            else:
                return jsonify({
                    "msg_response": "Responde con una opción válida:\n¿En qué universidad estudias? \n1. UNITEC\n2. UVM\n3. UPAEP\n4. UNIVA\n5. Otra\n\n0. Regresar al inicio",
                    "asignar": False,
                    "fin": False
                }), 200
            
        
        elif step == 9:
            response = procesar_mensaje(msg, from_number)
            return jsonify(response), 200
        

    except Exception as e:
        print(f"Error procesando la solicitud: {e}")
        return jsonify({"error": "Error procesando la solicitud"}), 500


if __name__ == '__main__':
    # Configura el puerto en el que se ejecutará la aplicación
    # Obtener el puerto desde las variables de entorno
    app.run(host='0.0.0.0', port=port, debug=True)