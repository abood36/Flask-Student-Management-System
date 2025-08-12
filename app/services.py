from .models import Student
from .extensions import db
from sqlalchemy import or_

class StudentService:
    def __init__(self, query=None):
        self.query = query or Student.query

    def create(self, data: dict) -> Student:
        s = Student(**data)
        db.session.add(s)
        db.session.commit()
        return s

    def update(self, student: Student, data: dict) -> Student:
        for k, v in data.items():
            if hasattr(student, k):
                setattr(student, k, v)
        db.session.commit()
        return student

    def delete(self, student: Student):
        db.session.delete(student)
        db.session.commit()

    def get(self, student_id: int):
        return Student.query.get(student_id)

    def search(self, q: str):
        q = f"%{q}%"
        return self.query.filter(or_(Student.first_name.ilike(q),
                                     Student.last_name.ilike(q),
                                     Student.email.ilike(q),
                                     Student.roll.ilike(q)))

    def paginate(self, page: int, per_page: int, base_query=None):
        q = base_query or self.query.order_by(Student.created_at.desc())
        return q.paginate(page=page, per_page=per_page, error_out=False)
