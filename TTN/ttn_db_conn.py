import sys
import ttn
import argparse
from influxdb import InfluxDBClient

receivedNodeUplinkMsg = False
nodeMsg = 0


def uplinkCallback(msg, client):

    global receivedNodeUplinkMsg
    global nodeMsg
    print()
    print(msg)
    print("\r\nThis is the payload:")
    print(msg.payload_fields.varResistorAnalogValue)
    print(type(msg.payload_fields.varResistorAnalogValue))
    receivedNodeUplinkMsg = True
    nodeMsg = msg.payload_fields.varResistorAnalogValue


def main():

    global receivedNodeUplinkMsg

    parser = argparse.ArgumentParser(description='TTN cloud and \
                                    database connection')

    parser.add_argument("-d",
                        "--dbaddr",
                        dest='dbaddr',
                        help="database network address",
                        type=str,
                        default='localhost'
                        )

    parser.add_argument("-a",
                        "--appid",
                        dest='appid',
                        help="TTN application id",
                        type=str,
                        default='testapptelecomproject_868'
                        )

    parser.add_argument("-k",
                        "--accessKey",
                        dest='accessKey',
                        help="TTN Application Access Key",
                        type=str,
                        default='yourAccessKey'
                        )

    args = parser.parse_args()
    dbAddress = args.dbaddr
    app_id = args.appid
    access_key = args.accessKey
    # ttn application credentials
    # app_id = "testapptelecomproject_868"
    # access_key = "ttn-account-v2.2GeA7EbqY7SBG-14tG7ma5m4I17VoQTJ4UZS0ZP1-ZQ"

    # TTN handlers
    handler = ttn.HandlerClient(app_id, access_key)
    # using mqtt client
    mqtt_client = handler.data()
    # set the callback function for uplink-Msgs
    mqtt_client.set_uplink_callback(uplinkCallback)
    mqtt_client.connect()

    # connect to database
    client = InfluxDBClient(host=dbAddress, port=8086)
    client.switch_database('MySensors')

    while True:
        try:
            if receivedNodeUplinkMsg:
                json_body = [
                    {
                        "measurement": "VarResistorData",
                        "tags": {
                            "Sensor": "varRes1",
                        },
                        "fields": {
                            "analogValue": nodeMsg
                        }
                    }]

                # write to database
                client.write_points(json_body)
                # reset uplink-msg flag
                receivedNodeUplinkMsg = False

        except KeyboardInterrupt:
            mqtt_client.close()
            print()
            print("You Pressed CTRL+C")
            print("Quiting Program - Bye!")
            sys.exit(0)

    # time.sleep(60)
    # mqtt_client.close()


if __name__ == '__main__':
    main()
