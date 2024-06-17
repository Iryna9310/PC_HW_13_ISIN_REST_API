from sqlalchemy.orm import Session
from app import models, schemas, utils

# Функції для роботи з користувачами
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not utils.verify_password(password, user.hashed_password):
        return None
    return user

def verify_user_email(db: Session, email: str):
    user = get_user_by_email(db, email)
    if user:
        user.is_verified = True
        db.commit()
        db.refresh(user)
    return user

def update_user_avatar(db: Session, user_id: int, avatar_url: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.avatar_url = avatar_url
        db.commit()
        db.refresh(user)
    return user

# Функції для роботи з контактами
def create_contact(db: Session, contact: schemas.ContactCreate, user_id: int):
    db_contact = models.Contact(**contact.dict(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10, search: str = None, user_id: int = None):
    query = db.query(models.Contact).filter(models.Contact.owner_id == user_id)
    if search:
        query = query.filter(models.Contact.name.ilike(f"%{search}%") | models.Contact.email.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int, user_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == user_id).first()

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate, user_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == user_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, user_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == user_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


