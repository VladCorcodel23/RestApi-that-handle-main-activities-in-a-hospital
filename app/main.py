from fastapi import FastAPI
from app.api import routes_auth, routes_user, routes_doctor, routes_assistant, routes_patient, routes_treatment, routes_patient_assignment, routes_treatment_application
from app.api.routes_patient_assignment import router as patient_assignment_router
from app.api import routes_report

app = FastAPI()

app.include_router(routes_user.router)
app.include_router(routes_doctor.router)
app.include_router(routes_assistant.router)
app.include_router(routes_patient.router)
app.include_router(routes_treatment.router, prefix="/treatments", tags=["Treatments"])
app.include_router(routes_patient_assignment.router, prefix="/assignments", tags=["Patient Assignments"])
app.include_router(routes_treatment_application.router, prefix="/applications", tags=["Treatment Applications"])
app.include_router(routes_auth.router, tags=["Auth"])
app.include_router(routes_assistant.router, prefix="/assistants", tags=["Assistants"])
app.include_router(routes_patient.router, prefix="/patients", tags=["patients"])
app.include_router(routes_treatment_application.router, prefix="/treatment-applications", tags=["Treatment Applications"])
app.include_router(patient_assignment_router, prefix="/assignments", tags=["Assignments"])
app.include_router(routes_report.router, prefix="/report")