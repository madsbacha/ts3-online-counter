# ts3-online-counter

## docker-compose
Example docker-compose file

```
version: '3.8'
services: 
  tsstatus:
    build: .
    command: ["python", "./tsstatus.py"]
    environment: 
      - TS_HOST=<ip>
      - TS_USERNAME=serveradmin
      - TS_PASSWORD=<password>
      - REDIS_HOST=redis
      - PYTHONUNBUFFERED=1
    restart: always
  api:
    build: .
    command: ["python", "./api.py"]
    environment: 
      - REDIS_HOST=redis
    ports: 
      - 5000:5000
    restart: always
  discord:
    build: .
    command: ["python", "./discordbot.py"]
    environment: 
      - REDIS_HOST=redis
      - DISCORD_CHANNEL_ID=<channel_id>
      - DISCORD_TOKEN=<discord_bot_token>
      - PYTHONUNBUFFERED=1
    restart: always
  redis:
    image: redis
```