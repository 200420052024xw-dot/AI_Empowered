from agent.profile_generation.profile_generation import profile_generation
from agent.commentator.comment_create import comment_create
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

if __name__ == '__main__':
    uvicorn.run(f'{os.path.basename(__file__).split(".")[0]}:app', host='0.0.0.0', port=8845, reload=True)
