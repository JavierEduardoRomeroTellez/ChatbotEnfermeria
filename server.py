from flask import Flask, request, abort, jsonify, make_response
import json
import requests
import datetime
from rivescript import RiveScript
from config import token, auth_token


app = Flask(__name__)

app.debug = True



@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and verify_token == auth_token:
        print('correct')
        return challenge
    else:
        return jsonify(error='Invalid Token'), 400
    
@app.route('/webhook', methods=['POST'])
def webhook():
    request_body = request.get_data(as_text=True)
    print(request_body)
    data = json.loads(request_body)
    
    if 'messages' in data['entry'][0]['changes'][0]['value']:
        timestamp = data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
        now = datetime.datetime.now()
        timestamp_datetime = datetime.datetime.fromtimestamp(int(timestamp))
        
        if (now - timestamp_datetime) < datetime.timedelta(minutes=10):
            
            if data['entry'][0]['changes'][0]['value']['messages'][0]['type'] == 'interactive':
                mensaje = data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["id"]  
                if mensaje == 'Información':
                    mensaje = 'informacion'       
            else:
                mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            
            bot = RiveScript()
            bot.load_file('answers.rive')
            bot.sort_replies()
            
            print(mensaje)
            
            respuesta = bot.reply("localuser", mensaje)
            
            wa_id = data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
            phone_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                
            wa_id = wa_id[0:2] + wa_id[3:]
            url = "https://graph.facebook.com/v16.0/107611362336645/messages"
            
            if respuesta == 'Saludo':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        "body": {
                            "text": "¡Hola! Soy tu asistente virtual para contratar un enfermero cuidador. ¿En qué puedo ayudarte hoy?"
                        },
                        "action": {
                            "button": "Opciones",
                            "sections": [
                                {
                                    "title": "Selecciona",
                                    "rows": [
                                        {
                                            "id": "enfermero",
                                            "title": "Buscar enfermero",
                                            "description": ""
                                        },
                                        {
                                            "id": "contratacion",
                                            "title": "Proceso de contratación",
                                            "description": ""
                                        },
                                        {
                                            "id": "pregunta",
                                            "title": "Otra pregunta",
                                            "description": ""
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                })
                
            if respuesta == 'contratacion':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        "body": {
                            "text": "¡Excelente! Estás en el lugar correcto. El proceso de contratación es sencillo. Primero, necesitamos conocer los detalles de la ubicación donde se necesitará el enfermero cuidador, el horario de trabajo y el nivel de experiencia que estás buscando. Con esa información, podemos hacer una búsqueda de enfermeros cuidadores que se adapten a tus necesidades. \n\nUna vez que tengamos una lista de candidatos, te enviaremos la información de contacto y los perfiles de los candidatos para que puedas revisarlos. Luego, tú puedes seleccionar al candidato que más te interese. Nosotros nos encargaremos del proceso de verificación y te ayudaremos a finalizar el contrato. \n\nSi tienes alguna pregunta específica sobre el proceso de contratación, por favor házmelo saber y estaré encantado de ayudarte."
                        },
                        "action": {
                            "button": "Opciones",
                            "sections": [
                                {
                                    "title": "Selecciona",
                                    "rows": [
                                        {
                                            "id": "enfermero",
                                            "title": "Buscar enfermero",
                                            "description": ""
                                        },
                                        {
                                            "id": "pregunta",
                                            "title": "Otra pregunta",
                                            "description": ""
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                })
            
            
            if respuesta == 'pregunta':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": str(wa_id),
                    "type": "text",
                    "text": {
                        "body": "Claro, estaré encantado de ayudarte con cualquier pregunta que tengas. ¿En qué puedo ayudarte?"
                    }
                })

            if respuesta == 'enfermero':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        "body": {
                            "text": "Perfecto, primero necesito saber en qué ubicación necesitas un enfermero cuidador."
                        },
                        "action": {
                            "button": "Opciones",
                            "sections": [
                                {
                                    "title": "Selecciona",
                                    "rows": [
                                        {
                                            "id": "mexicali",
                                            "title": "Mexicali",
                                            "description": ""
                                        },
                                        {
                                            "id": "tijuana",
                                            "title": "Tijuana",
                                            "description": ""
                                        },
                                        {
                                            "id": "otraubicacion",
                                            "title": "Otra ubicación",
                                            "description": ""
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                })
            
            if respuesta == 'horario':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        "body": {
                            "text": "Excelente, ¿Cuál es el horario que necesitas cubrir?"
                        },
                        "action": {
                            "button": "Opciones",
                            "sections": [
                                {
                                    "title": "Selecciona",
                                    "rows": [
                                        {
                                            "id": "completo",
                                            "title": "Jornada completa (8 hr)",
                                            "description": ""
                                        },
                                        {
                                            "id": "medio",
                                            "title": "Medio tiempo (4 hr)",
                                            "description": ""
                                        },
                                        {
                                            "id": "nocturno",
                                            "title": "Nocturno (12 hr)",
                                            "description": ""
                                        },
                                        {
                                            "id": "otrohorario",
                                            "title": "Otra opción",
                                            "description": ""
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                })
                
            if respuesta == 'experiencia':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        "body": {
                            "text": "¿Cuál es el nivel de experiencia que estás buscando?"
                        },
                        "action": {
                            "button": "Opciones",
                            "sections": [
                                {
                                    "title": "Selecciona",
                                    "rows": [
                                        {
                                            "id": "menos1a",
                                            "title": "Menos de 1 año",
                                            "description": ""
                                        },
                                        {
                                            "id": "1a3a",
                                            "title": "1 a 3 años",
                                            "description": ""
                                        },
                                        {
                                            "id": "3a5a",
                                            "title": "3 a 5 años",
                                            "description": ""
                                        },
                                        {
                                            "id": "mas5a",
                                            "title": "Más de 5 años",
                                            "description": ""
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                })
                
            if respuesta == 'gracias':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": str(wa_id),
                    "type": "text",
                    "text": {
                        "body": "Gracias por proporcionar esos detalles. Pronto le contestará un agente para presentarle las opciones"
                    }
                })
                
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token
            }
                
            response = requests.request("POST", url, headers=headers, data=payload)      
            
    response = make_response('')
    response.status_code = 200
    return response    
    
       
if __name__ == '__main__':
    app.run()
