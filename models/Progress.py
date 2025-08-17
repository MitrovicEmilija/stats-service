from models import db
from datetime import date

class Progress(db.Model):
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)

    weight = db.Column(db.Float, nullable=True)
    mood = db.Column(db.String(50), nullable=True)
    sleep_hours = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.isoformat(),
            "weight": self.weight,
            "mood": self.mood,
            "sleep_hours": self.sleep_hours
        }
