#TESTE UTILIZANDO O GOOGLE IOT COM FLOWDATA

import datetime
import json
import os
import ssl
import time

import jwt
import paho.mqtt.client as mqtt



def create_jwt(project_id, private_key_file, algorithm):
    # Create a JWT (https://jwt.io) to establish an MQTT connection.
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    # Convert a Paho error to a human readable string.
    return '{}: {}'.format(rc, mqtt.error_string(rc))


import socketio

class Device(object):
    # Device implementation.
    def __init__(self):
        self.connected = False       

    def wait_for_connection(self, timeout):
        # Wait for the device to become connected.
        total_time = 0
        while not self.connected and total_time < timeout:
            time.sleep(1)
            total_time += 1

        if not self.connected:
            raise RuntimeError('Could not connect to MQTT bridge.')

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        # Callback on connection.
        print('Connection Result:', error_str(rc))
        self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        # Callback on disconnect.
        print('Disconnected:', error_str(rc))
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        # Callback on PUBACK from the MQTT bridge.
        print('Published message acked.')

    def on_subscribe(self, unused_client, unused_userdata, unused_mid,
                     granted_qos):
        # Callback on SUBACK from the MQTT bridge.
        print('Subscribed: ', granted_qos)
        if granted_qos[0] == 128:
            print('Subscription failed.')

    def on_message(self, unused_client, unused_userdata, message):
        # Callback on a subscription.
        payload = message.payload.decode('utf-8')
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(payload, message.topic, str(message.qos)))
        
        if not payload:
            return
        # Parse incoming JSON.
        data = json.loads(payload)
        print('retornou', data['led1'])

           
def main():
    # GCP parameters 
    project_id = 'montabaco'  # Your project ID.
    registry_id = 'montabacov32'  # Your registry name.
    device_id = 'medidor-0000000016223e72'  # Your device name.
    private_key_file = '/etc/loader/loader/loader_c/rsa_private.pem'  # Path to private key.
    algorithm = 'RS256'  # Authentication key format.
    cloud_region = 'us-central1'  # Project region.
    ca_certs = '/etc/loader/loader/loader_c/roots.pem'  # CA root certificate path.
    mqtt_bridge_hostname = 'mqtt.googleapis.com'  # GC bridge hostname.
    mqtt_bridge_port = 8883  # Bridge port.
    message_type = 'event'  # Message type (event or state).
    global client
    client = mqtt.Client(
        client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id,
            cloud_region,
            registry_id,
            device_id))
    try:
        client.username_pw_set(
            username='unused',
            password=create_jwt(
                project_id,
                private_key_file,
                algorithm))
    except Exception as e:
        print('ERRO', e)
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    device = Device()

    client.on_connect = device.on_connect
    client.on_publish = device.on_publish
    client.on_disconnect = device.on_disconnect
    client.on_subscribe = device.on_subscribe
    client.on_message = device.on_message
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)
    client.loop_start()

    mqtt_telemetry_topic = '/devices/{}/events'.format(device_id)
    mqtt_config_topic = '/devices/{}/config'.format(device_id)

    # Wait up to 5 seconds for the device to connect.
    device.wait_for_connection(5)

    client.subscribe(mqtt_config_topic, qos=1)

    try:   
        sio = socketio.Client()
        global contador
        contador = 295
        @sio.event
        def connect():
            print('connection established')
        @sio.event
        def medicao(data):
            global contador
            contador += 1
            print(data)
            if contador > 10:
                contador = 0
                payload = json.dumps(data, indent=4)
                print('Publishing payload', payload)
                global client
                client.publish(mqtt_telemetry_topic, payload, qos=1)
        @sio.event
        def disconnect():
            print('disconnected from server')
        vr_erro = 0 #caso de erro de conexão ele tenta 10 vezes com intervalo de tempo exponencial
        while True:
            vr_erro = vr_erro+1
            try:
                sio.connect('http://0.0.0.0:35494')
                print('my sid is', sio.sid)
                break
            except Exception as e:
                print('erro no servidor', e)
                if vr_erro > 9:
                    print('erro socket')
                    break
                time.sleep(5.0*vr_erro)     
        sio.wait()   

    except KeyboardInterrupt:
        # Exit script on ^C.
        pass
        client.disconnect()
        client.loop_stop()
        print('Exit with ^C. Goodbye!')
        

if __name__ == '__main__':
    main()
