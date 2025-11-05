from app import create_app, db
from app.models.task import Task

my_app = create_app()
with my_app.app_context():
    tasks = [
        Task(title="Go grocery shopping.", description="Get milk, eggs, bread, bananas"),
        Task(title="Finish Task API", description="Finish wave 4")
    ]
    db.session.add_all(tasks)
    db.session.commit()
