#!/usr/bin/env python3
"""
Sonos NodeServer for UDI Polyglot v2
by Einstein.42 (James Milne) milne.james@gmail.com
"""

import polyinterface
import sys
import soco
import requests
import json
#add re library
import re

<<<<<<< Updated upstream
LOGGER = polyinterface.LOGGER
=======
LOGGER = udi_interface.LOGGER
# DD need to get custom params
Custom = udi_interface.Custom
>>>>>>> Stashed changes

with open('server.json') as data:
    SERVERDATA = json.load(data)
    data.close()
try:
    VERSION = SERVERDATA['credits'][0]['version']
except (KeyError, ValueError):
    LOGGER.info('Version not found in server.json.')
    VERSION = '0.0.0'

<<<<<<< Updated upstream
class Controller(polyinterface.Controller):
=======
class Controller(object):

>>>>>>> Stashed changes
    def __init__(self, polyglot):
        super().__init__(polyglot)
        self.name = 'Sonos Controller'
        # DD net to get custom params / add controller node
        self.poly = polyglot
        self.discovery = False
        self.Params = Custom(polyglot, 'customparams')
        polyglot.subscribe(polyglot.CUSTOMPARAMS, self.parameterHandler)
        polyglot.ready()
        self.start()
				
    def start(self):
        LOGGER.info('Starting Sonos Polyglot v2 NodeServer version {}, polyinterface: {}'.format(VERSION, polyinterface.__version__))
        self.discover()

<<<<<<< Updated upstream
    def shortPoll(self):
        if self.discovery:
            return
        for node in self.nodes:
            self.nodes[node].update()

    def update(self):
        """
        Nothing to update for the controller.
        """
        pass
=======
    # DD add routine to load parameters
    def parameterHandler(self, params):
        LOGGER.info("running parameterHandler")
        self.Params.load(params)
        
	## strip special characters from names	
    def get_valid_node_name(self, name):
        name = bytes(name, 'utf-8').decode('utf-8','ignore')
        return re.sub(r"[<>'~!@#$%^&*(){}[\]?/\\;:\"']+","",name)
>>>>>>> Stashed changes

    def discover(self, command = None):
        LOGGER.info('Starting Speaker Discovery...')
        self.discovery = True
		# DD - added ability to scan on other subnets
        netscan = False 
        kwargs = {}
        for netparam in self.Params:
            LOGGER.info('Starting network scan')
            match = re.match( "networks_to_scan", netparam, re.I)
            if match is not None:
                netscanlist = self.Params[netparam].split(",")
                kwargs = {"networks_to_scan": netscanlist}
                netscan = True

        speakers = soco.discover(5,False,None,"Sonos",netscan,**kwargs)

        if speakers:
            LOGGER.info('Found {} Speaker(s)'.format(len(speakers)))
            for speaker in speakers:
                address = speaker.uid[8:22].lower()
                if address not in self.nodes:
                    self.addNode(Speaker(self, self.address, address, speaker.player_name, speaker.ip_address))
                else:
                    LOGGER.info('Speaker {} already configured.'.format(speaker.player_name))
        else:
            LOGGER.info('No Speakers found. Are they powered on?')
<<<<<<< Updated upstream
=======
            polyglot.Notices['error'] = 'No speakers found. Make sure they are powered on and try Disover again.'

        # DD - Add manual nodes
        LOGGER.info('add speakers from custom parameters')
        
        for param in self.Params:
            # Look for customParam starting with sonos_
            match = re.match( "sonos_(.*)", param, re.I)
            LOGGER.info('param={} match={}'.format(param,match))
            if match is not None:
                # The Sonos address is everything following the sonos_
                address = match.group(1).lower()
                LOGGER.info('process param={0} address={1}'.format(param,address))
                # Get the customParam value which is json code
                #  { "name": "Sonos FamilyRoom", "host": "192.168.1.86" }
                cfg = self.Params[param]
                cfgd = None
                try:
                    cfgd = json.loads(cfg)
                except:
                    err = sys.exc_info()[0]
                    LOGGER.error('failed to parse cfg={0} Error: {1}'.format(cfg,err))
                if cfgd is not None:
                    # Check that name and host are defined.
                    addit = True
                    if not 'name' in cfgd:
                        LOGGER.error('No name in customParam {0} value={1}'.format(param,cfg))
                        addit = False
                    if not 'host' in cfgd:
                        LOGGER.error('No host in customParam {0} value={1}'.format(param,cfg))
                        addit = False
                    if addit:
                        sonos_name = self.get_valid_node_name(cfgd['name'])
                        sonos_ip = self.get_valid_node_name(cfgd['host'])
                        if not polyglot.getNode(address): 
                            polyglot.addNode(Speaker(polyglot, address, address, sonos_name, sonos_ip))
                        else:
                            LOGGER.info('Speaker {} already configured.'.format(sonos_name))
>>>>>>> Stashed changes
        self.discovery = False

    commands = {'DISCOVER': discover}

class Speaker(polyinterface.Node):
    def __init__(self, controller, primary, address, name, ip):
        self.ip = ip
        self.zone = soco.SoCo(self.ip)
        LOGGER.info('Sonos Speaker: {}@{} Current Volume: {}'\
                    .format(name, ip, self.zone.volume))
        super().__init__(controller, primary, address, 'Sonos {}'.format(name))

    def start(self):
        LOGGER.info("{} ready to rock!".format(self.name))
<<<<<<< Updated upstream
=======
		# DD - fixed polling flag was using shortpoll, changed to shortPoll
        self.update('shortPoll')

    def update(self, pollflag):
		# DD - fixed polling flag was using shortpoll, changed to shortPoll
        if pollflag == 'shortPoll':
            try:
                self.setDriver('ST', self._get_state())
                self.setDriver('SVOL', self.zone.volume)
                self.setDriver('GV1', self.zone.bass)
                self.setDriver('GV2', self.zone.treble)
                # DD - added mute status variable
				muteval = 1 if self.zone.mute == True else 0 
                self.setDriver('GV3', muteval)
            except requests.exceptions.ConnectionError as e:
                LOGGER.error('Connection error to Speaker or ISY.: %s', e)
>>>>>>> Stashed changes

    def update(self):
        try:
            self.setDriver('ST', self._get_state())
            self.setDriver('SVOL', self.zone.volume)
            self.setDriver('GV1', self.zone.bass)
            self.setDriver('GV2', self.zone.treble)
        except requests.exceptions.ConnectionError as e:
            LOGGER.error('Connection error to Speaker or ISY.: %s', e)

    def query(self, command=None):
<<<<<<< Updated upstream
        self.update()
=======
        self.update('shortPoll')
>>>>>>> Stashed changes
        self.reportDrivers()

    def _get_state(self):
        text = self.zone.get_current_transport_info()['current_transport_state'].upper()
        return {
            'PLAYING': '0',
            'TRANSITIONING': '1',
            'PAUSED_PLAYBACK': '2',
            'STOPPED': '3'
        }.get(text, '3')

    def _play(self, command):
        try:
            self.zone.play()
            self.setDriver('ST', self._get_state())
        except:
            LOGGER.info('Transition not available. This typically means no music is selected.')

    def _stop(self, command):
        try:
            self.zone.stop()
            self.setDriver('ST', self._get_state())
        except:
            LOGGER.info('Transition not available. This typically means no music is selected.')

    def _pause(self, command):
        try:
            self.zone.pause()
            self.setDriver('ST', self._get_state())
        except:
            LOGGER.info('Transition not available. This typically means no music is selected.')

    def _next(self, command):
        try:
            self.zone.next()
        except:
            LOGGER.info('This typically means that the station or mode you are in doesn\'t support it.')

    def _previous(self, command):
        try:
            self.zone.previous()
        except:
            LOGGER.info('This typically means that the station or mode you are in doesn\'t support it.')

    def _partymode(self, command):
        try:
            self.zone.partymode()
        except:
            LOGGER.info('Your Sonos didn\'t like that. Make sure you are doing things correctly.')

    def _mute(self, command):
        self.zone.mute = True
		# DD- added Mute status
        self.setDriver('GV3', 1)

    def _unmute(self, command):
        self.zone.mute = False
		# DD - added UnMute status
        self.setDriver('GV3', 0)

    def _volume(self, command):
        try:
            val = int(command.get('value'))
        except:
            LOGGER.error('volume: Invalid argument')
        else:
            self.zone.volume = val
            self.setDriver('SVOL', val)

    def _bass(self, command):
        try:
            val = int(command.get('value'))
        except:
            LOGGER.error('bass: Invalid argument')
        else:
            if -10 <= val <= 10:
                self.zone.bass = val
                self.setDriver('GV1', val)

    def _treble(self, command):
        try:
            val = int(command.get('value'))
        except:
            LOGGER.error('treble: Invalid argument')
        else:
            if -10 <= val <= 10:
                self.zone.treble = val
                self.setDriver('GV2', val)
    # DD - added mute status to drivers
    drivers = [{'driver': 'GV1', 'value': 0, 'uom': '56'},
                {'driver': 'GV2', 'value': 0, 'uom': '56'},
                {'driver': 'SVOL', 'value': 0, 'uom': '51'},
                {'driver': 'ST', 'value': 0, 'uom': '25'},
                {'driver': 'GV3', 'value': 0, 'uom': '2'}]

    commands = {    'PLAY': _play,
                    'STOP': _stop,
                    'DON': _play,
                    'DOF': _pause,
                    'PAUSE': _pause,
                    'NEXT': _next,
                    'PREVIOUS': _previous,
                    'PARTYMODE': _partymode,
                    'MUTE': _mute,
                    'UNMUTE': _unmute,
                    'BASS': _bass,
                    'TREBLE': _treble,
                    'VOLUME': _volume }

    id = 'sonosspeaker'

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('Sonos')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
