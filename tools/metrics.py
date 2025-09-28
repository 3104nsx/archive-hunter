
from fastapi import FastAPI, Response
import uvicorn

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(content="ok\n", media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9108)
