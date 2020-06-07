from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from multiprocessing import Process, Queue, Value


app = Flask(__name__)

settings_queue = None
new_settings_flag = False
settings = {
    'blur_size': 1,
    'max_face_size': -1,
    'blur_value': 50,
}


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


def start_server(queue):
    global settings_queue
    settings_queue = queue
    app.run(debug=True, threaded=False, use_reloader=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/update', methods = ["POST"])
def update():
    global settings_queue
    new_values = request.form
    invalid = []
    for setting_name in new_values:
        if setting_name in settings.keys():
            value = new_values[setting_name]
            try:
                settings[setting_name] = float(value)
            except:
                invalid.append(setting_name)
        else:
            invalid.append(setting_name)
    settings_queue.put(settings)

    if len(invalid) == 0:
        return jsonify({'OK': True})
    else:
        return jsonify({'OK': False, 'INVALID': invalid})


@app.route('/api/test')
def test():
    global settings_queue
    settings['blur_size'] = 2
    settings_queue.put(settings)
    return "OK"


if __name__ == '__main__':
    start_server(Queue(1))

