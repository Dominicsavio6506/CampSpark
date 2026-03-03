from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from groq import Groq

from .models import ChatHistory
from students.models import Student
from marks.models import Marks
from attendance.models import Attendance
from fees.models import Fee
from complaints_app.models import Complaint
from notifications.models import Notification
from events.models import Event
from .complaint_ai import complaint_statistics
from .smart_ai import smart_ai_response

from django.views.decorators.csrf import csrf_exempt
import json
import os

def campus_ai_chat(request):

    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return JsonResponse({"error": "API Key not configured"}, status=500)

    client = Groq(api_key=api_key)

    # continue your AI logic...


# ============================
# AI CHAT SYSTEM
# ============================

def ai_page(request):
    return render(request, "ai_chat.html")


def access_denied(request):
    return render(request, "access_denied.html")


@csrf_exempt
def ai_reply(request):
    user = request.user if request.user.is_authenticated else None

    data = json.loads(request.body.decode("utf-8")) if request.body else {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return JsonResponse({"reply": "Please type something."})

    if not any(topic in user_message.lower() for topic in allowed_topics):
        return JsonResponse({"reply": "⚠️ CampSpark AI answers only campus-related questions."})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are CampSpark AI. Answer only campus-related questions."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content

        user_type = "guest"
        if user:
            user_type = "admin" if user.is_superuser else "staff"

        if user:
            ChatHistory.objects.create(
                user=user,
                user_type=user_type,
                message=user_message,
                reply=reply
            )

        return JsonResponse({"reply": reply})

    except Exception as e:
        return JsonResponse({"reply": f"⚠️ Error: {str(e)}"})


# ============================
# SAFE AI ANALYTICS SYSTEM
# ============================

def detect_weak_students():
    weak_students = []

    for student in Student.objects.all():
        marks = Marks.objects.filter(student=student)
        if marks.exists():
            avg = sum(getattr(m, "total", 0) for m in marks) / marks.count()
            if avg < 40:
                weak_students.append(student.name)

    return weak_students


def detect_attendance_risk():
    risk_students = []

    for student in Student.objects.all():
        records = Attendance.objects.all()

        if records.exists():
            total = records.count()
            present = records.filter(status="Present").count()
            percent = (present / total) * 100 if total > 0 else 0

            if percent < 75:
                risk_students.append({
                    "name": student.name,
                    "percent": round(percent, 2)
                })

    return risk_students


def generate_staff_ai_insight():
    weak = detect_weak_students()
    attendance_risk = detect_attendance_risk()

    msg = "Overall class performance looks stable."

    if weak:
        msg = f"{len(weak)} weak students detected."

    if attendance_risk:
        msg += f" {len(attendance_risk)} attendance risks."

    return msg


def predict_student_performance():
    predictions = []

    for student in Student.objects.all():
        marks = Marks.objects.filter(student=student)

        if marks.exists():
            avg = sum(getattr(m, "total", 0) for m in marks) / marks.count()

            status = (
                "High improvement chance 📈" if avg >= 70 else
                "Moderate performance ⚖️" if avg >= 40 else
                "Failure risk ⚠️"
            )

            predictions.append({
                "name": student.name,
                "avg": round(avg, 2),
                "status": status
            })

    return predictions


def generate_study_recommendations():
    recommendations = []

    for student in Student.objects.all():
        marks = Marks.objects.filter(student=student)
        weak_subjects = []

        for m in marks:
            if getattr(m, "total", 0) < 40:
                weak_subjects.append(getattr(m, "subject", "Unknown"))

        if weak_subjects:
            recommendations.append({
                "name": student.name,
                "subjects": weak_subjects,
                "advice": "Focus more practice and revision"
            })

    return recommendations


def detect_fee_risk_students():
    risk_students = []

    for fee in Fee.objects.all():
        due = getattr(fee, "due_amount", 0)
        status = getattr(fee, "status", "").lower()

        if due > 5000 or status == "pending":
            student_name = getattr(getattr(fee, "student", None), "name", "Unknown")

            risk_students.append({
                "name": student_name,
                "due": due,
                "status": fee.status
            })

    return risk_students


def detect_complaint_patterns():
    status_stats = {}
    repeat_patterns = []

    complaints = Complaint.objects.all()

    for c in complaints:
        status = getattr(c, "status", "Unknown")
        status_stats[status] = status_stats.get(status, 0) + 1

        if complaints.filter(status=status).count() > 3:
            repeat_patterns.append(f"High complaint volume: {status}")

    return {
        "repeat_patterns": list(set(repeat_patterns)),
        "status_stats": status_stats,
        "total_complaints": complaints.count()
    }


def detect_dropout_risk():
    risk_summary = {"high_risk_count": 0, "medium_risk_count": 0, "low_risk_count": 0}

    for record in Attendance.objects.all():
        percentage = getattr(record, "percentage", None)
        if percentage is None:
            continue

        if percentage < 50:
            risk_summary["high_risk_count"] += 1
        elif percentage < 75:
            risk_summary["medium_risk_count"] += 1
        else:
            risk_summary["low_risk_count"] += 1

    return risk_summary


def detect_burnout_risk():
    burnout_list = []

    for student in Student.objects.all():
        marks = Marks.objects.filter(student=student)

        avg_marks = sum(getattr(m, "total", 0) for m in marks) / marks.count() if marks.exists() else 0
        weak_subject_count = marks.filter(total__lt=40).count() if marks.exists() else 0

        if avg_marks < 50 or weak_subject_count >= 2:
            burnout_list.append({
                "name": student.name,
                "avg_marks": round(avg_marks, 2),
                "weak_subjects": weak_subject_count
            })

    return burnout_list


def detect_placement_readiness():
    placement_list = []

    for student in Student.objects.all():
        marks = Marks.objects.filter(student=student)

        if marks.exists():
            avg = sum(getattr(m, "total", 0) for m in marks) / marks.count()

            status = (
                "Ready for Placement 💼" if avg >= 70 else
                "Needs Improvement 📈" if avg >= 50 else
                "Not Ready ❌"
            )

            placement_list.append({
                "name": student.name,
                "avg_marks": round(avg, 2),
                "status": status
            })

    return placement_list


def detect_top_students():
    topper_list = []

    for student in Student.objects.all():
        marks = Marks.objects.filter(student=student)

        if marks.exists():
            avg = sum(getattr(m, "total", 0) for m in marks) / marks.count()
            topper_list.append({"name": student.name, "avg_marks": round(avg, 2)})

    return sorted(topper_list, key=lambda x: x["avg_marks"], reverse=True)[:5]


def generate_smart_campus_insight():
    weak = detect_weak_students()
    attendance_risk = detect_attendance_risk()
    fee_risk = detect_fee_risk_students()
    dropout = detect_dropout_risk()
    burnout = detect_burnout_risk()

    summary = "Campus performance looks healthy."

    if weak:
        summary += f" {len(weak)} weak students."
    if attendance_risk:
        summary += f" {len(attendance_risk)} attendance risks."
    if fee_risk:
        summary += f" {len(fee_risk)} fee risk cases."
    if dropout:
        summary += f" {sum(dropout.values())} dropout risks."
    if burnout:
        summary += f" {len(burnout)} burnout alerts."

    return summary


# ============================
# VOICE AI
# ============================

@login_required
def voice_command_api(request):
    command = request.GET.get("command", "").strip().lower()
    user = request.user

    if not command:
        return JsonResponse({"reply": "Please say something."})

    # 🎓 ATTENDANCE PERCENTAGE
    if "attendance" in command or "percentage" in command:
        try:
            student = Student.objects.get(user=user)
            records = Attendance.objects.filter(student=student)

            if records.exists():
                total = records.count()
                present = records.filter(status="Present").count()
                percent = round((present / total) * 100, 2)

                reply = f"Your attendance percentage is {percent} percent."
            else:
                reply = "No attendance records found yet."

        except:
            reply = "Student profile not linked to your account."

        return JsonResponse({"reply": reply})

    # 🧠 Otherwise use Smart AI
    try:
        reply = smart_ai_response(command, "student")
    except:
        reply = "I'm here to help. Please say again."

    return JsonResponse({"reply": reply[:250]})

def voice_ai(request):
    return render(request, "voice_ai.html")


# ============================
# CAMPUS AI CHAT
# ============================

@csrf_exempt
def campus_ai_chat(request):
    if request.method != "POST":
        return JsonResponse({"reply": "POST only"})

    try:
        data = json.loads(request.body.decode("utf-8"))
        message = data.get("message", "").strip()
        role = data.get("role", "student")

        if not message:
            return JsonResponse({"reply": "Please type something."})

        reply = smart_ai_response(message, role)
        return JsonResponse({"reply": reply})

    except Exception as e:
        return JsonResponse({"reply": f"Error: {str(e)}"})


def test_ai_page(request):
    reply = smart_ai_response("Explain attendance rules", "student")
    return HttpResponse(reply)


@csrf_exempt
def ai_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").strip()

            if not message:
                return JsonResponse({"reply": "Please type something."})

            reply = smart_ai_response(message, "student")
            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"reply": f"AI Error: {str(e)}"})

    return JsonResponse({"reply": "Only POST allowed"})

# ============================
# COMPLAINT AI DASHBOARD API (RESTORED)
# ============================

def complaint_ai_dashboard(request):
    try:
        stats = detect_complaint_patterns()
        return JsonResponse(stats)
    except Exception:
        return JsonResponse({
            "repeat_patterns": [],
            "status_stats": {},
            "total_complaints": 0
        })

# TEXT AI MAIN API
# TEXT AI MAIN API
@csrf_exempt
def ai_chat_api(request):

    if request.method != "POST":
        return JsonResponse({"reply": "POST only"})

    try:
        data = json.loads(request.body)

        history = data.get("history", [])
        message = data.get("message", "").strip()

        if not message:
            return JsonResponse({"reply": "Please type something."})

        # ===============================
        # 🔍 Detect ERP Related Question
        # ===============================
        erp_keywords = [
            "attendance", "fee", "fees", "marks",
            "student", "staff", "admin",
            "event", "events",
            "complaint", "library",
            "dashboard", "campspark", "erp"
        ]

        msg_lower = message.lower()
        is_erp_question = any(word in msg_lower for word in erp_keywords)

        # ===============================
        # 🔥 Inject live ERP data ONLY if needed
        # ===============================
        if is_erp_question:

            total_students = Student.objects.count()
            total_events = Event.objects.count()
            total_attendance = Attendance.objects.count()
            total_fee_records = Fee.objects.count()

            erp_context = f"""
CampSpark ERP Context:
- Total Students: {total_students}
- Total Events: {total_events}
- Attendance Records: {total_attendance}
- Fee Records: {total_fee_records}
"""

            enhanced_message = f"""
{erp_context}

Now answer the user's question clearly.

User Question:
{message}
"""

        else:
            enhanced_message = message

        # ===============================
        # 🤖 SMART AI RESPONSE
        # ===============================
        reply = smart_ai_response(
            enhanced_message,
            "student",
            history
        )

        # ===============================
        # 💾 SAVE CHAT HISTORY
        # ===============================
        if request.user.is_authenticated:
            ChatHistory.objects.create(
                user=request.user,
                user_type="admin" if request.user.is_superuser else "staff",
                message=message,
                reply=reply
            )

        return JsonResponse({"reply": reply})

    except Exception as e:
        return JsonResponse({"reply": f"AI Error: {str(e)}"})