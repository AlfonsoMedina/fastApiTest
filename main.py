from fastapi import FastAPI #pip install "fastapi[all]"

app = FastAPI() 

@app.get("/") 
async def root():
    return {"message": "¡Ruta de prueba FastApi!"}

@app.post("/user") 
async def user():
    return {"name":"Alfonso"}