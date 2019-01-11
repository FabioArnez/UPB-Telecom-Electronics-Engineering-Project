#!/usr/bin/env python3

import paho.mqtt.client as mqtt


def main():
    # This is the Publisher
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.publish("topic/test", "Hello world!")
    client.disconnect()


if __name__ == '__main__':
    main()
