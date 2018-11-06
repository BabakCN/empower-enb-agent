#!/usr/bin/env python3
"""..."""

#
# Copyright (c) 2018 FBK-CREATENET
# AUTHOR: Abin Ninan Thomas
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

# Constants defining callback registration
INIT = 0x1
RELEASE = 0x2
DISCONNECTED = 0x3
CELL_SETUP_REQUEST = 0x4
ENB_SETUP_REQUEST = 0x5
UE_REPORT = 0x6
UE_MEASURE = 0x7
HANDOVER_UE = 0x8
CELL_MEASURE = 0x9

# Common Agent operations types

#  int init(void)
_INIT = ct.CFUNCTYPE(ct.c_int)

# int release(void)
_RELEASE = ct.CFUNCTYPE(ct.c_int)

# int disconnected(void)
_DISCONNECTED = ct.CFUNCTYPE(ct.c_int)

# int enb_setup_request(uint32_t mod)
_ENB = ct.CFUNCTYPE(ct.c_int, ct.c_uint32)

# int ue_report(uint32_t mod, int trig_id)
_UEREPORT = ct.CFUNCTYPE(ct.c_int, ct.c_uint32, ct.c_int)

# int ue_measure(...)
_UEMEASURE = ct.CFUNCTYPE(
    ct.c_int,    # return type
    ct.c_uint32, # mod
    ct.c_int,    # trig_id
    ct.c_uint8,  # measure_id
    ct.c_uint16, # rnti
    ct.c_uint16, # earfcn
    ct.c_uint16, # interval
    ct.c_int16,  # max_cells
    ct.c_int16)  # max_meas

# int handover_UE(...)
_HANDOVER = ct.CFUNCTYPE(
    ct.c_int,    # return type
    ct.c_uint32, # mod
    ct.c_uint16, # source_cell
    ct.c_uint16, # rnti
    ct.c_uint64, # target_enb
    ct.c_uint16, # target_cell
    ct.c_uint8)  # cause

# int cell_measure(uint16_t cell, uint32_t mod, int32_t interval, int trig_id)
_CELLMEASURE = ct.CFUNCTYPE(ct.c_uint16, ct.c_uint32, ct.c_int32, ct.c_int)

# int setup_request(uint32_t mod)
_SETUP_REQUEST = ct.POINTER(ct.CFUNCTYPE(ct.c_uint32))

# int slice_request(uint32_t mod, uint64_t slice)
_SLICE_REQUEST = ct.POINTER(ct.CFUNCTYPE(ct.c_uint32, ct.c_uint64))

# int slice_rem(uint32_t mod, uint64_t slice)
_SLICE_REM = ct.CFUNCTYPE(ct.c_uint32, ct.c_uint64)

_NO_OF_USERS = ct.c_int
_USERS = ct.c_uint16*32

_USER_SCHED = ct.c_int
_RBG = ct.c_int

# Layer 2 RAN slicing configuration
class _RanL2Config(ct.Structure):
    _fields_ = [
        ('user_sched', _USER_SCHED),
        ('rbg', _RBG)]

_L2 = _RanL2Config

# RAN slicing configuration for a specific slice
class _RanConfig(ct.Structure):
    _fields_ = [
        ('nof_users', _NO_OF_USERS),
        ('users', _USERS),
        ('l2', _L2)]

# int slice_add(uint32_t mod, uint64_t slice, em_RAN_conf * det)
_SLICE_ADD  = ct.CFUNCTYPE(ct.c_uint32, ct.c_uint64, ct.POINTER(_RanConfig))

# int slice_conf(uint32_t mod, uint64_t slice, em_RAN_conf * conf)
_SLICE_CONF = ct.CFUNCTYPE(ct.c_uint32, ct.c_uint64, ct.POINTER(_RanConfig))

# RAN slicing callback system to provide to the agent library
class _RanOperations(ct.Structure):
    _fields_ = [
        ('setup_request', _SETUP_REQUEST),
        ('slice_request', _SLICE_REQUEST),
        ('slice_add', _SLICE_ADD),
        ('slice_rem', _SLICE_REM),
        ('slice_conf', _SLICE_CONF)]

# Callback system structure to provide to the agent library
class _Operations(ct.Structure):
    """Em-Agent_Ops """
    _fields_ = [
        ('init', _INIT),
        ('release', _RELEASE),
        ('disconnected', _DISCONNECTED),
        ('enb_setup_request', _ENB),
        ('ue_report', _UEREPORT),
        ('ue_measure', _UEMEASURE),
        ('handover_UE', _HANDOVER),
        ('cell_measure', _CELLMEASURE),
        ('ran', _RanOperations)]

# Poiner to _Operations structure
C_POINT_OP = ct.POINTER(_Operations)