#!/usr/bin/env python3
"""
Sonos NodeServer for UDI Polyglot v2
by Einstein.42 (James Milne) milne.james@gmail.com
"""

import udi_interface
import sys
import soco
import requests
import json

LOGGER = udi_interface.LOGGER

with open('server.json') as data:
    SERVERDATA = json.load(data)
    data.close()
try:
    VERSION = SERVERDATA['credits'][0]['version']
except (KeyError, ValueError):
    LOGGER.info('Version not found in server.json.')
    VERSION = '0.0.0'

class Controller(object):
    def __init__(self, polyglot):
        self.name = 'Sonos Controller'
        self.discovery = False

    def start(self):
        LOGGER.info('Starting Sonos Polyglot v3 NodeServer version {}, udi_interface: {}'.format(VERSION, udi_interface.__version__))
        self.discover()


    def discover(self, command = None):
        LOGGER.info('Starting Speaker Discovery...')
        polyglot.Notices.clear()
        self.discovery = True
        speakers = soco.discover()
        if speakers:
            LOGGER.info('Found {} Speaker(s)'.format(len(speakers)))
            for speaker in speakers:
                address = speaker.uid[8:22].lower()
                if not polyglot.getNode(address):
                    polyglot.addNode(Speaker(polyglot, address, address, speaker.player_name, speaker.ip_address))
                else:
                    LOGGER.info('Speaker {} already configured.'.format(speaker.player_name))
        else:
            LOGGER.info('No Speakers found. Are they powered on?')
            polyglot.Notices['error'] = 'No speakers found. Make sure they are powered on and try Disover again.'
        self.discovery = False


class Speaker(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, ip):
        self.ip = ip
        self.zone = soco.SoCo(self.ip)
        LOGGER.info('Sonos Speaker: {}@{} Current Volume: {}'\
                    .format(name, ip, self.zone.volume))
        super().__init__(polyglot, primary, address, 'Sonos {}'.format(name))

        polyglot.subscribe(polyglot.START, self.start, address)
        polyglot.subscribe(polyglot.POLL, self.update)

    def start(self):
        LOGGER.info("{} ready to rock!".format(self.name))
        self.update('shortpoll')

    def update(self, pollflag):
        if pollflag == 'shortpoll':
            try:
                self.setDriver('ST', self._get_state())
                self.setDriver('SVOL', self.zone.volume)
                self.setDriver('GV1', self.zone.bass)
                self.setDriver('GV2', self.zone.treble)
            except requests.exceptions.ConnectionError as e:
                LOGGER.error('Connection error to Speaker or ISY.: %s', e)


    def query(self, command=None):
        self.update('shortpoll')
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

    def _unmute(self, command):
        self.zone.mute = False

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

    drivers = [{'driver': 'GV1', 'value': 0, 'uom': '56'},
                {'driver': 'GV2', 'value': 0, 'uom': '56'},
                {'driver': 'SVOL', 'value': 0, 'uom': '51'},
                {'driver': 'ST', 'value': 0, 'uom': '25'}]

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
        polyglot = udi_interface.Interface([])
        polyglot.start()
        polyglot.setCustomParamsDoc()
        polyglot.updateProfile()
        control = Controller(polyglot)
        
        polyglot.subscribe(polyglot.DISCOVER, control.discover)

        polyglot.ready()
        control.start()

        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
