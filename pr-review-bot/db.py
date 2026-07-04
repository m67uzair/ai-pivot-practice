import os
from datetime import datetime
from pathlib import Path

from sqlalchemy import ForeignKey, create_engine, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

from models import Review

_DB_PATH = Path(__file__).parent / "reviews.db"


def _database_url() -> str:
    # Railway (and most hosts) inject DATABASE_URL; local dev falls back to SQLite.
    url = os.environ.get("DATABASE_URL")
    if not url:
        return f"sqlite:///{_DB_PATH}"
    # SQLAlchemy 2.0 drives Postgres via psycopg (v3) — rewrite the scheme so the
    # `postgresql://…` Railway hands us uses that driver.
    for prefix in ("postgresql://", "postgres://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


engine = create_engine(_database_url())
SessionLocal = sessionmaker(bind=engine)   # call SessionLocal() to get a session


class Base(DeclarativeBase):
    pass


class StoredReview(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    repo: Mapped[str]
    pr_number: Mapped[int]
    summary: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    issues: Mapped[list["StoredIssue"]] = relationship(
        back_populates="review", cascade="all, delete-orphan"
    )


class StoredIssue(Base):
    __tablename__ = "issue"

    id: Mapped[int] = mapped_column(primary_key=True)
    review_id: Mapped[int] = mapped_column(ForeignKey("review.id"))
    severity: Mapped[str]
    title: Mapped[str]
    file: Mapped[str]
    explanation: Mapped[str]
    suggested_fix: Mapped[str]

    review: Mapped["StoredReview"] = relationship(back_populates="issues")


def save_review(repo: str, pr_number: int, review: Review) -> int:
    with SessionLocal() as session:
        row = StoredReview(
            repo=repo,
            pr_number=pr_number,
            summary=review.summary,
            # Assigning child objects sets their review_id automatically on commit.
            issues=[
                StoredIssue(
                    severity=i.severity.value,
                    title=i.title,
                    file=i.file,
                    explanation=i.explanation,
                    suggested_fix=i.suggested_fix,
                )
                for i in review.issues
            ],
        )
        session.add(row)      # stage the parent (children cascade in)
        session.commit()      # one transaction: INSERT review + INSERTs issues
        return row.id
