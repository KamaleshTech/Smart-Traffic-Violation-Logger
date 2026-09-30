from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


class Violation(db.Model):
    __tablename__ = "violations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    vehicle_number = db.Column(
        db.String(20),
        nullable=False
    )

    violation_type = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(200),
        nullable=False
    )

    violation_date = db.Column(
        db.Date,
        nullable=False
    )

    fine_amount = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Unpaid"
    )

    def __repr__(self):
        return (
            f"<Violation {self.id} "
            f"{self.vehicle_number}>"
        )