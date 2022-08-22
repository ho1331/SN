### Launch application

+ running
        
        docker-compose up

+ initialize database
        
        docker-compose exec api flask db init
        docker-compose exec api flask db migrate
        docker-compose exec api flask db upgrade

### Base API documentation
        
        http://localhost/swagger

### Automated bot
        docker-compose exec api python bot.py