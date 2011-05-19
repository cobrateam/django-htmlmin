import os
import subprocess
from urllib import urlopen

TESTS_DIR = os.path.dirname(__file__)
MAKE_PATH = os.path.abspath(os.path.join(TESTS_DIR, '..', '..'))

class Server(object):

    url = "http://localhost:8000/raw"

    def run(self):
        output = open('/dev/null', 'w')
        cwd = os.getcwd()
        os.chdir(MAKE_PATH)
        subprocess.Popen(['make', 'pico_django'], stdout=output, stderr=output)
        self.wait_until_start()
        os.chdir(cwd)
        output.close()

    def stop(self):
        output = open('/dev/null', 'w')
        cwd = os.getcwd()
        os.chdir(MAKE_PATH)
        subprocess.Popen(['make', 'kill_pico_django'], stdout=output, stderr=output)
        self.wait_until_stop()
        os.chdir(cwd)
        output.close()

    def wait_until_start(self):
        while True:
            try:
                urlopen(self.url)
                break
            except IOError:
                pass

    def wait_until_stop(self):
        while True:
            try:
                response = urlopen(self.url)
                if response.code == 404:
                    break
            except IOError:
                break

server = Server()

def setup():
    server.run()

def teardown():
    server.stop()
