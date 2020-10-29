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
  redis:
    image: redis
```