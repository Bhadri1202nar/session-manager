import time
from datetime import timedelta
from fastapi import HTTPException,Response
def authenticate_user(username,password):
    if username=="test" and password =="test":
        return True
    return False
def get_login_time_diff(request,session_cookie_name="session"):
    if session_cookie_name in request.cookies:
        login_time=request.cookies.get(session_cookie_name)
        if login_time:
            return timedelta(seconds=int(time.time()-float(login_time)))
    return None 
def set_session_cookie(response:Response,session_cookie_name="session"):
    response.set_cookie(key=session_cookie_name,value=str(time.time()),httponly=True,samesite='lax')
    return response

def unset_session_cookie(response:Response,session_cookie_name="session"):
    response.delete_cookie(key=session_cookie_name,httponly=True,samesite='lax')
    return response
def login_required(request,session_cookie_name="session"):
    if session_cookie_name not in request.cookies:
        raise HTTPException(status_code=401,detail="Not logged in")
    

