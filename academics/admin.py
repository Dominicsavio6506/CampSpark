from django.contrib import admin
from .models import *
from .models import Timetable
from .models import Exam
from .models import TimeSlot, Classroom, SmartTimetable


admin.site.register(Exam)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(FacultySubjectAssign)
admin.site.register(Timetable)
admin.site.register(TimeSlot)
admin.site.register(Classroom)
admin.site.register(SmartTimetable)
