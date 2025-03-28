from app.database.session import SessionLocal
from app.models import User, Doctor, Assistant, Patient, Treatment, PatientAssignment, TreatmentApplication

# Creeaza sesiunea DB
db = SessionLocal()

# Șterge datele existente (optional, doar pentru test)
db.query(TreatmentApplication).delete()
db.query(PatientAssignment).delete()
db.query(Treatment).delete()
db.query(Patient).delete()
db.query(Doctor).delete()
db.query(Assistant).delete()
db.query(User).delete()
db.commit()

# === USERS ===
user_manager = User(username="manager1", email="manager1@demo.com", password="pass", role="manager")
user_doctor = User(username="doctor1", email="doctor1@demo.com", password="pass", role="doctor")
user_assistant = User(username="assistant1", email="assistant1@demo.com", password="pass", role="assistant")

db.add_all([user_manager, user_doctor, user_assistant])
db.commit()

# === DOCTOR ===
doctor = Doctor(user_id=user_doctor.id, specialization="Cardiology")
db.add(doctor)
db.commit()

# === ASSISTANT ===
assistant = Assistant(user_id=user_assistant.id, department="ER")
db.add(assistant)
db.commit()

# === PATIENT ===
patient = Patient(name="John Doe", age=45, address="123 Main St", doctor_id=doctor.id)
db.add(patient)
db.commit()

# === TREATMENT ===
treatment = Treatment(name="Heart Therapy", description="Daily medication", doctor_id=doctor.id, patient_id=patient.id)
db.add(treatment)
db.commit()

# === PATIENT ASSIGNMENT ===
assignment = PatientAssignment(patient_id=patient.id, assistant_id=assistant.id)
db.add(assignment)
db.commit()

# === TREATMENT APPLICATION ===
application = TreatmentApplication(treatment_id=treatment.id, assistant_id=assistant.id)
db.add(application)
db.commit()

db.close()
print("Fixture data loaded successfully.")
