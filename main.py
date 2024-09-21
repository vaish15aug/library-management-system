from fastapi import FastAPI
from routes.user import userRouter
from routes.admin import adminRouter
from routes.book import bookRouter
from routes.system import systemRouter
import uvicorn

app = FastAPI(debug=True)
app.include_router(userRouter)
app.include_router(adminRouter)
app.include_router(bookRouter)
app.include_router(systemRouter)




@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, debug=True, log_level='info')




