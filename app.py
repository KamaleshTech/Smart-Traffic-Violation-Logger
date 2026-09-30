from datetime import datetime
from functools import wraps
import os

import qrcode

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from models import db, User, Violation


# =========================================================
# AUTHENTICATION
# =========================================================

def login_required(view_function):

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if not session.get("logged_in"):

            flash(
                "Please sign in as an officer to continue.",
                "danger"
            )

            return redirect(
                url_for(
                    "login",
                    next=request.path
                )
            )

        return view_function(*args, **kwargs)

    return wrapped_view


# =========================================================
# APP FACTORY
# =========================================================

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "smart-traffic-violation-logger-secret"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///traffic_violations.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)


    # =====================================================
    # DATABASE
    # =====================================================

    with app.app_context():

        db.create_all()

        if User.query.first() is None:

            default_user = User(
                username="trafficadmin",
                password_hash=generate_password_hash(
                    "Traffic@123"
                ),
            )

            db.session.add(default_user)
            db.session.commit()


    # =====================================================
    # HOME
    # PUBLIC
    # =====================================================

    @app.route("/")
    def index():

        return render_template(
            "index.html"
        )


    # =====================================================
    # LOGIN
    # PUBLIC
    # =====================================================

    @app.route(
        "/login",
        methods=["GET", "POST"]
    )
    def login():

        if session.get("logged_in"):

            return redirect(
                url_for("index")
            )


        if request.method == "POST":

            username = request.form.get(
                "username",
                ""
            ).strip()

            password = request.form.get(
                "password",
                ""
            )

            next_page = request.form.get(
                "next",
                ""
            ).strip()


            if not username or not password:

                flash(
                    "Username and password are required.",
                    "danger"
                )

                return render_template(
                    "login.html",
                    next_page=next_page
                )


            user = User.query.filter_by(
                username=username
            ).first()


            if user and check_password_hash(
                user.password_hash,
                password
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
                    "success"
                )

                return redirect(
                    url_for("index")
                )


            flash(
                "Invalid username or password.",
                "danger"
            )


        return render_template(
            "login.html",
            next_page=request.args.get(
                "next",
                ""
            )
        )


    # =====================================================
    # LOGOUT
    # =====================================================

    @app.route("/logout")
    def logout():

        session.clear()

        return redirect(
            url_for("index")
        )


    # =====================================================
    # ADD VIOLATION
    # PROTECTED
    # =====================================================

    @app.route(
        "/add-violation",
        methods=["GET", "POST"]
    )
    @login_required
    def add_violation():

        if request.method == "POST":

            vehicle_number = request.form.get(
                "vehicle_number",
                ""
            ).strip().upper()

            violation_type = request.form.get(
                "violation_type",
                ""
            ).strip()

            location = request.form.get(
                "location",
                ""
            ).strip()

            violation_date_text = request.form.get(
                "violation_date",
                ""
            ).strip()

            fine_amount_text = request.form.get(
                "fine_amount",
                ""
            ).strip()


            if not vehicle_number:
                flash(
                    "Vehicle number is required.",
                    "danger"
                )
                return render_template(
                    "add_violation.html"
                )


            if not violation_type:
                flash(
                    "Violation type is required.",
                    "danger"
                )
                return render_template(
                    "add_violation.html"
                )


            if not location:
                flash(
                    "Location is required.",
                    "danger"
                )
                return render_template(
                    "add_violation.html"
                )


            try:

                violation_date = datetime.strptime(
                    violation_date_text,
                    "%Y-%m-%d"
                ).date()

            except ValueError:

                flash(
                    "Please provide a valid date.",
                    "danger"
                )

                return render_template(
                    "add_violation.html"
                )


            try:

                fine_amount = float(
                    fine_amount_text
                )

                if fine_amount < 0:
                    raise ValueError

            except ValueError:

                flash(
                    "Fine amount must be a valid positive number.",
                    "danger"
                )

                return render_template(
                    "add_violation.html"
                )


            violation = Violation(
                vehicle_number=vehicle_number,
                violation_type=violation_type,
                location=location,
                violation_date=violation_date,
                fine_amount=fine_amount,
                status="Unpaid",
            )


            db.session.add(violation)
            db.session.commit()


            flash(
                "Violation record added successfully.",
                "success"
            )

            return redirect(
                url_for("history")
            )


        return render_template(
            "add_violation.html"
        )


    # =====================================================
    # HISTORY
    # PROTECTED
    # =====================================================

    @app.route("/history")
    @login_required
    def history():

        query = Violation.query


        vehicle_number = request.args.get(
            "vehicle_number",
            ""
        ).strip()

        date_text = request.args.get(
            "date",
            ""
        ).strip()

        status = request.args.get(
            "status",
            ""
        ).strip()

        violation_type = request.args.get(
            "violation_type",
            ""
        ).strip()


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
                    "%Y-%m-%d"
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


        violations = query.order_by(
            Violation.id.desc()
        ).all()


        return render_template(
            "history.html",
            violations=violations
        )


    # =====================================================
    # UPDATE STATUS
    # PROTECTED
    # =====================================================

    @app.route(
        "/update-status/<int:violation_id>",
        methods=["POST"]
    )
    @login_required
    def update_status(violation_id):

        violation = db.get_or_404(
            Violation,
            violation_id
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
            "success"
        )


        return redirect(
            request.referrer
            or url_for("history")
        )


    # =====================================================
    # EDIT
    # PROTECTED
    # =====================================================

    @app.route(
        "/edit-violation/<int:violation_id>",
        methods=["GET", "POST"]
    )
    @login_required
    def edit_violation(violation_id):

        violation = db.get_or_404(
            Violation,
            violation_id
        )


        if request.method == "POST":

            vehicle_number = request.form.get(
                "vehicle_number",
                ""
            ).strip().upper()

            violation_type = request.form.get(
                "violation_type",
                ""
            ).strip()

            location = request.form.get(
                "location",
                ""
            ).strip()

            violation_date_text = request.form.get(
                "violation_date",
                ""
            ).strip()

            fine_amount_text = request.form.get(
                "fine_amount",
                ""
            ).strip()


            if not vehicle_number:
                flash(
                    "Vehicle number is required.",
                    "danger"
                )

                return render_template(
                    "edit_violation.html",
                    violation=violation
                )


            if not violation_type:
                flash(
                    "Violation type is required.",
                    "danger"
                )

                return render_template(
                    "edit_violation.html",
                    violation=violation
                )


            if not location:
                flash(
                    "Location is required.",
                    "danger"
                )

                return render_template(
                    "edit_violation.html",
                    violation=violation
                )


            try:

                violation_date = datetime.strptime(
                    violation_date_text,
                    "%Y-%m-%d"
                ).date()

            except ValueError:

                flash(
                    "Please provide a valid date.",
                    "danger"
                )

                return render_template(
                    "edit_violation.html",
                    violation=violation
                )


            try:

                fine_amount = float(
                    fine_amount_text
                )

                if fine_amount < 0:
                    raise ValueError

            except ValueError:

                flash(
                    "Fine amount must be a valid positive number.",
                    "danger"
                )

                return render_template(
                    "edit_violation.html",
                    violation=violation
                )


            violation.vehicle_number = vehicle_number
            violation.violation_type = violation_type
            violation.location = location
            violation.violation_date = violation_date
            violation.fine_amount = fine_amount


            db.session.commit()


            flash(
                "Violation record updated successfully.",
                "success"
            )


            return redirect(
                url_for("history")
            )


        return render_template(
            "edit_violation.html",
            violation=violation
        )


    # =====================================================
    # DELETE
    # PROTECTED
    # =====================================================

    @app.route(
        "/delete-violation/<int:violation_id>",
        methods=["POST"]
    )
    @login_required
    def delete_violation(violation_id):

        violation = db.get_or_404(
            Violation,
            violation_id
        )


        db.session.delete(violation)

        db.session.commit()


        flash(
            "Violation record deleted successfully.",
            "success"
        )


        return redirect(
            url_for("history")
        )


    # =====================================================
    # DIGITAL CHALLAN
    # PROTECTED
    # =====================================================

    @app.route(
        "/challan/<int:violation_id>"
    )
    @login_required
    def challan(violation_id):

        violation = db.get_or_404(
            Violation,
            violation_id
        )


        qr_folder = os.path.join(
            app.static_folder,
            "qrcodes"
        )

        os.makedirs(
            qr_folder,
            exist_ok=True
        )


        qr_filename = (
            f"violation_{violation.id}.png"
        )

        qr_path = os.path.join(
            qr_folder,
            qr_filename
        )


        public_url = url_for(
            "public_status",
            violation_id=violation.id,
            _external=True
        )


        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )

        qr.add_data(public_url)
        qr.make(fit=True)


        qr_image = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        qr_image.save(qr_path)


        qr_image_url = url_for(
            "static",
            filename=f"qrcodes/{qr_filename}"
        )


        return render_template(
            "challan.html",
            violation=violation,
            qr_image_url=qr_image_url
        )


    # =====================================================
    # PUBLIC STATUS
    # NO LOGIN
    # =====================================================

    @app.route(
        "/status/<int:violation_id>"
    )
    def public_status(violation_id):

        violation = db.get_or_404(
            Violation,
            violation_id
        )


        return render_template(
            "public_status.html",
            violation=violation
        )


    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        debug=True
    )