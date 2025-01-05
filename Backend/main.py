from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import pandas as pd
import joblib

app = FastAPI(title="Green Finance Optimization Platform")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class Project(BaseModel):
    name: str
    description: str
    budget: float
    sector: str
    expected_co2_reduction: float
    social_impact_score: float
    governance_score: float
    timeline_months: int
    risk_score: Optional[float] = None

class ProjectScore(BaseModel):
    project_id: int
    esg_score: float
    risk_score: float
    roi_estimate: float
    impact_metrics: dict

# Mock database
projects_db = []
model = None

# Initialize ML model (mock)
def init_model():
    global model
    # In reality, you would load your trained model here
    model = joblib.load('path_to_your_model.pkl')

@app.on_event("startup")
async def startup_event():
    init_model()

# API Endpoints
@app.post("/projects/", response_model=Project)
async def create_project(project: Project):
    project_dict = project.dict()
    project_dict["id"] = len(projects_db) + 1
    projects_db.append(project_dict)
    return project_dict

@app.get("/projects/", response_model=List[Project])
async def get_projects():
    return projects_db

@app.post("/analyze/project/{project_id}")
async def analyze_project(project_id: int):
    project = next((p for p in projects_db if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Mock ESG scoring logic
    esg_score = (
        project["expected_co2_reduction"] * 0.4 +
        project["social_impact_score"] * 0.3 +
        project["governance_score"] * 0.3
    )
    
    # Mock risk assessment
    risk_score = np.random.normal(0.5, 0.1)  # Random risk score for demonstration
    
    # Mock ROI calculation
    roi_estimate = (esg_score * 0.6 - risk_score * 0.4) * project["budget"] * 0.15
    
    return {
        "project_id": project_id,
        "esg_score": esg_score,
        "risk_score": risk_score,
        "roi_estimate": roi_estimate,
        "impact_metrics": {
            "environmental": project["expected_co2_reduction"],
            "social": project["social_impact_score"],
            "governance": project["governance_score"]
        }
    }

@app.post("/optimize/portfolio")
async def optimize_portfolio(budget: float, risk_tolerance: float):
    if len(projects_db) == 0:
        raise HTTPException(status_code=400, detail="No projects available")
    
    # Simple portfolio optimization (mock)
    scored_projects = []
    total_budget = 0
    
    for project in sorted(projects_db, key=lambda x: x["expected_co2_reduction"] / x["budget"], reverse=True):
        if total_budget + project["budget"] <= budget:
            scored_projects.append(project)
            total_budget += project["budget"]
    
    return {
        "selected_projects": scored_projects,
        "total_budget_allocated": total_budget,
        "expected_impact": {
            "total_co2_reduction": sum(p["expected_co2_reduction"] for p in scored_projects),
            "average_social_score": np.mean([p["social_impact_score"] for p in scored_projects]),
            "average_governance_score": np.mean([p["governance_score"] for p in scored_projects])
        }
    }

@app.get("/dashboard/summary")
async def get_dashboard_summary():
    if not projects_db:
        return {
            "total_projects": 0,
            "total_budget": 0,
            "average_esg_score": 0,
            "total_co2_reduction": 0
        }
    
    return {
        "total_projects": len(projects_db),
        "total_budget": sum(p["budget"] for p in projects_db),
        "average_esg_score": np.mean([
            (p["expected_co2_reduction"] + p["social_impact_score"] + p["governance_score"]) / 3 
            for p in projects_db
        ]),
        "total_co2_reduction": sum(p["expected_co2_reduction"] for p in projects_db)
    }