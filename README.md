# Quiz Master

It is a multi-user app (one requires an administrator and other users) that acts as an exam preparation site for multiple courses.

## Frameworks to be used

- SQLite for data storage
- Flask for API
- VueJS for UI
- VueJS Advanced with CLI (only if required, not necessary)
- Jinja2 templates if using CDN only for entry point (Not to be used for UI)
- Bootstrap for HTML generation and styling (No other CSS framework is allowed)
- SQLite for database (No other database is permitted)
- Redis for caching
- Redis and Celery for batch jobs

## Running The Application:

- **Backend** : `flask --app backend run --debug`
- **Frontend** : `npm run dev`