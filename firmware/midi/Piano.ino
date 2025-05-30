#include <Audio.h>
#include <USBHost_t36.h>
#include "HatSamples.h"
#include "PercSamples.h"
#include "SnareSamples.h"
#include "KickSamples.h"
#include "ClapSamples.h"
#include "PercSamples.h"
#include <SPI.h>
#include <mcp2515.h>


struct can_frame canMsg;
MCP2515 mcp2515(10);  // CS pin

// USB MIDI Setup
USBHost usbHost;
USBHub hub1(usbHost);
MIDIDevice_BigBuffer midiKeyboard(usbHost);

//sustain pedal variables
bool sustainPedalOn = false;
bool noteIsOn[128] = { false };           // Track which notes are actively sounding
bool sustainedNotes[128] = { false };     // Track notes that were released while sustain pedal was down
elapsedMillis sustainPedalTimeout;
const int sustainTimeoutMS = 5000; // e.g. 5 seconds


// Audio System Setup (Piano)
AudioSynthWaveform waveform[16];
AudioEffectEnvelope envelope[16];


AudioMixer4 drumMixer;
AudioMixer4 percMixer;
AudioMixer4 clapMixer;
AudioMixer4 clapPercMixer;  // ✅ fixed
AudioMixer4 mixer1, mixer2, mixer3, mixer4;
AudioMixer4 finalMixer1, finalMixer2;
AudioEffectDelay delayL, delayR;
AudioFilterStateVariable colorFilterL, colorFilterR;
AudioMixer4 delayMixerL, delayMixerR;
AudioEffectFreeverb reverbL, reverbR;
AudioMixer4 reverbMixerL, reverbMixerR;
AudioAmplifier finalGainL, finalGainR;

// Audio System Setup (Drums)
AudioPlayMemory kick1, kick2, kick3;
AudioPlayMemory snare1, snare2, snare3;
AudioPlayMemory hat1, hat2, hat3;
AudioPlayMemory clap1, clap2, clap3;
AudioPlayMemory perc1, perc2, perc3;
AudioPlayMemory* kickVoices[]  = { &kick1, &kick2, &kick3 };
AudioPlayMemory* snareVoices[] = { &snare1, &snare2, &snare3 };
AudioPlayMemory* hatVoices[]   = { &hat1, &hat2, &hat3 };
AudioPlayMemory* clapVoices[]  = { &clap1, &clap2, &clap3 };
AudioPlayMemory* percVoices[] = { &perc1, &perc2, &perc3 };
AudioEffectFreeverb drumReverbL, drumReverbR;
AudioMixer4 drumReverbMixerL, drumReverbMixerR;
AudioOutputI2S i2s1;
AudioControlSGTL5000 sgtl5000_1;

// Audio PatchCords
AudioConnection* patchCords[32];
AudioConnection mix1(mixer1, 0, finalMixer1, 0);
AudioConnection mix2(mixer2, 0, finalMixer1, 1);
AudioConnection mix3(mixer3, 0, finalMixer2, 0);
AudioConnection mix4(mixer4, 0, finalMixer2, 1);
AudioConnection delayConnL(finalMixer1, 0, delayL, 0);
AudioConnection delayConnR(finalMixer2, 0, delayR, 0);
AudioConnection delayWetL(delayL, 0, colorFilterL, 0);
AudioConnection delayWetR(delayR, 0, colorFilterR, 0);
AudioConnection filterOutL(colorFilterL, 0, delayMixerL, 1);
AudioConnection filterOutR(colorFilterR, 0, delayMixerR, 1);
AudioConnection dryOutL(finalMixer1, 0, delayMixerL, 0);
AudioConnection dryOutR(finalMixer2, 0, delayMixerR, 0);
AudioConnection reverbLIn(delayMixerL, 0, reverbL, 0);
AudioConnection reverbRIn(delayMixerR, 0, reverbR, 0);
AudioConnection reverbDryL(delayMixerL, 0, reverbMixerL, 0);
AudioConnection reverbDryR(delayMixerR, 0, reverbMixerR, 0);
AudioConnection reverbWetL(reverbL, 0, reverbMixerL, 1);
AudioConnection reverbWetR(reverbR, 0, reverbMixerR, 1);
AudioConnection finalL1(reverbMixerL, 0, finalGainL, 0);
AudioConnection finalL2(reverbMixerR, 0, finalGainL, 0);
AudioConnection finalR1(reverbMixerL, 0, finalGainR, 0);
AudioConnection finalR2(reverbMixerR, 0, finalGainR, 0);
AudioConnection patchKick1(kick1, 0, drumMixer, 0);
AudioConnection patchKick2(kick2, 0, drumMixer, 0);
AudioConnection patchKick3(kick3, 0, drumMixer, 0);
AudioConnection patchSnare1(snare1, 0, drumMixer, 1);
AudioConnection patchSnare2(snare2, 0, drumMixer, 1);
AudioConnection patchSnare3(snare3, 0, drumMixer, 1);
AudioConnection patchHat1(hat1, 0, drumMixer, 2);
AudioConnection patchHat2(hat2, 0, drumMixer, 2);
AudioConnection patchHat3(hat3, 0, drumMixer, 2);
AudioConnection patchClap1(clap1, 0, clapMixer, 0);
AudioConnection patchClap2(clap2, 0, clapMixer, 1);
AudioConnection patchClap3(clap3, 0, clapMixer, 2);

// Combine Perc samples into percMixer
AudioConnection patchPerc1(perc1, 0, percMixer, 0);
AudioConnection patchPerc2(perc2, 0, percMixer, 1);
AudioConnection patchPerc3(perc3, 0, percMixer, 2);

// Final combined mixer for claps + percs
AudioConnection patchClapToCombined(clapMixer, 0, clapPercMixer, 0);
AudioConnection patchPercToCombined(percMixer, 0, clapPercMixer, 1);
AudioConnection patchClapPercOut(clapPercMixer, 0, drumMixer, 3);

AudioConnection drumToReverbL(drumMixer, 0, drumReverbL, 0);
AudioConnection drumToReverbR(drumMixer, 0, drumReverbR, 0);
AudioConnection drumDryL(drumMixer, 0, drumReverbMixerL, 0);
AudioConnection drumDryR(drumMixer, 0, drumReverbMixerR, 0);
AudioConnection drumWetL(drumReverbL, 0, drumReverbMixerL, 1);
AudioConnection drumWetR(drumReverbR, 0, drumReverbMixerR, 1);
AudioConnection drumFinalL(drumReverbMixerL, 0, finalMixer1, 2);
AudioConnection drumFinalR(drumReverbMixerR, 0, finalMixer2, 2);
AudioConnection outL(finalGainL, 0, i2s1, 0);
AudioConnection outR(finalGainR, 0, i2s1, 1);

// Config
#define AUDIO_MEMORY_SIZE 340
elapsedMicros lastDrumHit;
const int DRUM_COOLDOWN = 2500;

float noteVolume = 0.8;
float masterVolume = 1.0;
int activeNotes[16] = { -1 };
int waveformType = 0;
float reverbDecay = 0.0;
float reverbSize = 0.0;
float reverbMix = 0.0;
float delayTime = 0;         // In ms
float delayMix = 0.0;         // Wet mix
float delayColor = 0.0;        // Low-pass
float delayFeedback = 0.0;     // Ignored unless you route it back in
float delayMod = 0.0; 

// Dynamic drum note mapping (default values)
uint8_t kickNote  = 20;
uint8_t snareNote = 21;
uint8_t hatNote   = 22;
uint8_t clapNote  = 23;
uint8_t percNote   = 19;

//drum sample type:
int kickType = 0;
int snareType = 0;
int hatType   = 0;
int clapType  = 0;
int percType  = 0;


void setup() {
    Serial.begin(115200);
    usbHost.begin();
    AudioMemory(AUDIO_MEMORY_SIZE + 60);
    sgtl5000_1.enable();
    sgtl5000_1.volume(1.0);
    sgtl5000_1.unmuteLineout();
    sgtl5000_1.unmuteHeadphone();
    sgtl5000_1.enhanceBassDisable();
    sgtl5000_1.autoVolumeDisable();
    sgtl5000_1.surroundSoundDisable();
        // Somewhere in your main loop (or setup)
    Serial.print("Audio memory used: ");
    Serial.println(AudioMemoryUsage()); // number of blocks currently used

    Serial.print("Max Audio memory used: ");
    Serial.println(AudioMemoryUsageMax()); // max blocks ever used


    mcp2515.reset();
    mcp2515.setBitrate(CAN_500KBPS, MCP_16MHZ);
    mcp2515.setNormalMode();

    drumMixer.gain(0, 0.8);
    drumMixer.gain(1, 0.8);
    drumMixer.gain(2, 0.8);
    drumMixer.gain(3, 0.8);
    clapMixer.gain(0, 0.8);
    clapMixer.gain(1, 0.8);
    clapMixer.gain(2, 0.8);
    percMixer.gain(0, 0.8);
    percMixer.gain(1, 0.8);
    percMixer.gain(2, 0.8);
    clapPercMixer.gain(0, 0.8);
    clapPercMixer.gain(1, 0.8);
    finalMixer1.gain(2, 0.8);
    finalMixer2.gain(2, 0.8);

    for (int i = 0; i < 16; i++) {
        waveform[i].begin(WAVEFORM_SINE);
        envelope[i].attack(20);
        envelope[i].decay(300);
        envelope[i].sustain(0.7); //fadeout
        envelope[i].release(10); 

        patchCords[i] = new AudioConnection(waveform[i], envelope[i]);
        patchCords[i + 16] = new AudioConnection(envelope[i], 0,
                                                 (i < 4 ? mixer1 :
                                                  i < 8 ? mixer2 :
                                                  i < 12 ? mixer3 : mixer4), i % 4);
        activeNotes[i] = -1;
    }

    for (int i = 0; i < 4; i++) {
        mixer1.gain(i, 0.25);
        mixer2.gain(i, 0.25);
        mixer3.gain(i, 0.25);
        mixer4.gain(i, 0.25);
    }

    setMasterVolume(masterVolume);
    updateReverbSettings();
    updateDelaySettings();
    updateDrumReverbAmount();
}

void loop() {
    usbHost.Task();
    checkMIDI();
    checkCAN();  // <-- NEW
    delay(5);
    if (sustainPedalOn && sustainPedalTimeout > sustainTimeoutMS) {
    Serial.println("Sustain pedal timeout — assuming unplugged");
    sustainPedalOn = false;
    releaseAllSustainedNotes();
}
}


void checkMIDI() {
    if (midiKeyboard.read()) {
        byte type = midiKeyboard.getType();
        byte note = midiKeyboard.getData1();
        byte velocity = midiKeyboard.getData2();
        float freq = 440.0 * pow(2.0, (note - 69) / 12.0);

         Serial.printf("RAW MIDI: type=%d (0x%X), data1=%d, data2=%d\n", type, type, note, velocity);

        // Sustain pedal (Control Change #64)
        if (type == midiKeyboard.ControlChange) {
            byte control = note;
            byte value = velocity;

            if (control == 64) {
                sustainPedalOn = value >= 64;
                sustainPedalTimeout = 0;  // Reset timeout every time pedal is touched

                Serial.print("Sustain Pedal: ");
                Serial.println(sustainPedalOn ? "ON" : "OFF");

                if (!sustainPedalOn) {
                    releaseAllSustainedNotes();
                }
            }
            return;
        }


        // Note On
        if (type == midiKeyboard.NoteOn && velocity > 0) {
            noteIsOn[note] = true;
            sustainedNotes[note] = false;

            sendNoteCAN(note);

            if (note == kickNote || note == snareNote || note == hatNote || note == clapNote || note == percNote) {
                playDrum(note);
            } else {
                playNote(note, freq);
            }
        }

        // Note Off or NoteOn with velocity 0
        else if (type == midiKeyboard.NoteOff || velocity == 0) {
            noteIsOn[note] = false;

            if (sustainPedalOn) {
                sustainedNotes[note] = true; // Hold note until pedal released
            } else {
                stopNote(note);
            }
        }
    }
}



void checkCAN() {
    if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK) {
        
        // 🎚 Drum note remapping
        if (canMsg.can_id == 0x101 && canMsg.can_dlc >= 5) {
            kickNote  = canMsg.data[0];
            snareNote = canMsg.data[1];
            hatNote   = canMsg.data[2];
            clapNote  = canMsg.data[3];
            percNote = canMsg.data[4];
            Serial.printf("Updated Drum Map - Kick: %d, Snare: %d, Hat: %d, Clap: %d\n",
                          kickNote, snareNote, hatNote, clapNote);
        }

        // 🎛 Parameter control (Volume, Reverb, Delay, etc.)
        if ((canMsg.can_id & 0xFF00) == 0x100 && canMsg.can_dlc >= 5) {
            uint8_t paramID = canMsg.data[0];
            float value;
            memcpy(&value, &canMsg.data[1], sizeof(float));

            switch (paramID) {
                case 1: reverbMix = value; updateReverbSettings(); break;
                case 2: reverbSize = value; updateReverbSettings(); break;
                case 3: reverbDecay = value; updateReverbSettings(); break;
                case 4: delayTime = value; updateDelaySettings(); break;
                case 5: delayMix = value; updateDelaySettings(); break;
                case 6: delayFeedback = value; updateDelaySettings(); break;
                case 7: delayColor = value; updateDelaySettings(); break;
                case 8: delayMod = value; updateDelaySettings(); break;
                case 9: noteVolume = value; updateNoteVolumes(); break;
                case 10: setMasterVolume(value); break;
                case 11: updateWaveformType((int)value); break;
            }

            Serial.printf("[CAN 0x100] Param: %d, Value: %.2f\n", paramID, value);
        }

        // 🥁 Drum sample assignment (note + type + sample index)
        if (canMsg.can_id == 0x110 && canMsg.can_dlc >= 3) {
            uint8_t note       = canMsg.data[0];
            uint8_t drumType   = canMsg.data[1];
            uint8_t sampleIdx  = canMsg.data[2];

        switch (drumType) {
            case 0:
                if (note == kickNote) kickType = sampleIdx;
                break;
            case 1:
                if (note == snareNote) snareType = sampleIdx;
                break;
            case 2:
                if (note == hatNote) hatType = sampleIdx;
                break;
            case 3:
                if (note == clapNote) clapType = sampleIdx;
                break;
            case 4:
                if (note == percNote) percType = sampleIdx;
                break;
        }


            Serial.printf("Mapped Note %d to Type %d Sample #%d\n", note, drumType, sampleIdx);
        }
    }
}



void sendNoteCAN(byte note) {
    canMsg.can_id = 0x100;
    canMsg.can_dlc = 1;
    canMsg.data[0] = note;
    mcp2515.sendMessage(&canMsg);
}

void releaseAllSustainedNotes() {
    for (int note = 0; note < 128; ++note) {
        if (sustainedNotes[note]) {
            stopNote(note);                 // fade out
            sustainedNotes[note] = false;   // mark released
        }
    }
}





void playDrum(byte note) {
    if (lastDrumHit < DRUM_COOLDOWN) return;
    lastDrumHit = 0;

    if (note == kickNote) {
        const unsigned int* selectedKick = nullptr;
        switch (kickType) {
            case 0: selectedKick = AudioSampleKick1985wav; break;
            case 1: selectedKick = AudioSampleKickasacschraderwavf; break;
            case 2: selectedKick = AudioSampleKickboilerwav; break;
            case 3: selectedKick = AudioSampleKickborefest2021wavf; break;
            case 4: selectedKick = AudioSampleKickchipsynthwav; break;
            case 5: selectedKick = AudioSampleKickcoffeeshopwavv; break;
            case 6: selectedKick = AudioSampleKickdarkroomwav; break;
            case 7: selectedKick = AudioSampleKickdevastatewav; break;
            case 8: selectedKick = AudioSampleKickdusterwav; break;
            case 9: selectedKick = AudioSampleKickedgywav; break;
            case 10: selectedKick = AudioSampleKickfistpumpwav; break;
            case 11: selectedKick = AudioSampleKickglitcherwav; break;
            case 12: selectedKick = AudioSampleKickgrandmasterwav; break;
            case 13: selectedKick = AudioSampleKickhardwav; break;
            case 14: selectedKick = AudioSampleKickitwav; break;
            case 15: selectedKick = AudioSampleKickjuicywav; break;
            case 16: selectedKick = AudioSampleKickjunowav; break;
            case 17: selectedKick = AudioSampleKickloridawav; break;
            case 18: selectedKick = AudioSampleKicklowrezwavw; break;
            case 19: selectedKick = AudioSampleKickmechawav; break;
            case 20: selectedKick = AudioSampleKicknailgunwav; break;
            case 21: selectedKick = AudioSampleKickneatowav; break;
            case 22: selectedKick = AudioSampleKickoceanbreezewavf; break;
            case 23: selectedKick = AudioSampleKickpotswav; break;
            case 24: selectedKick = AudioSampleKickquakewav; break;
            case 25: selectedKick = AudioSampleKickretrowav; break;
            case 26: selectedKick = AudioSampleKickroundaboutwav; break;
            case 27: selectedKick = AudioSampleKickrummmmblewav; break;
            case 28: selectedKick = AudioSampleKickshowerwav; break;
            case 29: selectedKick = AudioSampleKickshowstopperwav; break;
            case 30: selectedKick = AudioSampleKickslowlowwavfil; break;
            case 31: selectedKick = AudioSampleKicksonyawav; break;
            case 32: selectedKick = AudioSampleKickswooshywav; break;
            case 33: selectedKick = AudioSampleKicktekkwav; break;
            case 34: selectedKick = AudioSampleKickthumpsterwav; break;
            case 35: selectedKick = AudioSampleKicktightwav; break;
            case 36: selectedKick = AudioSampleKicktronwav; break;
            default: selectedKick = AudioSampleKick1985wav; break;
        }
        playSample(kickVoices, 3, selectedKick);
    }

    if (note == snareNote) {
        const unsigned int* selectedSnare = nullptr;
        switch (snareType) {
            case 0: selectedSnare = AudioSampleSnare1982drivewavf; break;
            case 1: selectedSnare = AudioSampleSnareanalogwav; break;
            case 2: selectedSnare = AudioSampleSnareblackoutwav; break;
            case 3: selectedSnare = AudioSampleSnarebreathewav; break;
            case 4: selectedSnare = AudioSampleSnarecassettewav; break;
            case 5: selectedSnare = AudioSampleSnareclappersdelightwavf; break;
            case 6: selectedSnare = AudioSampleSnarecrushedwav; break;
            case 7: selectedSnare = AudioSampleSnaredatasettewav; break;
            case 8: selectedSnare = AudioSampleSnaredoublebarrelwava; break;
            case 9: selectedSnare = AudioSampleSnareduotonewav; break;
            case 10: selectedSnare = AudioSampleSnareeightoheightwavfil; break;
            case 11: selectedSnare = AudioSampleSnarefroggerwav; break;
            case 12: selectedSnare = AudioSampleSnaregnrwav; break;
            case 13: selectedSnare = AudioSampleSnarehypemachinewava; break;
            case 14: selectedSnare = AudioSampleSnarejetwav; break;
            case 15: selectedSnare = AudioSampleSnarelastbarwav; break;
            case 16: selectedSnare = AudioSampleSnarelofiwav; break;
            case 17: selectedSnare = AudioSampleSnarenineohninewavvfi; break;
            case 18: selectedSnare = AudioSampleSnarenudiscowavw; break;
            case 19: selectedSnare = AudioSampleSnareoffgridwav; break;
            case 20: selectedSnare = AudioSampleSnareogwav; break;
            case 21: selectedSnare = AudioSampleSnarepapercutwav; break;
            case 22: selectedSnare = AudioSampleSnarepiccolowav; break;
            case 23: selectedSnare = AudioSampleSnareretrowav; break;
            case 24: selectedSnare = AudioSampleSnareslammerwav; break;
            case 25: selectedSnare = AudioSampleSnaresmoochiewav; break;
            case 26: selectedSnare = AudioSampleSnaresnapperwav; break;
            case 27: selectedSnare = AudioSampleSnaresuctionwav; break;
            case 28: selectedSnare = AudioSampleSnaretapestopwav; break;
            case 29: selectedSnare = AudioSampleSnaretightwav; break;
            case 30: selectedSnare = AudioSampleSnaretrappedwav; break;
            case 31: selectedSnare = AudioSampleSnareurbanwav; break;
            case 32: selectedSnare = AudioSampleSnareussrwav; break;
            case 33: selectedSnare = AudioSampleSnareverbotronwav; break;
            case 34: selectedSnare = AudioSampleSnarevhswav; break;
            case 35: selectedSnare = AudioSampleSnarevinylwav; break;
            default: selectedSnare = AudioSampleSnare1982drivewavf; break;
        }
        playSample(snareVoices, 3, selectedSnare);
    }

    if (note == hatNote) {
        const unsigned int* selectedHat = nullptr;
        switch (hatType) {
            case 0: selectedHat = AudioSampleHatsmassamollawav; break;
            case 1: selectedHat = AudioSampleHatsmetalwav; break;
            case 2: selectedHat = AudioSampleHatsmicrowav; break;
            case 3: selectedHat = AudioSampleHatsnoisewav; break;
            case 4: selectedHat = AudioSampleHatspedalwav; break;
            case 5: selectedHat = AudioSampleHatssaltywav; break;
            case 6: selectedHat = AudioSampleHatssizzlewav; break;
            case 7: selectedHat = AudioSampleHatsspringwaterwav; break;
            case 8: selectedHat = AudioSampleHatsstutterwav; break;
            case 9: selectedHat = AudioSampleHatssweetwav; break;
            case 10: selectedHat = AudioSampleHatsvinylwav; break;
            case 11: selectedHat = AudioSampleHatswonkywav; break;
            case 12: selectedHat = AudioSampleHatszippowav; break;
            default: selectedHat = AudioSampleHatsmicrowav; break;
        }
        playSample(hatVoices, 3, selectedHat);
    }

    if (note == clapNote) {
        const unsigned int* selectedClap = nullptr;
        switch (clapType) {
            case 0: selectedClap = AudioSampleClapcrackle1wavf; break;
            case 1: selectedClap = AudioSampleClapcrackle2wavf; break;
            case 2: selectedClap = AudioSampleClapcrackle3wavf; break;
            case 3: selectedClap = AudioSampleClapcrackle4wavf; break;
            case 4: selectedClap = AudioSampleClapflangewav; break;
            case 5: selectedClap = AudioSampleClapgianniswav; break;
            case 6: selectedClap = AudioSampleClapliquidwav; break;
            case 7: selectedClap = AudioSampleClapneatwav; break;
            case 8: selectedClap = AudioSampleClaptapewav; break;
            case 9: selectedClap = AudioSampleClapvinyl1wavv; break;
            case 10: selectedClap = AudioSampleClapvinyl2wavv; break;
            default: selectedClap = AudioSampleClapliquidwav; break;
        }
        playSample(clapVoices, 3, selectedClap);
    }
    if (note == percNote) {
        const unsigned int* selectedPerc = nullptr;
        switch (percType) {
            case 0: selectedPerc = AudioSamplePercanalog1wavf; break;
            case 1: selectedPerc = AudioSamplePercanalog2wavf; break;
            case 2: selectedPerc = AudioSamplePercboxwav; break;
            case 3: selectedPerc = AudioSamplePercdigitalnoisewavf; break;
            case 4: selectedPerc = AudioSamplePerckungfuwave; break;
            case 5: selectedPerc = AudioSamplePercoldcomputerwavf; break;
            case 6: selectedPerc = AudioSamplePercretrostickwav; break;
            case 7: selectedPerc = AudioSamplePercskipperwav; break;
            case 8: selectedPerc = AudioSamplePercspringboardwav; break;
            case 9: selectedPerc = AudioSamplePerctambowav; break;
            case 10: selectedPerc = AudioSamplePerctomtomwav; break;
            case 11: selectedPerc = AudioSamplePerctransitwav; break;
            case 12: selectedPerc = AudioSamplePercwobblewav; break;
            default: selectedPerc = AudioSamplePercanalog1wavf; break;
        }
        playSample(percVoices, 3, selectedPerc);
    }
}



bool playSample(AudioPlayMemory* players[], int count, const unsigned int* sample) {
    for (int i = 0; i < count; i++) {
        if (!players[i]->isPlaying()) {
            players[i]->play(sample);
            return true;
        }
    }
    players[0]->play(sample);
    return false;
}

void playNote(byte note, float freq) {
    // Try to find a free voice
    for (int i = 0; i < 16; i++) {
        if (activeNotes[i] == -1) {
            waveform[i].frequency(freq);
            waveform[i].begin(waveformType);
            envelope[i].noteOn();
            activeNotes[i] = note;
            updateNoteVolumes();
            return;
        }
    }

    // If all voices are in use: steal the first voice
    int stealIndex = 0;
    envelope[stealIndex].noteOff(); // fade old note
    activeNotes[stealIndex] = note;
    waveform[stealIndex].frequency(freq);
    waveform[stealIndex].begin(waveformType);
    envelope[stealIndex].noteOn();
    updateNoteVolumes();
}


void stopNote(byte note) {
    for (int i = 0; i < 16; i++) {
        if (activeNotes[i] == note) {
            envelope[i].noteOff();  // start release fade
            activeNotes[i] = -1;    // free the voice
            updateNoteVolumes();
        }
    }
}



void updateNoteVolumes() {
    int activeCount = 0;
    for (int i = 0; i < 16; i++) if (activeNotes[i] != -1) activeCount++;
    float perNoteVolume = noteVolume / sqrtf(max(1, activeCount));
    for (int i = 0; i < 16; i++)
        waveform[i].amplitude(activeNotes[i] != -1 ? perNoteVolume : 0);
}

void updateReverbSettings() {
    reverbL.roomsize(reverbSize);
    reverbR.roomsize(reverbSize);
    reverbL.damping(reverbDecay);
    reverbR.damping(reverbDecay);
    reverbMixerL.gain(1, reverbMix);
    reverbMixerR.gain(1, reverbMix);
}

void updateDelaySettings() {
    // Keep delay time safe (max = 1500 ms)
    int safeDelay = constrain((int)delayTime, 0, 500);
    delayL.delay(0, safeDelay);
    delayR.delay(0, safeDelay);

    // Low-pass filter to smooth repeats
    float freq = 500 + delayColor * 2500;  // 500–3000 Hz
    colorFilterL.frequency(freq);
    colorFilterR.frequency(freq);
    colorFilterL.resonance(0.7);
    colorFilterR.resonance(0.7);

    // Actual feedback handling via delay signal re-entry
    // You may not be using delayFeedback right now — simulate it using input + output mix

    // Adjust wet/dry ratio
    float wet = constrain(delayMix, 0.0, 1.0);
    float dry = 1.0 - wet;
    delayMixerL.gain(0, dry);
    delayMixerL.gain(1, wet);
    delayMixerR.gain(0, dry);
    delayMixerR.gain(1, wet);
}


void updateDrumReverbAmount() {
    float drumReverbAmount = 0.5;
    drumReverbMixerL.gain(0, 1.0 - drumReverbAmount);
    drumReverbMixerL.gain(1, drumReverbAmount);
    drumReverbMixerR.gain(0, 1.0 - drumReverbAmount);
    drumReverbMixerR.gain(1, drumReverbAmount);
}

void updateWaveformType(int type) {
    waveformType = constrain(type, 0, 3);
    for (int i = 0; i < 16; i++) {
        waveform[i].begin(waveformType);
    }
}

void setMasterVolume(float volume) {
    masterVolume = constrain(volume, 0.0, 1.0);
    finalGainL.gain(masterVolume);
    finalGainR.gain(masterVolume);
}
