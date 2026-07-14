import sys
import os
import random
from datetime import date, timedelta
from decimal import Decimal

# Setup Django path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campspark.settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone

# --- Idempotency check: skip if DB is already seeded ---
from students.models import Student as _StudentCheck
if _StudentCheck.objects.exists():
    print("Database already seeded — skipping seed_prod_data.py")
    sys.exit(0)

from academics.models import Department as AcademicsDepartment, Course, Semester, Subject, Exam
from students.models import Student
from camp_staff.models import Staff
from library.models import Book, BorrowRecord
from assets.models import Location, Asset, AssetIssue
from events.models import Event, EventStaffIncharge, EventStudentHead, EventRegistration
from projects.models import Project, ProjectMember, ProjectProgress, Department as ProjectsDepartment
from attendance.models import Attendance, AttendanceRecord
from marks.models import Marks
from camp_fees.models import Fee, FeePayment, Scholarship
from complaints_app.models import Complaint
from notifications.models import Notification, NotificationTarget

def clear_data():
    print("Clearing old data...")
    # Delete in order of dependencies
    NotificationTarget.objects.all().delete()
    Notification.objects.all().delete()
    
    BorrowRecord.objects.all().delete()
    Book.objects.all().delete()
    
    AssetIssue.objects.all().delete()
    Asset.objects.all().delete()
    Location.objects.all().delete()
    
    EventRegistration.objects.all().delete()
    EventStaffIncharge.objects.all().delete()
    EventStudentHead.objects.all().delete()
    Event.objects.all().delete()
    
    ProjectProgress.objects.all().delete()
    ProjectMember.objects.all().delete()
    Project.objects.all().delete()
    ProjectsDepartment.objects.all().delete()
    
    AttendanceRecord.objects.all().delete()
    Attendance.objects.all().delete()
    
    Marks.objects.all().delete()
    
    FeePayment.objects.all().delete()
    Scholarship.objects.all().delete()
    Fee.objects.all().delete()
    
    Complaint.objects.all().delete()
    
    Student.objects.all().delete()
    Staff.objects.all().delete()
    
    Subject.objects.all().delete()
    Exam.objects.all().delete()
    Semester.objects.all().delete()
    Course.objects.all().delete()
    AcademicsDepartment.objects.all().delete()
    
    User.objects.exclude(username="admin").delete()
    print("Cleanup completed.")

def populate():
    # 1. Ensure Superuser 'admin' exists
    admin_user, _ = User.objects.get_or_create(username="admin")
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.set_password("adminpass")
    admin_user.save()
    print("Superuser 'admin' ensured.")

    # 2. Create Academics Departments
    dept_names = ["Computer Science", "Physics", "Chemistry", "Mathematics", "English Literature", "Business Commerce"]
    academics_depts = []
    for name in dept_names:
        d = AcademicsDepartment.objects.create(name=name)
        academics_depts.append(d)
    print(f"Created {len(academics_depts)} academics departments.")

    # 3. Create Projects Departments (defined inside projects.models)
    projects_depts = []
    for name in dept_names:
        d = ProjectsDepartment.objects.create(name=name)
        projects_depts.append(d)
    print(f"Created {len(projects_depts)} projects departments.")

    # 4. Create Courses & Semesters
    courses = []
    semesters = []
    course_data = {
        "Computer Science": ["B.Sc Computer Science", "MCA", "M.Sc Data Science"],
        "Physics": ["B.Sc Physics", "M.Sc Physics"],
        "Chemistry": ["B.Sc Chemistry"],
        "Mathematics": ["B.Sc Mathematics", "M.Sc Mathematics"],
        "English Literature": ["BA English"],
        "Business Commerce": ["B.Com", "M.Com"]
    }
    for dept in academics_depts:
        names = course_data.get(dept.name, ["General Course"])
        for cname in names:
            course = Course.objects.create(name=cname, department=dept)
            courses.append(course)
            # Create Semesters 1 to 4 for each course
            for sem_num in range(1, 5):
                sem = Semester.objects.create(course=course, number=sem_num)
                semesters.append(sem)
    print(f"Created {len(courses)} courses and {len(semesters)} semesters.")

    # 5. Create Subjects
    subjects = []
    subject_samples = {
        "Computer Science": ["Programming in C", "Data Structures", "Database Management Systems", "Artificial Intelligence", "Web Development", "Computer Networks"],
        "Physics": ["Classical Mechanics", "Quantum Physics", "Electromagnetism", "Optics", "Thermodynamics"],
        "Chemistry": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Analytical Chemistry"],
        "Mathematics": ["Calculus", "Algebra", "Real Analysis", "Differential Equations", "Linear Algebra"],
        "English Literature": ["Shakespeare Studies", "British Poetry", "American Literature", "Indian Writing in English"],
        "Business Commerce": ["Financial Accounting", "Corporate Law", "Business Economics", "Marketing Management", "Auditing"]
    }
    for sem in semesters:
        dept_name = sem.course.department.name
        names = subject_samples.get(dept_name, ["General Elective"])
        # Create 2 random subjects per semester
        for name in random.sample(names, min(len(names), 2)):
            sub = Subject.objects.create(name=f"{name} ({sem.course.name})", semester=sem, credits=random.choice([3, 4]))
            subjects.append(sub)
    print(f"Created {len(subjects)} subjects.")

    # 6. Create Staff Members (12 staff users)
    staffs = []
    staff_names = [
        ("Dr. John Smith", "Computer Science"),
        ("Dr. Emily Davis", "Computer Science"),
        ("Prof. Robert Miller", "Physics"),
        ("Prof. Susan Wilson", "Physics"),
        ("Dr. Michael Brown", "Chemistry"),
        ("Dr. Sarah Thomas", "Chemistry"),
        ("Prof. William Jones", "Mathematics"),
        ("Prof. Mary Martinez", "Mathematics"),
        ("Dr. David Taylor", "English Literature"),
        ("Dr. Linda Anderson", "English Literature"),
        ("Prof. Richard Jackson", "Business Commerce"),
        ("Prof. Barbara White", "Business Commerce")
    ]
    for idx, (name, dept_name) in enumerate(staff_names, start=1):
        username = f"staff{idx}"
        email = f"{username}@campspark.edu"
        user = User.objects.create_user(username=username, email=email, password="staffpass")
        user.is_staff = True
        user.first_name = name.split()[1]
        user.last_name = name.split()[2] if len(name.split()) > 2 else ""
        user.save()

        # Create Staff Profile
        staff = Staff.objects.create(
            user=user,
            name=name,
            department=dept_name,
            is_hod=(idx % 2 == 1)
        )
        staffs.append(staff)
    print(f"Created {len(staffs)} staff members.")

    # 7. Create Student Members (30 students spread across departments/semesters)
    students = []
    first_names = ["Arun", "Bala", "Chitra", "Divya", "Elango", "Fathima", "Ganesh", "Hari", "Indu", "Jaya", "Kavin", "Latha",
                   "Mani", "Nisha", "Oviya", "Prabhu", "Ravi", "Sandhya", "Tarun", "Uma", "Varun", "Yasmine"]
    last_names = ["Kumar", "Rajan", "Devi", "Siddharth", "Prakash", "Begum", "Moorthy", "Prasad", "Krishnan", "Selvam"]

    selected_semesters = random.choices(semesters, k=30)
    for idx in range(1, 31):
        username = f"student{idx}"
        email = f"{username}@campspark.edu"
        user = User.objects.create_user(username=username, email=email, password="studpass")
        user.save()

        # Pick random sem/course
        sem = selected_semesters[idx-1]
        course = sem.course
        dept = course.department

        # Fetch student model (signal auto-created it, retrieve and update)
        student = Student.objects.get(user=user)
        student.name = f"{random.choice(first_names)} {random.choice(last_names)}"
        student.roll_number = f"CS-{dept.name[:2].upper()}-{2024}{idx:02d}"
        student.department = dept.name
        student.department_fk = dept
        student.course = course
        student.semester = sem
        student.year = random.choice([1, 2, 3, 4])
        student.phone = f"98765{idx:05d}"
        student.save()
        students.append(student)
    print(f"Created/Updated {len(students)} student profiles.")

    # 8. Create Library Books (20 Books)
    books = []
    book_titles = [
        ("Introduction to Algorithms", "Thomas H. Cormen", "Computer Science"),
        ("Database System Concepts", "Abraham Silberschatz", "Computer Science"),
        ("Computer Networking", "James F. Kurose", "Computer Science"),
        ("Concepts of Modern Physics", "Arthur Beiser", "Physics"),
        ("Introduction to Electrodynamics", "David J. Griffiths", "Physics"),
        ("Organic Chemistry", "Morrison & Boyd", "Chemistry"),
        ("Inorganic Chemistry", "Gary L. Miessler", "Chemistry"),
        ("Calculus", "Michael Spivak", "Mathematics"),
        ("Linear Algebra and Its Applications", "Gilbert Strang", "Mathematics"),
        ("The Riverside Shakespeare", "William Shakespeare", "English Literature"),
        ("A History of English Literature", "Arthur Compton-Rickett", "English Literature"),
        ("Financial Accounting", "R. Narayanaswamy", "Business Commerce"),
        ("Marketing Management", "Philip Kotler", "Business Commerce"),
    ]
    for idx, (title, author, dept_name) in enumerate(book_titles):
        book = Book.objects.create(
            title=title,
            author=author,
            isbn=f"978-0-13-{100000+idx}",
            category=dept_name,
            total_quantity=5,
            available_quantity=random.choice([2, 3, 4, 5]),
            department=dept_name,
            description=f"A standard reference textbook for {dept_name} courses."
        )
        books.append(book)
    print(f"Created {len(books)} library books.")

    # 9. Create Library Borrow Records
    for _ in range(25):
        student_user = random.choice(students).user
        book = random.choice(books)
        is_returned = random.choice([True, False])
        issue_d = timezone.now() - timedelta(days=random.randint(1, 30))
        due_d = issue_d + timedelta(days=14)
        ret_d = issue_d + timedelta(days=random.randint(1, 15)) if is_returned else None

        BorrowRecord.objects.create(
            student=student_user,
            book=book,
            issue_date=issue_d,
            due_date=due_d,
            return_date=ret_d
        )
    print("Created library borrow records.")

    # 10. Create Asset Locations & Assets
    locations = [
        Location.objects.create(building="Main Block", room="Lab 101"),
        Location.objects.create(building="Main Block", room="Lab 102"),
        Location.objects.create(building="Science Block", room="Physics Lab"),
        Location.objects.create(building="Science Block", room="Chemistry Lab"),
        Location.objects.create(building="Library Building", room="Reading Hall"),
        Location.objects.create(building="Admin Block", room="Office Room 1"),
    ]

    assets = []
    asset_samples = [
        ("Desktop Computer", "Electronics", "Computer Science", 30),
        ("LCD Projector", "Electronics", "Computer Science", 4),
        ("Oscilloscope", "Lab Instrument", "Physics", 10),
        ("Centrifuge", "Lab Instrument", "Chemistry", 5),
        ("Air Conditioner", "Electrical", "Library Building", 6),
        ("Printer", "Office Supply", "Admin Block", 3)
    ]
    for name, cat, dept, qty in asset_samples:
        loc = random.choice(locations)
        working_qty = qty - random.randint(0, 3)
        asset = Asset.objects.create(
            name=name,
            category=cat,
            department=dept,
            location=loc,
            total_quantity=qty,
            working_quantity=working_qty,
            status='working' if working_qty == qty else 'repair',
            scope='LAB' if 'Lab' in cat or 'Instrument' in cat else 'GENERAL'
        )
        assets.append(asset)
    print(f"Created {len(assets)} assets.")

    # 11. Create Asset Issues
    for _ in range(8):
        asset = random.choice(assets)
        staff_user = random.choice(staffs).user
        priority = random.choice(['low', 'medium', 'high'])
        status = random.choice(['open', 'repair', 'completed'])
        resolved_d = timezone.now() if status == 'completed' else None

        AssetIssue.objects.create(
            asset=asset,
            reported_by=staff_user,
            issue_text=f"Issues with the {asset.name} performance. Needs maintenance check.",
            priority=priority,
            resolved_at=resolved_d,
            status=status
        )
    print("Created asset issues.")

    # 12. Create Events & Registrations
    events = [
        ("TechFest 2026", "Technical", "Annual national technical symposium"),
        ("Sports Meet", "Sports", "Inter-department sports event"),
        ("Cultural Fest", "Cultural", "College cultural festival"),
        ("Physics Workshop", "Workshop", "Hands-on seminar on electromagnetism"),
        ("Management Seminar", "Seminar", "Financial accounting methodologies"),
    ]
    for idx, (title, etype, desc) in enumerate(events):
        event = Event.objects.create(
            title=title,
            type=etype,
            description=desc,
            date=date.today() + timedelta(days=random.randint(1, 30)),
            time=(timezone.now() + timedelta(hours=random.randint(1, 6))).time(),
            registration_deadline_date=date.today() + timedelta(days=random.randint(1, 10)),
            registration_deadline_time=(timezone.now() + timedelta(hours=random.randint(1, 6))).time(),
            place=f"Seminar Hall {idx+1}" if etype != "Sports" else "Main Sports Field",
            rules="Standard college guidelines apply.",
            max_participants=100
        )
        
        # Staff incharge
        EventStaffIncharge.objects.create(event=event, staff=random.choice(staffs).user)
        # Student head
        EventStudentHead.objects.create(event=event, student=random.choice(students).user)

        # Event registrations (random students registering)
        for student in random.sample(students, k=random.randint(5, 12)):
            EventRegistration.objects.get_or_create(event=event, student=student.user)
    print(f"Created {len(events)} events and registrations.")

    # 13. Create Projects
    project_samples = [
        ("AI chatbot for College Website", "Team Alpha", "Computer Science", "Artificial Intelligence"),
        ("Realtime Weather Predictor", "Team Delta", "Computer Science", "Data Science"),
        ("Fiber Optic Waveguide Analysis", "Photonics Team", "Physics", "Optics"),
        ("Green Synthesis of Nanoparticles", "Bio-Chem Lab", "Chemistry", "Nanochemistry"),
        ("Analysis of E-Commerce Growth", "Market Analysts", "Business Commerce", "Commerce"),
    ]
    for idx, (title, tname, dept_name, domain) in enumerate(project_samples):
        student_leader = random.choice(students)
        staff_guide = random.choice(staffs)
        proj_dept = random.choice(projects_depts)
        
        project = Project.objects.create(
            title=title,
            team_name=tname,
            department=proj_dept,
            domain=domain,
            abstract=f"An in-depth study and implementation of {title}.",
            technology_used="Python, Django, React, PostgreSQL",
            created_by=student_leader.user,
            guide_staff=staff_guide.user,
            year=3,
            deadline=date.today() + timedelta(days=random.randint(30, 90)),
            status=random.choice(['ONGOING', 'COMPLETED', 'ARCHIVE'])
        )

        # Team members
        ProjectMember.objects.create(project=project, student=student_leader.user, is_leader=True)
        for s in random.sample(students, k=2):
            if s != student_leader:
                ProjectMember.objects.get_or_create(project=project, student=s.user, defaults={"is_leader": False})

        # Progress
        steps = ['IDEA', 'PROPOSAL', 'PHASE1', 'PHASE2', 'FINAL']
        for step in steps[:random.randint(2, 5)]:
            ProjectProgress.objects.create(
                project=project,
                step_name=step,
                description=f"Completed {step} checkpoint tasks.",
                approved_by_staff=random.choice([True, False])
            )
    print(f"Created {len(project_samples)} projects.")

    # 14. Create Attendance & Records
    for s in staffs:
        for offset in range(3):
            att_date = date.today() - timedelta(days=offset)
            att = Attendance.objects.create(
                staff=s,
                date=att_date,
                status="Present"
            )
            dept_students = [stud for stud in students if stud.department == s.department]
            if not dept_students:
                dept_students = students[:10]
            
            for student in dept_students:
                AttendanceRecord.objects.create(
                    attendance=att,
                    student=student,
                    present=random.choices([True, False], weights=[0.85, 0.15])[0]
                )
    print("Created attendance logs and records.")

    # 15. Create Exams
    exams = []
    exam_names = ["Internal Test 1", "Internal Test 2", "Semester Finals"]
    for name in exam_names:
        exam = Exam.objects.create(
            name=name,
            exam_date=date.today() - timedelta(days=random.randint(1, 20)),
            course="General"
        )
        exams.append(exam)
    print(f"Created {len(exams)} exams.")

    # 16. Create Marks
    for student in students:
        selected_subjects = random.sample(subjects, min(len(subjects), 3))
        for idx, sub in enumerate(selected_subjects):
            exam = random.choice(exams)
            staff = random.choice(staffs)
            internal = random.randint(15, 25)
            sem_mark = random.randint(30, 75)
            
            Marks.objects.create(
                student=student,
                subject=sub.name,
                exam=exam,
                internal_mark=internal,
                semester_mark=sem_mark,
                graded_by=staff
            )
    print("Created marks records.")

    # 17. Create Fees, Payments, Scholarships
    for student in students:
        total_amt = Decimal("25000.00")
        paid_amt = Decimal("0.00")
        scholarship_amt = Decimal("0.00")
        has_scholarship = random.choices([True, False], weights=[0.2, 0.8])[0]
        if has_scholarship:
            scholarship_amt = Decimal(random.choice([3000, 5000, 7500]))
            
        fee = Fee.objects.create(
            student=student,
            total_amount=total_amt,
            paid_amount=paid_amt,
            due_amount=total_amt - scholarship_amt,
            status="DUE"
        )
        
        if has_scholarship:
            Scholarship.objects.create(
                student=student,
                amount=scholarship_amt,
                reason="Merit Cum Means Scholarship"
            )
            fee.refresh_from_db()

        payment_status = random.choice(["FULL", "PARTIAL", "NONE"])
        if payment_status == "FULL":
            payable = fee.total_amount
            FeePayment.objects.create(fee=fee, amount_paid=payable, method="Online Banking")
            fee.refresh_from_db()
            fee.status = "PAID"
            fee.save()
        elif payment_status == "PARTIAL":
            payable = fee.total_amount / 2
            FeePayment.objects.create(fee=fee, amount_paid=payable, method="UPI")
            fee.refresh_from_db()
            fee.status = "DUE"
            fee.save()
    print("Created fee records, payments, and scholarships.")

    # 18. Create Complaints
    complaints = [
        ("Library", "Medium", "Library Building", "Need more copies of Algorithms textbook.", False, "Pending"),
        ("Infrastructure", "High", "Science Block", "Oscilloscopes in physics lab need calibration.", True, "Pending"),
        ("Hostel", "Low", "Hostel Block A", "Wifi connection is intermittent in third floor.", True, "Resolved"),
        ("Academics", "Medium", "Main Block", "Requesting additional remedial classes for DBMS course.", False, "Pending")
    ]
    for cat, urg, dept_loc, desc, is_anon, status in complaints:
        Complaint.objects.create(
            category=cat,
            urgency=urg,
            department=dept_loc,
            description=desc,
            is_anonymous=is_anon,
            status=status
        )
    print("Created complaints.")

    # 19. Create Notifications and Targets
    notifs = [
        ("📢 Annual Sports Day registration open", "Sports registration starts today. Please register on the portal.", "general", "normal"),
        ("⚠️ Pending Fees Alert", "All students are requested to clear their tuition fee dues.", "fee", "high"),
        ("📝 Final Semester Exam Schedule Released", "Semester finals start from next month. View schedule in Academics.", "exam", "high")
    ]
    for title, msg, cat, prio in notifs:
        notif = Notification.objects.create(
            title=title,
            message=msg,
            category=cat,
            priority=prio,
            expires_at=timezone.now() + timedelta(days=30)
        )
        for student in students:
            NotificationTarget.objects.create(
                notification=notif,
                user=student.user,
                is_read=random.choice([True, False])
            )
    print("Created notifications and targets.")
    print("\nDATABASE SUCCESSFULLY POPULATED WITH SAMPLE DATA!")

if __name__ == "__main__":
    clear_data()
    populate()
