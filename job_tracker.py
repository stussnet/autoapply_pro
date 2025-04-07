import pandas as pd
import os

TRACKER_FILE = "job_tracker.csv"
STATUS_OPTIONS = ["Interested", "Applied", "Interviewing", "Offer", "Rejected"]

def load_job_tracker():
    if os.path.exists(TRACKER_FILE):
        return pd.read_csv(TRACKER_FILE)
    else:
        return pd.DataFrame(columns=["title", "company", "link", "status", "notes"])

def save_job_tracker(df):
    df.to_csv(TRACKER_FILE, index=False)

def update_tracker(df, job_index, status=None, notes=None):
    if status is not None:
        df.at[job_index, "status"] = status
    if notes is not None:
        df.at[job_index, "notes"] = notes
    save_job_tracker(df)
    return df
