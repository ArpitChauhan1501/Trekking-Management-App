from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, Trek

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
@auth_bp.route("/home")
def home():
    treks = Trek.query.limit(3).all()
    return render_template("index.html", treks=treks)

@auth_bp.route("/about")
def about():
    return render_template("about.html")

@auth_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return redirect(url_for("auth.contact"))
    return render_template("contact.html")
    
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST": 
        name = request.form.get("name").strip() #type:ignore
        email = request.form.get("email").strip().lower() #type:ignore
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")
        existing_user = User.query.filter_by(email=email).first()
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))
        if existing_user:
            flash("Email already registered.", "warning")
            return redirect(url_for("auth.register"))
        approved = True if role == "user" else False
        hashed_password = generate_password_hash(password) #type:ignore
        user = User(name=name, email=email, password=hashed_password, role=role, approved=approved, blacklisted=False, phone=phone) #type:ignore
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember")
        remember = remember is not None
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))
        if not check_password_hash(user.password, password): #type:ignore
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))
        if user.blacklisted:
            flash("Your account has been blacklisted.", "danger")
            return redirect(url_for("auth.login"))
        if not user.approved:
            flash("Your account is waiting for admin approval.", "warning")
            return redirect(url_for("auth.login"))
        login_user(user, remember=remember)
        flash(f"Welcome {user.name}!", "success")
        if user.role == "admin":
            return redirect(url_for("admin.admin_dashboard"))
        elif user.role == "staff":
            return redirect(url_for("staff.staff_dashboard"))
        else:
            return redirect(url_for("user.user_dashboard"))
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile/profile.html")

@auth_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        current_user.name = request.form.get("name", "").strip()
        current_user.phone = request.form.get("phone", "").strip()
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("auth.profile"))
    return render_template("profile/edit_profile.html")