from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/pagar', methods=['POST'])
def pagar():
    try:
        response = requests.post('http://microservico2:5001/notificar', json=request.json)
        return jsonify({"message": "Notificação enviada com sucesso", "response": response.json()}), 200
    except Exception as e:
        return jsonify({"error": "Erro ao enviar notificação", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
