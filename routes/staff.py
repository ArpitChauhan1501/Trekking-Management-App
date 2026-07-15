from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Booking, Trek

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/staff/dashboard")
@login_required
def staff_dashboard():
    if current_user.role != "staff":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    treks = Trek.query.filter_by(staff_id=current_user.id).all()
    return render_template("staff/dashboard.html", treks=treks)

@staff_bp.route("/staff/bookings")
@login_required
def staff_bookings():
    if current_user.role != "staff":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    bookings = Booking.query.join(Trek).filter(Trek.staff_id == current_user.id).all()
    return render_template("staff/bookings.html", bookings=bookings)

@staff_bp.route("/staff/treks")
@login_required
def assigned_treks():
    if current_user.role != "staff":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    treks = Trek.query.filter_by(staff_id=current_user.id).all()
    return render_template("staff/assigned_treks.html", treks=treks)