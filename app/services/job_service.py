import threading
import time
import json
from pathlib import Path
from app.models.job import JobStatus

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

def process_job(job_id: str, file_id: str, save_job, load_job):
    def task():
        time.sleep(3)
        job = load_job(job_id)
        if not job:
            return

        job["status"] = JobStatus.COMPLETED
        job["result"] = {"message": f"Processed file {file_id}"}
        save_job(job_id, job)

        result_path = RESULTS_DIR / f"{job_id}.json"
        result_data = {"job_id": job_id, "output": {"message": f"Processed file {file_id}"}}
        with result_path.open("w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2)

    threading.Thread(target=task, daemon=True).start()
