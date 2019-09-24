"""App entry point."""
from application import create_app
from config import DevConfig

app = create_app(DevConfig)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
