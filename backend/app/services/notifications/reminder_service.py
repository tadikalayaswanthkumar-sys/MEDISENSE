from datetime import datetime, timezone

class ReminderService:
    @staticmethod
    def calculate_due_reminders(medicines: list) -> list:
        now_str = datetime.now(timezone.utc).strftime("%H:%M")
        due_list = []
        
        for med in medicines:
            if med.get("is_active", True):
                times = med.get("times", [])
                due_list.append({
                    "medicine_id": med.get("_id"),
                    "name": med.get("name"),
                    "dosage": med.get("dosage"),
                    "scheduled_time": times[0] if times else "08:00 AM",
                    "status": "Due"
                })
        return due_list
