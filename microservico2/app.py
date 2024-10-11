from flask import Flask, request, jsonify
import pika
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

def send_to_rabbitmq(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    
    channel.queue_declare(queue='paymentsQueue')
    
    channel.basic_publish(exchange='',
                          routing_key='paymentsQueue',
                          body=message)
    connection.close()

@app.route('/notificar', methods=['POST'])
def notificar():
    """
    Recebe notificação e envia para o RabbitMQ.
    ---
    tags:
      - Notificação
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Notificação
          required:
            - id
            - amount
          properties:
            id:
              type: integer
              description: ID do pagamento
            amount:
              type: number
              description: Valor do pagamento
            description:
              type: string
              description: Descrição do pagamento
    responses:
      200:
        description: Notificação enviada ao RabbitMQ
      500:
        description: Erro ao enviar notificação
    """
    notificacao = request.json
    try:
        send_to_rabbitmq(str(notificacao))
        return jsonify({"message": "Notificação enviada"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao enviar notificação: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
