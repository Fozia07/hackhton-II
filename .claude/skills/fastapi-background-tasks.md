# FastAPI Background Tasks & Async Workers

## Expertise
Expert skill for implementing background tasks and asynchronous workers in FastAPI applications. Specializes in FastAPI BackgroundTasks, Celery integration, Redis Queue, task monitoring, error handling, retries, and scheduled tasks for production workloads.

## Purpose
This skill handles asynchronous task processing, enabling you to:
- Execute long-running operations without blocking API responses
- Process tasks in background workers
- Schedule periodic tasks (cron-like jobs)
- Implement task queues with priority and retry logic
- Monitor task execution and handle failures
- Scale task processing horizontally
- Integrate with message brokers (Redis, RabbitMQ)
- Handle task results and callbacks

## When to Use
Use this skill when you need to:
- Send emails without blocking API responses
- Process file uploads asynchronously
- Generate reports or exports in the background
- Perform data synchronization or ETL operations
- Execute scheduled maintenance tasks
- Handle webhook processing
- Implement job queues for batch processing
- Scale task processing independently from API servers

## Core Concepts

### 1. FastAPI BackgroundTasks (Simple Tasks)

**Basic BackgroundTasks Usage**:
```python
from fastapi import BackgroundTasks, FastAPI
import time

app = FastAPI()

def send_email(email: str, message: str):
    """
    Background task to send email.
    Runs after response is sent to client.
    """
    time.sleep(2)  # Simulate email sending
    print(f"Email sent to {email}: {message}")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    message: str,
    background_tasks: BackgroundTasks
):
    """
    Send notification and return immediately.
    Email is sent in background.
    """
    background_tasks.add_task(send_email, email, message)
    return {"message": "Notification will be sent"}
```

**Multiple Background Tasks**:
```python
def log_activity(user_id: int, action: str):
    """Log user activity."""
    print(f"User {user_id} performed: {action}")

def update_analytics(action: str):
    """Update analytics."""
    print(f"Analytics updated for: {action}")

@app.post("/users/{user_id}/action")
async def perform_action(
    user_id: int,
    action: str,
    background_tasks: BackgroundTasks
):
    """
    Perform action with multiple background tasks.
    """
    # Add multiple tasks
    background_tasks.add_task(log_activity, user_id, action)
    background_tasks.add_task(update_analytics, action)

    return {"message": "Action completed"}
```

**Background Task with Dependency Injection**:
```python
from sqlmodel import Session
from core.dependencies import get_db

def process_order(order_id: int, db: Session):
    """
    Process order in background.
    Note: Create new session for background tasks.
    """
    # Process order logic
    order = db.get(Order, order_id)
    if order:
        order.status = "processing"
        db.commit()

@app.post("/orders/")
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create order and process in background.
    """
    # Create order
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Process in background (create new session)
    background_tasks.add_task(
        process_order,
        new_order.id,
        Session(engine)  # New session for background task
    )

    return new_order
```

**When to Use FastAPI BackgroundTasks**:
- Simple, short-running tasks (< 30 seconds)
- Tasks that don't need retry logic
- Tasks that can fail without critical impact
- Low-volume task processing
- Tasks that don't need monitoring

**When NOT to Use FastAPI BackgroundTasks**:
- Long-running tasks (> 1 minute)
- Tasks requiring retry logic
- High-volume task processing
- Tasks needing monitoring and observability
- Tasks requiring distributed processing

### 2. Celery Integration (Production Tasks)

**Celery Setup**:
```bash
# Install Celery and Redis
pip install celery[redis]
pip install redis
```

**Celery Configuration**:
```python
# core/celery_app.py
from celery import Celery
from core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["tasks.email_tasks", "tasks.report_tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Task routing
celery_app.conf.task_routes = {
    "tasks.email_tasks.*": {"queue": "emails"},
    "tasks.report_tasks.*": {"queue": "reports"},
}
```

**Celery Task Definition**:
```python
# tasks/email_tasks.py
from core.celery_app import celery_app
from services.email_service import EmailService
import logging

logger = logging.getLogger(__name__)

@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60
)
def send_email_task(self, to: str, subject: str, body: str):
    """
    Send email via Celery task.

    Args:
        to: Recipient email
        subject: Email subject
        body: Email body

    Raises:
        Retry: If email sending fails
    """
    try:
        logger.info(f"Sending email to {to}")
        email_service = EmailService()
        email_service.send(to=to, subject=subject, body=body)
        logger.info(f"Email sent successfully to {to}")
        return {"status": "sent", "to": to}

    except Exception as exc:
        logger.error(f"Failed to send email to {to}: {exc}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@celery_app.task
def send_bulk_emails(recipients: list[str], subject: str, body: str):
    """
    Send emails to multiple recipients.
    Uses Celery group for parallel execution.
    """
    from celery import group

    # Create group of tasks
    job = group(
        send_email_task.s(recipient, subject, body)
        for recipient in recipients
    )

    # Execute group
    result = job.apply_async()
    return {"task_id": result.id, "count": len(recipients)}
```

**Using Celery Tasks in FastAPI**:
```python
# routers/notifications.py
from fastapi import APIRouter, BackgroundTasks
from tasks.email_tasks import send_email_task, send_bulk_emails
from schemas.notification import NotificationCreate

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/send-email")
async def send_email(notification: NotificationCreate):
    """
    Send email asynchronously via Celery.
    Returns immediately with task ID.
    """
    task = send_email_task.delay(
        to=notification.email,
        subject=notification.subject,
        body=notification.body
    )

    return {
        "message": "Email queued for sending",
        "task_id": task.id
    }

@router.post("/send-bulk")
async def send_bulk(
    recipients: list[str],
    subject: str,
    body: str
):
    """
    Send bulk emails via Celery group.
    """
    result = send_bulk_emails.delay(recipients, subject, body)

    return {
        "message": f"Bulk email queued for {len(recipients)} recipients",
        "task_id": result.id
    }

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Get Celery task status.
    """
    from core.celery_app import celery_app

    task = celery_app.AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": task.state,
        "result": task.result if task.ready() else None,
        "error": str(task.info) if task.failed() else None
    }
```

**Celery Task with Database Access**:
```python
# tasks/report_tasks.py
from core.celery_app import celery_app
from sqlmodel import Session, create_engine, select
from core.config import get_settings
from models.report import Report
import logging

logger = logging.getLogger(__name__)
settings = get_settings()
engine = create_engine(settings.database_url)

@celery_app.task(bind=True)
def generate_report(self, report_id: int):
    """
    Generate report in background.
    Creates its own database session.
    """
    try:
        with Session(engine) as db:
            # Get report
            report = db.get(Report, report_id)
            if not report:
                raise ValueError(f"Report {report_id} not found")

            # Update status
            report.status = "processing"
            db.commit()

            # Generate report (expensive operation)
            logger.info(f"Generating report {report_id}")
            data = generate_report_data(report)

            # Save results
            report.data = data
            report.status = "completed"
            db.commit()

            logger.info(f"Report {report_id} completed")
            return {"report_id": report_id, "status": "completed"}

    except Exception as exc:
        logger.error(f"Report generation failed: {exc}")
        with Session(engine) as db:
            report = db.get(Report, report_id)
            if report:
                report.status = "failed"
                report.error = str(exc)
                db.commit()
        raise
```

**Running Celery Worker**:
```bash
# Start Celery worker
celery -A core.celery_app worker --loglevel=info

# Start worker with specific queue
celery -A core.celery_app worker -Q emails --loglevel=info

# Start multiple workers
celery -A core.celery_app worker --concurrency=4 --loglevel=info

# Start worker with autoreload (development)
celery -A core.celery_app worker --loglevel=info --reload
```

### 3. Scheduled Tasks (Celery Beat)

**Celery Beat Configuration**:
```python
# core/celery_app.py
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    # Run every day at midnight
    "cleanup-old-data": {
        "task": "tasks.maintenance_tasks.cleanup_old_data",
        "schedule": crontab(hour=0, minute=0),
    },
    # Run every hour
    "sync-external-data": {
        "task": "tasks.sync_tasks.sync_external_data",
        "schedule": crontab(minute=0),
    },
    # Run every 5 minutes
    "process-pending-orders": {
        "task": "tasks.order_tasks.process_pending_orders",
        "schedule": 300.0,  # seconds
    },
    # Run every Monday at 9 AM
    "weekly-report": {
        "task": "tasks.report_tasks.generate_weekly_report",
        "schedule": crontab(hour=9, minute=0, day_of_week=1),
    },
}
```

**Scheduled Task Definition**:
```python
# tasks/maintenance_tasks.py
from core.celery_app import celery_app
from datetime import datetime, timedelta
from sqlmodel import Session, select
import logging

logger = logging.getLogger(__name__)

@celery_app.task
def cleanup_old_data():
    """
    Cleanup old data (runs daily at midnight).
    """
    logger.info("Starting cleanup task")

    with Session(engine) as db:
        # Delete old sessions (> 30 days)
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        result = db.execute(
            select(Session).where(Session.created_at < cutoff_date)
        )
        old_sessions = result.scalars().all()

        for session in old_sessions:
            db.delete(session)

        db.commit()
        logger.info(f"Deleted {len(old_sessions)} old sessions")

    return {"deleted": len(old_sessions)}

@celery_app.task
def process_pending_orders():
    """
    Process pending orders (runs every 5 minutes).
    """
    logger.info("Processing pending orders")

    with Session(engine) as db:
        # Get pending orders
        result = db.execute(
            select(Order).where(Order.status == "pending")
        )
        pending_orders = result.scalars().all()

        processed = 0
        for order in pending_orders:
            try:
                # Process order
                process_order_logic(order)
                order.status = "processed"
                processed += 1
            except Exception as e:
                logger.error(f"Failed to process order {order.id}: {e}")
                order.status = "failed"

        db.commit()
        logger.info(f"Processed {processed} orders")

    return {"processed": processed}
```

**Running Celery Beat**:
```bash
# Start Celery Beat scheduler
celery -A core.celery_app beat --loglevel=info

# Run worker and beat together (development only)
celery -A core.celery_app worker --beat --loglevel=info
```

### 4. Task Monitoring and Error Handling

**Task Result Backend**:
```python
# Check task status
from core.celery_app import celery_app

task = send_email_task.delay("user@example.com", "Subject", "Body")

# Get task ID
task_id = task.id

# Check if task is ready
if task.ready():
    result = task.result
    print(f"Task completed: {result}")

# Get task state
state = task.state  # PENDING, STARTED, SUCCESS, FAILURE, RETRY

# Get task info
info = task.info  # Exception info if failed
```

**Custom Task Base Class with Logging**:
```python
# core/base_task.py
from celery import Task
import logging

logger = logging.getLogger(__name__)

class LoggingTask(Task):
    """
    Base task class with logging and error handling.
    """

    def on_success(self, retval, task_id, args, kwargs):
        """Called when task succeeds."""
        logger.info(f"Task {task_id} succeeded: {retval}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Called when task fails."""
        logger.error(f"Task {task_id} failed: {exc}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Called when task is retried."""
        logger.warning(f"Task {task_id} retrying: {exc}")

# Use custom base class
@celery_app.task(base=LoggingTask, bind=True)
def my_task(self):
    """Task with custom logging."""
    pass
```

**Task Error Handling with Callbacks**:
```python
@celery_app.task(bind=True)
def process_payment(self, order_id: int):
    """Process payment with error handling."""
    try:
        # Process payment
        result = payment_service.process(order_id)
        return result

    except PaymentError as exc:
        # Handle payment-specific errors
        logger.error(f"Payment failed for order {order_id}: {exc}")

        # Update order status
        with Session(engine) as db:
            order = db.get(Order, order_id)
            order.status = "payment_failed"
            db.commit()

        # Don't retry payment errors
        raise

    except Exception as exc:
        # Retry other errors
        logger.error(f"Unexpected error processing payment: {exc}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)
```

**Task Chaining and Workflows**:
```python
from celery import chain, group, chord

# Chain: Execute tasks sequentially
workflow = chain(
    task1.s(arg1),
    task2.s(),
    task3.s()
)
result = workflow.apply_async()

# Group: Execute tasks in parallel
job = group(
    task1.s(1),
    task1.s(2),
    task1.s(3)
)
result = job.apply_async()

# Chord: Execute tasks in parallel, then callback
callback = chord(
    [task1.s(1), task1.s(2), task1.s(3)]
)(callback_task.s())
```

### 5. Redis Queue (RQ) Alternative

**RQ Setup** (Simpler alternative to Celery):
```bash
pip install rq
```

**RQ Configuration**:
```python
# core/rq_config.py
from redis import Redis
from rq import Queue
from core.config import get_settings

settings = get_settings()
redis_conn = Redis.from_url(settings.redis_url)

# Create queues
default_queue = Queue("default", connection=redis_conn)
email_queue = Queue("emails", connection=redis_conn)
report_queue = Queue("reports", connection=redis_conn)
```

**RQ Task Definition**:
```python
# tasks/email_tasks.py
import time

def send_email_rq(to: str, subject: str, body: str):
    """
    Send email via RQ.
    Simple function, no decorators needed.
    """
    time.sleep(2)  # Simulate email sending
    print(f"Email sent to {to}")
    return {"status": "sent", "to": to}
```

**Using RQ in FastAPI**:
```python
from fastapi import APIRouter
from core.rq_config import email_queue
from tasks.email_tasks import send_email_rq

router = APIRouter()

@router.post("/send-email")
async def send_email(to: str, subject: str, body: str):
    """Enqueue email sending task."""
    job = email_queue.enqueue(
        send_email_rq,
        to=to,
        subject=subject,
        body=body,
        job_timeout="5m"
    )

    return {
        "message": "Email queued",
        "job_id": job.id
    }

@router.get("/job/{job_id}")
async def get_job_status(job_id: str):
    """Get RQ job status."""
    from rq.job import Job

    job = Job.fetch(job_id, connection=redis_conn)

    return {
        "job_id": job_id,
        "status": job.get_status(),
        "result": job.result if job.is_finished else None,
        "error": str(job.exc_info) if job.is_failed else None
    }
```

**Running RQ Worker**:
```bash
# Start RQ worker
rq worker default emails reports --url redis://localhost:6379

# Start worker with burst mode (process existing jobs and exit)
rq worker default --burst
```

## Best Practices

### 1. Task Design
- Keep tasks idempotent (safe to run multiple times)
- Make tasks atomic (single responsibility)
- Pass minimal data (IDs, not full objects)
- Set appropriate timeouts
- Implement proper error handling

### 2. Error Handling
- Use retry logic with exponential backoff
- Set maximum retry limits
- Log all errors with context
- Update task status in database
- Implement dead letter queues for failed tasks

### 3. Performance
- Use task routing for different priorities
- Set worker concurrency appropriately
- Monitor queue lengths
- Use task prefetching wisely
- Implement rate limiting for external APIs

### 4. Monitoring
- Track task execution time
- Monitor queue depths
- Alert on failed tasks
- Log task lifecycle events
- Use monitoring tools (Flower for Celery)

### 5. Production Considerations
- Use separate workers for different task types
- Implement graceful shutdown
- Use supervisor or systemd for worker management
- Set resource limits (memory, CPU)
- Implement health checks for workers

## Monitoring with Flower (Celery)

**Install and Run Flower**:
```bash
# Install Flower
pip install flower

# Run Flower
celery -A core.celery_app flower --port=5555

# Access at http://localhost:5555
```

**Flower Configuration**:
```python
# core/celery_app.py
celery_app.conf.update(
    # Enable events for Flower
    worker_send_task_events=True,
    task_send_sent_event=True,
)
```

## Summary

This skill provides comprehensive guidance for implementing background tasks and async workers in FastAPI applications with:
- FastAPI BackgroundTasks for simple tasks
- Celery integration for production workloads
- Scheduled tasks with Celery Beat
- Task monitoring and error handling
- Redis Queue (RQ) as simpler alternative
- Task chaining and workflows
- Best practices for reliability and performance
- Production deployment patterns

Use this skill to handle long-running operations asynchronously, scale task processing independently, and build robust background job systems for production FastAPI applications.
