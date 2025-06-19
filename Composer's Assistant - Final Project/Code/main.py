import random
from midiutil import MIDIFile   
import tkinter
from tkinter import PhotoImage, ttk

# Indian music words : 
    # taal : rhythm/metre (each taal has a basic reference pattern)
    # raag : scale 
    # laya : speed(loose tempo) (vilambit : slow, madhyam : medium, drut : fast)
    # lehra : background tune 

# Supporting functions

def notetomidi(tonicnote, octave):          # converts letter notes to MIDI numbers - either the first, or for a specific octave
    if octave == 'NA' :                     # gets the first (practical) MIDI note of that note
        midifirstcalcdict = {'C' : 12, 'C#' : 13, 'DB' : 13, 'D' : 14, 'D#' : 15, 'EB' : 15, 'E' : 16, 'F' : 17, 'F#' : 18, 'GB' : 18, 'G' : 19, 'G#' :  20, 'AB' :  20, 'A' : 21, 'A#' : 22, 'BB' : 22, 'B' : 23 }     # dictionary with each notes first MIDI number
        tonicmidi = midifirstcalcdict[tonicnote.upper()]        # avoids case sensitivitiy
    else :                                  # for when an octave is given as well
        midicalcdict = {'C' : 12*octave, 'C#' : 13 + ((octave-1)*12), 'DB' : 13 + ((octave-1)*12), 'D' : 14 + ((octave-1)*12), 'D#' : 15 + ((octave-1)*12), 'EB' : 15 + ((octave-1)*12), 'E' : 16 + ((octave-1)*12), 'F' : 17 + ((octave-1)*12), 'F#' : 18 + ((octave-1)*12), 'GB' : 18 + ((octave-1)*12), 'G' : 19 + ((octave-1)*12), 'G#' :  20 + ((octave-1)*12), 'AB' :  20 + ((octave-1)*12), 'A' : 21 + ((octave-1)*12), 'A#' : 22 + ((octave-1)*12), 'BB' : 22 + ((octave-1)*12), 'B' : 23 + ((octave-1)*12) }
        tonicmidi = midicalcdict[tonicnote.upper()]
    return tonicmidi

def midiwholescales (tonicnote, scale):     # makes a list of all the MIDI numbers in a particular scale from a particular tonic
    tonicmidi = notetomidi(tonicnote, 'NA') # calls previous function  
    t = 2           # makes scale formulae easier to apply
    s = 1
    note = tonicmidi  
    scalelist = [tonicmidi]                 # ensures the first note in the list is the tonic (useful for scale weights later)
    if scale.upper() == 'MAJOR':            # goes across a long range, for numbers at certain positions, adds either a tone or semitone
        for i in range(1,70):  
            if i%7 == 0 or (i-3)%7 == 0 :   # these conditions are what change for each scale
                note = note + s
            else : 
                note = note + t
            if note >= tonicmidi and note <= 127 :      # checks if the note is in the MIDI range
                scalelist.append(note)                  # if so, adds it to the scale list
    if scale.upper() == 'MINOR':            
        for i in range(1,70):
            if (i-2)%7 == 0 or (i-5)%7 == 0 :   # conditions for t-s-t-t-s-t-t
                note = note + s
            else :
                note = note + t
            if note >= tonicmidi and note <= 127 :
                scalelist.append(note)
    if scale.upper() == 'DORIAN':
        for i in range(1,70):
            if (i-2)%7 == 0 or (i-6)%7 == 0 :   # conditions for t-s-t-t-t-s-t 
                note = note + s
            else : 
                note = note + t
            if note >= tonicmidi and note <= 127 : 
                scalelist.append(note)
    if scale.upper() == 'PHRYGIAN':
        for i in range(1,70):
            if (i-1)%7 == 0 or (i-5) == 0 :     # conditions for s-t-t-t-s-t-t
                note = note + s
            else : 
                note = note + t
            if note >= tonicmidi and note <= 127 : 
                scalelist.append(note)
    if scale.upper() == 'MIXOLYDIAN':
        for i in range(1,70):
            if (i-3)%7 == 0 or (i-6)%7 == 0 :   # conditions for t-t-s-t-t-s-t
                note = note + s
            else : 
                note = note + t
            if note >= tonicmidi and note <= 127 : 
                scalelist.append(note)
    return scalelist

def midiscaleweight(scalelist):             # makes a list of probablities of each MIDI number (favours tonic, dominant and subdominant)
    scaleweight = []
    
    for i in range(1,(len(scalelist)+1)):   # spans length of scale list
        if i == 1 or (i-1)%7 == 0 :         # based on the position in the list (i), a probability is assigned
            scaleweight.append(30)
        elif (i+3)%7 == 0 : 
            scaleweight.append(14)
        elif (i+2)%7 == 0 : 
            scaleweight.append(20)
        else : 
            scaleweight.append(9)
    return scaleweight

def midiwholeraags (tonicnote, raag):       # makes a list of all the MIDI numbers in a particular raag from a particular tonic - works like midiwholescales
    tonicmidi = notetomidi(tonicnote, 'NA')  
    t = 2    
    s = 1
    note = tonicmidi  
    raaglist = [tonicmidi]
    if raag.upper() == 'RAAG YAMAN' : 
        for i in range(1,70):
            if (i-4)%7 ==0 or i%7==0 :      # conditions for t-t-t-s-t-t-s 
                note = note + s
            else : 
                note = note + t
            if note >=12 and note <= 127 : 
                raaglist.append(note)
    if raag.upper() == 'RAAG BHAIRAV' : 
        for i in range(1,70):
            if (i-1)%7 ==0 or (i-3)%7==0 or (i-5)%7==0 :   # conditions for s-1.5t-s-t-s-1.5t-s
                note = note + s
            if (i-2)%7 ==0 or (i-6)%7==0 : 
                note = note + t + s         # there are bigger jumps in this scale, so an extra condition is added
            else : 
                note = note + t
            if note >=12 and note <= 127 : 
                raaglist.append(note)
    if raag.upper() == 'RAAG BILAWAL' :
        for i in range(1,70):  
            if i%7 == 0 or (i-3)%7 == 0 :   # same conditions as western major scale - same notes
                note = note + s
            else : 
                note = note + t
            if note >=12 and note <= 127 :
                raaglist.append(note)
    return raaglist

def midiraagweight(raag, raaglist):         # makes a list of probabilities of each MIDI number (favours different notes for each raag) - works similar to scaleweight
    raagweight = []
    # could also be modified to be based on phrases of melodies, instead of individual notes
    if raag == 'Raag Yaman' : 
        for i in range(1,(len(raaglist)+1)):
            if i == 3 or (i-3)%7 == 0 :         # 3rd and 7th most important
                raagweight.append(32)
            elif i%7 == 0 : 
                raagweight.append(23)
            else : 
                raagweight.append(9)
    
    if raag == 'Raag Bhairav' : 
        for i in range(1,(len(raaglist)+1)):
            if (i+1)%7 == 0 :         # 6th and 2nd most important
                raagweight.append(32)
            elif (i-2)%7 == 0 : 
                raagweight.append(23)
            else : 
                raagweight.append(9)

    if raag == 'Raag Bilawal' : 
        for i in range(1,(len(raaglist)+1)):
            if (i+1)%7 == 0 :         # 6th and 3th most important
                raagweight.append(32)
            elif (i-3)%7 == 0 : 
                raagweight.append(23)
            else : 
                raagweight.append(9)
    
    return raagweight

def taalrhythm(taal):                       # makes 4 lists of times that, together, create a taal reference for each taal
    # General MIDI does not include any Indian percussion instruments - so I have used western instruments to represent the different types of percussion hits in Indian music
    bass_free = []      # rep by acoustic bass drum (low open sound)
    bass_tight = []     # rep by side stick (low closed sound)
    long_open = []      # rep by hand clap (high open sound)
    short_open = []     # rep by acoustic snare (high closed sound)
    if taal == 'Teentaal': 

        bass_free =[0,1,2,3,4,5,6,7,8,13,14,15]
        bass_tight = [9,10]
        long_open = [1,2,5,6,9,10,13,14]
        short_open = [0,3,4,7,8,11,12,15]

    if taal == 'Jhaptaal': 

        bass_free =[0,2,3,7,8]
        bass_tight = [5]
        long_open = [0,2,3,5,7,8]
        short_open = [1,4,6,9]
    
    if taal == 'Keherwa':

        bass_free =[0,1,6]
        bass_tight = [3,5]
        long_open = [3,6]
        short_open = [2,4,7]
    
    rhythm_times = [bass_free, bass_tight, long_open, short_open]       # returns everything in one list to make it easier to use
    return rhythm_times

def lehra(tonicmidi,raag, taal):            # makes 3 lists of information that create different lehra (background melody) patterns for each raag and taal combination
    lehra_notes = []
    lehra_times = []
    lehra_durs = []
    if raag == 'Raag Yaman' :               # generates a standard simple pattern - no customisation here (for reference)
        lehra_notes = [tonicmidi+4,tonicmidi-1,tonicmidi+6,tonicmidi+4,tonicmidi]
        if taal == 'Teentaal' or taal == 'Keherwa':     # share similar metre, so one pattern can be used
            lehra_times = [0,3,4,5,6]
            lehra_durs = [3,1,1,1,2]
        if taal == 'Jhaptaal':                          # different (5/4) metre, so needs a different pattern
            lehra_times = [0,3,5,6,8]
            lehra_durs = [3,2,1,2,2]
    if raag == 'Raag Bhairav' :
        lehra_notes = [tonicmidi+8,tonicmidi+1,tonicmidi+8,tonicmidi+1,tonicmidi]
        if taal == 'Teentaal' or taal == 'Keherwa':
            lehra_times = [0,2,4,5,6]
            lehra_durs = [2,2,1,1,2]
        if taal == 'Jhaptaal':
            lehra_times = [0,2,4,5,8]
            lehra_durs = [2,2,1,3,2]
    if raag == 'Raag Bilawal' :
        lehra_notes = [tonicmidi+4,tonicmidi+9,tonicmidi+4,tonicmidi]
        if taal == 'Teentaal' or taal == 'Keherwa':
            lehra_times = [0,2,4,6]
            lehra_durs = [2,2,2,2]
        if taal == 'Jhaptaal':
            lehra_times = [0,2,5,8]
            lehra_durs = [2,3,3,2]
    lehra_out = [lehra_notes,lehra_times,lehra_durs]    # again, return as a list to make it easier to use
    return lehra_out

def mainrhythm(rhypattern):                 # makes 3/4 lists of times for different standard rhythm patterns
    kicks = []          # different lists = different rhythmic elements
    snares = []
    hats = []
    sidesticks = []

    # adds different times to the 3 or 4 lists based on which pattern the user chooses
    if rhypattern == 'Four on the Floor' :
        kicks = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        snares = [1,3,5,7,9,11,13,15]
        hats = [i + 0.5 for i in range(0,16)]
    
    if rhypattern == 'Backbeat' : 
        kicks = [0,2,4,6,8,10,12,14]
        snares = [1,3,5,7,9,11,13,15]
        hats = [i + 0.5 for i in range(0,16)]

    if rhypattern == 'Half-Time Shuffle' : 
        kicks = [0,8]
        snares = [10]
        hats = [0,2,3,5,6,8,10,11,13,14]
        sidesticks = [1,3,5,7,9,11,13,15]
    
    if rhypattern == 'Bo Diddley Beat' : 
        kicks = [0,3,5,7,9]
        snares = [2,5,8]
        hats = [i + 0.5 for i in range(0,16)]
    
    out_rhythm = [kicks, snares, hats, sidesticks]      # return as a list of all lists
    return out_rhythm

def percrhythm(percpattern):                # outputs a list for each percussion pattern option
    perc_pattern_dict = {       # uses a dictionary; values were generated using list comprehensions and print statements (as list comprehensions don't work with floats)
        'Simple Eighths': [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5],
        'Off-beat Eighths': [0.25,0.75,1.25,1.75,2.25,2.75,3.25,3.75,4.25,4.75,5.25,5.75,6.25,6.75,7.25,7.75,8.25, 8.75, 9.25, 9.75, 10.25, 10.75, 11.25, 11.75, 12.25, 12.75, 13.25, 13.75, 14.25, 14.75, 15.25, 15.75],
        'Triplet Eighths': [0,0.375,0.75,1,1.375,1.75,2,2.375,2.75,3,3.375,3.75,4,4.375,4.75,5,5.375,5.75,6,6.375,6.75,7,7.375,7.75,8, 8.375, 8.75, 9, 9.375, 9.75, 10, 10.375, 10.75, 11, 11.375, 11.75, 12, 12.375, 12.75, 13, 13.375, 13.75, 14, 14.375, 14.75, 15, 15.375, 15.75],
        'Triplets': [0,0.75,1.5,2.25,3,3.5,4,4.75,5.5,6.25,7,7.5,8, 8.75, 9.5, 10.25, 11, 11.5, 12, 12.75, 13.5, 14.25, 15, 15.5]
    }
    out_perc = perc_pattern_dict[percpattern]
    return out_perc

def midichords(tonic, scale, octave, progression):  # generates a list of lists based on a chosen chord progression and scale
    tonicmidi = notetomidi(tonic, octave)
    chordlist = []
    if scale == 'Major' and progression == 'I vi V IV':            # used 'and' as multiple enclosed if statements was confusing
        chord1 = [tonicmidi, tonicmidi + 4, tonicmidi + 7]         # adds in the appropriate chord using the tonicmidi number as a reference
        chord2 = [tonicmidi + 9, tonicmidi + 12, tonicmidi + 16]
        chord3 = [tonicmidi + 7, tonicmidi + 11, tonicmidi + 14]
        chord4 = [tonicmidi + 5, tonicmidi + 9, tonicmidi + 12]
        chordlist = [chord1, chord2, chord3, chord4]               # a list of chords that make up the progression
    if scale == 'Major' and progression == 'I V vi IV':
        chord1 = [tonicmidi, tonicmidi + 4, tonicmidi + 7]
        chord3 = [tonicmidi + 9, tonicmidi + 12, tonicmidi + 16]
        chord2 = [tonicmidi + 7, tonicmidi + 11, tonicmidi + 14]
        chord4 = [tonicmidi + 5, tonicmidi + 9, tonicmidi + 12]
        chordlist = [chord1, chord2, chord3, chord4]
    if scale == 'Minor' and progression == 'i iv v i':
        chord1 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chord2 = [tonicmidi + 5, tonicmidi + 8, tonicmidi + 12]
        chord3 = [tonicmidi + 7, tonicmidi + 10, tonicmidi + 14]
        chord4 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chordlist = [chord1, chord2, chord3, chord4]
    if scale == 'Minor' and progression == 'i ii v i':
        chord1 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chord2 = [tonicmidi + 2, tonicmidi + 5, tonicmidi + 8]
        chord3 = [tonicmidi + 7, tonicmidi + 10, tonicmidi + 14]
        chord4 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chordlist = [chord1, chord2, chord3, chord4]
    if scale == 'Dorian' and progression == 'i IV i v' : 
        chord1 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chord2 = [tonicmidi + 5, tonicmidi + 9, tonicmidi + 12]
        chord3 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chord4 = [tonicmidi + 7, tonicmidi + 10, tonicmidi + 14]
        chordlist = [chord1, chord2, chord3, chord4]
    if scale == 'Dorian' and  progression == 'i ii IV i' : 
        chord1 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chord2 = [tonicmidi + 2, tonicmidi + 5, tonicmidi + 9]
        chord3 = [tonicmidi + 5, tonicmidi + 9, tonicmidi + 12]
        chord4 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chordlist = [chord1, chord2, chord3, chord4]
    if scale == 'Phrygian' and progression == 'i bII i v' : 
        chord1 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chord2 = [tonicmidi + 1, tonicmidi + 5, tonicmidi + 8]
        chord3 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chord4 = [tonicmidi + 7, tonicmidi + 10, tonicmidi + 14]
        chordlist = [chord1, chord2, chord3, chord4]
    if scale == 'Phrygian' and progression == 'i iv bII i' : 
        chord1 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chord2 = [tonicmidi + 5, tonicmidi + 8, tonicmidi + 12]
        chord3 = [tonicmidi + 1, tonicmidi + 5, tonicmidi + 8]
        chord4 = [tonicmidi, tonicmidi + 3, tonicmidi + 7]
        chordlist = [chord1, chord2, chord3, chord4]
    if scale == 'Mixolydian' and progression == 'I bVII IV I' : 
        chord1 = [tonicmidi, tonicmidi + 4, tonicmidi + 7]
        chord2 = [tonicmidi + 9, tonicmidi + 12, tonicmidi + 16]
        chord3 = [tonicmidi + 5, tonicmidi + 9, tonicmidi + 12]
        chord4 = [tonicmidi, tonicmidi + 4, tonicmidi + 7]
        chordlist = [chord1, chord2, chord3, chord4]
    if scale == 'Mixolydian' and progression == 'I v IV I' : 
        chord1 = [tonicmidi, tonicmidi + 4, tonicmidi + 7]
        chord2 = [tonicmidi + 7, tonicmidi + 10, tonicmidi + 14]
        chord3 = [tonicmidi + 5, tonicmidi + 9, tonicmidi + 12]
        chord4 = [tonicmidi, tonicmidi + 4, tonicmidi + 7]
        chordlist = [chord1, chord2, chord3, chord4]
    return chordlist

def midichords_alt(tonic, octave, chordlist):       # alters the chordlist by moving certain notes down an octave for closer movements
    tonicmidi = notetomidi(tonic, octave)
    chord1 = chordlist[0]
    chord2 = chordlist[1]
    chord3 = chordlist[2]
    chord4 = chordlist[3]
    chord1alt = []
    chord2alt = []
    chord3alt = []
    chord4alt = []
    chordlistalt = [chord1alt, chord2alt, chord3alt, chord4alt]
    
    for item in chord1:
        if item < tonicmidi + 11:   # checks if the note is below the 7th note of the scale
            chord1alt.append(item)  
        elif item >= tonicmidi + 11: 
            chord1alt.append(item-12)   # if it is above, it's transposed an octave down

    for item in chord2:
        if item < tonicmidi + 11:
            chord2alt.append(item)
        elif item >= tonicmidi + 11: 
            chord2alt.append(item-12)
    
    for item in chord3:
        if item < tonicmidi + 11:
            chord3alt.append(item)
        elif item >= tonicmidi + 11: 
            chord3alt.append(item-12)

    for item in chord4:
        if item < tonicmidi + 11:
            chord4alt.append(item)
        elif item >= tonicmidi + 11: 
            chord4alt.append(item-12)
    
    return chordlistalt

def arpmidimaker(arppattern, chordlist):    # makes a list of lists in different orders for different arpeggio patterns for the selected chords
    chord1 = chordlist[0]
    chord2 = chordlist[1]
    chord3 = chordlist[2]
    chord4 = chordlist[3]
    arplist1 = []
    arplist2 = []
    arplist3 = []
    arplist4 = []
    if arppattern == 'Ascending and Descending' :   # makes each list - ordering the notes of each chord differently according to the pattern 
        arplist1 = [chord1[0]+12, chord1[1]+12, chord1[2]+12, chord1[1]+12, chord1[0]+12, chord1[1]+12, chord1[2]+12, chord1[1]+12]     # transposes these notes up an octave to keep them separate from the chord octave
        arplist2 = [chord2[0]+12, chord2[1]+12, chord2[2]+12, chord2[1]+12, chord2[0]+12, chord2[1]+12, chord2[2]+12, chord2[1]+12]
        arplist3 = [chord3[0]+12, chord3[1]+12, chord3[2]+12, chord3[1]+12, chord3[0]+12, chord3[1]+12, chord3[2]+12, chord3[1]+12]
        arplist4 = [chord4[0]+12, chord4[1]+12, chord4[2]+12, chord4[1]+12, chord4[0]+12, chord4[1]+12, chord4[2]+12, chord4[1]+12]
    
    if arppattern == 'Ascending' : 
        arplist1 = [chord1[0]+12, chord1[1]+12, chord1[2]+12, chord1[0]+12, chord1[1]+12, chord1[2]+12, chord1[0]+12, chord1[1]+12]
        arplist2 = [chord2[0]+12, chord2[1]+12, chord2[2]+12, chord2[0]+12, chord2[1]+12, chord2[2]+12, chord2[0]+12, chord2[1]+12]
        arplist3 = [chord3[0]+12, chord3[1]+12, chord3[2]+12, chord3[0]+12, chord3[1]+12, chord3[2]+12, chord3[0]+12, chord3[1]+12]
        arplist4 = [chord4[0]+12, chord4[1]+12, chord4[2]+12, chord4[0]+12, chord4[1]+12, chord4[2]+12, chord4[0]+12, chord4[1]+12]

    if arppattern == 'Descending' : 
        arplist1 = [chord1[2]+12, chord1[1]+12, chord1[0]+12, chord1[2]+12, chord1[1]+12, chord1[0]+12, chord1[2]+12, chord1[1]+12]
        arplist2 = [chord2[2]+12, chord2[1]+12, chord2[0]+12, chord2[2]+12, chord2[1]+12, chord2[0]+12, chord2[2]+12, chord2[1]+12]
        arplist3 = [chord3[2]+12, chord3[1]+12, chord3[0]+12, chord3[2]+12, chord3[1]+12, chord3[0]+12, chord3[2]+12, chord3[1]+12]
        arplist4 = [chord4[2]+12, chord4[1]+12, chord4[0]+12, chord4[2]+12, chord4[1]+12, chord4[0]+12, chord4[2]+12, chord4[1]+12]

    if arppattern == 'Highest and Lowest 1' : 
        arplist1 = [chord1[0]+12, chord1[2]+12, chord1[0]+12, chord1[2]+12, chord1[0]+12, chord1[2]+12, chord1[0]+12, chord1[2]+12]
        arplist2 = [chord2[0]+12, chord2[2]+12, chord2[0]+12, chord2[2]+12, chord2[0]+12, chord2[2]+12, chord2[0]+12, chord2[2]+12]
        arplist3 = [chord3[0]+12, chord3[2]+12, chord3[0]+12, chord3[2]+12, chord3[0]+12, chord3[2]+12, chord3[0]+12, chord3[2]+12]
        arplist4 = [chord4[0]+12, chord4[2]+12, chord4[0]+12, chord4[2]+12, chord4[0]+12, chord4[2]+12, chord4[0]+12, chord4[2]+12]

    if arppattern == 'Highest and Lowest 2' : 
        arplist1 = [chord1[2]+12, chord1[0]+12, chord1[2]+12, chord1[0]+12, chord1[2]+12, chord1[0]+12, chord1[2]+12, chord1[0]+12]
        arplist2 = [chord2[2]+12, chord2[0]+12, chord2[2]+12, chord2[0]+12, chord2[2]+12, chord2[0]+12, chord2[2]+12, chord2[0]+12]
        arplist3 = [chord3[2]+12, chord3[0]+12, chord3[2]+12, chord3[0]+12, chord3[2]+12, chord3[0]+12, chord3[2]+12, chord3[0]+12]
        arplist4 = [chord4[2]+12, chord4[0]+12, chord4[2]+12, chord4[0]+12, chord4[2]+12, chord4[0]+12, chord4[2]+12, chord4[0]+12]
    
    arplistglob = [arplist1, arplist2, arplist3, arplist4]
    return arplistglob

def chord_trigger_midi(trigger_pattern):    # makes a list of times for different chord trigger patterns
    rand_trigger_choices = [0.25,0.5,0.75,1]    # used to generate random times for a random trigger setting
    trig_pattern_dict = {
        'Crotchet Trigger': [i for i in range(0,16)],   # used list comprehension to make crotchet pattern
        'Quaver Trigger' : [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5],    
        'Triplet Trigger' : [0,0.75,1.5,2.25,3,3.5,4,4.75,5.5,6.25,7,7.5,8, 8.75, 9.5, 10.25, 11, 11.5, 12, 12.75, 13.5, 14.25, 15, 15.5],
        'Random Trigger' : [i + random.choice(rand_trigger_choices) for i in range(0,16)]   # used list comprehension and random choices to make random pattern 
    }
    out_trigger = trig_pattern_dict[trigger_pattern]   
    return out_trigger

def composed_popup(mode, msg_inputs):       # GUI function that brings up a small window whenever a MIDI file is created (or altered)
        if mode == 'western' :              # conditional statements change the message displayed for Indian and Western mode
            key = msg_inputs[0].upper() + ' ' + msg_inputs[1] 
            msg = key + ' at ' + str(msg_inputs[2]) + ' bpm' 
            
        elif mode == 'indian' : 
            msg = msg_inputs[1] + ' in ' + msg_inputs[0].upper() + ' in ' + msg_inputs[2]
        
        # GUI creation
        root_composed = tkinter.Toplevel()              # top level window and window details
        root_composed.title('Western MIDI Composed!')   
        root_composed.geometry('250x250')
        
        bg_pop = PhotoImage(file = 'popup.png')         # setting the window's background image
        back_label3 = tkinter.Label(root_composed, image = bg_pop)
        back_label3.image = bg_pop
        back_label3.place(x=0, y=0)

        # label creation
        composed_label = tkinter.Label(root_composed, text = 'Composed!', font = 'Palatino 24 bold', pady=60, bg='#482218', fg = '#E0D7C4')
        sub_label = tkinter.Label(root_composed, text = 'Open your new MIDI file', font = 'Palatino 14', pady=60, bg='#482218', fg = '#E0D7C4')
        sub_label2 = tkinter.Label(root_composed, text = msg, font = 'Palatino 14', bg='#482218', fg = '#E0D7C4', pady=60)

        # making the grid
        root_composed.columnconfigure(0, weight = 1, uniform = 'a')
        root_composed.rowconfigure((0,1,2,3,4), weight = 1, uniform = 'a')

        # placing things in the grid
        composed_label.grid(row=1, column=0, sticky = 's')
        sub_label.grid(row=2, column=0)
        sub_label2.grid(row=3, column=0)


# main function - function that references all supporting functions

def runtest():      # function is called when the user presses the 'Start' button
    fin_filename = file_text.get() + '.mid'     # makes it so the user doesn't need to add the file extension themselves
    print (fin_filename)        

    # setting background images
    bg_comp1 = PhotoImage(file = 'root_west.png')  
    bg_comp2 = PhotoImage(file = 'root_ind.png')
    
    def midiwesterncomposer():                          # calls all western composition functions and adds data to MIDI file
        
        # receving all the user-inputted data from the GUI and assigning it to variables
        # basic
        tonic = str(tonic_text.get())
        length = int(length_text.get())
        tempo = int(tempo_text.get())
        num_tracks = int(numtracks_spin.get())
        scale = str(scale_drop.get())
       
        # note divisions
        biggestnote = str(mindev_drop.get())
        smallestnote = str(maxdev_drop.get())
        
        # pitch range
        minrange = [str(minrannote_drop.get()),int(minranoct_drop.get())]
        maxrange = [str(maxrannote_drop.get()),int(maxranoct_drop.get())]
        
        # chords
        progression = str(prog_drop.get())
        voice_alt = str(chord_voice_alt_drop.get())
        octave = int(octave_text.get())

        # patterns
        rhypattern = str(rhythm_drop.get())
        arppattern = str(arps_drop.get())
        percpattern = str(perc_drop.get())
        trigger_pattern = str(trigs_drop.get())

        # instruments
        mel_instrument = str(inst_drop.get())
        chord_instrument = str(chord_inst_drop.get())
        arp_instrument = str(arp_inst_drop.get())
        perc_inst_choice = str(perc_inst_drop.get())


        # dictionaries 
        notedivs = {'Semibreve' : 4,            # assigns note names to beat values
                    'Dotted Minum' : 3, 
                    'Minum' : 2, 
                    'Crotchet' : 1, 
                    'Quaver' : 0.5}
        
        biggestdiv = notedivs[biggestnote]      # changes the note name to a usable value
        smallestdiv = notedivs[smallestnote]

        instruments = {'Grand Piano' : 0,       # assigns available instruments to General MIDI numbers
                       'Electric Piano' : 4, 
                       'Dulcimer' : 15, 
                       'Church Organ' : 19, 
                       'Nylon Guitar' : 24, 
                       'String Ensemble' : 48, 
                       'Choir' : 52, 
                       'Brass Section' : 61 }
    
        perc_instruments = {'Cowbell' : 56,     # assigns available instruments to General MIDI numbers on Channel 9 (for percussion instruments)
                            'Tambourine' : 54,
                            'Maracas' : 70,
                            'Hand Claps' : 39,
                            'Claves' : 75, 
                            'Ride' : 59,
                            'Hi Hats' : 42
                            }
        
        instrument_ranges = {'Grand Piano' : (21, 108),     # assigns instruments to appropriate MIDI ranges (so melodies don't exceed an instrument's range)
                             'Electric Piano' : (21, 108),  # these ranges are not for the actual version of the instrument
                             'Dulcimer' : (24,72),          # they are for the digital instrument - so what sounds good on the digital instrument (for a digital composer)
                             'Church Organ' : (24,60), 
                             'Nylon Guitar' : (36,60), 
                             'String Ensemble' : (24,84), 
                             'Choir' : (26,60), 
                             'Brass Section' : (24,72) }
        
        mel_range = instrument_ranges[mel_instrument]       # gets appropriate range information from dictionaries and user input
        mel_min = mel_range[0]
        mel_max = mel_range[1]

        acctrack_1 = num_tracks                             # creates correct track number and assigns different track numbers to variables
        acctrack_2 = num_tracks + 1
        acctrack_3 = num_tracks + 4
        rhytrack = num_tracks + 2
        perctrack = num_tracks + 3


        midiWESTcomp = MIDIFile(num_tracks+5)               # creates the MIDI file and sets the right number of tracks

        # gives each appropriate track its name and channel (for rhythm and percussion)
        midiWESTcomp.addTrackName(acctrack_1, 0, 'Block Chords')
        midiWESTcomp.addTrackName(acctrack_2, 0, 'Arpeggiated Chords')
        midiWESTcomp.addTrackName(acctrack_3, 0, 'Chord Trigger')
        midiWESTcomp.addTrackName(rhytrack, 9, 'Rhythm')
        midiWESTcomp.addTrackName(perctrack, 9, 'Percussion')

        midiWESTcomp.addTempo(0, 0, tempo)      # adds tempo information to MIDI file
        
        for i in range(0,(num_tracks)):         # assigns melody instrument to each of the melody tracks
            midiWESTcomp.addProgramChange(i, 0, 0, instruments[mel_instrument])


        # assigns the chord and arp instruments to the appropriate tracks    
        midiWESTcomp.addProgramChange(acctrack_1, 0, 0, instruments[chord_instrument])
        midiWESTcomp.addProgramChange(acctrack_2, 0, 0, instruments[arp_instrument])

        # time variables that will be used later to generate different elements
        time = 0
        time2 = 0

        # converts the pitch range to MIDI information
        minrangemidi = notetomidi(minrange[0],int(minrange[1])+2)
        maxrangemidi = notetomidi(maxrange[0],int(maxrange[1])+2)

        # calls functions to get relevant scale and chord information
        scalelist = midiwholescales(tonic, scale)
        scaleweight = midiscaleweight(scalelist)

        chordlist = midichords(tonic, scale, octave, progression)

        # leaves the chords the same if the user doesn't want closer chord movement
        if voice_alt == 'No' : 
            chordlist = midichords(tonic, scale, octave, progression)
            print('No')     # used to check if it is working without having to open the MIDI file

        # uses the transposition function if the user DOES want closer chord movement
        if voice_alt == 'Yes' : 
            chordlist = midichords_alt(tonic, octave, chordlist)
            print('Yes')

        arplistglob = arpmidimaker(arppattern, chordlist)       # calls this function AFTER the voice_alt check so the arp is also in the same inversions
        print ('Arplistglob : ', arplistglob)

        # adds each note in each chord to the MIDI file in semibreves
        for item in chordlist:
            midiWESTcomp.addNote(acctrack_1,0,item[0], time, 4, random.randint(60,110))
            midiWESTcomp.addNote(acctrack_1,0,item[1], time, 4, random.randint(60,110))
            midiWESTcomp.addNote(acctrack_1,0,item[2], time, 4, random.randint(60,110))
            time = time + 4

        print ('Chord list : ', chordlist)
        
        # adds the quaver value into the list if the user has included it in their selection - as there is no other way to include a SINGLE float value in a random selection
        note_div_choices_narrow = []
        if smallestdiv == 0.5 : 
            smallestdiv_upd = 1
            note_div_choices_narrow.append(0.5)     # adds 0.5 to the list of possible times and durations
            for i in range (smallestdiv_upd, biggestdiv + 1, 1):    # goes on to add the other values (ints)
                note_div_choices_narrow.append(i)
        else : 
            for i in range (smallestdiv, biggestdiv + 1, 1):        # JUST adds the integer values
                note_div_choices_narrow.append(i)

        print (note_div_choices_narrow)


        # generating the melodies
        for x in range(num_tracks):     # generates multiple melodies based on user input
            starttime = 0
            genseq = []  
            notes = random.choices(scalelist, scaleweight, k=length)        # makes a list of user chosen length using the scalelist and scaleweights from other functions
            for item in notes :
                if item >= minrangemidi and item <= (maxrangemidi + 1) and item >= mel_min and item <= mel_max :    # checks if each note is in the range chosen by the user, and the instrument range 
                    genseq.append(item)     # if so, it is added to the sequence
                    # this is why the length will not be exactly what the user wants - based on the instrument and pitch range, it will be closer or further from the length they choose
            for item in genseq:   
                midiWESTcomp.addNote(x, 0, item, starttime,random.choice(note_div_choices_narrow),random.randint(60,127) )      # adds each item in the sequence to the MIDI file at a random time and with a random (audible) velocity  
                starttime = starttime + random.choice(note_div_choices_narrow)     # adds a random time to the time used for the next note 

        print('Genseq : ', genseq)
            
        # adds each MIDI note in from the list of arpeggiated notes - also follows 1 chord per bar
        for item in arplistglob:
            midiWESTcomp.addNote(acctrack_2, 0, item[0], time2, 0.5, random.randint(60,110))    # also randomises velocity (in an audible range)
            midiWESTcomp.addNote(acctrack_2, 0, item[1], time2 + 0.5, 0.5, random.randint(60,110))
            midiWESTcomp.addNote(acctrack_2, 0, item[2], time2 + 1, 0.5, random.randint(60,110))
            midiWESTcomp.addNote(acctrack_2, 0, item[3], time2 + 1.5 , 0.5, random.randint(60,110))
            midiWESTcomp.addNote(acctrack_2, 0, item[4], time2 + 2, 0.5, random.randint(60,110))
            midiWESTcomp.addNote(acctrack_2, 0, item[5], time2 + 2.5, 0.5, random.randint(60,110))
            midiWESTcomp.addNote(acctrack_2, 0, item[6], time2 + 3, 0.5, random.randint(60,110))
            midiWESTcomp.addNote(acctrack_2, 0, item[7], time2 + 3.5 , 0.5, random.randint(60,110))
            time2 = time2 + 4 

        out_trigger = chord_trigger_midi(trigger_pattern)       # calls function to get chord trigger information

        for i in out_trigger:       # spans length of chord trigger list and adds each chord based on the position(i) - adding the first chord in bar 1, and so on
            if i >= 0 and i < 4 :   # first bar (beat 0,4) 
                chord1 = chordlist[0]
                midiWESTcomp.addNote(acctrack_3,0,chord1[0], i, 0.5, random.randint(60,110))
                midiWESTcomp.addNote(acctrack_3,0,chord1[1], i, 0.5, random.randint(60,110))
                midiWESTcomp.addNote(acctrack_3,0,chord1[2], i, 0.5, random.randint(60,110))
                print (i, chord1[0], chord1[1],chord1[2])
            elif i >= 4 and i < 8 : # second bar
                chord2 = chordlist[1]
                midiWESTcomp.addNote(acctrack_3,0,chord2[0], i, 0.5, random.randint(60,110))
                midiWESTcomp.addNote(acctrack_3,0,chord2[1], i, 0.5, random.randint(60,110))
                midiWESTcomp.addNote(acctrack_3,0,chord2[2], i, 0.5, random.randint(60,110))
                print (i, chord2[0], chord2[1],chord2[2])
            elif i >= 8 and i < 12 : # third bar 
                chord3 = chordlist[2]
                midiWESTcomp.addNote(acctrack_3,0,chord3[0], i, 0.5, random.randint(60,110))
                midiWESTcomp.addNote(acctrack_3,0,chord3[1], i, 0.5, random.randint(60,110))
                midiWESTcomp.addNote(acctrack_3,0,chord3[2], i, 0.5, random.randint(60,110))
                print (i, chord3[0], chord3[1],chord3[2])
            elif i >= 12 and i < 16 : # fourth bar - don't want a note on 16 - so the user can loop the 4 bars easily 
                chord4 = chordlist[3]
                midiWESTcomp.addNote(acctrack_3,0,chord4[0], i, 0.5, random.randint(60,110))
                midiWESTcomp.addNote(acctrack_3,0,chord4[1], i, 0.5, random.randint(60,110))
                midiWESTcomp.addNote(acctrack_3,0,chord4[2], i, 0.5, random.randint(60,110))
                print (i, chord4[0], chord4[1],chord4[2])
                

        # calling function to get rhythm lists and separating them into rhythm parts
        out_rhythm = mainrhythm(rhypattern)
        kicks = out_rhythm[0]
        snares = out_rhythm[1]
        hats = out_rhythm[2]
        sidesticks = out_rhythm[3]

        print ('Out rhythm : ', out_rhythm)

        # adds each element (through different MIDI notes) at the times specified in the different lists
        for i in kicks:
            midiWESTcomp.addNote(rhytrack, 9, 35, i, 0.5, 100)
        for i in snares: 
            midiWESTcomp.addNote(rhytrack, 9, 38, i, 0.5, 100)
        for i in hats: 
            midiWESTcomp.addNote(rhytrack, 9, 42, i, 0.5, 100)
        
        # this one pattern also has sidesticks, so if that is chosen, then it is addressed, otherwise it's overlooked
        if rhypattern == 'Half-Time Shuffle' : 
            for i in sidesticks: 
                midiWESTcomp.addNote(rhytrack, 9, 37, i, 0.5, 100)

        # calling function to get the percussion times list
        out_perc = percrhythm(percpattern)
        
        # same concept as rhythm lists
        for i in out_perc : 
            midiWESTcomp.addNote(perctrack, 9, perc_instruments[perc_inst_choice], i, 0.25, 100)
        
        

        # finally, writes the MIDI file
        with open(fin_filename, "wb") as file:
            midiWESTcomp.writeFile(file)

        # opens the popup window ONLY if the MIDI file has been generated (or altered)
        composed_popup('western', msg_inputs=[tonic, scale, tempo])       # sends relevant information to the window for display
        
    def midiindiancomposer(minnotediv=1, maxnotediv=2,num_tracks=1):    # calls all indian composition functions and adds data to MIDI file
        
        # receiving data from GUI and assigning it to variables
        # basics
        tonic = str(tonic_text.get())
        length = int(length_text.get())

        # indian mode basics
        raag = str(raag_drop.get()) 
        laya = str(laya_drop.get())
        num_tracks = int(numtracks_spin.get())
        taal = str(taal_drop.get())

        # instruments
        instrument_mel = str(inst_mel_drop.get())
        instrument_leh = str(inst_leh_drop.get())

        # dictionary that assigns available instruments to General MIDI numbers - due to General MIDI limitations, I'v used the accordion for the harmonium, flute for the bansuri, and stringe ensemble for the drone
        instruments = {'Sitar' : 104, 'Shehnai' : 111, 'Violin' : 110, 'Bansuri' : 73, 'Harmonium' : 21 }
        
        # Laya to tempo conversion - randomises tempo within a range for each laya - due to DAW limitations, free tempo within a range is not an option, which would be more appropriate for the laya
        if laya == 'Drut' : 
            tempo = random.randint(120,150)
        if laya == 'Madhyam' : 
            tempo = random.randint(90,119)
        if laya == 'Vilambit' :
            tempo = random.randint(50, 89)
        
        # sets track numbers to variables
        acctrack_1 = num_tracks
        acctrack_2 = num_tracks + 1
        rhytrack = num_tracks + 2
        
        # creats the MIDI file with the right number of tracks and the user-inputted laya (tempo)
        midiINDCOMP = MIDIFile(num_tracks+3)
        midiINDCOMP.addTempo(0, 0, tempo)
        
        # assigns list to time signature based on the taal and adds it to the MIDI file - allows the DAW metronome and barlines to sync up
        rhythm_times = taalrhythm(taal)
        time_sigs_taals_dict = {
            'Teentaal' : [4,2],
            'Jhaptaal' : [5,2],
            'Keherwa' : [2,2]
        }
        time_sig = time_sigs_taals_dict[taal]
        midiINDCOMP.addTimeSignature(0, 0, time_sig[0], time_sig[1], 24, 8)
        
        # getting the tonic midi note from the notetomidifunction
        tonicmidi = int(notetomidi(tonic, 3))
        

        # assigns MIDI range based on instrument range
        if instrument_mel == 'Sitar' : 
            minrangemidi = 52   
            maxrangemidi = 79
        
        if instrument_mel == 'Shehnai' : 
            minrangemidi = 57   
            maxrangemidi = 81

        if instrument_mel == 'Violin' : 
            minrangemidi = 43   
            maxrangemidi = 88

        if instrument_mel == 'Bansuri' : 
            minrangemidi = 51   
            maxrangemidi = 91
        
        if instrument_mel == 'Harmonium' : 
            minrangemidi = 48   
            maxrangemidi = 85
        

        # drone generator 
        midiINDCOMP.addProgramChange(acctrack_1, 0, 0, 48 )
        midiINDCOMP.addTrackName(acctrack_1, 0, 'Drone')
        midiINDCOMP.addNote(acctrack_1, 0, tonicmidi, 0, length, 70)        # adds a single drone note to the file on the tonic note


        # rhythm pattern generator
        bass_free = rhythm_times[0]     # gets lists from taal function
        bass_tight = rhythm_times[1]
        long_open = rhythm_times[2]
        short_open = rhythm_times[3]
        
        # adds notes on reference instruments (listed in taal function) at times specified in the generated lists
        for i in bass_free:
            midiINDCOMP.addNote(rhytrack, 9, 35,i,1,100)
    
        for x in bass_tight:
            midiINDCOMP.addNote(rhytrack,9,37,x, 1, 100)

        for y in long_open:
            midiINDCOMP.addNote(rhytrack,9,39,y, 1, 100)

        for z in short_open:
            midiINDCOMP.addNote(rhytrack,9,38,z, 1, 100)

       
        # sets each melody track to the right melodic instrument
        for i in range(0, num_tracks):
            midiINDCOMP.addProgramChange(i, 0, 0, instruments[instrument_mel])
        
        # calls previous functions to get lists for melody generation
        raaglist = midiwholeraags(tonic, raag)
        raagweights = midiraagweight(raag, raaglist)


        # melodic phrase generator
        for x in range(num_tracks):     # generates user-chosen number of different melody tracks
            starttime = 0
            genseq = []   
            notes = random.choices(raaglist, raagweights,k= length)     # again, creates a new notes list for each track of user-chosen length with appropriate probabilities for that raag 
            for item in notes:
                if item >= minrangemidi and item <= maxrangemidi:       # checks if the note is in the range of the chosen instrument - hence the actual length will not be exactly what the user entered, it'll change based on which instrument was used   
                    genseq.append(item)  
            for item in genseq:         # adds the sequence's notes to the MIDI file at random times and durations   
                midiINDCOMP.addNote(x, 0, item, starttime, 1/(random.randint(minnotediv,maxnotediv)), random.randint(60,127))   
                starttime = starttime + (random.randint(minnotediv,maxnotediv))


        # lehra generator - pulls a standard pattern from the lehra function and adds it to the MIDI file
        midiINDCOMP.addProgramChange(acctrack_2, 0, 0, instruments[instrument_leh])
        midiINDCOMP.addTrackName(acctrack_2, 0, 'Lehra')

        lehra_out = lehra(tonicmidi,raag, taal)
        lehra_notes = lehra_out[0]
        lehra_times = lehra_out[1]
        lehra_durs = lehra_out[2]
        lehra_len = len(lehra_notes)

        print (lehra_len)
        print (lehra_out)

        for i in range(0, lehra_len):   # spans length of lehra, adding in each note according to item in each list position
            leh_note = lehra_notes[i]
            leh_time = lehra_times[i]
            leh_dur = lehra_durs[i]

            print(leh_note, leh_time, leh_dur)
            
            midiINDCOMP.addNote(acctrack_2, 0, leh_note, leh_time, leh_dur, 100)    # adding to MIDI file

    
        # finally writing the MIDI file
        with open(fin_filename, "wb") as file:
            midiINDCOMP.writeFile(file)
        
        # opens popup window ONLY after MIDI file has been generated or altered
        composed_popup('indian', msg_inputs=[tonic, raag, taal, laya])

    if mode_drop.get() == 'Western' :                   # opens western composer window if the user selects western mode
        def update_options(event):                      # function that changes the chord progression options based on the scale chosen 
            category = scale_drop.get()
            prog_drop['values'] = prog_options.get(category, [])    # changes the values list based on the scale chosen (from a dictionary defined below)
            prog_drop.set((''))                     # if the scale is changed, the progression is set back to nothing

        # window settings
        root_west = tkinter.Toplevel()
        root_west.title('Western MIDI Composer')
        root_west.geometry('1500x550')

        # window background image
        back_label2 = tkinter.Label(root_west, image = bg_comp1)
        back_label2.place(x = 0, y = 0)

        # window objects - all using the same stylistic elements, and using the most convenient input method availabl for each information type
        west_title_label = tkinter.Label(root_west, text = 'Western MIDI Composer', font = 'Palatino 24 bold', bg = '#E0D7C4', fg = '#341811')
        
        # scale
        scales = ['Major', 'Minor', 'Dorian', 'Phrygian', 'Mixolydian']     # choices for scales
        scale_label = tkinter.Label(root_west, text = 'Choose Scale Type', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        scale_drop = ttk.Combobox(root_west, value = scales)
        scale_drop.bind('<<ComboboxSelected>>', update_options)
        scale_drop.set('Major')

        # tempo
        tempo_label = tkinter.Label(root_west, text = 'Tempo', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        tempo_text = tkinter.Entry(root_west, bg = '#E0D7C4', fg = '#341811')   # entry box for tempo seemed most customisable

        
        # note divisions
        divopts = ['Semibreve','Dotted Minum', 'Minum', 'Crotchet', 'Quaver']

        mindev_label = tkinter.Label(root_west, text = 'Max note value', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        mindev_drop = ttk.Combobox(root_west, values = divopts)
        mindev_drop.set('Semibreve')

        maxdev_label = tkinter.Label(root_west, text = 'Min note value', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        maxdev_drop = ttk.Combobox(root_west, values = divopts)
        maxdev_drop.set('Quaver')
 
        # pitch range
        notes = ['C','C#','Db','D','D#','Eb','F','F#','Gb','G','G#','Ab','A','A#','Bb','B']     # note options for pitch range
        octaves = [1,2,3,4,5,6,7,8]                                                             # octave options for pitch range
        
        minran_label = tkinter.Label(root_west, text = 'Lowest', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        minrannote_drop = ttk.Combobox(root_west, values = notes )
        minrannote_drop.set('C')
        minranoct_drop = ttk.Combobox(root_west, values = octaves)      # makes it convenient to enter a pitch using a drop down list
        minranoct_drop.set(1)

        maxran_label = tkinter.Label(root_west, text = 'Highest', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        maxrannote_drop = ttk.Combobox(root_west, values = notes)
        maxrannote_drop.set('C')
        maxranoct_drop = ttk.Combobox(root_west, values = octaves)
        maxranoct_drop.set(8)

        # number of melodies
        numtracks_label = tkinter.Label(root_west, text = 'Number of Melody Tracks', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        numtracks_spin = tkinter.Spinbox(root_west, from_ = 1, to = 20, bg = '#E0D7C4', fg = '#341811')     # defaults to 1

        
        # chord progression
        prog_options = {
            'Major' : ['I vi V IV','I V vi IV'],
            'Minor' : ['i iv v i','i ii v i'],
            'Dorian' :['i IV i v','i ii IV i'],
            'Phrygian' : ['i bII i v','i iv bII i'],
            'Mixolydian' : ['I bVII IV I','I v IV I']
        }
        
        prog_label = tkinter.Label(root_west, text = 'Chord Progression: ', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        prog_drop = ttk.Combobox(root_west, state = 'readonly')
   
        # chord customisation
        octave_label = tkinter.Label(root_west, text = 'Chord Octave', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        octave_text = tkinter.Entry(root_west, bg = '#E0D7C4', fg = '#341811')

        chord_voice_alt_label = tkinter.Label(root_west, text = 'Move voicings closer', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        chord_voice_alt_drop = ttk.Combobox(root_west, values = ['Yes','No'])
        chord_voice_alt_drop.set('No')

        # pattern choices
        rhythms = ['Four on the Floor', 'Backbeat', 'Half-Time Shuffle', 'Bo Diddley Beat']
        rhythm_label = tkinter.Label(root_west, text = 'Rhythm Pattern', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        rhythm_drop = ttk.Combobox(root_west, values = rhythms)
        rhythm_drop.set('Four on the Floor')

        percs = ['Simple Eighths', 'Off-beat Eighths', 'Triplet Eighths', 'Triplets']
        perc_label = tkinter.Label(root_west, text = 'Percussion Pattern', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        perc_drop = ttk.Combobox(root_west, values = percs)
        perc_drop.set('Simple Eighths')

        arps = ['Ascending and Descending', 'Ascending', 'Descending', 'Highest and Lowest 1', 'Highest and Lowest 2' ]
        arps_label = tkinter.Label(root_west, text = 'Arp Pattern', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        arps_drop = ttk.Combobox(root_west, values = arps)
        arps_drop.set('Ascending and Descending')

        chord_trigs = ['Crotchet Trigger','Quaver Trigger','Triplet Trigger','Random Trigger']
        trigs_label = tkinter.Label(root_west, text = 'Trigger Pattern', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        trigs_drop = ttk.Combobox(root_west, values = chord_trigs)
        trigs_drop.set('Crotchet Trigger')
 
        # instrument choices
        insts = ['Grand Piano', 'Electric Piano', 'Dulcimer', 'Church Organ', 'Nylon Guitar', 'String Ensemble', 'Choir', 'Brass Section']
        inst_label = tkinter.Label(root_west, text = 'Melody Instrument', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        inst_drop = ttk.Combobox(root_west, values = insts)
        inst_drop.set('Grand Piano')

        perc_insts = ['Cowbell','Tambourine','Maracas','Hi Hats','Claves','Ride','Hand Claps']
        perc_inst_label = tkinter.Label(root_west, text = 'Percussion Instrument', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        perc_inst_drop = ttk.Combobox(root_west, values = perc_insts)
        perc_inst_drop.set('Cowbell')

        chord_inst_label = tkinter.Label(root_west, text = 'Chord Instrument', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        chord_inst_drop = ttk.Combobox(root_west, values = insts, width = 20)
        chord_inst_drop.set('Grand Piano')

        arp_inst_label = tkinter.Label(root_west, text = 'Arp and Trigger Instrument', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        arp_inst_drop = ttk.Combobox(root_west, values = insts)
        arp_inst_drop.set('Grand Piano')

        # compose button - calls western composer function and creates MIDI file - will open another little popup window
        compose_button = tkinter.Button(root_west, text = 'Compose!', font = 'Palatino 24', bg = '#E0D7C4', fg = '#341811', command = lambda:midiwesterncomposer())

        # making grid - positioning all GUI elements for this window
        root_west.columnconfigure((0,1,2), weight = 1, uniform = 'a')
        root_west.rowconfigure((0,1,2,3,4,5), weight = 1, uniform = 'a' ) 

        # placing everything in the grid
        west_title_label.grid(row=0, column=1, sticky = 's')

            # first row
        scale_label.grid(row=1, column=0, sticky='n', padx = 20)
        scale_drop.grid(row=1, column=0, sticky='n', pady=20, padx = 20)

        tempo_label.grid(row=1, column=1,sticky='n', padx = 20)
        tempo_text.grid(row=1, column=1, sticky='n', pady=20, padx = 20)

        numtracks_label.grid(row=1,column=2, sticky='n', padx = 20)
        numtracks_spin.grid(row=1,column=2, sticky='n', pady=20, padx = 20)

            # second row
        mindev_label.grid(row=2, column=0, sticky='nw', pady=10, padx = 140)
        mindev_drop.grid(row=2,column=0, sticky='ne', pady=10, padx=40)

        maxdev_label.grid(row=2, column=0, sticky='sw', pady=10, padx = 140)
        maxdev_drop.grid(row=2,column=0, sticky='se', pady=10, padx=40)

        rhythm_label.grid(row=2, column=1, sticky='nw', pady=30, padx = 20)
        rhythm_drop.grid(row=2, column=1, sticky='sw', pady=10, padx = 20)

        perc_label.grid(row=2, column=1, sticky='ne', pady=30, padx = 20)
        perc_drop.grid(row=2, column=1, sticky='se', pady=10, padx = 20)

        minran_label.grid(row=2, column=2, sticky='nw', pady=5)
        minrannote_drop.grid(row=2,column=2, sticky='w')
        minranoct_drop.grid(row=2,column=2, sticky='sw')

        maxran_label.grid(row=2, column=2, sticky='ne', pady=5, padx = 80)
        maxrannote_drop.grid(row=2,column=2, sticky='e', padx = 80)
        maxranoct_drop.grid(row=2,column=2, sticky='se', padx = 80)

            # third row
        prog_label.grid(row=3, column=0, sticky='nw', pady=10, padx = 80)
        prog_drop.grid(row=3, column=0, sticky='nw', pady=30, padx = 80)

        chord_voice_alt_label.grid(row=3, column=0, sticky='ne', pady=10)
        chord_voice_alt_drop.grid(row=3, column=0, sticky='ne', pady=30)

        octave_label.grid(row=3, column=1, sticky='n', pady=10, padx = 20)
        octave_text.grid(row=3, column=1, sticky='n', pady=30, padx = 20)

        arps_label.grid(row=3, column=2, sticky='nw', pady=10)
        arps_drop.grid(row=3, column=2, sticky='nw', pady=30)

        trigs_label.grid(row=3, column=2, sticky='ne', pady=10, padx = 80)
        trigs_drop.grid(row=3, column=2, sticky='ne', pady=30, padx = 80)

            # fourth row
        inst_label.grid(row=4, column=0, sticky='nw', padx = 80)
        inst_drop.grid(row=4, column=0, sticky='nw', pady=20, padx = 80)

        chord_inst_label.grid(row=4, column=0, sticky='ne')
        chord_inst_drop.grid(row=4, column=0, sticky='ne', pady=20)

        perc_inst_label.grid(row=4, column=1, sticky='n', padx = 20)
        perc_inst_drop.grid(row=4, column=1, sticky='n', pady=20, padx = 20)

        arp_inst_label.grid(row=4, column=2, sticky='n', padx = 20)
        arp_inst_drop.grid(row=4, column=2, sticky='n', pady=20, padx = 20)

            # fifth row
        compose_button.grid(row=5, column=1, sticky = 'n')

            # closing the western composer window loop
        root_west.mainloop()
          
    elif mode_drop.get() == 'Indian' :                  # opens indian composer window if the user selects indian mode
        
        # window settings
        root_ind = tkinter.Toplevel()
        root_ind.title('Indian MIDI Composer')
        root_ind.geometry('1300x400')

        # background image settings
        back_label2 = tkinter.Label(root_ind, image = bg_comp2)
        back_label2.place(x = 0, y = 0)

        # window widgets
        indian_title = tkinter.Label(root_ind, text = 'Indian MIDI Composer', font = 'Palatino 24 bold', bg = '#E0D7C4', fg = '#341811', pady = 60)
        
        numtracks_label = tkinter.Label(root_ind, text = 'Number of Melody Tracks', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        numtracks_spin = tkinter.Spinbox(root_ind, from_=1, to=20, bg = '#E0D7C4', fg = '#341811')
        
        # laya
        laya_options = ['Vilambit', 'Madhyam', 'Drut']
        laya_label = tkinter.Label(root_ind, text = 'Choose Laya', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        laya_drop = ttk.Combobox(root_ind, value = laya_options)
        laya_drop.set('Vilambit')
        
        # raag
        raags = ['Raag Yaman', 'Raag Bhairav', 'Raag Bilawal']
        raag_label = tkinter.Label(root_ind, text = 'Choose Raag', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        raag_drop = ttk.Combobox(root_ind, value = raags)
        raag_drop.set('Raag Yaman')
        
        # taal
        taal_options = ['Teentaal', 'Jhaptaal', 'Keherwa']
        taal_label = tkinter.Label(root_ind, text = 'Choose Taal', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        taal_drop = ttk.Combobox(root_ind, values = taal_options)
        taal_drop.set('Teentaal')
        
        # instruments
        ind_insts = ['Sitar', 'Shehnai', 'Violin', 'Bansuri', 'Harmonium']

        inst_mel_label = tkinter.Label(root_ind, text = 'Instrument for Melody', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        inst_mel_drop = ttk.Combobox(root_ind, values = ind_insts)
        inst_mel_drop.set('Sitar')
        
        inst_leh_label = tkinter.Label(root_ind, text = 'Instrument for Lehra', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
        inst_leh_drop = ttk.Combobox(root_ind, values = ind_insts)
        inst_leh_drop.set('Harmonium')
        
        # compose button - calls indian composer function and opens popup when MIDI file is created or altered
        compose_button = tkinter.Button(root_ind, text = 'Compose!', font = 'Palatino 24', bg = '#E0D7C4', fg = '#341811', command = lambda:midiindiancomposer())

        # making the grid - layout
        root_ind.columnconfigure((0,1,2), weight = 1, uniform = 'a')
        root_ind.rowconfigure((0,1,2,3,4,5,6), weight = 1, uniform = 'a')       # added an extra row at the top and bottom for some more padding

        # placing stuff on the grid
            
            # first row
        indian_title.grid(row=1, column=1, sticky = 's')

            # second row
        numtracks_label.grid(row=2, column=1, sticky='n', pady=5)
        numtracks_spin.grid(row=2, column=1, sticky='s')

            # third row
        laya_label.grid(row=3, column=0, sticky='n', pady=5)
        laya_drop.grid(row=3, column=0, sticky='s')

        raag_label.grid(row=3, column=1, sticky='n', pady=5)
        raag_drop.grid(row=3, column=1, sticky='s')

        taal_label.grid(row=3, column=2, sticky='n', pady=5)
        taal_drop.grid(row=3, column=2, sticky='s')

            # fourth row
        inst_mel_label.grid(row=4, column=1, sticky='nw', pady=5)
        inst_mel_drop.grid(row=4, column=1, sticky='sw')

        inst_leh_label.grid(row=4, column=1, sticky='ne', pady=5)
        inst_leh_drop.grid(row=4, column=1, sticky='se')

            # fifth row
        compose_button.grid(row=5, column=1, sticky='s')

        root_ind.mainloop()         # closing out the indian composer window

# Composer settings window GUI 

# window settings
root1 = tkinter.Tk()
root1.title('Composer Settings')
root1.geometry('500x500')

# background image settings
bgimg = PhotoImage(file = 'root1ex.png')
back_label = tkinter.Label(root1, image = bgimg)
back_label.place(x = 0, y = 0)

# window objects
title_label = tkinter.Label(root1, text = 'Composer Settings', font = 'Palatino 20 bold', bg = '#E0D7C4', fg = '#341811')

# file name
file_label = tkinter.Label(root1, text = 'Enter File Name ', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
file_text = tkinter.Entry(root1, bg = '#E0D7C4', fg = '#341811')

# mode
modes = ['Western', 'Indian']
mode_label = tkinter.Label(root1, text = 'Choose a mode ', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
mode_drop = ttk.Combobox(root1, values = modes)

# tonic
tonic_label = tkinter.Label(root1, text = 'Enter Tonic Note', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
tonic_text = tkinter.Entry(root1, bg = '#E0D7C4', fg = '#341811')

# length
length_label = tkinter.Label(root1, text = 'Enter length (10-500 notes)', font = 'Palatino', bg = '#E0D7C4', fg = '#341811')
length_text = ttk.Scale(root1,orient='horizontal', from_ = 10, to=500, style='Horizontal.TScale')

# start button
enterbutton = tkinter.Button(root1, text = 'Start', font = 'Palatino 24', background=  '#A39C8F', command = lambda:runtest())

# making the grid - layout
root1.columnconfigure(0, weight = 1, uniform = 'a')
root1.rowconfigure((0,1,2,3,4,5,6,7), weight = 1, uniform = 'a')    # extra rows for padding

# placing everything
    
    # first row
title_label.grid(row = 1, column = 0)

    # second row
file_label.grid(row = 2, column = 0, sticky = 'n')
file_text.grid(row = 2, column = 0, sticky = 'n', pady = 20)

    # third row
mode_label.grid(row = 3, column = 0, sticky = 'n')
mode_drop.grid(row = 3, column = 0, sticky = 'n', pady = 20)

    # fourth row
tonic_label.grid(row = 4, column = 0, sticky = 'n')
tonic_text.grid(row = 4, column = 0, sticky = 'n', pady = 20)

    # fifth row
length_label.grid(row = 5, column = 0, sticky = 'n')
length_text.grid(row = 5, column = 0, sticky = 'n', pady = 20)

    # sixth row
enterbutton.grid(row = 6, column = 0, sticky = 'n')

root1.mainloop()        # closing out the composer settings window