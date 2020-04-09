# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
import paho.mqtt.client as mqtt
import time
import os

# Flask
app = Flask(__name__)

# MQTT
broker_url = str(os.getenv('MQTT_URL'))
broker_port = int(os.getenv('MQTT_PORT'))
client = mqtt.Client(client_id="punch", clean_session=False)
print(broker_url, broker_port)
client.connect(broker_url, broker_port)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello():
    return 'Hello World'

# path in url is used to collect variables
@app.route('/<org>/<dept>/<punch>/', methods = ['POST', 'GET'])
def punch(org, dept, punch):

    path='/%s/%s/%s/' % (org, dept, punch)
    topic='Punch/%s/%s/%s' % (punch, org, dept)

    if request.method == 'POST':
        user = request.form['nm']
        lat = request.form['lat']
        lon = request.form['lon']
        if not user == "":
            res = make_response('<h1>%s has been checked %s. </h1>' % (user, punch))
            res.set_cookie('userName', user)

            localtime = time.asctime( time.localtime(time.time()) )
            message = '{"Name"="%s", "Org"="%s", "Dept"="%s", "Punch"="%s", Time"="%s", Lat"=%s, "Lon"=%s}' % (user, org, dept, punch, localtime, lat, lon)
            print(message)
            client.publish(topic=topic, payload=message, qos=1, retain=True)

    else:
        if not request.cookies.get('userName'):
            user = ""
        else:
            user = request.cookies.get('userName')

        res = make_response(render_template('hello.html', path = path, direction = punch, nm=user))


    return res

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0')
