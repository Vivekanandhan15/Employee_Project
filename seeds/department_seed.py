# seeds/department_seed.py

from sqlalchemy.orm import Session

from models.department import Department


def seed_departments(db: Session):

    predefined_departments = [
        "HR",
        "Engineering"
    ]

    for dept_name in predefined_departments:

        existing_department = (
            db.query(Department)
            .filter(Department.dept_name == dept_name)
            .first()
        )

        if not existing_department:

            department = Department(
                dept_name=dept_name
            )

            db.add(department)

    db.commit()
    