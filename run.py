from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # This setup is "Industrial" because it works both on your laptop
    # and on hosting platforms like Render or Heroku.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)