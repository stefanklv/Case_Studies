import subprocess
import webbrowser
import time
import logging
import sys

logging.basicConfig(filename='app.log', level=logging.DEBUG)

def start_flask_app():
    logging.info('Starting Flask app...')
    if sys.platform == "win32":
        proc = subprocess.Popen(['python', 'app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        proc = subprocess.Popen(['python', 'app.py'])
    return proc

if __name__ == '__main__':
    proc = start_flask_app()
    time.sleep(5)  # Gi Flask-serveren tid til å starte
    webbrowser.open('http://127.0.0.1:5000/')  # Åpner nettleseren til Flask-applikasjonen

    try:
        proc.wait()
    except KeyboardInterrupt:
        logging.info('Process interrupted.')
        proc.terminate()
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        proc.terminate()
