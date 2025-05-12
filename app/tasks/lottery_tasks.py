from app.tasks.celery_worker import celery_app
from app.services.lottery_service import LotteryService
from app.database.session import get_db
from app.core.logging import logger
from datetime import datetime
from zoneinfo import ZoneInfo

@celery_app.task(name="app.tasks.lottery_tasks.pick_today_lottery_winner")
def pick_today_lottery_winner():
    """Select a winner for today's lottery.

    This task is scheduled to run at midnight every day.
    It selects a random winner from all ballots submitted for the previous day's lottery.
    The task is managed by Celery Beat scheduler.

    Note:
        This task should be scheduled to run at midnight (00:00) in the Europe/Amsterdam timezone.
        The actual winner selection logic is handled by LotteryService.pick_today_winner.
    """
    try:
        now = datetime.now(ZoneInfo("Europe/Amsterdam"))
        logger.info(f"Task running at {now} (hour: {now.hour})")
        db = next(get_db())
        LotteryService.pick_today_winner(db=db)
    except Exception as e:
        logger.error(f"Error in lottery winner selection task: {str(e)}", exc_info=True)
        raise
