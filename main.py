from agent.profile_generation.profile_generation import profile_generation
from agent.document_interpret.interpret import file_interpret
from agent.commentator.comment_create import comment_create
from agent.review.content_review import content_review
from service.tool import clean_result
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

class UserInput(BaseModel):
    ID:str
    content:str
    profile:str
    information:str
    file_path:str

@app.post("/commentator")
def commentator(user:UserInput):
    result = comment_create(user.content,user.profile,user.information)
    commentator_result={
        "ID":user.ID,
        "comment":result
    }
    return commentator_result

@app.post("/profile_generation")
def profile_create(user:UserInput):
    result = profile_generation(user.content,user.profile,user.information)
    result = clean_result(result)
    profile_result={
        "ID": user.ID,
        "profile": result
    }
    return profile_result

@app.post("/review")
def review_content(user:UserInput):
    result = content_review(user.content,user.profile,user.information)
    review_result={
        "ID":user.ID,
        "result":result['result'],
        "explanation":result['explanation']
    }
    return review_result

@app.post("/document_interpret")
def interpret_document(user:UserInput):
    result = file_interpret(user.file_path)
    return result

if __name__ == '__main__':
    uvicorn.run(f'{os.path.basename(__file__).split(".")[0]}:app', host='0.0.0.0', port=8845, reload=True)
