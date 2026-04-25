from app.models.job import Job, Application
from app.models.user import User, UserIdentity
from app.models.profile import Profile
from app.core.database import SessionLocal

def clear_demo():
    db = SessionLocal()
    email = 'demo@hunteros.ai'
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Delete related applications first if cascade is not set
        db.query(Application).filter(Application.user_id == user.id).delete()
        db.query(UserIdentity).filter(UserIdentity.user_id == user.id).delete()
        db.delete(user)
    
    db.query(Profile).filter(Profile.email == email).delete()
    db.commit()
    print('Demo data cleared')
    db.close()

if __name__ == "__main__":
    clear_demo()
