## To compile
- Install project dependencies
```bash
$ pip3 install -r requirements.txt
$ sudo apt-get install protobuf-compiler
```
- Migrate database tables
```bash
$ cd mysite/
$ python3 manage.py migrate
```
- Make pb2
```bash
$ make
```

## To run
### start Message Broker
```bash
$ sudo docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```
### run server
```bash
$ cd mysite
$ python3 manage.py runserver 0.0.0.0:8000
```
### run fiboncci server
```bash
$ python3 fib_server.py --ip 0.0.0.0 --port 8080
```
### run logging server
```bash
$ python3 log_server.py --ip 0.0.0.0 --port 8090
```