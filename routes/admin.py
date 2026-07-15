from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Trek, Booking, User
from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    return render_template("admin/dashboard.html")

@admin_bp.route("/admin/treks")
@login_required
def admin_treks():
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    treks = Trek.query.all()
    return render_template("admin/treks.html",treks=treks)

@admin_bp.route("/admin/treks/add", methods=["GET", "POST"])
@login_required
def add_trek():
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        difficulty = request.form.get("difficulty", "")
        duration = int(request.form.get("duration", 0))
        price = float(request.form.get("price", 0))
        max_participants = int(request.form.get("max_participants", 0))
        description = request.form.get("description", "").strip()
        image = request.files.get("image")
        image_filename = None
        staff_id = request.form.get("staff_id")
        staff_id = int(staff_id) if staff_id else None
        if image and image.filename:
            image_filename = secure_filename(image.filename)
            os.makedirs("static/uploads", exist_ok=True)
            image.save(os.path.join("static", "uploads", image_filename))
        trek = Trek(name=name,location=location,difficulty=difficulty,duration=duration,price=price,max_participants=max_participants,description=description,image=image_filename, staff_id = staff_id) #type: ignore
        db.session.add(trek)
        db.session.commit()
        flash("Trek added successfully.", "success")
        return redirect(url_for("admin.admin_treks"))
    staff = User.query.filter_by(role="staff", approved=True, blacklisted=False).all()
    return render_template("admin/add_trek.html", staff = staff)

@admin_bp.route("/admin/treks/edit/<int:trek_id>", methods=["GET", "POST"])
@login_required
def edit_trek(trek_id):
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    trek = Trek.query.get_or_404(trek_id)
    if request.method == "POST":
        trek.name = request.form.get("name", "").strip()
        trek.location = request.form.get("location", "").strip()
        trek.difficulty = request.form.get("difficulty", "")
        trek.duration = int(request.form.get("duration", 0))
        trek.price = float(request.form.get("price", 0))
        trek.max_participants = int(request.form.get("max_participants", 0))
        trek.description = request.form.get("description", "").strip()
        staff_id = request.form.get("staff_id")
        trek.staff_id = int(staff_id) if staff_id else None
        image = request.files.get("image")
        if image and image.filename:
            image_filename = secure_filename(image.filename)
            os.makedirs("static/uploads", exist_ok=True)
            image.save(os.path.join("static", "uploads", image_filename))
            trek.image = image_filename
        db.session.commit()
        flash("Trek updated successfully.", "success")
        return redirect(url_for("admin.admin_treks"))
    staff = User.query.filter_by(role="staff", approved=True, blacklisted=False).all()
    return render_template("admin/edit_trek.html", trek=trek, staff=staff)

@admin_bp.route("/admin/treks/delete/<int:trek_id>", methods=["POST"])
@login_required
def delete_trek(trek_id):
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    trek = Trek.query.get_or_404(trek_id)
    bookings = Booking.query.filter_by(trek_id=trek.id).all()
    for booking in bookings:
        db.session.delete(booking)
    db.session.delete(trek)
    db.session.commit()
    flash("Trek deleted successfully.", "success")
    return redirect(url_for("admin.admin_treks"))
    
@admin_bp.route("/admin/bookings")
@login_required
def admin_bookings():
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    bookings = Booking.query.all()
    return render_template("admin/bookings.html", bookings=bookings)

@admin_bp.route("/admin/users")
@login_required
def admin_users():
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    users = User.query.filter_by(role="user").all()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/admin/staff")
@login_required
def admin_staff():
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    staff = User.query.filter_by(role="staff").all()
    return render_template("admin/staff.html", staff=staff)

@admin_bp.route("/admin/staff/approve/<int:user_id>", methods=["POST"])
@login_required
def approve_user(user_id):
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    user = User.query.get_or_404(user_id)
    if user.role != "staff":
        flash("Only staff members can be approved.", "warning")
        return redirect(url_for("admin.admin_staff"))
    user.approved = True
    db.session.commit()
    flash("Staff approved successfully.", "success")
    return redirect(url_for("admin.admin_staff"))

@admin_bp.route("/admin/users/blacklist/<int:user_id>", methods=["POST"])
@login_required
def blacklist_user(user_id):
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    user = User.query.get_or_404(user_id)
    user.blacklisted = True
    db.session.commit()
    flash("User blacklisted successfully.", "success")
    if user.role == "staff":
        return redirect(url_for("admin.admin_staff"))
    return redirect(url_for("admin.admin_users"))

@admin_bp.route("/admin/users/unblacklist/<int:user_id>", methods=["POST"])
@login_required
def unblacklist_user(user_id):
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.home"))
    user = User.query.get_or_404(user_id)
    user.blacklisted = False
    db.session.commit()
    flash("User unblacklisted successfully.", "success")
    if user.role == "staff":
        return redirect(url_for("admin.admin_staff"))
    return redirect(url_for("admin.admin_users"))