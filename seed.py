from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Teacher, Subject, Grade
from faker import Faker
import random
from datetime import datetime

# Database connection URL
DATABASE_URL = "postgresql://some_user:some_password@localhost:5432/postgres"

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize Faker
fake = Faker()

# Clear existing data
session.query(Grade).delete()
session.query(Student).delete()
session.query(Subject).delete()
session.query(Teacher).delete()
session.query(Group).delete()
session.commit()

# Create groups
groups = [Group(name=fake.word()) for _ in range(3)]
session.add_all(groups)
session.commit()

# Create teachers
teachers = [Teacher(name=fake.name()) for _ in range(3, 6)]
session.add_all(teachers)
session.commit()

# Create subjects
subject_names = [
    'Mathematics',
    'Physics',
    'Chemistry',
    'Biology',
    'History',
    'Geography',
    'Literature',
    'Computer Science'
]

subjects = [Subject(name=name, teacher_id=random.choice(teachers).id) for name in subject_names]
session.add_all(subjects)
session.commit()

# Create students
students = [Student(name=fake.name(), group_id=random.choice(groups).id) for _ in range(30, 50)]
session.add_all(students)
session.commit()

# Create grades for students
grades = []
for student in students:
    for _ in range(20):
        subject = random.choice(subjects)
        grade = Grade(
            student_id=student.id,
            subject_id=subject.id,
            grade=random.randint(1, 10),
            date_received=fake.date_between(start_date='-1y', end_date='today')
        )
        grades.append(grade)

session.add_all(grades)
session.commit()

# Close session
session.close()
print("Database seeded successfully!")