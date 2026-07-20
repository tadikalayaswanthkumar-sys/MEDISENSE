from sqlalchemy import select
from app.config.database import db_instance
from app.db.models import MedicalReport, HealthRecord

class MedicalReportRepository:
    @staticmethod
    async def create_report(report_doc: dict) -> dict:
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                report_id = report_doc.get("_id") or report_doc.get("id")
                report = MedicalReport(
                    id=report_id,
                    user_id=report_doc["user_id"],
                    title=report_doc["title"],
                    file_name=report_doc.get("file_name") or report_doc.get("title"),
                    file_path=report_doc.get("file_path"),
                    file_type=report_doc.get("file_type"),
                    upload_date=report_doc.get("upload_date"),
                    raw_text=report_doc.get("raw_text", ""),
                    health_score=report_doc.get("health_score", 90),
                    biomarkers=report_doc.get("biomarkers", {}),
                    risk_assessment=report_doc.get("risk_assessment", []),
                    recommendations=report_doc.get("recommendations", []),
                    summary=report_doc.get("summary", "")
                )
                session.add(report)
                # Flush report first so PostgreSQL foreign key constraint is satisfied for health_record
                await session.flush()

                health_record = HealthRecord(
                    id=f"{report_id}_hr",
                    user_id=report_doc["user_id"],
                    report_id=report.id,
                    health_score=report_doc.get("health_score", 90),
                    risk_assessment=report_doc.get("risk_assessment", []),
                    biomarkers=report_doc.get("biomarkers", {}),
                    created_at=report_doc.get("upload_date")
                )
                session.add(health_record)
                await session.commit()
                await session.refresh(report)
                return report.to_dict()
        else:
            if "reports" not in db_instance.in_memory_store:
                db_instance.in_memory_store["reports"] = {}
            db_instance.in_memory_store["reports"][report_doc["_id"]] = report_doc
            return report_doc

    @staticmethod
    async def get_user_reports(user_id: str) -> list:
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                result = await session.execute(
                    select(MedicalReport)
                    .where(MedicalReport.user_id == user_id)
                    .order_by(MedicalReport.upload_date.desc())
                    .limit(100)
                )
                reports = result.scalars().all()
                return [r.to_dict() for r in reports]
        else:
            if "reports" not in db_instance.in_memory_store:
                return []
            reports = [r for r in db_instance.in_memory_store["reports"].values() if r.get("user_id") == user_id]
            return sorted(reports, key=lambda x: x.get("upload_date", ""), reverse=True)

    @staticmethod
    async def get_report_by_id(report_id: str, user_id: str) -> dict:
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                result = await session.execute(
                    select(MedicalReport).where(
                        MedicalReport.id == report_id,
                        MedicalReport.user_id == user_id
                    )
                )
                report = result.scalar_one_or_none()
                return report.to_dict() if report else None
        else:
            if "reports" not in db_instance.in_memory_store:
                return None
            report = db_instance.in_memory_store["reports"].get(report_id)
            if report and report.get("user_id") == user_id:
                return report
            return None
