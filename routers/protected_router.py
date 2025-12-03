# Protect a route with JWT token verification
from fastapi import Security, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_utils import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = verify_token(token)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_data  # Return the decoded JWT payload


@app.get("/protected-route")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}
