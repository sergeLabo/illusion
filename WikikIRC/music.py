#!/usr/bin/env python
# -*- coding: utf8 -*-

from time import sleep

import OSC.OSC as OSC

import threading
import socket

ip = '127.0.0.1'
port = 9001
buffer_size = 1024
do_loop = True

Dictionary = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5,
              'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11,
              'm':12, 'n':13, 'o':14, 'p':15, 'q':16, 'r':17,
              's':18, 't':19, 'u':20, 'v':21, 'w':22, 'x':23,
              'y':24, 'z':25}

# count message to change midi channel sometimes
n = 0

##----------------   -----------------##
def main():
    set_audio()
    plug()
    listen()

##----------------   -----------------##
def plug():
    global my_socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        my_socket.bind((ip, port))
        my_socket.setblocking(0)
        my_socket.settimeout(0.1)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
        print 'Plug : IP = ', ip,  'Port = ', port,  'Buffer Size =', buffer_size
    except:
        print 'No connected'
        pass

def listen():
    global n
    print 'Ligne numéro:', n
    while do_loop:
        try:
            sleep(0.1)
            raw_data = my_socket.recv(buffer_size)
            sortie = OSC.decodeOSC(raw_data)
            n += 1
            thread_note(n, sortie[2])
        except socket.error:
            pass

def set_audio():
    '''Set fluidsynth, be carefull with fonts path'''
    try:
        import pyFluidSynth.fluidsynth as fluidsynth
        global fs
        fs = fluidsynth.Synth()
        fs.start(driver='alsa')
        # This path is a problem because it's absolute
        #sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
        # Manjaro
        sfid = fs.sfload("/usr/share/soundfonts/FluidR3_GM2-2.sf2")

        # .program_select(channel,    sfid,   bank,   bank number)
        fs.program_select(  1  ,      sfid,   0,      0  ) # yamaha grand piano
        fs.program_select(  2  ,      sfid,   0,      40 ) # violin
        fs.program_select(  3  ,      sfid,   0,      37 ) # pop bass
        fs.program_select(  4  ,      sfid,   0,      56 ) # trompet
        fs.program_select(  5  ,      sfid,   0,      66 ) # tenor sax
        fs.program_select(  6  ,      sfid,   0,      114) # steel drums
        fs.program_select(  7  ,      sfid,   0,      118) # synth drum
        fs.program_select(  8  ,      sfid,   0,      119) # reverse cymbal
        fs.program_select(  9  ,      sfid,   0,      116) # taiko drum
        fs.program_select(  10  ,     sfid,   0,      73 ) # flute
        fs.program_select(  11  ,     sfid,   0,      70 ) # basson
        fs.program_select(  12  ,     sfid,   0,      46 ) # harp
        fs.program_select(  13  ,     sfid,   0,      13 ) # xylophone
        fs.program_select(  14  ,     sfid,   0,      24 ) # nylon string guitar
        fs.program_select(  15  ,     sfid,   0,      25 ) # steel string guitar
        fs.program_select(  16  ,     sfid,   0,      29 ) # overdrive guitar

    except:
        print "For sound synthetizer, you must install:"
        print "sudo apt-get install fluidsynth fluid-soundfont-gm fluid-soundfont-gs"
        print "Be carefull with Sound Font Path"
        pass

def sortie_to_note(n, sortie):
    channel = 1
    life = 0.1
    volume = 100
    print n
    for j in sortie:
        if n%4 == 0:
            channel = 9
            life = 0.5
        elif n%3 == 0:
            channel = 13
            life = 0.1
        else:
            channel = 1
            life = 0.1
        if j.isdigit():
            volume = 30 + 10*int(j)
        if not j.isdigit():
            sleep(0.01)
            note = 50 + 3*Dictionary[j]
            playNote(note, life, channel, volume)

def playNote(note, life, channel, volume):
    '''note from 0 to 127 but all values are not possible in all bank
    life 0 to ?
    channel 1 to 16
    volume 0 to 127'''
    fs.noteon(channel, note, volume)
    sleep(life)
    fs.noteoff(channel, note)

def thread_note(n, sortie):
    thread = threading.Thread(target=sortie_to_note, args=(n, sortie))
    thread.start()

##----------------   -----------------##
main()
