#!/usr/bin/env python

""" Copyright (C) 2016  Maani Ghaffari Jadidi

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""

import rospy
import blescan
import sys
import bluetooth._bluetooth as bluez
from ble_scanner.msg import *


class BLEScannerNode():
    def __init__(self):
        rospy.init_node("blescanner", anonymous=True)

        dev_id = 0
        try:
            self.sock = bluez.hci_open_dev(dev_id)
            print "ble thread started"
        except:
            print "error accessing bluetooth device..."
            sys.exit(1)

        blescan.hci_le_set_scan_parameters(self.sock)
        blescan.hci_enable_le_scan(self.sock)

        self.pub = rospy.Publisher('ble_data', BLEData, queue_size=10, latch=True)

        while not rospy.is_shutdown():
            self.returnedList = blescan.parse_events(self.sock, 10)
            msg = BLEData()
            msg.header.stamp = rospy.Time.now()
            for beacon in self.returnedList:
                submsg = BLEBeacon()
                submsg.mac_address = beacon[0:17]
                submsg.rssi = int(beacon[-3:])
                msg.data.append(submsg)

            self.pub.publish(msg)


if __name__ == "__main__":
    try:
        bleScanner = BLEScannerNode()
    except rospy.ROSInterruptException:
        pass
