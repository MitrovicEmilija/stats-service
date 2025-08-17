import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from graphene import ObjectType, String, Float, Int, List, Schema
from flask_graphql import GraphQLView

from config import Config

app = Flask(__name__)
CORS(app, origins=["http://localhost:3006"], supports_credentials=True)
app.config.from_object(Config)
app.config["JWT_ALGORITHM"] = "HS512"
print("🔑 Loaded JWT_SECRET_KEY:", app.config["JWT_SECRET_KEY"])
print("🔒 Flask JWT secret:", repr(app.config["JWT_SECRET_KEY"]))

# GraphQL type
class ExerciseType(ObjectType):
    name = String()
    calories_per_hour = Float()
    duration_minutes = Int()
    total_calories = Float()
    
# Query class
class Query(ObjectType):
    top_exercises = List(ExerciseType, activity=String(default_value="skiing"))

    @staticmethod
    def resolve_top_exercises(self, info, activity):
        try:
            url = f"https://api.api-ninjas.com/v1/caloriesburned?activity={activity}"
            response = requests.get(url, headers={"X-Api-Key": "zP+P7AySdHgg0dHEPf105g==OUOeAMxcNSOR0CIn"})
            data = response.json()
            return [
                {
                    "name": item["name"],
                    "calories_per_hour": item["calories_per_hour"],
                    "duration_minutes": item["duration_minutes"],
                    "total_calories": item["total_calories"]
                }
                for item in data[:3]
            ]
        except Exception as e:
            print("❌ Error:", e)
            return []

schema = Schema(query=Query)

# GraphQL route
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

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
