"""PanduitTemperatureSensorMap
Gathers Temperature Sensors from Panduit Environmental Monitoring Devices
"""

from Products.DataCollector.plugins.CollectorPlugin import (SnmpPlugin, GetTableMap)


class PanduitTemperatureSensorMap(SnmpPlugin):
    relname = 'panduitTemperatureSensors'
    modname = 'ZenPacks.community.PanduitMonitoring.PanduitTemperatureSensor'

    snmpGetTableMaps = (
        GetTableMap(
            'ipTHAEntry', '.1.3.6.1.4.1.3711.24.1.1.1.2.2.1', {
                '.3':'ipTHAName',
                '.1':'ipTHAChan',
                '.6':'ipTHAType',
                }
        ),
    )

    def process(self, device, results, log):
        """ Process results and return a relationship map"""
        log.info('processing %s for device %s', self.name(), device.id)

        sensorinfo = results[1].get('ipTHAEntry', {})

        relmap = self.relMap()
        for snmpindex, row in sensorinfo.items():
            # do check for no data?

            name = row.get('ipTHAName')

            if row.get('ipTHAType') == 2:
                relmap.append(self.objectMap({
                    'id': self.prepId(name),
                    'title': name,
                    'snmpindex': snmpindex.strip('.'),
                    'channel': row.get('ipTHAChan'),
                    }))
        return relmap

