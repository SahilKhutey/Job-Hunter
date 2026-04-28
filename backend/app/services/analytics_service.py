from typing import List, Dict, Any
from app.models.job import Application, Job

class AnalyticsService:
    """
    Computes performance metrics and learning insights from application history.
    """
    def compute_dashboard_stats(self, applications: List[Application], analyzed_jobs: List[Job] = None):
        total = len(applications)
        risks_avoided = 0
        if analyzed_jobs:
            for j in analyzed_jobs:
                score = getattr(j, "strategic_risk_score", 0) if not isinstance(j, dict) else j.get("strategic_risk_score", 0)
                if (score or 0) > 60:
                    risks_avoided += 1

        if total == 0:
            return {
                "total_applications": 0,
                "interview_rate": 0,
                "rejection_rate": 0,
                "active_applications": 0,
                "status_breakdown": {},
                "risks_avoided": risks_avoided
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
            "status_breakdown": status_counts,
            "risks_avoided": risks_avoided
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

    def analyze_score_correlation(self, applications: List[Application]):
        """
        Analyzes if higher match scores correlate with better outcomes.
        """
        buckets = {
            "90-100": {"total": 0, "interviews": 0},
            "80-89": {"total": 0, "interviews": 0},
            "70-79": {"total": 0, "interviews": 0},
            "below 70": {"total": 0, "interviews": 0}
        }
        
        for app in applications:
            score = (app.applied_match_score or 0) * 100
            bucket = "below 70"
            if score >= 90: bucket = "90-100"
            elif score >= 80: bucket = "80-89"
            elif score >= 70: bucket = "70-79"
            
            buckets[bucket]["total"] += 1
            if app.status == "interview":
                buckets[bucket]["interviews"] += 1
                
        # Calculate conversion per bucket
        correlation = {}
        for b, data in buckets.items():
            rate = round((data["interviews"] / data["total"]) * 100, 1) if data["total"] > 0 else 0
            correlation[b] = {"rate": rate, "volume": data["total"]}
            
        return correlation

    def generate_ai_insights(self, stats: Dict[str, Any], resume_perf: Dict[str, Any], platform_perf: Dict[str, Any], score_corr: Dict[str, Any]):
        """
        Generates actionable recommendations based on data patterns.
        """
        insights = []
        
        # 1. Interview Rate Insight
        if stats.get("interview_rate", 0) < 10 and stats.get("total_applications", 0) > 10:
            insights.append({
                "type": "warning",
                "message": "Low conversion rate detected. Your resume might be missing critical keywords for current target roles."
            })
        elif stats.get("interview_rate", 0) > 25:
            insights.append({
                "type": "success",
                "message": "Exceptional interview rate! Your tailoring strategy is highly effective."
            })

        # 2. Score Correlation Insight
        high_tier = score_corr.get("90-100", {})
        if high_tier.get("volume", 0) > 3 and high_tier.get("rate", 0) > 30:
            insights.append({
                "type": "success",
                "message": "Strong correlation: Applications with 90%+ match scores are significantly more likely to trigger interviews."
            })
        elif high_tier.get("volume", 0) > 3 and high_tier.get("rate", 0) < 10:
             insights.append({
                "type": "caution",
                "message": "High match scores aren't converting. Consider reviewing your manual 'Custom Answers' or 'Cover Letter' quality."
            })

        # 3. Resume Version Insight
        if len(resume_perf) > 1:
            best_v = max(resume_perf, key=lambda x: resume_perf[x]["rate"])
            if resume_perf[best_v]["rate"] > 0:
                insights.append({
                    "type": "info",
                    "message": f"Resume version '{best_v}' is outperforming others. Consider using this structure as your primary template."
                })
            
        # 4. Platform Insight
        if platform_perf:
            best_p = max(platform_perf, key=lambda x: platform_perf[x]["rate"])
            if platform_perf[best_p]["rate"] > 0:
                insights.append({
                    "type": "success",
                    "message": f"You have the highest success rate on {best_p}. Double down on applications via this platform."
                })

        # 5. Volume Insight
        if stats.get("total_applications", 0) < 5:
            insights.append({
                "type": "info",
                "message": "Data volume is low. Submit more applications to unlock predictive conversion analytics."
            })

        return insights

analytics_service = AnalyticsService()
