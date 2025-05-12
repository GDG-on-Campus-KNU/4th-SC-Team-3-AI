# 1. Python Slim 베이스 이미지
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 종속성 설치용 파일 복사
COPY requirements.txt .

# 4. 종속성 설치
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# 5. 프로젝트 코드 복사 (모델은 제외)
COPY ./app ./app
COPY main.py .

# 6. 모델 디렉토리는 외부 마운트 예정
VOLUME ["/ke_t5_natural_prompt2dict_model"]

# 6. 포트 오픈
EXPOSE 8000

# 7. FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
