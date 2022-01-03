from typing import List
from fastapi import FastAPI, Depends, HTTPException

import fastapi.security as _security

import sqlalchemy.orm as _orm

import services as _services
import schemas as _schemas

# from services import get_db, get_user_by_email, create_user

app = FastAPI()


@app.get("/")
def hello():
    return {
        "message": "The app is running properly. Go to /docs path to access the documentation."
    }


@app.get("/api")
def root():
    return {
        "message": "The API is UP and working as expected."
    }


@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="email alread in use.")
    await _services.create_user(user, db)
    
    return await _services.create_token(user)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = Depends(),
    db: _orm.Session = Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    return await _services.create_token(user)

@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user:_schemas.User=Depends(_services.get_current_user)):
    return user


@app.post("/api/leads", response_model=_schemas.Lead)
async def create_lead(lead: _schemas.LeadCreate, 
                      user: _schemas.User = Depends(_services.get_current_user),
                      db: _orm.Session = Depends(_services.get_db)):
    
    return await _services.create_lead(user=user, db=db, lead=lead)

@app.get("/api/leads", response_model=List[_schemas.Lead])
async def get_leads(user: _schemas.User = Depends(_services.get_current_user),
                      db: _orm.Session = Depends(_services.get_db)):
    return await _services.get_leads(user=user, db=db)

@app.get("/api/leads/{lead_id}", status_code=200)
async def get_lead(lead_id: int, 
                   user: _schemas.User = Depends(_services.get_current_user), 
                   db: _orm.Session = Depends(_services.get_db)):
    return await _services.get_lead(lead_id=lead_id, user=user, db=db)

@app.delete("/api/leads/{lead_id}", status_code=204)
async def delete_lead(lead_id: int, 
                   user: _schemas.User = Depends(_services.get_current_user), 
                   db: _orm.Session = Depends(_services.get_db)):
    await _services.delete_lead(lead_id=lead_id, user=user, db=db)
    
    return {"message":"Sucessfully deleted."}

@app.put("/api/leads/{lead_id}", status_code=204)
async def update_lead(lead_id: int, 
                      lead: _schemas.LeadCreate,
                      user: _schemas.User = Depends(_services.get_current_user), 
                      db: _orm.Session = Depends(_services.get_db)):
    await _services.update_lead(lead_id=lead_id, lead=lead, user=user, db=db)
    return {"message":"Sucessfully updated."}
