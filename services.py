# services.py
from models import db, Client, Program, Enrollment
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

class ClientService:
    @staticmethod
    def register_client(first_name, last_name, email, dob):
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        try:
            client = Client(
                first_name=first_name,
                last_name=last_name,
                email=email,
                date_of_birth=dob_date
            )
            db.session.add(client)
            db.session.commit()
            return client
        except IntegrityError as e:
            db.session.rollback()
            if 'email' in str(e).lower():
                raise ValueError("Email already registered")
            raise ValueError("Client registration failed")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError("Database error") from e

    @staticmethod
    def search_clients(search_term):
        try:
            return Client.query.filter(
                (Client.first_name.ilike(f'%{search_term}%')) |
                (Client.last_name.ilike(f'%{search_term}%')) |
                (Client.email.ilike(f'%{search_term}%'))
            ).all()
        except SQLAlchemyError as e:
            raise RuntimeError("Search failed") from e

class ProgramService:
    @staticmethod
    def create_program(name, description=""):
        try:
            program = Program(name=name, description=description)
            db.session.add(program)
            db.session.commit()
            return program
        except IntegrityError as e:
            db.session.rollback()
            if 'name' in str(e).lower():
                raise ValueError("Program name exists")
            raise ValueError("Program creation failed")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError("Database error") from e

class EnrollmentService:
    @staticmethod
    def enroll_client(client_id, program_id):
        try:
            enrollment = Enrollment(
                client_id=client_id,
                program_id=program_id
            )
            db.session.add(enrollment)
            db.session.commit()
            return enrollment
        except IntegrityError as e:
            db.session.rollback()
            if 'foreign key' in str(e).lower():
                raise ValueError("Invalid client/program ID")
            raise ValueError("Enrollment failed")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError("Database error") from e