from bot import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets this automatically
    app.run(host="0.0.0.0", port=port)
