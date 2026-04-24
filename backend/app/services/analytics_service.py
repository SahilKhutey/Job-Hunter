from typing import List, Dict, Any
from app.models.job import Application, Job

class AnalyticsService:
    """
    Computes performance metrics and learning insights from application history.
    """
    def compute_dashboard_stats(self, applications: List[Application]):
        total = len(applications)
        if total == 0:
            return {
                "total_applications": 0,
                "interview_rate": 0,
                "rejection_rate": 0,
                "active_applications": 0,
                "status_breakdown": {}
            }

        status_counts = {}
        for app in applications:
            status_counts[app.status] = status_counts.get(app.status, 0) + 1

        interview_count = status_counts.get("interview", 0)
        rejection_count = status_counts.get("rejected", 0)
        active_count = total - rejection_count - status_counts.get("offer", 0)

        return {
            "total_applications": total,
            "interview_rate": round((interview_count / total) * 100, 1),
            "rejection_rate": round((rejection_count / total) * 100, 1),
            "active_applications": active_count,
            "status_breakdown": status_counts
        }

    def analyze_resume_performance(self, applications: List[Application]):
        """
        Calculates conversion rates per resume version.
        """
        perf = {}
        for app in applications:
            version = app.resume_version or "default"
            if version not in perf:
                perf[version] = {"total": 0, "interviews": 0, "rate": 0}
            
            perf[version]["total"] += 1
            if app.status == "interview":
                perf[version]["interviews"] += 1
        
        for v in perf:
            total = perf[v]["total"]
            interviews = perf[v]["interviews"]
            perf[v]["rate"] = round((interviews / total) * 100, 1) if total > 0 else 0
            
        return perf

    def analyze_platform_performance(self, applications: List[Application]):
        """
        Calculates conversion rates per job platform.
        """
        platforms = {}
        for app in applications:
            p = app.platform or "other"
            if p not in platforms:
                platforms[p] = {"total": 0, "interviews": 0, "rate": 0}
            
            platforms[p]["total"] += 1
            if app.status == "interview":
                platforms[p]["interviews"] += 1

        for p in platforms:
            total = platforms[p]["total"]
            interviews = platforms[p]["interviews"]
            platforms[p]["rate"] = round((interviews / total) * 100, 1) if total > 0 else 0
            
        return platforms

    def generate_ai_insights(self, stats: Dict[str, Any], resume_perf: Dict[str, Any]):
        """
        Generates actionable recommendations based on data patterns.
        """
        insights = []
        
        # Interview Rate Insight
        if stats["interview_rate"] < 10 and stats["total_applications"] > 20:
            insights.append({
                "type": "warning",
                "message": "Low conversion rate detected. Your resume might be missing critical keywords for current target roles."
            })
        elif stats["interview_rate"] > 25:
            insights.append({
                "type": "success",
                "message": "Exceptional interview rate! Your tailoring strategy is highly effective."
            })

        # Resume Version Insight
        if len(resume_perf) > 1:
            best_v = max(resume_perf, key=lambda x: resume_perf[x]["rate"])
            insights.append({
                "type": "info",
                "message": f"Resume version '{best_v}' is outperforming others. Consider using this structure as your primary template."
            })

        return insights

analytics_service = AnalyticsService()
