import database as _database
import models as _models
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import schemas as _schemas
import jwt as _jwt
import fastapi.security as _security
from fastapi import Depends, HTTPException
import datetime as _dt


MY_JWT_SECRET="testing1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2schema= _security.OAuth2PasswordBearer(tokenUrl="/api/token")



def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
    # return _database.Base.metadata.create_all(bind=_database.engine)

async def get_user_by_email(email:str, db:_orm.Session):
    
    return db.query(_models.User).filter(_models.User.email == email).first()

async def create_user(user:_schemas.UserCreate, db:_orm.Session):

    user_obj=_models.User(email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password))

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    return user_obj

from datetime import datetime, timedelta

async def create_token(user: _models.User):
    
    user_obj = _schemas.User.from_orm(user)
    # user_obj = user_obj.dict()

    expire = datetime.utcnow() + timedelta(minutes=720)
    print(expire)
    token=_jwt.encode(user_obj.dict(), MY_JWT_SECRET)
    
    return dict(access_token=token, token_type="bearer")


async def authenticate_user(email:str, password:str, db:_orm.Session):
    user = await get_user_by_email(db=db, email=email)
    
    if not user:
        return False
    
    if not user.verify_password(password):
        return False
    
    return user


async def get_current_user(db: _orm.Session = Depends(get_db), token: str=Depends(oauth2schema)):
    try:
        payload=_jwt.decode(token, MY_JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return _schemas.User.from_orm(user)


async def create_lead(user: _schemas.User, db: _orm.Session, lead: _schemas.LeadCreate):
    lead = _models.Lead(**lead.dict(), owner_id=user.id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return _schemas.Lead.from_orm(lead)

async def get_leads(user: _schemas.User, db: _orm.Session):
    leads = db.query(_models.Lead).filter_by(owner_id=user.id)
    return list(map(_schemas.Lead.from_orm, leads))


async def _lead_selector(lead_id:int, user: _schemas.User, db: _orm.Session):
    lead = db.query(_models.Lead).filter_by(owner_id=user.id).filter(_models.Lead.id==lead_id).first()
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead does not exist")
    
    return lead


async def get_lead(lead_id:int, user: _schemas.User, db: _orm.Session):
    lead = await _lead_selector(lead_id=lead_id, user=user, db=db)
    return _schemas.Lead.from_orm(lead)


async def delete_lead(lead_id:int, user: _schemas.User, db: _orm.Session):
    lead = await _lead_selector(lead_id=lead_id, user=user, db=db)
    db.delete(lead)
    db.commit()
    
    return "Ok"

async def update_lead(lead_id:int, lead:_schemas.LeadCreate, user: _schemas.User, db: _orm.Session):
    lead_db = await _lead_selector(lead_id=lead_id, user=user, db=db)
    
    lead_db.first_name= lead.first_name
    lead_db.last_name= lead.last_name
    lead_db.email= lead.email
    lead_db.company= lead.company
    lead_db.note= lead.note
    lead_db.date_last_update= _dt.datetime.utcnow()
    
    db.commit()
    db.refresh(lead_db)
    
    return _schemas.Lead.from_orm(lead_db)

