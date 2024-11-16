import datetime
import sys
import os
from flask import Flask, request, jsonify

app = Flask(__name__)


# Helper function to get the correct path when packaged
def resource_path(relative_path):
    """
    Get the correct absolute path for resources when the application is packaged with PyInstaller.
    
    Args:
        relative_path (str): The relative path to the resource file/directory
        

    Returns:
        str: The absolute path to the resource
    """
    try:
        base_path = getattr(sys, '_MEIPASS', None)
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def echo_webhook(path):
    response_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'method': request.method,
        'path': f'/{path}',
        'headers': dict(request.headers),
        'query_params': dict(request.args),
        'body': request.get_json(silent=True) or request.form.to_dict() or None,
        'raw_data': request.get_data(as_text=True) or None
    }
    
    return jsonify(response_data)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def echo_webhook_root():
    return echo_webhook('')

def main():
    app.run(debug=False, host='0.0.0.0', port=6000)

if __name__ == '__main__':
    main() 
