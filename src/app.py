from flask import Flask, request, jsonify
import base64
from utils.graph import generate_comparison_chart

app = Flask(__name__)

@app.route('/diavsdia', methods=['POST'])
def compare_days():
    data = request.get_json()
    
    if not isinstance(data, list) or len(data) != 2:
        return jsonify({'error': 'Input must be an array of two day objects'}), 400

    dia1 = data[0]
    dia2 = data[1]

    try:
        graph_image = generate_comparison_chart(dia1, dia2)
        return jsonify({'image': graph_image}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)