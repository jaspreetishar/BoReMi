from subprocess import Popen


def load_jupyter_server_extension(nbapp):
    """serve the bokeh-app directory with bokeh server"""
    Popen(["bokeh", "serve", "Binder/main.py", "--allow-websocket-origin=*", "--port 8080"])
