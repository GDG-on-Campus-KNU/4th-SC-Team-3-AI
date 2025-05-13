from fastapi import HTTPException

class GeminiException(HTTPException):
    def __init__(self, status: int, message: str):
        super().__init__(status_code=status, detail=message)
        # 상태 코드와 메시지를 초기화
        self.status = status
        self.message = message

    def __str__(self):
        # 예외 객체를 출력할 때 상태 코드와 메시지를 포함
        return f"GeminiException (status: {self.status}, message: {self.message})"