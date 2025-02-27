from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime

main_bp = Blueprint("main_bp", __name__)

@main_bp.route("/")
def home():
    return render_template("login.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password_hash=password).first()
        if user:
            session["user_id"] = user.user_id
            session["role"] = user.role
            if user.role == "admin":
                return redirect(url_for("main_bp.admin_dashboard"))
            else:
                return redirect(url_for("main_bp.user_dashboard"))
        else:
            flash("Invalid credentials. Try again.")
    return render_template("login.html")

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        full_name = request.form.get("full_name")
        qualification = request.form.get("qualification")
        dob = request.form.get("dob")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.")
            return redirect(url_for("main_bp.register"))

        new_user = User(
            email=email,
            password_hash=password,
            full_name=full_name,
            qualification=qualification,
            dob=dob,
            role="user"
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for("main_bp.login"))
    return render_template("register.html")

@main_bp.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("main_bp.home"))
    subjects = Subject.query.all()
    return render_template("admin_dashboard.html", subjects=subjects)

@main_bp.route("/admin/add_subject", methods=["GET","POST"])
def add_subject():
    if session.get("role") != "admin":
        return redirect(url_for("main_bp.home"))
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        new_subject = Subject(name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for("main_bp.admin_dashboard"))
    return render_template("subject_form.html")

@main_bp.route("/admin/subject/<int:subject_id>/add_chapter", methods=["GET","POST"])
def add_chapter(subject_id):
    if session.get("role") != "admin":
        return redirect(url_for("main_bp.home"))
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        new_chapter = Chapter(subject_id=subject_id, name=name, description=description)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for("main_bp.admin_dashboard"))
    return render_template("chapter_form.html", subject_id=subject_id)

@main_bp.route("/admin/quiz/create/<int:chapter_id>", methods=["GET","POST"])
def create_quiz(chapter_id):
    if session.get("role") != "admin":
        return redirect(url_for("main_bp.home"))
    if request.method == "POST":
        date_str = request.form.get("date")
        duration = request.form.get("duration")
        date_dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M') if date_str else datetime.utcnow()
        new_quiz = Quiz(chapter_id=chapter_id, date=date_dt, duration=int(duration))
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for("main_bp.admin_dashboard"))
    return render_template("quiz_form.html", chapter_id=chapter_id)

@main_bp.route("/admin/quiz/<int:quiz_id>/add_question", methods=["GET","POST"])
def add_question(quiz_id):
    if session.get("role") != "admin":
        return redirect(url_for("main_bp.home"))
    if request.method == "POST":
        question_text = request.form.get("question_text")
        option_1 = request.form.get("option_1")
        option_2 = request.form.get("option_2")
        option_3 = request.form.get("option_3")
        option_4 = request.form.get("option_4")
        correct_option = request.form.get("correct_option")

        new_question = Question(
            quiz_id=quiz_id,
            question_text=question_text,
            option_1=option_1,
            option_2=option_2,
            option_3=option_3,
            option_4=option_4,
            correct_option=int(correct_option)
        )
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for("main_bp.admin_dashboard"))
    return render_template("question_form.html", quiz_id=quiz_id)

@main_bp.route("/user/dashboard")
def user_dashboard():
    if session.get("role") != "user":
        return redirect(url_for("main_bp.home"))
    quizzes = Quiz.query.all()
    return render_template("user_dashboard.html", quizzes=quizzes)

@main_bp.route("/quiz/attempt/<int:quiz_id>", methods=["GET","POST"])
def quiz_attempt(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    if request.method == "POST":
        correct_count = 0
        for q in questions:
            answer = request.form.get(f"question_{q.question_id}")
            if answer and int(answer) == q.correct_option:
                correct_count += 1
        new_score = Score(
            user_id=session["user_id"],
            quiz_id=quiz_id,
            total_questions=len(questions),
            correct_answers=correct_count,
            score=correct_count
        )
        db.session.add(new_score)
        db.session.commit()
        flash(f"You scored {correct_count} out of {len(questions)}.")
        return redirect(url_for("main_bp.user_dashboard"))
    return render_template("quiz_attempt.html", quiz=quiz, questions=questions)