#!/usr/bin/env python3
"""Binding to C Agent wrapper"""

#
# Copyright (c) 2018 FBK-CREATENET
# Author: Abin Ninan Thomas
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import ctypes as ct

from emage import _RanL2Config
from emage import _RanConfig
from emage import _RanOperations
from emage import _Operations
from emage import C_POINT_OP
from emage import _INIT
from emage import _RELEASE
from emage import _DISCONNECTED
from emage import _ENB
from emage import _UEREPORT
from emage import _UEMEASURE
from emage import _HANDOVER
from emage import _CELLMEASURE
from emage import INIT
from emage import RELEASE
from emage import DISCONNECTED
from emage import CELL_SETUP_REQUEST
from emage import ENB_SETUP_REQUEST
from emage import UE_REPORT
from emage import UE_MEASURE
from emage import HANDOVER_UE
from emage import CELL_MEASURE

class EmpowerAgent:
    """ EMpower Agent binding(wrapper) in python to work with the C agent"""

    def __init__(self, **kwargs):
        self.conp = ct.CDLL("libemproto.so")
        self.conv = ct.CDLL("libemagent.so")

        # Callbacks which is possible to register to
        self.registeredto = {
            'INIT':[],
            'RELEASE':[],
            'DISCONNECTED':[],
            'CELL_SETUP_REQUEST':[],
            'ENB_SETUP_REQUEST':[],
            'UE_REPORT':[],
            'UE_MEASURE':[],
            'HANDOVER_UE':[],
            'MAC_REPORT':[]}

        if 'id' in kwargs:
            self._id = (kwargs.get('id'))
        else:
            self._id = ct.c_uint64(1)

        if 'ctrl_addr' in kwargs:
            self._ctrl_addr = \
                ct.c_char_p(kwargs.get('ctrl_addr').encode('utf-8'))
        else:
            self._ctrl_addr = ct.c_char_p(("127.0.0.1").encode('utf-8'))

        if 'ctrl_port' in kwargs:
            self._ctrl_port = ct.c_ushort(kwargs.get('ctrl_port'))
        else:
            self._ctrl_port = ct.c_ushort(2210)

        # This is in charge of avoiding changes to the eNB properties once the
        # Agent has started.
        _locked = False

        self._ops = _Operations(
            init=_INIT(self.__handler_init), 
            release=_RELEASE(self.__handler_release),
            disconnected=_DISCONNECTED(self.__handler_disconnected),
            enb_setup_request=_ENB(self.__handler_enbcap),
            ue_report=_UEREPORT(self.__handler_ue_report),
            ue_measure=_UEMEASURE(self.__handler_ue_measure),
            handover_UE=_HANDOVER(self.__handler_handover_UE),
            cell_measure=_CELLMEASURE(self.__handler_cell_measure))


    @property
    def enb_id(self):
        """To retrieve the ID of the EnB"""
        return self._id


    @enb_id.setter
    def enb_id(self, enbid):
        """ Setting EnB ID"""
        if not self._locked:
            self._id = enbid


    @property
    def ctrl_addr(self):
        """To retrieve the address of the controller to connect to"""
        return self._ctrl_addr


    @ctrl_addr.setter
    def ctrl_addr(self, ctrl_addr):
        """To set the address of the controller to which the agent has to 
        connect"""
        if not self._locked:
            self._ctrl_addr = ctrl_addr


    @property
    def ctrl_port(self):
        """To retrieve the port number of the controller to connect to"""
        return self._ctrl_port


    @ctrl_port.setter
    def ctrl_port(self, ctrl_port):
        """To set the address of the controller to which the agent has to 
        connect"""
        if not self._locked:
            self._ctrl_port = ctrl_port


    def register_to(self, event, *args):
        """Used to register callbacks to a particular event which are then 
        called back as and when the events occur"""

        if event == INIT:
            for handler in args:
                self.registeredto['INIT'].append(handler)

        if event == RELEASE:
            for handler in args:
                self.registeredto['RELEASE'].append(handler)

        if event == DISCONNECTED:
            for handler in args:
                self.registeredto['DISCONNECTED'].append(handler)

        if event == ENB_SETUP_REQUEST:
            for handler in args:
                self.registeredto['ENB_SETUP_REQUEST'].append(handler)

        if event == UE_REPORT:
            for handler in args:
                self.registeredto['UE_REPORT'].append(handler)

        if event == UE_MEASURE:
            for handler in args:
                self.registeredto['UE_MEASURE'].append(handler)

        if event == HANDOVER_UE:
            for handler in args:
                self.registeredto['HANDOVER_UE'].append(handler)

        if event == CELL_MEASURE:
            for handler in args:
                self.registeredto['CELL_MEASURE'].append(handler)

    # handlers of all the event along with their respecetive arguments
    # Dive into documentation for more information on these handlers

    def __handler_init(self):
        """Agent initialization event handler in empowerAgent"""
        for callback in self.registeredto['INIT']:
            callback()
        return 0


    def __handler_release(self):
        """Release event handler in empowerAgent"""
        for callback in self.registeredto['RELEASE']:
            callback()
        return 0


    def __handler_disconnected(self):
        """Disconnect event handler in empowerAgent where the wrapper is 
        notified of the controller disconnecting
        from the agent"""
        for callback in self.registeredto['DISCONNECTED']:
            callback()
        return 0


    def __handler_enbcap(self, mod):
        """EnB capabilities event handler when controller requests the current 
        setup of the base station"""
        for callback in self.registeredto['ENB_SETUP_REQUEST']:
            callback(mod)
        return 0


    def __handler_ue_report(self, mod, trigid):
        """UE Report event handler when the controller requests a log of UE 
        activity """
        for callback in self.registeredto['UE_REPORT']:
            callback(mod, trigid)
        return 0


    def __handler_ue_measure(
            self, mod, src_cell, rnti, target_enb, target_cell, cause):
        """UE measurements event handler when controller requests measurement 
        for a certain device"""
        for callback in self.registeredto['UE_MEASURE']:
            callback(mod, src_cell, rnti, target_enb, target_cell, cause)
        return 0


    def __handler_handover_UE(
            self, mod, src_cell, rnti, target_enb, target_cell, cause):
        """UE Handover event handler when the controller requests a handover of 
        UE from on base station to another"""
        for callback in self.registeredto['HANDOVER_UE']:
            callback(mod, src_cell, rnti, target_enb, target_cell, cause)
        return 0


    def __handler_cell_measure(self, cell, mod, interval, trigid):
        """MAC Report event handler informs the wrapper that the controller is 
        required to report the status of the MAC layer"""
        for callback in self.registeredto['HANDOVER_UE']:
            callback(cell, mod, interval, trigid)
        return 0

    #
    # WARNING: RAN Slicing callbacks system has not be integrated yet.
    # Coming soon!
    #

    def has_trigger(self, trig_id):
        """Check if a particular trigger is enabled or not with EnB id and 
        trigger id"""
        hastrigger = self.conv.em_has_trigger
        hastrigger.restype = ct.c_int
        hastrigger.argtypes = [ct.c_uint64, ct.c_int]
        return hastrigger(self._id, trig_id)


    def del_trigger(self, trig_id):
        """Delete an identified trigger associated with the EnB using trigger 
        ID and EnB ID"""
        deltrigger = self.conv.em_del_trigger
        deltrigger.restype = ct.c_int
        deltrigger.argtypes = [ct.c_uint64, ct.c_int]
        return deltrigger(self._id, trig_id)


    def is_connected(self):
        """Check if the enb is connected to the controller using its identifier
        """
        _connected = self.conv.em_is_connected
        _connected.restype = ct.c_int
        _connected.argtypes = [ct.c_uint64]
        return _connected(self._id)


    def __send(self):
        """Sends a message to the connected controller"""
        send = self.conv.em_send
        send.restype = ct.c_int
        send.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_uint]
        # msg is just a message, char type placeholder
        msg = ct.c_char_p()
        size = 0
        #return send(self._id, msg, size)
        return -1


    def start(self):
        """Starts the Agent logic and communicates with the controller 
        arguments passed are base station identifier, dependent callbacks, 
        controller address and port"""
        ems = self.conv.em_start
        ems.restype = ct.c_int
        ems.argtypes = [ct.c_uint64, C_POINT_OP, (ct.c_char_p), ct.c_ushort]
        
        ret = ems(self._id, self._ops, self._ctrl_addr, self._ctrl_port)

        # Cannot change Agent properties anymore
        if ret == 0:
            self._locked = True

        return ret


    def terminate(self):
        """Command used by the agent to terminate the operations of a single
        VBS based on its id"""
        terminate = self.conv.em_terminate_agent
        terminate.restype = ct.c_int
        terminate.argtypes = [ct.c_uint64]
        
        ret = terminate(self._id)

        # You can change again the Agent properties now
        if ret == 0:
            self._locked = False

        return ret
