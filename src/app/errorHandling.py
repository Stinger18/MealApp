from fastapi import HTTPException

class EmailAlreadyExists(HTTPException):
    def __init__(self, email: str):
        super().__init__(status_code=400, detail=f'Error: Email {email} already exists')