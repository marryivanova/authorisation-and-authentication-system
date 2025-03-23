from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models import Base, User

engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def test_create_user_with_unique_username_and_email():
    session = SessionLocal()
    user = User(
        username="uniqueuser",
        email="uniqueuser@example.com",
        hashed_password="hashedpassword123",
    )

    session.add(user)
    session.commit()

    retrieved_user = session.query(User).filter_by(username="uniqueuser").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "uniqueuser"
    assert retrieved_user.email == "uniqueuser@example.com"
    session.close()


def test_user_creation_with_duplicate_email():
    session = SessionLocal()
    user1 = User(
        username="user1", email="test@example.com", hashed_password="hashed_password1"
    )
    user2 = User(
        username="user2", email="test@example.com", hashed_password="hashed_password2"
    )

    session.add(user1)
    session.commit()

    try:
        session.add(user2)
        session.commit()
    except Exception as e:
        session.rollback()
        assert "UNIQUE constraint failed" in str(e)
    finally:
        session.close()
