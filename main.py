from fastapi import FastAPI
from pydantic import BaseModel
from models.teacher import Teacher
from models.student import Student

app = FastAPI(
    title="TC-AGI",
    description="Tam Kapasite AGI - V 5.0",
    version="5.0"
)

class Query(BaseModel):
    text: str

teacher = Teacher()
student = Student()

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "5.0"}

@app.post("/chat")
def chat(query: Query):
    response = teacher.distill_to(student, query.text)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
