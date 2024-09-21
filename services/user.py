from models.user import User
from sqlalchemy.orm import Session
import bcrypt
from schema.user import UserLogin, UserUpdate


def checkUser(email, db:Session):
    try:

        userInfo = db.query(User).filter(User.email == email).first()
        if userInfo:
            return userInfo
        else: 
            return None
    except Exception as e:
        print(e)
        raise Exception(e)
    
    
# signup
def createUserDb(data, db: Session):
    try:

        userInfo = User(
            name= data.name,
            email = data.email,
            phone = data.phone,
            password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                       )
        db.add(userInfo)
        db.commit()
        db.refresh(userInfo)

        if userInfo: 
            return userInfo
        else: 
            return None
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception(e)
    

    # login

def userLoginDb(data: UserLogin, db:Session):
    try:
       
        userInfo = db.query(User).filter(User.email == data.email).first()
        print(userInfo)
        if userInfo is None:
            return None
        
        password = userInfo.password
        
        if not bcrypt.checkpw( data.password.encode("utf-8"),
            password.encode("utf-8")):
            raise Exception("Incorrect password")
       
        return userInfo
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception(e)

# update

def userUpdateDb(data:UserUpdate,id:str, db:Session):
    try:
        
        # if not data.id:
        #     raise ValueError("User ID must be provided for update")
        user = db.query(User).filter(User.id == id).first()
        
        if user is None:
            raise Exception("User not found")
      
        if data.name:
            user.name = data.name
        if data.phone:
            user.phone= data.phone
      
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception("failed to update user")
    

# delete

def deleteUserDb(id: str, db: Session):
    try:
        
        user = db.query(User).filter(User.id == id).first()

        if user:  
            db.delete(user)
            db.commit()
            return user  
        else:
            raise Exception("User  not found")

    except Exception as e:
        print(e)
        db.rollback()  
        raise Exception("Failed to delete user ")

# find user


def find_userDb(id: str, db: Session):
    try:
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise Exception("user not found")
        return user
    except Exception as e:
        print(e)
        raise Exception("Failed to find user")







