from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request


app = Flask(__name__)

settings = {
    'blur_size': 1,
    'max_face_size': 0.25,
    'blur_value': 50,
}

def start_server():
    app.run(debug=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/update')
def update():
    new_values = request.get_json()
    invalid = []
    for setting_name in new_values.keys():
        if setting_name in settings.keys():
            settings[setting_name] = new_values[setting_name]
        else:
            invalid.append(setting_name)

    if len(invalid) == 0:
        return jsonify({'OK': True})
    else:
        return jsonify({'OK': False, 'INVALID': invalid})


if __name__ == '__main__':
    start_server()

