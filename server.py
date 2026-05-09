from fastapi import FastAPI, Query
from client.rq_client import queue
from queues.worker import process_query
app = FastAPI()

@app.get("/")
def read_root():
    return {"Status": "Server is running!"}



@app.post("/chat")
def chat(query: str = Query(..., description="The user's query to the chatbot")):
    job=queue.enqueue(process_query, query)
    return {"job_id": job.id, "status": "Query has been enqueued for processing."}


@app.get("/job-status")
def get_result(job_id:str=Query(..., description="The ID of the job to retrieve the result for")):
    job = queue.fetch_job(job_id=job_id)
    result = job.result
    return {"job_id": job_id, "result": result}
    
    
    
    
