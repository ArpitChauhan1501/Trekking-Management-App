from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Trek, Booking, db

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/dashboard")
@login_required
def user_dashboard():
    if current_user.role != "user":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    return render_template("user/dashboard.html")

@user_bp.route("/user/treks")
@login_required
def user_treks():
    if current_user.role != "user":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    treks = Trek.query.all()
    return render_template("user/treks.html", treks=treks)

@user_bp.route("/user/book/<int:trek_id>", methods=["POST"])
@login_required
def book_trek(trek_id):
    if current_user.role != "user":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    trek = Trek.query.get_or_404(trek_id)
    booking = Booking(user_id=current_user.id, trek_id=trek.id) # type: ignore
    db.session.add(booking)
    db.session.commit()
    flash("Trek booked successfully.", "success")
    return redirect(url_for("user.my_bookings"))

@user_bp.route("/user/bookings")
@login_required
def my_bookings():
    if current_user.role != "user":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("user/bookings.html", bookings=bookings)

@user_bp.route("/user/bookings/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    if current_user.role != "user":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash("You are not authorized to cancel this booking.", "danger")
        return redirect(url_for("user.my_bookings"))
    db.session.delete(booking)
    db.session.commit()
    flash("Booking cancelled successfully.", "success")
    return redirect(url_for("user.my_bookings"))