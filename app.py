import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from ariadne import QueryType, graphql_sync, make_executable_schema
from ariadne.explorer import ExplorerGraphiQL

from config import Config

app = Flask(__name__)
CORS(app, origins=["http://localhost:3006"], supports_credentials=True)
app.config.from_object(Config)
app.config["JWT_ALGORITHM"] = "HS512"
print("🔑 Loaded JWT_SECRET_KEY:", app.config["JWT_SECRET_KEY"])
print("🔒 Flask JWT secret:", repr(app.config["JWT_SECRET_KEY"]))

# --- Ariadne GraphQL type definitions ---
type_defs = """
    type Exercise {
        name: String!
        calories_per_hour: Float!
        duration_minutes: Int!
        total_calories: Float!
    }

    type Query {
        topExercises(activity: String!): [Exercise!]!
    }
"""

query = QueryType()

@query.field("topExercises")
def resolve_top_exercises(_, info, activity):
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

schema = make_executable_schema(type_defs, query)

# --- GraphQL playground (GET) ---
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return ExplorerGraphiQL().html(None), 200

# --- GraphQL query execution (POST) ---
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    return jsonify(result)

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
