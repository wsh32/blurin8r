from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from multiprocessing import Process, Queue, Value


app = Flask(__name__)
settings_queue = Queue(1)

settings = {
    'blur_size': 1,
    'max_face_size': -1,
    'blur_value': 50,
}

test_value = Value('d', 0.5)


def put_new_settings(new_settings):
    if settings_queue.full():
        try:
            settings_queue.get_nowait()
        except:
            pass
    settings_queue.put(new_settings)


def update_settings():
    try:
        settings = settings_queue.get_nowait()
    except:
        pass


def start_server():
    app.run(debug=True, threaded=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/update', methods = ["POST"])
def update():
    new_values = request.form
    invalid = []
    for setting_name, value in new_values:
        if setting_name in settings.keys():
            try:
                settings[setting_name] = float(value)
            except:
                invalid.append(setting_name)
        else:
            invalid.append(setting_name)
    put_new_settings(settings)

    if len(invalid) == 0:
        return jsonify({'OK': True})
    else:
        return jsonify({'OK': False, 'INVALID': invalid})


@app.route('/api/test')
def test():
    settings['blur_size'] = 2
    put_new_settings(settings)
    test_value.value = 100
    return "OK"


if __name__ == '__main__':
    start_server()

