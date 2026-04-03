from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Check if we are running on a cloud server or locally
    is_prod = os.environ.get("FLASK_ENV") == "production"
    
    port = int(os.environ.get("PORT", 5000))
    
    # Debug is only for your Hyderabad local dev environment
    app.run(
        host="0.0.0.0", 
        port=port, 
        debug=not is_prod
    )