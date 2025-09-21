# Arsitektur
```
+----------------+
|    API Gateway |
+----------------+
       |
       | REST / HTTP
       v
+-------------------------+
|  QueryTool Microservice |
|-------------------------|
| - SQLServer (py micro)  |
+-------------------------+
       |
       | Pool / driver
       v
+----------------+
| Databases      |
| - SQLServer    |
+----------------+

```

## Manual Debug
```
source venv/Scripts/activate
uvicorn src.main:app --reload --port 8001
curl -X POST http://127.0.0.1:8001/mssql2000/query   -H "Content-Type: application/json"   -d '{"sql": "SELECT TOP 10 name, id FROM sysobjects", "skip": 0, "take": 10}'
```

## Hasil
```
{"columns":["name","id"],"rows":[{"name":"sysobjects","id":1},{"name":"sysindexe
s","id":2},{"name":"syscolumns","id":3},{"name":"systypes","id":4},{"name":"sysc
omments","id":6},{"name":"sysfiles1","id":8},{"name":"syspermissions","id":9},{"
name":"sysusers","id":10},{"name":"sysproperties","id":11},{"name":"sysdepends",
"id":12}],"totalCount":10}
```
