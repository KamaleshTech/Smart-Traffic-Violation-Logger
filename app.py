from datetime import datetime
from functools import wraps
import os

import qrcode
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, Violation, db


DEFAULT_OFFICER_USERNAME = "trafficadmin"
DEFAULT_OFFICER_PASSWORD = "Traffic@123"


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please sign in as an officer to continue.", "danger")
            return redirect(url_for("login", next=request.path))
        return view_function(*args, **kwargs)

    return wrapped_view


def get_violation_payload(form_data):
    vehicle_number = form_data.get("vehicle_number", "").strip().upper()
    violation_type = form_data.get("violation_type", "").strip()
    location = form_data.get("location", "").strip()
    violation_date_text = form_data.get("violation_date", "").strip()
    fine_amount_text = form_data.get("fine_amount", "").strip()

    errors = []

    if not vehicle_number:
        errors.append("Vehicle number is required.")

    if not violation_type:
        errors.append("Violation type is required.")

    if not location:
        errors.append("Location is required.")

    if not violation_date_text:
        errors.append("Violation date is required.")

    if violation_date_text:
        try:
            violation_date = datetime.strptime(
                violation_date_text, "%Y-%m-%d"
            ).date()
        except ValueError:
            errors.append("Please provide a valid date.")
            violation_date = None
    else:
        violation_date = None

    if not fine_amount_text:
        errors.append("Fine amount is required.")

    if fine_amount_text:
        try:
            fine_amount = float(fine_amount_text)

            if fine_amount < 0:
                raise ValueError

        except ValueError:
            errors.append("Fine amount must be a valid positive number.")
            fine_amount = None
    else:
        fine_amount = None

    if errors:
        return {
            "ok": False,
            "errors": errors,
            "vehicle_number": vehicle_number,
            "violation_type": violation_type,
            "location": location,
            "violation_date": violation_date,
            "fine_amount": fine_amount,
        }

    return {
        "ok": True,
        "vehicle_number": vehicle_number,
        "violation_type": violation_type,
        "location": location,
        "violation_date": violation_date,
        "fine_amount": fine_amount,
    }


def generate_violation_qr(app, violation_id):
    """
    Generate or refresh the QR code for a violation.

    The QR code points to the public verification page.
    Returns the static URL of the generated QR image.
    """
    qr_folder = os.path.join(app.static_folder, "qrcodes")
    os.makedirs(qr_folder, exist_ok=True)

    qr_filename = f"violation_{violation_id}.png"
    qr_path = os.path.join(qr_folder, qr_filename)

    public_url = url_for(
        "public_status",
        violation_id=violation_id,
        _external=True,
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )

    qr.add_data(public_url)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    qr_image.save(qr_path)

    return url_for(
        "static",
        filename=f"qrcodes/{qr_filename}",
    )


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "smart-traffic-violation-logger-secret",
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///traffic_violations.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

        if User.query.first() is None:
            default_user = User(
                username=DEFAULT_OFFICER_USERNAME,
                password_hash=generate_password_hash(
                    DEFAULT_OFFICER_PASSWORD
                ),
            )

            db.session.add(default_user)
            db.session.commit()

    @app.route("/")
    def index():
        dashboard = session.get("logged_in", False)

        if not dashboard:
            return render_template("index.html")

        total_violations = Violation.query.count()

        unpaid_violations = Violation.query.filter_by(
            status="Unpaid"
        ).count()

        paid_violations = Violation.query.filter_by(
            status="Paid"
        ).count()

        recent_violations = (
            Violation.query
            .order_by(Violation.id.desc())
            .limit(4)
            .all()
        )

        return render_template(
            "index.html",
            dashboard=True,
            total_violations=total_violations,
            unpaid_violations=unpaid_violations,
            paid_violations=paid_violations,
            recent_violations=recent_violations,
        )

    @app.route("/check-violation")
    def check_violation():
        vehicle_number = (
            request.args.get("vehicle_number", "")
            .strip()
            .upper()
        )

        violations = []
        searched = bool(vehicle_number)

        if vehicle_number:
            violations = (
                Violation.query
                .filter(
                    Violation.vehicle_number.ilike(vehicle_number)
                )
                .order_by(
                    Violation.violation_date.desc(),
                    Violation.id.desc(),
                )
                .all()
            )

        return render_template(
            "vehicle_search.html",
            vehicle_number=vehicle_number,
            violations=violations,
            searched=searched,
        )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if session.get("logged_in"):
            return redirect(url_for("index"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            next_page = request.form.get("next", "").strip()

            if not username or not password:
                flash(
                    "Username and password are required.",
                    "danger",
                )

                return render_template(
                    "login.html",
                    next_page=next_page,
                )

            user = User.query.filter_by(
                username=username
            ).first()

            if user and check_password_hash(
                user.password_hash,
                password,
            ):
                session.clear()

                session["logged_in"] = True
                session["user_id"] = user.id
                session["username"] = user.username

                if (
                    next_page
                    and next_page.startswith("/")
                    and not next_page.startswith("//")
                ):
                    return redirect(next_page)

                flash(
                    "Officer login successful.",
                    "success",
                )

                return redirect(url_for("index"))

            flash(
                "Invalid username or password.",
                "danger",
            )

        return render_template(
            "login.html",
            next_page=request.args.get("next", ""),
        )

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    @app.route("/status/<int:violation_id>")
    def public_status(violation_id):
        violation = db.get_or_404(
            Violation,
            violation_id,
        )

        # Generate the QR code for the public verification page.
        qr_image_url = generate_violation_qr(
            app,
            violation.id,
        )

        return render_template(
            "public_status.html",
            violation=violation,
            qr_image_url=qr_image_url,
        )

    @app.route(
        "/payment/<int:violation_id>",
        methods=["GET", "POST"],
    )
    def make_payment(violation_id):
        violation = db.get_or_404(
            Violation,
            violation_id,
        )

        if violation.status == "Paid":
            flash(
                "This challan is already marked as paid.",
                "success",
            )

            return redirect(
                url_for(
                    "public_status",
                    violation_id=violation.id,
                )
            )

        if request.method == "POST":
            confirmation = request.form.get(
                "payment_confirmation",
                "",
            ).strip()

            if confirmation != "confirm":
                flash(
                    "Please confirm the payment to continue.",
                    "danger",
                )

                return render_template(
                    "payment.html",
                    violation=violation,
                )

            violation.status = "Paid"

            db.session.commit()

            flash(
                "Payment confirmed successfully. "
                "This is a demo payment flow; "
                "no real money was processed.",
                "success",
            )

            return redirect(
                url_for(
                    "public_status",
                    violation_id=violation.id,
                )
            )

        return render_template(
            "payment.html",
            violation=violation,
        )

    @app.route(
        "/add-violation",
        methods=["GET", "POST"],
    )
    @login_required
    def add_violation():
        if request.method == "POST":
            payload = get_violation_payload(
                request.form
            )

            if not payload["ok"]:
                for message in payload["errors"]:
                    flash(message, "danger")

                return render_template(
                    "add_violation.html"
                )

            violation = Violation(
                vehicle_number=payload["vehicle_number"],
                violation_type=payload["violation_type"],
                location=payload["location"],
                violation_date=payload["violation_date"],
                fine_amount=payload["fine_amount"],
                status="Unpaid",
            )

            db.session.add(violation)
            db.session.commit()

            flash(
                "Violation record added successfully.",
                "success",
            )

            return redirect(
                url_for("history")
            )

        return render_template(
            "add_violation.html"
        )

    @app.route("/history")
    @login_required
    def history():
        query = Violation.query

        vehicle_number = (
            request.args.get("vehicle_number", "")
            .strip()
        )

        date_text = (
            request.args.get("date", "")
            .strip()
        )

        status = (
            request.args.get("status", "")
            .strip()
        )

        violation_type = (
            request.args.get("violation_type", "")
            .strip()
        )

        if vehicle_number:
            query = query.filter(
                Violation.vehicle_number.ilike(
                    f"%{vehicle_number}%"
                )
            )

        if date_text:
            try:
                selected_date = datetime.strptime(
                    date_text,
                    "%Y-%m-%d",
                ).date()

                query = query.filter(
                    Violation.violation_date
                    == selected_date
                )

            except ValueError:
                pass

        if status:
            query = query.filter(
                Violation.status == status
            )

        if violation_type:
            query = query.filter(
                Violation.violation_type
                == violation_type
            )

        violations = (
            query
            .order_by(Violation.id.desc())
            .all()
        )

        return render_template(
            "history.html",
            violations=violations,
        )

    @app.route(
        "/update-status/<int:violation_id>",
        methods=["POST"],
    )
    @login_required
    def update_status(violation_id):
        violation = db.get_or_404(
            Violation,
            violation_id,
        )

        violation.status = (
            "Paid"
            if violation.status == "Unpaid"
            else "Unpaid"
        )

        db.session.commit()

        flash(
            f"Violation #{violation.id} is now "
            f"{violation.status}.",
            "success",
        )

        return redirect(
            request.referrer
            or url_for("history")
        )

    @app.route(
        "/edit-violation/<int:violation_id>",
        methods=["GET", "POST"],
    )
    @login_required
    def edit_violation(violation_id):
        violation = db.get_or_404(
            Violation,
            violation_id,
        )

        if request.method == "POST":
            payload = get_violation_payload(
                request.form
            )

            if not payload["ok"]:
                for message in payload["errors"]:
                    flash(message, "danger")

                return render_template(
                    "edit_violation.html",
                    violation=violation,
                )

            violation.vehicle_number = (
                payload["vehicle_number"]
            )

            violation.violation_type = (
                payload["violation_type"]
            )

            violation.location = (
                payload["location"]
            )

            violation.violation_date = (
                payload["violation_date"]
            )

            violation.fine_amount = (
                payload["fine_amount"]
            )

            db.session.commit()

            flash(
                "Violation record updated successfully.",
                "success",
            )

            return redirect(
                url_for("history")
            )

        return render_template(
            "edit_violation.html",
            violation=violation,
        )

    @app.route(
        "/delete-violation/<int:violation_id>",
        methods=["POST"],
    )
    @login_required
    def delete_violation(violation_id):
        violation = db.get_or_404(
            Violation,
            violation_id,
        )

        db.session.delete(violation)
        db.session.commit()

        flash(
            "Violation record deleted successfully.",
            "success",
        )

        return redirect(
            url_for("history")
        )

    @app.route("/challan/<int:violation_id>")
    @login_required
    def challan(violation_id):
        violation = db.get_or_404(
            Violation,
            violation_id,
        )

        qr_image_url = generate_violation_qr(
            app,
            violation.id,
        )

        return render_template(
            "challan.html",
            violation=violation,
            qr_image_url=qr_image_url,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)