from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from models import db, Progress
from sqlalchemy import func

app = Flask(__name__)
CORS(app, origins=["http://localhost:3006"], supports_credentials=True)
app.config.from_object(Config)
app.config["JWT_ALGORITHM"] = "HS512"
print("🔑 Loaded JWT_SECRET_KEY:", app.config["JWT_SECRET_KEY"])
print("🔒 Flask JWT secret:", repr(app.config["JWT_SECRET_KEY"]))

db.init_app(app)

@app.route('/stats/<int:user_id>', methods=['GET'])
def get_stats(user_id):
    avg_weight = db.session.query(func.avg(Progress.Progress.weight)).scalar() \
        .filter(Progress.Progress.user_id == user_id, Progress.Progress.weight is not None).scalar()

    avg_sleep = db.session.query(func.avg(Progress.Progress.sleep_hours)) \
        .filter(Progress.Progress.user_id == user_id, Progress.Progress.sleep_hours is not None).scalar()

    stats = {
        "userId": user_id,
        "average_weight": round(avg_weight, 2) if avg_weight else None,
        "average_sleep": round(avg_sleep, 2) if avg_sleep else None
    }
    return jsonify(stats)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
