from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg, Count
from .models import Candidate, Question, Result, Subject, Test


# ── Inlines ────────────────────────────────────────────────
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('que', 'a', 'b', 'c', 'd', 'ans')
    show_change_link = True


class TestInline(admin.TabularInline):
    model = Test
    extra = 1
    show_change_link = True


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0
    readonly_fields = ('date', 'time', 'attempt', 'right', 'wrong', 'score_display')
    fields = ('date', 'time', 'attempt', 'right', 'wrong', 'score_display')
    can_delete = False

    def score_display(self, obj):
        color = 'green' if obj.points >= 5 else ('orange' if obj.points >= 3 else 'red')
        return format_html('<b style="color:{}">{:.1f}/10</b>', color, obj.points)
    score_display.short_description = 'Score'


# ── Subject ─────────────────────────────────────────────────
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'test_count')
    search_fields = ('name',)
    inlines = [TestInline]

    def test_count(self, obj):
        count = obj.test_set.count()
        return format_html('<b style="color:#1e4c63">{}</b>', count)
    test_count.short_description = 'Tests'


# ── Test ────────────────────────────────────────────────────
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject', 'question_count', 'status_badge')
    search_fields = ('name', 'subject__name')
    list_filter = ('subject',)
    inlines = [QuestionInline]

    def question_count(self, obj):
        return obj.question_set.count()
    question_count.short_description = 'Questions'

    def status_badge(self, obj):
        count = obj.question_set.count()
        if count >= 10:
            return format_html('<span style="background:#198754;color:#fff;padding:2px 10px;border-radius:12px;font-size:.82em;">✓ Ready</span>')
        return format_html('<span style="background:#dc3545;color:#fff;padding:2px 10px;border-radius:12px;font-size:.82em;">Need {} more</span>', 10 - count)
    status_badge.short_description = 'Status'


# ── Candidate ────────────────────────────────────────────────
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'testattemped', 'avg_score_display', 'performance_bar')
    search_fields = ('username', 'name')
    list_filter = ('testattemped',)
    readonly_fields = ('testattemped', 'points', 'full_result_history')
    inlines = [ResultInline]

    fieldsets = (
        ('Student Info', {
            'fields': ('username', 'name', 'password')
        }),
        ('Performance Summary', {
            'fields': ('testattemped', 'points', 'full_result_history'),
        }),
    )

    def avg_score_display(self, obj):
        score = round(obj.points, 2)
        color = '#198754' if score >= 5 else ('#fd7e14' if score >= 3 else '#dc3545')
        return format_html('<b style="color:{};font-size:1.05em;">{}/10</b>', color, score)
    avg_score_display.short_description = 'Avg Score'

    def performance_bar(self, obj):
        pct = min(int(obj.points * 10), 100)
        color = '#198754' if obj.points >= 5 else ('#fd7e14' if obj.points >= 3 else '#dc3545')
        return format_html(
            '<div style="width:120px;background:#eee;border-radius:6px;height:12px;">'
            '<div style="width:{}%;background:{};height:12px;border-radius:6px;"></div></div>',
            pct, color
        )
    performance_bar.short_description = 'Score Bar'

    def full_result_history(self, obj):
        results = Result.objects.filter(username=obj).order_by('-date', '-time')
        if not results:
            return "No tests taken yet."
        rows = ''.join(
            f'<tr style="border-bottom:1px solid #eee;">'
            f'<td style="padding:4px 10px;">{r.date}</td>'
            f'<td style="padding:4px 10px;">{r.time}</td>'
            f'<td style="padding:4px 10px;color:green;font-weight:bold;">{r.right}</td>'
            f'<td style="padding:4px 10px;color:red;font-weight:bold;">{r.wrong}</td>'
            f'<td style="padding:4px 10px;font-weight:bold;">{r.points:.1f}/10</td>'
            f'</tr>'
            for r in results
        )
        return format_html(
            '<table style="border-collapse:collapse;width:100%;font-size:.9em;">'
            '<thead><tr style="background:#1e4c63;color:#fff;">'
            '<th style="padding:5px 10px;">Date</th><th style="padding:5px 10px;">Time</th>'
            '<th style="padding:5px 10px;">Correct</th><th style="padding:5px 10px;">Wrong</th>'
            '<th style="padding:5px 10px;">Score</th></tr></thead>'
            '<tbody>{}</tbody></table>', format_html(rows)
        )
    full_result_history.short_description = 'Full Test History'


# ── Question ─────────────────────────────────────────────────
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qid', 'test', 'subject_name', 'short_question', 'ans')
    search_fields = ('que',)
    list_filter = ('test__subject', 'test', 'ans')

    def subject_name(self, obj):
        return obj.test.subject.name
    subject_name.short_description = 'Subject'

    def short_question(self, obj):
        return obj.que[:80] + '...' if len(obj.que) > 80 else obj.que
    short_question.short_description = 'Question'


# ── Result ───────────────────────────────────────────────────
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('resultid', 'student_name', 'username_display', 'date', 'time',
                    'attempt', 'right', 'wrong', 'score_badge', 'grade_label')
    search_fields = ('username__username', 'username__name')
    list_filter = ('date', 'username')
    readonly_fields = ('resultid', 'date', 'time')
    date_hierarchy = 'date'

    def student_name(self, obj):
        return obj.username.name
    student_name.short_description = 'Full Name'

    def username_display(self, obj):
        return obj.username.username
    username_display.short_description = 'Username'

    def score_badge(self, obj):
        color = '#198754' if obj.points >= 5 else ('#fd7e14' if obj.points >= 3 else '#dc3545')
        return format_html('<b style="color:{};font-size:1.05em;">{:.1f}/10</b>', color, obj.points)
    score_badge.short_description = 'Score'

    def grade_label(self, obj):
        if obj.points >= 7:
            return format_html('<span style="background:#198754;color:#fff;padding:2px 10px;border-radius:12px;font-size:.82em;">🏆 Excellent</span>')
        elif obj.points >= 5:
            return format_html('<span style="background:#0d6efd;color:#fff;padding:2px 10px;border-radius:12px;font-size:.82em;">✅ Pass</span>')
        elif obj.points >= 3:
            return format_html('<span style="background:#fd7e14;color:#fff;padding:2px 10px;border-radius:12px;font-size:.82em;">📝 Average</span>')
        return format_html('<span style="background:#dc3545;color:#fff;padding:2px 10px;border-radius:12px;font-size:.82em;">📚 Fail</span>')
    grade_label.short_description = 'Grade'
