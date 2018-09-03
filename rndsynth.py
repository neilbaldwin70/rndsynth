#! /usr/bin/env python3

from lxml import etree as ET
from typing import NamedTuple
import random
import math
import sys

random.seed(a=None,version=2)

class dp(NamedTuple):
    parameterType: str
    type: str
    init: int
    typeList: dict
    canModulate: bool
    group: bool

def int32(x):
  if x>0xFFFFFFFF:
    raise OverflowError
  if x>0x7FFFFFFF:
    x=int(0x100000000-x)
    if x<2147483648:
      return -x
    else:
      return -2147483648
  return x

def htosi(val):
    uintval = int(val,16)
    bits = 4 * (len(val) - 2)
    if uintval >= math.pow(2,bits-1):
        uintval = int(0 - (math.pow(2,bits) - uintval))
    return uintval

def hex2(n):
    return hex(n & 0xFFFFFFFF)

def rndSelection(list):
    return list[random.randint(0,len(list)-1)]

def addTag(_parent,_tag,_text):
    _result = ET.SubElement(_parent,_tag)
    _result.text = _text
    return _result

def hexString(x):
    h = (hex(x & 0xFFFFFFFF))
    if len(h) < 10:
        h = '0x' + ('0' * (len(h) - 8)) + h[2:]
    return h


#set defaults for command line options
octaveRange = 4
semitones = False
patchAll = False
patchLimit = 8
unisonLimit = 4
delayLimit = 10
lpfMinimum = 25
hpfMaximum = 25
resLimit = 20
reverbLimit = 25
srrLimit = 2
brrLimit = 2
saturationLimit = 2
noiseLimit = 20
rndArpeggiator = False
rndModFX = False
verbose = False

smin = -2147483648
smax = 2147483647
mMin = -1073741800
mMax = 1073741800
eMin = -2147483648
eMax = 0

sInt50range = abs(smin) + smax
sInt50step = int(sInt50range / 50)
int50range = smax
int50step = int(smax / 50)
mIntRange = abs(mMin) + mMax
mIntStep = int(mIntRange / 50)
eIntRange = abs(eMin) + eMax
eIntStep = int(eIntRange / 50)

sInt50 = []
int50 = []
mInt = []
eInt = []

# sInt50 : singned integer, 0x80000000 to 0x7FFFFFFF, full 32-bit range
for i in range(smin, smax, sInt50step):
    sInt50.append(hexString(i))

#int50 : decimal integer, full 32-bt range
for i in range(0, smax, int50step):
    int50.append(hexString(i))

#mInt: signed integer, 0 to 0x7FFFFFFF, biased towards higher numbers > 0 (> 25)
for i in range(mMin, mMax, int50step):
    mInt.append(hexString(i))

#eInt: signed integer, 0x80000000 to 0, biased towards lower numbers < 0 (< 25)
for i in range(eMin, eMax, eIntStep):
    eInt.append(hexString(i))


patchCableSourceList = [
    "lfo1",
    "lfo2",
    "envelope1",
    "envelope2",
    "velocity",
    "note",
    "random",
    "aftertouch"
# "compressor"
]

patchCableDestinationList = [
        "oscAVolume",
        "oscBVolume",
        # "volume",
        "noiseVolume",
        "range",
        "oscAPhaseWidth",
        "oscBPhaseWidth",
        "lpfResonance",
        "hpfResonance",
        "pan",
        "modulator1Volume",
        "modulator2Volume",
        "lpfFrequency",
        "pitch",
        "oscAPitch",
        "oscBPitch",
        "modulator1Pitch",
        "modulator2Pitch",
        "hpfFrequency",
        "lfo2Rate",
        "env1Attack",
        "env1Decay",
        "env1Sustain",
        "env1Release",
        "env2Attack",
        "env2Decay",
        "env2Sustain",
        "env2Release",
        "lfo1Rate",
        "volumePostFX",
        "volumePostReverbSend",
        "delayRate",
        "delayFeedback",
        "reverbAmount",
        "modFXRate",
        "modFXDepth",
        "arpRate",
        "modulator1Feedback",
        "modulator2Feedback",
        "carrier1Feedback",
        "carrier2Feedback",
]

modKnobDestinationsSubtractive = [
    "pan",
    "volume",
    "lpfResonance",
    "lpfFrequency",
    "env1Release",
    "env1Attack",
    "delayFeedback",
    "delayRate",
    "reverbAmount",
    "volumePostReverbSend",
    "pitch",
    "lfo1Rate",
    "portamento",
    "stutterRate",
    "bitCrushAmount",
    "sampleRateReduction",
]

modKnobDestinationsFM = [
    "pan",
    "volume",
    "modulator2Volume",
    "modulator1Volume",
    "env1Release",
    "env1Attack",
    "delayFeedback",
    "delayRate",
    "reverbAmount",
    "volumePostReverbSend",
    "pitch",
    "lfo1Rate",
    "portamento",
    "stutterRate",
    "carrier2Feedback",
    "carrier1Feedback",
]

modKnobDestinationsRingMod = [
    "pan",
    "volume",
    "lpfResonance",
    "lpfFrequency",
    "env1Release",
    "env1Attack",
    "delayFeedback",
    "delayRate",
    "reverbAmount",
    "volumePostReverbSend",
    "pitch",
    "lfo1Rate",
    "portamento",
    "stutterRate",
    "oscAPhaseWidth",
    "oscBPhaseWidth",
]



def randomParameter(p):
    t = delugeParameters.get(p)
    if t[3] == True:
        if t[0] == "TEXT":
            return (random.choice(t[2]))
        elif t[0] == "INT":
            return str((random.randint(t[2][0], t[2][1])))
        elif t[0] == "LINT" or t[0] == "SINT":
            return (random.choice(t[2]))
    else:
        if t[0] == "TEXT":
            return str(t[2][0])
        elif t[0] == "SINT" or t[0] == "LINT":
            return hexString(t[1])
        else:
            return str(t[1])


def addTag(_element, _tag, _text):
    ET.SubElement(_element,_tag).text = str(_text)
    return _text


fileNameBase = ""

for arg in range(len(sys.argv)):
    if sys.argv[arg] == '--outputBase':
        fileNameBase = str(sys.argv[arg + 1])
        if len(fileNameBase) < 3 or len(fileNameBase) > 3:
            print()
            print("Error: filename base must be 3 digits e.g. 250")
            print()
            sys.exit(1)
    if sys.argv[arg] == '--semitones':
        argText = sys.argv[arg + 1]
        if argText == 'true' or argText == 'True':
            semitones = True
        else:
            semitones = False
    if sys.argv[arg] == '--patchAll':
        argText = sys.argv[arg + 1]
        if argText == 'true' or argText == 'True':
            patchAll = True
        else:
            patchAll = False
    if sys.argv[arg] == '--rndArpeggiator':
        argText = sys.argv[arg + 1]
        if argText == 'true' or argText == 'True':
            rndArpeggiator = True
        else:
            rndArpeggiator = False
    if sys.argv[arg] == '--octaveRange':
        octaveRange = int(sys.argv[arg + 1])
        if octaveRange < 1 or octaveRange > 8:
            octaveRange = 4
    if sys.argv[arg] == '--patchLimit':
        patchLimit = int(sys.argv[arg + 1])
        if patchLimit < 1 or patchLimit > 32:
            patchLimit = 8
    if sys.argv[arg] == '--unisonLimit':
        unisonLimit = int(sys.argv[arg + 1])
        if unisonLimit < 1 or unisonLimit > 8:
            unisonLimit = 4
    if sys.argv[arg] == '--delayLimit':
        delayLimit = int(sys.argv[arg + 1])
        if delayLimit < 0 or delayLimit > 50:
            delayLimit = 10
    if sys.argv[arg] == '--reverbLimit':
        reverbLimit = int(sys.argv[arg + 1])
        if reverbLimit < 0 or reverbLimit > 50:
            reverbLimit = 25
    if sys.argv[arg] == '--lpfMinimum':
        lpfMinimum = int(sys.argv[arg + 1])
        if lpfMinimum < 0 or lpfMinimum > 50:
            lpfMinimum = 20
    if sys.argv[arg] == '--hpfMaximum':
        hpfMaximum = int(sys.argv[arg + 1])
        if hpfMaximum < 0 or hpfMaximum > 50:
            hpfMaximum = 20
    if sys.argv[arg] == '--resLimit':
        resLimit = int(sys.argv[arg + 1])
        if resLimit < 0 or resLimit > 50:
            resLimit = 20
    if sys.argv[arg] == '--srrLimit':
        srrLimit = int(sys.argv[arg + 1])
        if srrLimit < 0 or srrLimit > 50:
            srrLimit = 2
    if sys.argv[arg] == '--brrLimit':
        brrLimit = int(sys.argv[arg + 1])
        if brrLimit < 0 or brrLimit > 50:
            brrLimit = 2
    if sys.argv[arg] == '--saturationLimit':
        saturationLimit = int(sys.argv[arg + 1])
        if saturationLimit < 0 or saturationLimit > 50:
            saturationLimit = 2
    if sys.argv[arg] == '--noiseLimit':
        noiseLimit = int(sys.argv[arg + 1])
        if noiseLimit < 0 or noiseLimit > 50:
            noiseLimit = 20
    if sys.argv[arg] == '--verbose':
        verbose = True
    if sys.argv[arg] == '--rndModFX':
        argText = sys.argv[arg + 1]
        if argText == 'true' or argText == 'True':
            rndModFX = True
        else:
            rndModFX = False



delugeParameters = {
    "oscType": ["TEXT",10,["square","analogSquare","saw","analogSaw","sine","triangle"],True,True],
    "oscTranspose": ["INT",0,[-96, +96], True, True],
    "oscCents": ["INT", 0, [-99,+99], True, True],
    "oscRetrigPhase": ["INT", -1, [-1,270], True, True],
    "polyphonic": ["TEXT", 0, ["poly", "mono", "legato", "auto"], True, False],
    "clipping": ["INT", 0, [0,saturationLimit], True, True],
    "voicePriority": ["INT", 0, [0,2], True, True],
    "lfoType": ["TEXT", 0, ["triangle","sine","square","saw"], True, False],
    "lfoSyncLevel": ["INT", 0, [0,9], True, False],
    "mode": ["TEXT", 0, ["subtractive","fm","ringmod"], True, False],
    "unisonNumber": ["INT", 1, [1, unisonLimit], True, False],
    "unisonDetune": ["INT", 0, [0,50], True, False],
    "compressorSyncLevel": ["INT", 0, [0,9], False, False],
    "compressorAttack": ["LINT", 256, int50, False, False],
    "compressorRelease": ["LINT", 256, int50, False, False],
    "lpfMode": ["TEXT", 0, ["24db","12db","drive"], True, False],
    "modFXType": ["TEXT", 0, ["off","flanger","chorus","phaser"], True, False],
    "delayPingPong": ["INT", 0, [0,1], True, False],
    "delayAnalog": ["INT", 0, [0,1], True, False],
    "delaySyncLevel": ["INT", 7, [0,9], True, False],
    "arpeggiatorGate": ["SINT", 0, sInt50, False, False],
    "portamento": ["SINT", smin, sInt50, False, False],
    "compressorShape": ["SINT", 3693868466, sInt50, False, False],
    "oscVolume": ["SINT", smax, int50, True, False],
    "oscPulseWidth": ["LINT", 0, int50, True, False],
    "noiseVolume": ["SINT", smin, sInt50[0:noiseLimit+1], True, False],
    "volume": ["LINT", smax, int50, False, False],
    "pan": ["SINT", 0, sInt50, False, False],
    "lpfFrequency": ["SINT", smin, sInt50[lpfMinimum:], True, False],
    "lpfResonance": ["SINT", smin, sInt50[0:resLimit+1], True, False],
    "hpfFrequency": ["SINT", smin, sInt50[0:hpfMaximum+1], True, False],
    "hpfResonance": ["SINT", smin, sInt50[0:resLimit+1], True, False],
    "envelopeAttack": ["SINT", 0, sInt50, True, False],
    "envelopeDecay": ["SINT", 3865470548, sInt50, True, False],
    "envelopeSustain": ["SINT", smax, sInt50, True, False],
    "envelopeRelease": ["SINT", smin, sInt50, True, False],
    "lfoRate": ["LINT", 429496702, int50, True, False],
    "modulatorAmount": ["SINT", smin, sInt50, True, False],
    "modulatorFeedback": ["SINT", smin, sInt50, True, False],
    "carrierFeedback": ["SINT", smin, sInt50, True, False],
    "modFXRate": ["LINT", 0, int50, True, False],
    "modFXDepth": ["LINT", 0, int50, True, False],
    "delayRate": ["SINT", 0, int50, True, False],
    "delayFeedback": ["SINT", smin, sInt50[0:delayLimit+1], True, False],
    "reverbAmount": ["SINT", smin, sInt50[0:reverbLimit+1], True, False],
    "arpeggiatorRate": ["LINT", 0, int50, True, False],
    "patchCableSource": ["TEXT", 0, patchCableSourceList, True, False],
    "patchCableDestination": ["TEXT", 0, patchCableDestinationList, True, False],
    "patchCableAmount": ["SINT", 1073741800, mInt, True, False],
    "stutterRate": ["LINT", 0, int50, True, False],
    "sampleRateReduction": ["SINT", smin, sInt50[0:srrLimit+1], False, False],
    "bitCrush": ["SINT", smin, sInt50[0:brrLimit+1], False, False],
    "equalizerBass": ["SINT", 0, [0, 0], False, False],
    "equalizerTreble": ["SINT", 0, [0, 0], False, False],
    "equalizerBassFrequency": ["SINT", 0, [0, 0], False, False],
    "equalizerTrebleFrequency": ["SINT", 0, [0, 0], False, False],
    "modFXOffset": ["SINT", 0, int50, True, False],
    "modFXFeedback": ["SINT", 0, int50, True, False],
    "arpeggiatorMode": ["TEXT",0,[0,"up","down","both","random"], True, False],
    "arpeggiatorSyncLevel": ["INT",7,[0,9], True, False],
    "arpeggiatorOctaves": ["INT",1,[1,4], True, False],
    "modKnobControlsParam": ["SINT", 0, [0, 0], False, False]
}

oMax = octaveRange * 12
oMin = -octaveRange * 12

if fileNameBase == "" or len(sys.argv) < 2:
    print()
    print("RNDSYNTH : Deluge random Synth patch generator V0.11")
    print("---------------------------------------------------")
    print()
    print("Usage: rndsynth.py --outputBase <nnn> [--options]")
    print()
    print("--outputBase <nnn> = 3-figure patch number e.g. 250 on which 26 variations (a to z) will be generated based on options")
    print()
    print("Required")
    print()
    print("--outputBase\t\t<nnn>\t\t")
    print()
    print("Options")
    print("--semitones\t\tTrue/False\tdefault: False")
    print("--octaveRange\t\t<1 to 8>\tdefault: 4")
    print("--patchAll\t\tTrue/False\tdefault: False")
    print("--patchLimit\t\t1 to 16\t\tdefault: 8")
    print("--unisonLimit\t\t1 to 8\t\tdefault: 4")
    print("--delayLimit\t\t0 to 50\t\tdefault: 10")
    print("--reverbLimit\t\t0 to 50\t\tdefault: 25")
    print("--lpfMinimum\t\t0 to 50\t\tdefault: 25")
    print("--hpfMaximum\t\t0 to 50\t\tdefault: 25")
    print("--resLimit\t\t0 to 50\t\tdefault: 20")
    print("--noiseLimit\t\t0 to 50\t\tdefault: 20")
    print("--srrLimit\t\t0 to 50\t\tdefault: 2")
    print("--brrLimit\t\t0 to 50\t\tdefault: 2")
    print("--saturationLimit\t0 to 15\t\tdefault: 2")
    print("--rndArpeggiator\tTrue/False\tdefault: False")
    print("--rndModFX\t\tTrue/False\tdefault: False")
    print("--verbose\t\tprint out settings that were used to generate patches")

    sys.exit(1)


for fileLetter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

    #Build Sound
    sound = ET.Element("sound")
    osc1 = ET.SubElement(sound, "osc1")
    addTag(osc1, "type", randomParameter("oscType"))
    if semitones:
        addTag(osc1, "transpose", (random.randrange(oMin,oMax,1)))
    else:
        addTag(osc1, "transpose", (random.randrange(oMin,oMax,12)))
    addTag(osc1, "cents", randomParameter("oscCents"))
    addTag(osc1, "retrigPhase", randomParameter("oscRetrigPhase"))
    osc2 = ET.SubElement(sound, "osc2")
    addTag(osc2, "type", randomParameter("oscType"))
    if semitones:
        addTag(osc2, "transpose", (random.randrange(oMin,oMax,1)))
    else:
        addTag(osc2, "transpose", (random.randrange(oMin,oMax,12)))
    addTag(osc2, "cents", randomParameter("oscCents"))
    addTag(osc2, "retrigPhase", randomParameter("oscRetrigPhase"))
    addTag(sound,"polyphonic",randomParameter("polyphonic"))
    addTag(sound,"clippingAmount",randomParameter("clipping"))
    addTag(sound,"voicePriority",randomParameter("voicePriority"))
    lfo1 = ET.SubElement(sound,"lfo1")
    addTag(lfo1,"lfoType",randomParameter("lfoType"))
    addTag(lfo1,"lfoSyncLevel",randomParameter("lfoSyncLevel"))
    lfo2 = ET.SubElement(sound,"lfo2")
    addTag(lfo2,"lfoType",randomParameter("lfoType"))
    currentMode = addTag(sound,"mode",randomParameter("mode"))
    unison = ET.SubElement(sound,"unison")
    addTag(unison,"num",randomParameter("unisonNumber"))
    addTag(unison,"detune",randomParameter("unisonDetune"))
    compressor = ET.SubElement(sound,"compressor")
    addTag(compressor,"compressorSyncLevel",randomParameter("compressorSyncLevel"))
    addTag(compressor,"compressorAttack",randomParameter("compressorAttack"))
    addTag(compressor,"compressorRelease",randomParameter("compressorRelease"))
    addTag(sound,"lpfMode",randomParameter("lpfMode"))
    if rndModFX:
        addTag(sound,"modFXType",randomParameter("modFXType"))
    else:
        addTag(sound,"modFXType","off")
    delay = ET.SubElement(sound,"delay")
    addTag(delay,"delayPingPong",randomParameter("delayPingPong"))
    addTag(delay,"delayAnalog",randomParameter("delayAnalog"))
    addTag(delay,"delaySyncLevel",randomParameter("delaySyncLevel"))

    defaultParams = ET.SubElement(sound,"defaultParams")
    addTag(defaultParams,"arpeggiatorGate",randomParameter("arpeggiatorGate"))
    addTag(defaultParams,"portamento",randomParameter("portamento"))
    addTag(defaultParams,"compressorShape",randomParameter("compressorShape"))
    addTag(defaultParams,"oscAVolume",randomParameter("oscVolume"))
    addTag(defaultParams,"oscAPulseWidth",randomParameter("oscPulseWidth"))
    addTag(defaultParams,"oscBVolume",randomParameter("oscVolume"))
    addTag(defaultParams,"oscBPulseWidth",randomParameter("oscPulseWidth"))
    addTag(defaultParams,"noiseVolume",randomParameter("noiseVolume"))
    addTag(defaultParams,"volume",randomParameter("volume"))
    addTag(defaultParams,"pan",randomParameter("pan"))
    addTag(defaultParams,"lpfFrequency",randomParameter("lpfFrequency"))
    addTag(defaultParams,"lpfResonance",randomParameter("lpfResonance"))
    addTag(defaultParams,"hpfFrequency",randomParameter("hpfFrequency"))
    addTag(defaultParams,"hpfResonance",randomParameter("hpfResonance"))
    envelope1 = ET.SubElement(defaultParams,"envelope1")
    addTag(envelope1,"attack",randomParameter("envelopeAttack"))
    addTag(envelope1,"decay",randomParameter("envelopeDecay"))
    addTag(envelope1,"sustain",randomParameter("envelopeSustain"))
    addTag(envelope1,"release",randomParameter("envelopeRelease"))
    envelope2 = ET.SubElement(defaultParams,"envelope2")
    addTag(envelope2,"attack",randomParameter("envelopeAttack"))
    addTag(envelope2,"decay",randomParameter("envelopeDecay"))
    addTag(envelope2,"sustain",randomParameter("envelopeSustain"))
    addTag(envelope2,"release",randomParameter("envelopeRelease"))
    addTag(defaultParams,"lfo1Rate",randomParameter("lfoRate"))
    addTag(defaultParams,"lfo2Rate",randomParameter("lfoRate"))
    addTag(defaultParams,"modulator1Amount",randomParameter("modulatorAmount"))
    addTag(defaultParams,"modulator2Amount",randomParameter("modulatorAmount"))
    addTag(defaultParams,"modulator1Feedback",randomParameter("modulatorFeedback"))
    addTag(defaultParams,"modulator2Feedback",randomParameter("modulatorFeedback"))
    addTag(defaultParams,"carrier1Feedback",randomParameter("carrierFeedback"))
    addTag(defaultParams,"carrier2Feedback",randomParameter("carrierFeedback"))
    if rndModFX:
        addTag(defaultParams, "modFXRate", randomParameter("modFXRate"))
        addTag(defaultParams, "modFXDepth", randomParameter("modFXDepth"))
    else:
        addTag(defaultParams, "modFXRate", 0)
        addTag(defaultParams, "modFXDepth", 0)
    addTag(defaultParams,"delayRate",randomParameter("delayRate"))
    addTag(defaultParams,"delayFeedback",randomParameter("delayFeedback"))
    addTag(defaultParams,"reverbAmount",randomParameter("reverbAmount"))
    addTag(defaultParams,"arpeggiatorRate",randomParameter("arpeggiatorRate"))

    patchCables = ET.SubElement(defaultParams,"patchCables")

    #default patch cable velocity->volume
    patchCable = ET.SubElement(patchCables,"patchCable")
    addTag(patchCable,"source","velocity")
    addTag(patchCable,"destination","volume")
    addTag(patchCable,"amount",1073741800)

    if not patchAll:
        #pr = random.randint(1,rndPatchLimit)

        for p in range (1, patchLimit):
            patchCable = ET.SubElement(patchCables, "patchCable")
            addTag(patchCable, "source", randomParameter("patchCableSource"))
            addTag(patchCable, "destination", randomParameter("patchCableDestination"))
            addTag(patchCable, "amount", randomParameter("patchCableAmount"))
    else:
        for p in patchCableSourceList:
            patchCable = ET.SubElement(patchCables, "patchCable")
            addTag(patchCable, "source", p)
            addTag(patchCable, "destination", randomParameter("patchCableDestination"))
            addTag(patchCable, "amount", randomParameter("patchCableAmount"))

    addTag(defaultParams,"stutterRate",randomParameter("stutterRate"))
    addTag(defaultParams,"sampleRateReduction",randomParameter("sampleRateReduction"))
    addTag(defaultParams,"bitCrush",randomParameter("bitCrush"))
    equalizer = ET.SubElement(defaultParams,"equalizer")
    addTag(equalizer,"equalizerBass",randomParameter("equalizerBass"))
    addTag(equalizer,"equalizerTreble",randomParameter("equalizerTreble"))
    addTag(equalizer,"equalizerBassFrequency",randomParameter("equalizerBassFrequency"))
    addTag(equalizer,"equalizerTrebleFrequency",randomParameter("equalizerTrebleFrequency"))
    if rndModFX:
        addTag(defaultParams,"modFXOffset",randomParameter("modFXOffset"))
        addTag(defaultParams,"modFXFeedback",randomParameter("modFXFeedback"))
    else:
        addTag(defaultParams,"modFXOffset",0)
        addTag(defaultParams,"modFXFeedback",0)

    if rndArpeggiator:
        rm = randomParameter("arpeggiatorMode")
        if rm != "0":
            arpeggiator = ET.SubElement(sound,"arpeggiator")
            addTag(arpeggiator,"mode",rm)
            addTag(arpeggiator,"numOctaves",randomParameter("arpeggiatorOctaves"))
            addTag(arpeggiator,"syncLevel",randomParameter("arpeggiatorSyncLevel"))


    midiKnobs = ET.SubElement(sound,"midiKnobs")
    midiKnobs.text = ""

    modKnobs = ET.SubElement(sound,"modKnobs")
    if currentMode == 'subtractive':
        for mk in modKnobDestinationsSubtractive:
            modKnob = ET.SubElement(modKnobs,"modKnob")
            addTag(modKnob,"controlsParam",mk)
    elif currentMode == 'fm':
        for mk in modKnobDestinationsFM:
            modKnob = ET.SubElement(modKnobs, "modKnob")
            addTag(modKnob, "controlsParam", mk)
    else:
        #ringmod
        for mk in modKnobDestinationsRingMod:
            modKnob = ET.SubElement(modKnobs, "modKnob")
            addTag(modKnob, "controlsParam", mk)

    tree = ET.ElementTree(sound)
    xName = 'SYNT' + fileNameBase + fileLetter + '.XML'
    tree.write(xName,pretty_print=True, encoding='UTF-8', xml_declaration=True)

if verbose:

    print()
    print("octaveRange = " + str(octaveRange))
    print("semitones = " + str(semitones))
    print("patchAll = " + str(patchAll))
    print("patchLimit = " + str(patchLimit))
    print("unisonLimit = " + str(unisonLimit))
    print("delayLimit = "+str(delayLimit))
    print("reverbLimit = "+str(reverbLimit))
    print("lpfMinimum = "+str(lpfMinimum))
    print("hpfMaximum = "+str(hpfMaximum))
    print("resLimit = "+str(resLimit))
    print("srrLimit = "+str(srrLimit))
    print("brrLimit = "+str(brrLimit))
    print("saturationLimit = "+str(saturationLimit))
    print("noiseLimit = "+str(noiseLimit))
    print("rndArpeggiator = "+str(rndArpeggiator))
    print("rndModFX = "+str(rndModFX))


exit()

