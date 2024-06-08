from typing import TYPE_CHECKING

from taskiq import TaskiqScheduler
from taskiq_redis import ListQueueBroker, RedisScheduleSource

from loader import redis_link

if TYPE_CHECKING:  # pragma: no cover
    from taskiq.abc.broker import AsyncBroker
    from taskiq.abc.schedule_source import ScheduleSource

broker = ListQueueBroker(redis_link)

redis_source = RedisScheduleSource(redis_link)

scheduler = TaskiqScheduler(broker, sources=[redis_source])
