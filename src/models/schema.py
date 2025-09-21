from pydantic import BaseModel

class QueryRequest(BaseModel):
    sql: str
    skip: int = 0
    take: int = 100

class QueryResponse(BaseModel):
    columns: list[str]
    rows: list[dict]
    totalCount: int
