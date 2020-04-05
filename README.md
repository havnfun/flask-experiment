# flask-experiment
Playing with Flask and MQTT using very simple punchcard site

### To launch

```
docker run --name=punch -e MQTT_URL=URL_TO_MQTT_SERVER -e MQTT_PORT=1883 -p 5000:5000 -it havnfun/punch
```

### Note
Currently has no error handling or support for security on MQTT server
