from sqlalchemy.orm import Session
import random
from zoneinfo import ZoneInfo
from datetime import date, datetime, timedelta
from app.models import Lottery
from app.crud.lottery_crud import LotteryCRUD
from app.crud.ballot_crud import BallotCRUD
from app.crud.winning_ballot_crud import WinningBallotCRUD
from app.schemas.lottery import UpcomingLottery, UpcomingLotteriesResponse


class LotteryService:
    """Service handling lottery operations and winner selection.
    """

    @staticmethod
    def get_or_create_lottery_by_draw_date(db: Session, draw_date: date) -> Lottery:
        lottery = LotteryCRUD.get_by_draw_date(db=db, draw_date=draw_date)
        if not lottery:
            lottery = LotteryCRUD.create(db=db, draw_date=draw_date)
        return lottery

    @staticmethod
    def pick_today_winner(db: Session):
        """Select a winner for the lottery.

        This method selects a winner for either today's or yesterday's lottery based on the current hour:
        - If current hour is 0 (midnight), selects yesterday's lottery
        - Otherwise, selects today's lottery

        The method is called by a Celery task scheduled to run at midnight.
        Even if the task runs slightly before or after midnight, the hour check ensures
        we select the correct lottery.
        """
        now = datetime.now(ZoneInfo("Europe/Amsterdam"))
        
        # If it's midnight (hour 0), select yesterday's lottery
        # Otherwise, select today's lottery
        if now.hour == 0:
            draw_date = now.date() - timedelta(days=1)
        else:
            draw_date = now.date()
        
        lottery = LotteryCRUD.get_by_draw_date(db=db, draw_date=draw_date)

        if lottery:
            ballots = BallotCRUD.get_by_lottery_id(db=db, lottery_id=lottery.id)
            
            if ballots:
                winning_ballot = random.choice(ballots)                
                try:
                    # Create winning ballot
                    winning_ballot = WinningBallotCRUD.create(
                        db=db,
                        ballot_id=winning_ballot.id,
                    )
                    db.commit()
                except Exception as e:
                    db.rollback()

    @staticmethod
    def get_upcoming(db: Session) -> UpcomingLotteriesResponse:
        """Get all upcoming lotteries with their ballot counts.
        
        Returns:
            UpcomingLotteriesResponse: Response containing list of upcoming lotteries with their ballot counts
        """
        lotteries = LotteryCRUD.get_upcoming(db=db)
        return UpcomingLotteriesResponse(
            lotteries=[
                UpcomingLottery(
                    lottery_id=lottery.id,
                    draw_date=lottery.draw_date,
                    ballot_count=ballot_count
                )
                for lottery, ballot_count in lotteries
            ]
        )
