from fastapi import APIRouter, HTTPException, status
from src.models.schema import QueryRequest, QueryResponse
from src.services.querytool import run_query, insert_query, update_query, delete_query

router = APIRouter(prefix="/mssql2000", tags=["SQLServer2000"])

# --- SELECT ---
@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
def query_tool(payload: QueryRequest):
    try:
        result = run_query(payload.sql, payload.skip, payload.take)
        return {
            "columns": result["columns"],
            "rows": result["rows"],
            "totalCount": result["totalCount"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- INSERT ---
@router.post("/insert", status_code=status.HTTP_201_CREATED)
def insert_tool(payload: QueryRequest):
    try:
        result = insert_query(payload.sql)
        return {
            "message": result["message"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- UPDATE ---
@router.post("/update", status_code=status.HTTP_200_OK)
def update_tool(payload: QueryRequest):
    try:
        result = update_query(payload.sql)
        return {
            "message": result["message"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- DELETE ---
@router.post("/delete", status_code=status.HTTP_200_OK)
def delete_tool(payload: QueryRequest):
    try:
        result = delete_query(payload.sql)
        return {
            "message": result["message"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
