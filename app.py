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

@app.route('/global-nutrition-info', methods=['GET'])
def get_global_nutrition_info():
    try:
        # For demo: using static food item
        query = "1lb brisket and fries"
        api_url = f"https://api.api-ninjas.com/v1/nutrition?query={query}"

        response = requests.get(api_url, headers={
            "X-Api-Key": "zP+P7AySdHgg0dHEPf105g==OUOeAMxcNSOR0CIn"
        })

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch nutrition data"}), 500

        data = response.json()

        if not data:
            return jsonify({"error": "No data received"}), 404

        item = data[0]  # Only using first result

        return jsonify({
            "name": item["name"],
            "calories": item["calories"],
            "protein": item["protein_g"],
            "carbohydrates": item["carbohydrates_total_g"],
            "fat": item["fat_total_g"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
