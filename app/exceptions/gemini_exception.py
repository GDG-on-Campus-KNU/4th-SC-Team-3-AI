class GeminiException(Exception):
    def __init__(self, status: int, message: str):
        # 상태 코드와 메시지를 초기화
        self.status = status
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        # 예외 객체를 출력할 때 상태 코드와 메시지를 포함
        return f"GeminiException (status: {self.status}, message: {self.message})"