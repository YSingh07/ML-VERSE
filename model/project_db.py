
from datetime import datetime, timezone

from sqlalchemy import func
from database.database import db

class MLWiki(db.Model):

    __tablename__ = "ml_wiki"

    # Primary Information
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)

    image_path = db.Column(db.String(500))

    short_description = db.Column(db.String(500))

    # Knowledge and Documentation
    about = db.Column(db.Text)
    working = db.Column(db.Text)

    # Machine Learning Information
    model = db.Column(db.String(200))
    model_details = db.Column(db.Text)

    preprocessing = db.Column(db.Text)
    training = db.Column(db.Text)
    evaluation = db.Column(db.Text)

    # Usage Information
    usage = db.Column(db.Text)
    dataset = db.Column(db.Text)
    requirements = db.Column(db.Text)

    # Saved Model
    pkl_file = db.Column(db.String(500))

    # Publishing Information
    status = db.Column(
        db.String(20),
        default="DRAFT",
        nullable=False
    )

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    last_updated = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<MLWiki {self.title}>"
