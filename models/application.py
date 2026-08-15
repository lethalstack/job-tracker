from extensions import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100))

    status = db.Column(db.String(50), nullable=False)

    applied_date = db.Column(db.String(20))

    job_url = db.Column(db.String(300))

    notes = db.Column(db.Text)

    # Links this application to the user who owns it.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)