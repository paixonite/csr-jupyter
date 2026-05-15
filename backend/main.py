from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

# Caminho absoluto para a pasta frontend
frontend_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend')

# Inicializa o Flask
app = Flask(__name__, static_folder=frontend_folder, static_url_path='')

@app.route('/')
def index():
    # Serve o index.html na raiz
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    # Recebe o JSON do frontend
    data = request.get_json()
        
    code = data['code']
    
    try:
        # Executa o código python usando subprocess
        result = subprocess.run(
            ['python3', '-c', code],
            capture_output=True,
            text=True,
            timeout=5 # Limite de 5 segundos para timeout
        )  
        
        # Rodou com sucesso 
        if result.returncode == 0:
            output = result.stdout
        else:
            # Pega a mensagem de erro
            output = result.stderr

    except subprocess.TimeoutExpired:
        output = "Erro: Tempo de execução excedido ."
    except Exception as e:
        output = f"Erro interno: {str(e)}"
        
    return jsonify({'result': output})

if __name__ == '__main__':
    # Roda o servidor na porta
    app.run(host='0.0.0.0', port=6543)