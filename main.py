from app import create_app

#create and configure flask application
app = create_app()

if __name__=='__main__':
    app.run()