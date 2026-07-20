from app.api.v1.medical_reports.repository import MedicalReportRepository
from app.api.v1.medication.repository import MedicationRepository
from app.services.notifications.reminder_service import ReminderService

class DashboardService:
    @staticmethod
    async def get_user_dashboard_summary(user_id: str) -> dict:
        reports = await MedicalReportRepository.get_user_reports(user_id)
        medicines = await MedicationRepository.get_user_medicines(user_id)
        reminder_history = await MedicationRepository.get_user_reminder_history(user_id)
        
        # Calculate live health index score
        latest_report = reports[0] if reports else None
        health_score = latest_report["health_score"] if latest_report else 94
        disease_risks = latest_report["risk_assessment"] if latest_report else [
            {
                "condition": "Cardiovascular & Metabolic Health",
                "risk_level": "Low",
                "description": "Lab biomarkers are optimal and within healthy target reference ranges."
            }
        ]
        recommendations = latest_report["recommendations"] if latest_report else [
            "Maintain daily hydration (2-3L of water).",
            "Engage in 30 minutes of moderate activity daily."
        ]

        # Calculate due medicine reminders
        due_reminders = ReminderService.calculate_due_reminders(medicines)

        return {
            "health_score": health_score,
            "disease_risks": disease_risks,
            "recommendations": recommendations,
            "reports_count": len(reports),
            "latest_reports": reports[:5],
            "active_medicines": medicines,
            "due_reminders": due_reminders,
            "reminder_history": reminder_history[:5]
        }
