from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from extensions import db
from models.application import Application


application_bp = Blueprint(
    "applications",
    __name__
)


# READ - Show a small preview of recent applications on the dashboard
@application_bp.route("/")
@login_required
def dashboard():

    all_applications = Application.query.filter_by(user_id=current_user.id).all()

    recent_applications = (
        Application.query
        .filter_by(user_id=current_user.id)
        .order_by(Application.id.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        applications=all_applications,
        recent_applications=recent_applications
    )


# READ - Show the full list of applications, with optional search/filter
@application_bp.route("/applications")
@login_required
def all_applications():

    query = Application.query.filter_by(user_id=current_user.id)

    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "")

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            (Application.company.ilike(like_pattern)) |
            (Application.role.ilike(like_pattern))
        )

    if status_filter:
        query = query.filter_by(status=status_filter)

    applications = query.order_by(Application.id.desc()).all()

    return render_template(
        "applications.html",
        applications=applications,
        search=search,
        status_filter=status_filter
    )


# CREATE - Add application page
@application_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_application():

    if request.method == "POST":

        application = Application(

            company=request.form["company"],

            role=request.form["role"],

            location=request.form["location"],

            status=request.form["status"],

            applied_date=request.form["applied_date"],

            job_url=request.form["job_url"],

            notes=request.form["notes"],

            user_id=current_user.id

        )


        db.session.add(application)

        db.session.commit()


        return redirect(url_for("applications.dashboard"))


    return render_template("add_application.html")



# UPDATE - Edit application
@application_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_application(id):

    application = Application.query.get_or_404(id)

    # Prevent one user from editing another user's application
    # by guessing IDs in the URL.
    if application.user_id != current_user.id:
        abort(403)


    if request.method == "POST":

        application.company = request.form["company"]

        application.role = request.form["role"]

        application.location = request.form["location"]

        application.status = request.form["status"]

        application.applied_date = request.form["applied_date"]

        application.job_url = request.form["job_url"]

        application.notes = request.form["notes"]


        db.session.commit()


        return redirect(url_for("applications.dashboard"))


    return render_template(
        "edit_application.html",
        application=application
    )



# DELETE - Delete application
@application_bp.route("/delete/<int:id>")
@login_required
def delete_application(id):

    application = Application.query.get_or_404(id)

    if application.user_id != current_user.id:
        abort(403)


    db.session.delete(application)

    db.session.commit()


    return redirect(url_for("applications.dashboard"))