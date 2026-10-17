from fastapi import FastAPI

app = FastAPI(title="DocuFlow")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
