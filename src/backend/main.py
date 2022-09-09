import uvicorn

if __name__ == "__main__":
    uvicorn.run("routers.api:app", reload=True)
