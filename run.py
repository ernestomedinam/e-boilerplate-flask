import os
from app_name.app import create_app

app = create_app()

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port)
