from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, desc
from models import Student, Group, Teacher, Subject, Grade

DATABASE_URL = "postgresql://some_user:some_password@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def select_1():
    session = Session()
    results = (session.query(Student.name, func.avg(Grade.grade).label('avg_grade'))
               .join(Grade, Student.id == Grade.student_id)
               .group_by(Student.id)
               .order_by(desc('avg_grade'))
               .limit(5)
               .all())
    session.close()
    return [(name, float(avg_grade)) for name, avg_grade in results]

def select_2(subject_name):
    session = Session()
    subject_id = session.query(Subject.id).filter(Subject.name == subject_name).scalar()
    if subject_id is None:
        print(f"No subject found with name: {subject_name}")
        return None

    result = (session.query(Student.name, func.avg(Grade.grade).label('avg_grade'))
              .join(Grade, Student.id == Grade.student_id)
              .filter(Grade.subject_id == subject_id)
              .group_by(Student.id)
              .order_by(desc('avg_grade'))
              .first())
    session.close()
    if result:
        return (result[0], float(result[1]))
    else:
        print(f"No data found for subject: {subject_name}")
        return None

def select_3(group_name, subject_name):
    session = Session()
    group_id = session.query(Group.id).filter(Group.name == group_name).scalar()
    subject_id = session.query(Subject.id).filter(Subject.name == subject_name).scalar()
    if group_id is None or subject_id is None:
        print(f"No group found with name: {group_name} or subject found with name: {subject_name}")
        return None

    results = (session.query(Group.name, func.avg(Grade.grade).label('avg_grade'))
               .join(Student, Student.group_id == Group.id)
               .join(Grade, Student.id == Grade.student_id)
               .filter(Grade.subject_id == subject_id, Group.id == group_id)
               .group_by(Group.id)
               .all())
    session.close()
    return [(name, float(avg_grade)) for name, avg_grade in results]

def select_4():
    session = Session()
    result = session.query(func.avg(Grade.grade)).scalar()
    session.close()
    return float(result) if result else None

def select_5(teacher_name):
    session = Session()
    teacher_id = session.query(Teacher.id).filter(Teacher.name == teacher_name).scalar()
    if teacher_id is None:
        print(f"No teacher found with name: {teacher_name}")
        return None

    results = (session.query(Subject.name)
               .filter(Subject.teacher_id == teacher_id)
               .all())
    session.close()
    return [name for name, in results]

def select_6(group_name):
    session = Session()
    group_id = session.query(Group.id).filter(Group.name == group_name).scalar()
    if group_id is None:
        print(f"No group found with name: {group_name}")
        return None

    results = (session.query(Student.name)
               .filter(Student.group_id == group_id)
               .all())
    session.close()
    return [name for name, in results]

def select_7(group_name, subject_name):
    session = Session()
    group_id = session.query(Group.id).filter(Group.name == group_name).scalar()
    subject_id = session.query(Subject.id).filter(Subject.name == subject_name).scalar()
    if group_id is None or subject_id is None:
        print(f"No group found with name: {group_name} or subject found with name: {subject_name}")
        return None

    results = (session.query(Student.name, Grade.grade)
               .join(Grade, Student.id == Grade.student_id)
               .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
               .all())
    session.close()
    return results

def select_8(teacher_name):
    session = Session()
    teacher_id = session.query(Teacher.id).filter(Teacher.name == teacher_name).scalar()
    if teacher_id is None:
        print(f"No teacher found with name: {teacher_name}")
        return None

    result = (session.query(func.avg(Grade.grade).label('avg_grade'))
               .join(Subject, Subject.id == Grade.subject_id)
               .filter(Subject.teacher_id == teacher_id)
               .scalar())
    session.close()
    return float(result) if result else None

def select_9(student_name):
    session = Session()
    student_id = session.query(Student.id).filter(Student.name == student_name).scalar()
    if student_id is None:
        print(f"No student found with name: {student_name}")
        return None

    results = (session.query(Subject.name)
               .join(Grade, Subject.id == Grade.subject_id)
               .filter(Grade.student_id == student_id)
               .group_by(Subject.id)
               .all())
    session.close()
    return [name for name, in results]

def select_10(student_name, teacher_name):
    session = Session()
    student_id = session.query(Student.id).filter(Student.name == student_name).scalar()
    teacher_id = session.query(Teacher.id).filter(Teacher.name == teacher_name).scalar()
    if student_id is None or teacher_id is None:
        print(f"No student found with name: {student_name} or teacher found with name: {teacher_name}")
        return None

    results = (session.query(Subject.name)
               .join(Grade, Subject.id == Grade.subject_id)
               .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
               .group_by(Subject.id)
               .all())
    session.close()
    return [name for name, in results]
