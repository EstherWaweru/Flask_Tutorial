from app import create_app
from celery import make_celery

#create and configure flask application
app = create_app()
celery = make_celery(app)


if __name__=='__main__':
    app.run()