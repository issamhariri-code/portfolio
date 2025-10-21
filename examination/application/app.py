from flask import Flask

def routes(app):
    @app.route('/', methods=['GET'])
    def index():
        return "OK"
