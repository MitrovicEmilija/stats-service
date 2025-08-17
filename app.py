import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config

app = Flask(__name__)
CORS(app, origins=["http://localhost:3006"], supports_credentials=True)
app.config.from_object(Config)
app.config["JWT_ALGORITHM"] = "HS512"
print("🔑 Loaded JWT_SECRET_KEY:", app.config["JWT_SECRET_KEY"])
print("🔒 Flask JWT secret:", repr(app.config["JWT_SECRET_KEY"]))

#db.init_app(app)

@app.route('/global-exercise-info', methods=['GET'])
def get_global_nutrition_info():
    try:
        activity = "skiing"
        api_url = f"https://api.api-ninjas.com/v1/caloriesburned?activity={activity}"

        response = requests.get(api_url, headers={
            "X-Api-Key": "zP+P7AySdHgg0dHEPf105g==OUOeAMxcNSOR0CIn"
        })

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch nutrition data"}), 500

        data = response.json()
        if not data:
            return jsonify({"error": "No data received"}), 404

        top_results = data[:3]

        return jsonify([
            {
                "name": item["name"],
                "calories_per_hour": item["calories_per_hour"],
                "duration_minutes": item["duration_minutes"],
                "total_calories": item["total_calories"]
            }
            for item in top_results
        ])

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
