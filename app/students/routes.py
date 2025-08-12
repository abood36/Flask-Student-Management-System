from flask import render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from . import students
from .forms import StudentForm, DeleteForm
from ..services import StudentService
from ..models import Student
from ..extensions import db
import io, csv

@students.route("/students")
def list_students():
    q = request.args.get("q", "").strip()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", current_app.config.get("STUDENTS_PER_PAGE", 8)))
    service = StudentService()

    if q:
        base_q = service.search(q).order_by(Student.created_at.desc())
    else:
        base_q = Student.query.order_by(Student.created_at.desc())

    pagination = service.paginate(page=page, per_page=per_page, base_query=base_q)
    return render_template("students/list.html", students=pagination.items, pagination=pagination, q=q)

@students.route("/students/<int:student_id>")
def student_detail(student_id):
    s = Student.query.get_or_404(student_id)
    delete_form = DeleteForm()
    return render_template("students/detail.html", student=s, delete_form=delete_form)

@students.route("/students/create", methods=["GET", "POST"])
@login_required
def create_student():
    form = StudentForm()
    if form.validate_on_submit():
        data = {
            "first_name": form.first_name.data.strip(),
            "last_name": form.last_name.data.strip() if form.last_name.data else None,
            "email": form.email.data.strip() if form.email.data else None,
            "roll": form.roll.data.strip() if form.roll.data else None,
            "notes": form.notes.data.strip() if form.notes.data else None
        }
        service = StudentService()
        try:
            s = service.create(data)
            flash("Student created.", "success")
            return redirect(url_for("students.student_detail", student_id=s.id))
        except Exception as e:
            db.session.rollback()
            flash("Error creating student: " + str(e), "danger")
    return render_template("students/form.html", form=form, action="Create")

@students.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    s = Student.query.get_or_404(student_id)
    form = StudentForm(obj=s)
    if form.validate_on_submit():
        data = {
            "first_name": form.first_name.data.strip(),
            "last_name": form.last_name.data.strip() if form.last_name.data else None,
            "email": form.email.data.strip() if form.email.data else None,
            "roll": form.roll.data.strip() if form.roll.data else None,
            "notes": form.notes.data.strip() if form.notes.data else None
        }
        service = StudentService()
        try:
            service.update(s, data)
            flash("Student updated.", "success")
            return redirect(url_for("students.student_detail", student_id=s.id))
        except Exception as e:
            db.session.rollback()
            flash("Error updating student: " + str(e), "danger")
    return render_template("students/form.html", form=form, action="Edit")

@students.route("/students/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_student(student_id):
    s = Student.query.get_or_404(student_id)
    form = DeleteForm()
    if form.validate_on_submit():
        service = StudentService()
        service.delete(s)
        flash("Student deleted.", "warning")
        return redirect(url_for("students.list_students"))
    flash("Invalid request.", "danger")
    return redirect(url_for("students.student_detail", student_id=student_id))

@students.route("/students/export")
@login_required
def export_csv():
    # export current filtered list (basic)
    q = request.args.get("q", "").strip()
    service = StudentService()
    base_q = service.search(q).order_by(Student.created_at.desc()) if q else Student.query.order_by(Student.created_at.desc())
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(["id","first_name","last_name","email","roll","created_at"])
    for s in base_q.all():
        writer.writerow([s.id, s.first_name, s.last_name or "", s.email or "", s.roll or "", s.created_at.isoformat()])
    output = io.BytesIO()
    output.write(si.getvalue().encode("utf-8"))
    output.seek(0)
    return send_file(output, mimetype="text/csv", download_name="students.csv", as_attachment=True)
