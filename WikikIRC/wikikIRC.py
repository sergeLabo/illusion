#!/usr/bin/env python
# -*- coding: utf8 -*-

# WikikIRC est un petit script qui récupère le flux IRC du canal fr.wikipedia pour en faire des fichiers txt
# afin qu'ils soient lus et traduits en "MIDI" par Puredata via OSC.

# WikikIRC a été pondu par Olivier Baudu et Anthony Templier pour le Labomedia en septembre 2011.
# lamouraupeuple arobase gmail point com // http://lamomedia.net
# Publié sous license GPLv3 (http://www.gnu.org/licenses/gpl-3.0.html)

import OSC.OSC as OSC

import irclib.irclib as irclib
import irclib.ircbot as ircbot

import re

# Init OSC
client = OSC.OSCClient()
msg = OSC.OSCMessage()

b_client = OSC.OSCClient()
b_msg = OSC.OSCMessage()

print ("Connexion en cours sur l'IRC...")
    
class BotModeration(ircbot.SingleServerIRCBot):
    def __init__(self):
        # paramètres de connexion IRC
        ircbot.SingleServerIRCBot.__init__(self, [("irc.wikimedia.org", 6667)], "Labomedia-test", "Bot d'analyse syntaxique réalisé en Python avec ircbot")
        
        # filtre pour virer les codes couleurs et ne récupérer que le texte    
        self.filtre = re.compile( "\x03[0-9]{0,2}" )

    def on_welcome(self, serv, ev): 
        # connexion au canal IRC
        serv.join("#fr.wikipedia")
            
    def on_pubmsg(self, serv, ev):   
        global n
        message = ev.arguments()[0] # get new message
        sortie = self.filtre.sub('', message) # filtre les nouveaux messages
        
        # affiche le message en console
        sortie = str(sortie)
        sortie = re.sub(r'[_,.;:^\W]', '', sortie)
        sortie = sortie.lower()
        print sortie

        # send message to music.py
        msg.setAddress("/sortie")
        msg.append(sortie)
        try:
            client.sendto(msg, ('127.0.0.1', 9001))
            msg.clearData()
        except:
            print 'No connection with music.py'
            pass 
            
        # send message to blender
        b_msg.setAddress("/text")
        b_msg.append(sortie)
        try:
            b_client.sendto(b_msg, ('127.0.0.1', 8000))
            b_msg.clearData()
        except:
            print 'No connection with blender'
            pass        
        
if __name__ == "__main__":
    BotModeration().start()
