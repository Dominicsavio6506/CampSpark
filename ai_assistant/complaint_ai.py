from complaints_app.models import Complaint
from collections import Counter


def route_authority(category, urgency):
    if urgency.lower() == "critical":
        return "Principal"

    if category.lower() in ["harassment", "ragging"]:
        return "Complaint Officer"

    if category.lower() == "academic":
        return "HOD"

    return "Admin"


def risk_pattern_analysis():
    data = Complaint.objects.all()

    risk_departments = Counter()
    risk_categories = Counter()

    for c in data:
        if c.urgency.lower() in ["high", "critical"]:
            risk_departments[c.department] += 1
            risk_categories[c.category] += 1

    return {
        "top_risk_departments": dict(risk_departments),
        "top_risk_categories": dict(risk_categories)
    }


def complaint_statistics():
    data = Complaint.objects.all()

    total = data.count()

    category_stats = Counter([c.category for c in data])
    urgency_stats = Counter([c.urgency for c in data])
    department_stats = Counter([c.department for c in data])

    high_risk_cases = data.filter(
        urgency__in=["High", "Critical", "high", "critical"]
    ).count()

    routing = []

    for c in data:
        authority = route_authority(c.category, c.urgency)
        routing.append({
            "category": c.category,
            "urgency": c.urgency,
            "authority": authority
        })

    risk_patterns = risk_pattern_analysis()

    return {
        "total_complaints": total,
        "category_distribution": dict(category_stats),
        "urgency_distribution": dict(urgency_stats),
        "department_distribution": dict(department_stats),
        "high_risk_cases": high_risk_cases,
        "routing_preview": routing[:5],
        "risk_patterns": risk_patterns
    }
