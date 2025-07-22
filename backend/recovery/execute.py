import subprocess


def execute_photorec(command, settings, socketio):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            socketio.emit('recovery_update', {'data': output.strip()}, namespace='/recovery')
    rc = process.poll()
    return rc
