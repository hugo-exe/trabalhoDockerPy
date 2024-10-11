from flask import Flask, request, jsonify
import requests
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Endpoint para o Microserviço 1
@app.route('/pagar', methods=['POST'])
def processar_pagamento():
    """
    Processa o pagamento e notifica o Microserviço 2.
    ---
    tags:
      - Pagamento
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Pagamento
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
        description: Pagamento processado e notificação enviada
      500:
        description: Erro ao notificar
    """
    dados_pagamento = request.json

    # Enviar dados para o Microserviço 2
    microservice2_url = "http://microservice2:5001/notificar"
    response = requests.post(microservice2_url, json=dados_pagamento)

    if response.status_code == 200:
        return jsonify({"message": "Pagamento passou, enviado notificação"}), 200
    else:
        return jsonify({"message": "Erro ao notificar"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
