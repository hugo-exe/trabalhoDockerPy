from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

def conectar_rabbit():
    try:
        connection_parameters = pika.ConnectionParameters(
            host="rabbitmq",
            port=5672,
            credentials=pika.PlainCredentials(
                username="guest",
                password="guest"
            )
        )
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        print("Conectado ao RabbitMQ")
        return connection, channel
    except Exception as e:
        print(f"Falha ao conectar ao RabbitMQ: {str(e)}")
        return None, None

@app.route('/notificar', methods=['POST'])
def notificar():
    connection, channel = conectar_rabbit()
    if channel is None:
        return jsonify({"error": "Falha ao conectar ao RabbitMQ"}), 500

    channel.queue_declare(queue='data_queue', durable=True)
    mensagem = request.json.get('mensagem')

    try:
        channel.basic_publish(
            exchange='',
            routing_key='data_queue',
            body=mensagem,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        connection.close()
        return jsonify({"message": "Mensagem enviada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao enviar mensagem: {str(e)}"}), 500

@app.route('/consumir', methods=['GET'])
def consumir():
    connection, channel = conectar_rabbit()
    if channel is None:
        return jsonify({"error": "Falha ao conectar ao RabbitMQ"}), 500

    method_frame, header_frame, body = channel.basic_get(queue='data_queue')

    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        mensagem = body.decode('utf-8')
        __fechar_conexao(channel, connection)
        print(f"Mensagem consumida: {mensagem}")
        return jsonify({"mensagem": mensagem}), 200
    else:
        __fechar_conexao(channel, connection)
        return jsonify({"message": "Nenhuma mensagem encontrada na fila"}), 200

def __fechar_conexao(channel, connection):
    channel.close()
    connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
