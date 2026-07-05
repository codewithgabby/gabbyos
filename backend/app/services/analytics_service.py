from typing import List, Optional
from uuid import UUID
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.daily_log import DailyLog
from app.models.routine import Routine
from app.models.category import Category
from app.models.project import Project
from app.models.project_task import ProjectTask
from app.models.knowledge_item import KnowledgeItem
from app.models.inbox_item import InboxItem
from app.models.streak import Streak
from app.models.reflection import Reflection
from app.models.goal import Goal
from app.core.constants import LogStatus, ProjectStatus, KnowledgeStatus, GoalStatus


class AnalyticsService:
    """Service for all analytics and insights"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_full_analytics(self, user_id: UUID) -> dict:
        """Get complete analytics dashboard"""
        today = date.today()
        
        return {
            "completion_rates": self._get_completion_rates(user_id, today),
            "hours_by_category": self._get_hours_by_category(user_id, today),
            "top_routines": self._get_top_routines(user_id),
            "bottom_routines": self._get_bottom_routines(user_id),
            "current_streaks": self._get_streaks_summary(user_id),
            "projects_summary": self._get_projects_summary(user_id),
            "knowledge_summary": self._get_knowledge_summary(user_id),
            "recent_activity": self._get_recent_activity(user_id),
            "inbox_count": self._get_inbox_count(user_id),
            "overview": self._get_overview(user_id, today)
        }
    
    def _get_completion_rates(self, user_id: UUID, today: date) -> dict:
        """Calculate daily, weekly, monthly completion rates"""
        
        # Daily
        daily_logs = self.db.query(DailyLog).filter(
            DailyLog.user_id == user_id,
            DailyLog.log_date == today,
            DailyLog.is_deleted == False
        ).all()
        
        daily_total = len(daily_logs)
        daily_completed = sum(1 for log in daily_logs if log.status == LogStatus.COMPLETED)
        daily_rate = round((daily_completed / daily_total * 100), 1) if daily_total > 0 else 0
        
        # Weekly
        week_start = today - timedelta(days=today.weekday())
        weekly_logs = self.db.query(DailyLog).filter(
            DailyLog.user_id == user_id,
            DailyLog.log_date >= week_start,
            DailyLog.log_date <= today,
            DailyLog.is_deleted == False
        ).all()
        
        weekly_total = len(weekly_logs)
        weekly_completed = sum(1 for log in weekly_logs if log.status == LogStatus.COMPLETED)
        weekly_rate = round((weekly_completed / weekly_total * 100), 1) if weekly_total > 0 else 0
        
        # Monthly
        month_start = today.replace(day=1)
        monthly_logs = self.db.query(DailyLog).filter(
            DailyLog.user_id == user_id,
            DailyLog.log_date >= month_start,
            DailyLog.log_date <= today,
            DailyLog.is_deleted == False
        ).all()
        
        monthly_total = len(monthly_logs)
        monthly_completed = sum(1 for log in monthly_logs if log.status == LogStatus.COMPLETED)
        monthly_rate = round((monthly_completed / monthly_total * 100), 1) if monthly_total > 0 else 0
        
        return {
            "daily": {
                "date": today,
                "total": daily_total,
                "completed": daily_completed,
                "percentage": daily_rate
            },
            "weekly": {
                "start_date": week_start,
                "end_date": today,
                "total": weekly_total,
                "completed": weekly_completed,
                "percentage": weekly_rate
            },
            "monthly": {
                "start_date": month_start,
                "end_date": today,
                "total": monthly_total,
                "completed": monthly_completed,
                "percentage": monthly_rate
            }
        }
    
    def _get_hours_by_category(self, user_id: UUID, today: date) -> list:
        """Calculate hours spent by category from completed logs"""
        week_start = today - timedelta(days=today.weekday())
        
        results = self.db.query(
            Category.name,
            Category.color,
            func.sum(Routine.duration_minutes).label('total_minutes'),
            func.count(DailyLog.id).label('completed_count')
        ).join(
            Routine, Routine.category_id == Category.id
        ).join(
            DailyLog, DailyLog.routine_id == Routine.id
        ).filter(
            DailyLog.user_id == user_id,
            DailyLog.log_date >= week_start,
            DailyLog.status == LogStatus.COMPLETED,
            DailyLog.is_deleted == False
        ).group_by(
            Category.name, Category.color
        ).order_by(
            func.sum(Routine.duration_minutes).desc()
        ).all()
        
        return [
            {
                "category": name,
                "color": color,
                "hours": round(total_minutes / 60, 1),
                "completed_routines": completed_count
            }
            for name, color, total_minutes, completed_count in results
        ]
    
    def _get_top_routines(self, user_id: UUID) -> list:
        """Get most completed routines"""
        results = self.db.query(
            Routine.title,
            Category.name,
            func.count(DailyLog.id).label('completion_count')
        ).join(
            DailyLog, DailyLog.routine_id == Routine.id
        ).outerjoin(
            Category, Routine.category_id == Category.id
        ).filter(
            DailyLog.user_id == user_id,
            DailyLog.status == LogStatus.COMPLETED,
            DailyLog.is_deleted == False
        ).group_by(
            Routine.title, Category.name
        ).order_by(
            func.count(DailyLog.id).desc()
        ).limit(5).all()
        
        return [
            {
                "routine": title,
                "category": category_name,
                "completions": count
            }
            for title, category_name, count in results
        ]
    
    def _get_bottom_routines(self, user_id: UUID) -> list:
        """Get least completed routines"""
        results = self.db.query(
            Routine.title,
            Category.name,
            func.count(DailyLog.id).label('completion_count')
        ).join(
            DailyLog, DailyLog.routine_id == Routine.id
        ).outerjoin(
            Category, Routine.category_id == Category.id
        ).filter(
            DailyLog.user_id == user_id,
            DailyLog.is_deleted == False
        ).group_by(
            Routine.title, Category.name
        ).order_by(
            func.count(DailyLog.id).asc()
        ).limit(5).all()
        
        return [
            {
                "routine": title,
                "category": category_name,
                "completions": count
            }
            for title, category_name, count in results
        ]
    
    def _get_streaks_summary(self, user_id: UUID) -> dict:
        """Get streaks overview"""
        streaks = self.db.query(Streak).join(
            Routine, Streak.routine_id == Routine.id
        ).filter(
            Streak.user_id == user_id,
            Streak.is_deleted == False,
            Streak.current_streak > 0
        ).order_by(Streak.current_streak.desc()).all()
        
        return {
            "total_active": len(streaks),
            "top_streaks": [
                {
                    "routine": streak.routine.title if streak.routine else "Unknown",
                    "current_streak": streak.current_streak,
                    "longest_streak": streak.longest_streak
                }
                for streak in streaks[:5]
            ]
        }
    
    def _get_projects_summary(self, user_id: UUID) -> dict:
        """Get projects overview"""
        total = self.db.query(Project).filter(
            Project.user_id == user_id,
            Project.is_deleted == False
        ).count()
        
        in_progress = self.db.query(Project).filter(
            Project.user_id == user_id,
            Project.status == ProjectStatus.IN_PROGRESS,
            Project.is_deleted == False
        ).count()
        
        planned = self.db.query(Project).filter(
            Project.user_id == user_id,
            Project.status == ProjectStatus.PLANNED,
            Project.is_deleted == False
        ).count()
        
        completed = self.db.query(Project).filter(
            Project.user_id == user_id,
            Project.status == ProjectStatus.COMPLETED,
            Project.is_deleted == False
        ).count()
        
        return {
            "total": total,
            "in_progress": in_progress,
            "planned": planned,
            "completed": completed
        }
    
    def _get_knowledge_summary(self, user_id: UUID) -> dict:
        """Get knowledge workspace overview"""
        total = self.db.query(KnowledgeItem).filter(
            KnowledgeItem.user_id == user_id,
            KnowledgeItem.is_deleted == False
        ).count()
        
        in_progress = self.db.query(KnowledgeItem).filter(
            KnowledgeItem.user_id == user_id,
            KnowledgeItem.status == KnowledgeStatus.IN_PROGRESS,
            KnowledgeItem.is_deleted == False
        ).count()
        
        completed = self.db.query(KnowledgeItem).filter(
            KnowledgeItem.user_id == user_id,
            KnowledgeItem.status == KnowledgeStatus.COMPLETED,
            KnowledgeItem.is_deleted == False
        ).count()
        
        inbox_count = self.db.query(KnowledgeItem).filter(
            KnowledgeItem.user_id == user_id,
            KnowledgeItem.status == KnowledgeStatus.INBOX,
            KnowledgeItem.is_deleted == False
        ).count()
        
        return {
            "total": total,
            "in_progress": in_progress,
            "completed": completed,
            "inbox": inbox_count
        }
    
    def _get_recent_activity(self, user_id: UUID) -> dict:
        """Get recently added and completed items"""
        # Recently added knowledge items
        recent_knowledge = self.db.query(KnowledgeItem).filter(
            KnowledgeItem.user_id == user_id,
            KnowledgeItem.is_deleted == False
        ).order_by(KnowledgeItem.created_at.desc()).limit(5).all()
        
        # Recently completed daily logs
        recent_completed = self.db.query(DailyLog).join(
            Routine, DailyLog.routine_id == Routine.id
        ).filter(
            DailyLog.user_id == user_id,
            DailyLog.status == LogStatus.COMPLETED,
            DailyLog.is_deleted == False
        ).order_by(DailyLog.completed_at.desc().nullslast()).limit(5).all()
        
        return {
            "recently_added": [
                {
                    "title": item.title,
                    "type": "knowledge",
                    "date": item.created_at
                }
                for item in recent_knowledge
            ],
            "recently_completed": [
                {
                    "title": log.routine.title if log.routine else "Unknown",
                    "type": "routine",
                    "date": log.completed_at
                }
                for log in recent_completed
            ]
        }
    
    def _get_inbox_count(self, user_id: UUID) -> int:
        """Get unorganized inbox count"""
        return self.db.query(InboxItem).filter(
            InboxItem.user_id == user_id,
            InboxItem.is_organized == False,
            InboxItem.is_deleted == False
        ).count()
    
    def _get_overview(self, user_id: UUID, today: date) -> dict:
        """Get overall system overview"""
        return {
            "total_routines": self.db.query(Routine).filter(
                Routine.user_id == user_id, Routine.is_active == True, Routine.is_deleted == False
            ).count(),
            "total_goals": self.db.query(Goal).filter(
                Goal.user_id == user_id, Goal.status.in_([GoalStatus.NOT_STARTED, GoalStatus.IN_PROGRESS]), Goal.is_deleted == False
            ).count(),
            "total_projects": self.db.query(Project).filter(
                Project.user_id == user_id, Project.status.in_([ProjectStatus.PLANNED, ProjectStatus.IN_PROGRESS]), Project.is_deleted == False
            ).count(),
            "total_knowledge_items": self.db.query(KnowledgeItem).filter(
                KnowledgeItem.user_id == user_id, KnowledgeItem.status.in_([KnowledgeStatus.INBOX, KnowledgeStatus.PLANNED, KnowledgeStatus.IN_PROGRESS]), KnowledgeItem.is_deleted == False
            ).count(),
            "total_reflections": self.db.query(Reflection).filter(
                Reflection.user_id == user_id, Reflection.is_deleted == False
            ).count(),
            "today_reflection": self.db.query(Reflection).filter(
                Reflection.user_id == user_id, Reflection.reflection_date == today, Reflection.is_deleted == False
            ).first() is not None
        }