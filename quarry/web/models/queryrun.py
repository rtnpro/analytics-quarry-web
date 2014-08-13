from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from base import Base
from queryrevision import QueryRevision  # noqa


class QueryRun(Base):
    STATUS_QUEUED = 0
    STATUS_FAILED = 1
    STATUS_RUNNING = 2
    STATUS_KILLED = 3
    STATUS_COMPLETE = 4
    STATUS_SUPERSEDED = 5

    # TODO (phuedx, 2014/08/08): Make this translatable.
    STATUS_MESSAGES = [
        'queued',
        'failed',
        'running',
        'killed',
        'complete',
        'superseded'
    ]

    __tablename__ = 'query_run'

    id = Column(Integer, primary_key=True)
    query_rev_id = Column(Integer, ForeignKey('query_revision.id'))
    status = Column(Integer)
    timestamp = Column(DateTime)
    task_id = Column(String)

    rev = relationship('QueryRevision', uselist=False, primaryjoin='QueryRevision.id == QueryRun.query_rev_id')

    @property
    def status_message(self):
        return QueryRun.STATUS_MESSAGES[self.status]

    # Stick with "augmented" as common language.
    @property
    def augmented_sql(self):
        return "/* Run by Quarry for User %s as qrun id %s */ %s" % (
            self.rev.query.user.username,
            self.id,
            self.rev.text
        )
