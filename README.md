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
* Bot config file: bot_config.ini
* Bot logic: bot.py
```
Bot logic is completely independent from the application and simulates the work of the client
```
* The requests module must be installed for the bot to work