from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/hello/')
def hello_world():
    return 'Hello World!\n'


@app.route('/hello/<username>')
def hello_user(username):
    return 'Hello %s!\n' % username

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "success",
        "message": "L'API fonctionne parfaitement !",
        "version": "1.0.0"
    }), 200
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')