Versions:
01-09-18 V0.1 Initial release
02-09-18 V0.11
	- Added option to randomise modulation FX (chorus etc.) --rndModFX <True/False>
	- Fixed a couple of bugs which stopped overriding some default parameters
	- Lowered default delayLimit setting (delay feedback)



You can run rndsynth.py without any parameters for the correct options syntax.
Below is a brief explanation of what each option does.

octaveRange
Number of octaves over which the oscillator pitches are generated. Positive and negative values are generated so a value of 2 will generate pitches from -24 to +24

semitones
True/False, if True the pitches will be generated in semitones. If False only octave intervals will be used, the range determined by octaveRange

patchAll
True/False. If True, one random modulation connection will be made per modulation source. If False, a random number of modulation sources and destinations will be generated.

patchLimit
1 to 32. Number of modulation connections to randomly create.

unisonLimit
1 to 8. Limit to the number of random unison voice number setting.

delayLimit
0 to 50. Limit the amount of delay feedback. This is 20 by default to avoid overloading the feedback.

reverbLimit
0 to 50. Reverb amount limit.

lpfMinimum
0 to 50. Sets the minimum LPF frequency.

hpfMaximum
0 to 50. Sets the maximum HPF frequency.

resLimit
0 to 50. Sets the resonance limit for both LPF and HPF

srrLimit
0 to 50. Sets the limit for sample rate reduction effect

brrLimit
0 to 50. Sets the limit for bit rate reduction effect

saturationLimit
0 to 15. Sets the limit for saturation effect

noiseLimit
0 to 50. Sets the noise level limit

rndArpeggiator
True/False. If True, random arpeggiator settings will be generated. If False, they won't.

rndModFX
True/False. If True, random modulation FX will be generated.
