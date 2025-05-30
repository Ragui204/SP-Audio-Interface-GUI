#include <Audio.h>
#include <Audiostream.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <mcp2515.h>
#include "Bitcrusher.h"
#include "AudioEffectSoftSaturation.h"

struct can_frame canMsg;
MCP2515 mcp2515(10);  // CS pin 10

AudioInputI2S       audioInput;       // I2S Audio Input from Teensy Audio Shield (Stereo LINE-IN)
AudioOutputI2S      audioOutput;      // I2S Audio Output to Teensy Audio Shield (Headphone Out)

AudioAnalyzeFFT1024 fft;              // FFT Object (1024-point FFT for frequency analysis)

AudioFilterBiquad   input_biquad;          // Biquad filter (for filtering unwanted frequencies)
AudioFilterBiquad   output_biquad;         
AudioFilterBiquad   bitcrusher_biquad;     

AudioEffectDelay    delay_effect1;          // Delay effect repeats a note a number of times with increasing time for each subsequent delay
AudioEffectDelay    delay_effect2;
AudioEffectDelay    delay_effect3;
AudioEffectReverb   reverb_effect;
AudioEffectDelay    chorus_voice_effect1;   // Chorus effect using delay, each delay is a voice that's modulated in the main loop
AudioEffectDelay    chorus_voice_effect2;
AudioEffectDelay    chorus_voice_effect3;
AudioEffectDelay    chorus_voice_effect4;
elapsedMillis       choruslfoTimer;
Bitcrusher          bitcrusher_effect;   // Distortion 
AudioFilterBiquad   bitcrusher_filter;
AudioEffectSoftSaturation soft_saturator;
 
AudioMixer4         delay_mixer;  
AudioMixer4         reverb_mixer;   
AudioMixer4         chorus_mixer; 
AudioMixer4         bitcrusher_mixer; 
AudioMixer4         dry_mixer;  
AudioMixer4         effect_mixer;    
AudioMixer4         final_mixer; 

// Internal buffer already exists for teensy 4.1 at 128 sample blocks at 44.1kHz 

// Input and filter 
AudioConnection     Input_FFT(audioInput, 1, fft, 0); //Use right channel          
AudioConnection     Input_biquad(audioInput, 1, input_biquad, 0); // biquad is an audio filter object    

// Dry Signal
AudioConnection     biquad_dry_mixer(input_biquad, 0, dry_mixer, 0); // filtered signal sent to mixer for reconstruction       
AudioConnection     dry_mixer_final_mixer(dry_mixer, 0, final_mixer, 0); // filtered signal sent to mixer for reconstruction       

// Delay 
AudioConnection     biquad_delay_effect1(input_biquad, 0, delay_effect1, 0);         
AudioConnection     delay_effect1_delay_mixer(delay_effect1, 0, delay_mixer, 0);           
AudioConnection     biquad_delay_effect2(input_biquad, 0, delay_effect2, 0);          
AudioConnection     delay_effect_delay_mixer2(delay_effect2, 0, delay_mixer, 1);           
AudioConnection     biquad_delay_effect3(input_biquad, 0, delay_effect3, 0);           
AudioConnection     delay_effect_delay_mixer3(delay_effect3, 0, delay_mixer, 2);
AudioConnection     delay_mixer_effect_mixer(delay_mixer, 0, effect_mixer, 0); // **mixer total output is channel 0 (when any mixer is first)

// Reverb 
AudioConnection     biquad_reverb_effect(input_biquad, 0, reverb_effect, 0); 
AudioConnection     reverb_effect_reverb_mixer(reverb_effect, 0, reverb_mixer, 0); 
AudioConnection     reverb_mixer_effect_mixer(reverb_mixer, 0, effect_mixer, 1); 

//Chorus 
AudioConnection     biquad_chorus_voice_effect1(input_biquad, 0, chorus_voice_effect1, 0); 
AudioConnection     chorus_voice_effect1_chorus_mixer(chorus_voice_effect1, 0, chorus_mixer, 0); 
AudioConnection     biquad_chorus_voice_effect2(input_biquad, 0, chorus_voice_effect2, 0); 
AudioConnection     chorus_voice_effect_chorus_mixer2(chorus_voice_effect2, 0, chorus_mixer, 1); 
AudioConnection     biquad_chorus_voice_effect3(input_biquad, 0, chorus_voice_effect3, 0); 
AudioConnection     chorus_voice_effect_chorus_mixer3(chorus_voice_effect3, 0, chorus_mixer, 2); 
AudioConnection     biquad_chorus_voice_effect4(input_biquad, 0, chorus_voice_effect4, 0); 
AudioConnection     chorus_voice_effect_chorus_mixer4(chorus_voice_effect4, 0, chorus_mixer, 3); 
AudioConnection     chorus_mixer_effect_mixer(chorus_mixer, 0, effect_mixer, 2); 

//Bitcrusher 
//AudioConnection     biquad_bitcrusher_effect(input_biquad, 0, bitcrusher_effect, 0);
//AudioConnection     bitcrusher_effect_bitcrusher_mixer(bitcrusher_effect, 0, bitcrusher_mixer, 0);
//AudioConnection     bitcrusher_mixer_effect_mixer(bitcrusher_mixer, 0, effect_mixer, 3);

AudioConnection     biquad_bitcrusher_effect(input_biquad, 0, bitcrusher_effect, 0);
AudioConnection     bitcrusher_effect_bitcrusher_mixer(bitcrusher_effect, 0, bitcrusher_mixer, 0);
AudioConnection     bitcrusher_mixer_soft_saturator(bitcrusher_mixer, 0, soft_saturator, 0);
AudioConnection     soft_saturator_effect_mixer(soft_saturator, 0, effect_mixer, 3);

// Out                  
AudioConnection     effect_mixer_final_mixer(effect_mixer, 0, final_mixer, 1); //Channel one reserved for Dry signal 
AudioConnection     OutLeft(final_mixer, 0, audioOutput, 0);       
AudioConnection     OutRight(final_mixer, 0, audioOutput, 1);  

// Teensy Audio Processing Default 
AudioControlSGTL5000 audioShield;
#define BAUD_RATE 115200 
#define AUDIO_MEMORY 350

// Audioshield Default 
#define AUDIOSHIELD_VOLUME 1
#define LINE_IN_LEVEL 1

// FFT Filter/Biquad Default - make FFT set these later 
#define SET_HIGH_Hz 6000
#define SET_LOW_Hz 100
#define MAGNITUDE 0
float sample_rate = 44100;  
float filter_eq_Hz = 170; 
int fft_points = 1024; //number of time-domain samples using AudioWindowHanning1024 
int usable_bins = 512; //after fft conversion, number of points in the frequency-domain (with magnitude) available for usage without aliasing issues (Nyquist Theorum)

//DEFAULT ADJUSTABLE INITIAL VALUES
// Delay Default
bool DELAY_ON = false; 
int BPM = 120; //range 0 - 300
int DIVISION_MODE = 2; //range has to be a series of number 1, 2, 4, 9, and 16, (2(n-1), where 0 >= n <= 4)
int NUMBER_OF_DELAYS = 3; // range is 1 - 3
float DELAY_GAIN = 0.25f; //grange 0.0 - 0.25

// Reverb Default  
bool REVERB_ON = true; 
float REVERB_TIME = 4.0f; //range 0.0 - 5.0 seconds
float REVERB_GAIN = 0.25f; // 0.0 - 0.25

// Chorus Default 
bool CHORUS_ON = false; 
int NUMBER_OF_VOICES = 4; //ranges between 1 - 4, (when turning chorus on, second window must pop out to set Number of voices before editig the rest of chorus settings )
float BASE_DELAY_MS = 10.0f;    // 0.0 to 10 ms
float MOD_DEPTH_MS = 3.0f;  // range 0.0 - 10.0 ms  
float MOD_RATE_HZ = 0.5f;    //ranges  0.0 - 5 HZ   
float CHORUS_GAIN = 0.25f; //ranges 0.0 - 0.25

// Distortion Default 
bool DISTORTION_ON = true; 
int BITCRUSHER_BITS = 6; //ranges 1 - 7
float BITCRUSHER_GAIN = 0.25f; //ranges 0.0 - 0.25

// Final Mixer Default 
float DRY_SIGNAL = 0.1; //EDIT W/ GUI 

void setup() {
    mcp2515.reset();
    mcp2515.setBitrate(CAN_500KBPS, MCP_16MHZ);
    mcp2515.setNormalMode();
    Serial.begin(BAUD_RATE);
    AudioMemory(AUDIO_MEMORY);  // Allocate memory for audio processing

    // Initialize Audio Shield
    audioShield.enable();
    audioShield.volume(AUDIOSHIELD_VOLUME);    // Set output volume (0.0 to 1.0)

    // Configure Line-In Settings
    audioShield.inputSelect(AUDIO_INPUT_LINEIN);  // Use LINE-IN as input
    audioShield.lineInLevel(LINE_IN_LEVEL);  // Set input gain for expected signal level

    // Set up FFT Filter + Biquad
    fft.windowFunction(AudioWindowHanning1024);
    input_biquad.setHighpass(0, SET_LOW_Hz, 0.11);
    input_biquad.setLowpass(1, SET_HIGH_Hz, 0.11);  // Low-pass filter at 5kHz (Adjust as needed)

    // Set up reverb 
    reverb_effect.reverbTime(REVERB_TIME);

    // Set up chorus
    chorus_voice_effect1.delay(0, BASE_DELAY_MS);
    chorus_voice_effect2.delay(0, BASE_DELAY_MS);
    chorus_voice_effect3.delay(0, BASE_DELAY_MS);
    chorus_voice_effect4.delay(0, BASE_DELAY_MS);

    // Set up bitcrusher 
    bitcrusher_effect.sampleRate(sample_rate); //use regular sample rate at 44.1kHz for regular distortion sound 
    bitcrusher_effect.bits(BITCRUSHER_BITS); //4 for max 

    // Effect gains ** 0->0.25 
    effect_mixer.gain(0, DELAY_GAIN);  // Delay
    effect_mixer.gain(1, REVERB_GAIN);  // Reverb
    effect_mixer.gain(2, CHORUS_GAIN);  // Chorus
    effect_mixer.gain(3, BITCRUSHER_GAIN);  // Bitcrusher

    //If summed inside the mixer past 1, clipping occurs, set DRY_SIGNAL only, 0->1 
    final_mixer.gain(0, DRY_SIGNAL);  // Dry mixer 
    final_mixer.gain(1, (1 - DRY_SIGNAL));  // All effects
}

int bin_calculator (float Hz_to_filter) {
   float bin_resolution_Hz = 0;
   float bin_number = 0; 
   bin_resolution_Hz = sample_rate/fft_points; 
   bin_number = Hz_to_filter/bin_resolution_Hz; 
   return round(bin_number); 
}

void loop() {
    checkCAN();
    //FFT Send to biquad later, FFT only grabs frequency domain information for processing - test on bottom 
    bool notch_Q = false; 
    if (fft.available()) {
      float bin = bin_calculator(filter_eq_Hz); 
      float magnitude = fft.read(bin);
        if (magnitude > 0.1) {
          input_biquad.setNotch(0, filter_eq_Hz, 10); // Temporarily apply a notch
          notch_Q = true; 
        }
    }   

// Delay
    float BPMCALC = BPM;  
    float BPM_TO_MS = 60000/BPMCALC; 
    if (!DELAY_ON) {
      delay_effect1.disable(0);
      delay_effect2.disable(0);
      delay_effect3.disable(0);
    } else {
        effect_mixer.gain(0, DELAY_GAIN); 
        if (NUMBER_OF_DELAYS >= 1) { delay_effect1.delay(0, (BPM_TO_MS/DIVISION_MODE)); }
        if (NUMBER_OF_DELAYS >= 2) { delay_effect2.delay(0, ((BPM_TO_MS)*2)/DIVISION_MODE); }
        if (NUMBER_OF_DELAYS >= 3) { delay_effect3.delay(0, ((BPM_TO_MS)*3)/DIVISION_MODE); }
    }

// Reverb 
    if (!REVERB_ON) {
      reverb_effect.reverbTime(0); 
      effect_mixer.gain(1, 0); 
    } else if (REVERB_TIME == 0.0f || REVERB_GAIN == 0.0f) {
      reverb_effect.reverbTime(0.0f); 
      effect_mixer.gain(1, 0.0f); 
    } else {
      reverb_effect.reverbTime(REVERB_TIME); 
      effect_mixer.gain(1, REVERB_GAIN); 
    }


// Chorus 
    if (!CHORUS_ON) {
      effect_mixer.gain(2, 0);
    } else {
      effect_mixer.gain(2, CHORUS_GAIN);
      float t = choruslfoTimer / 1000.0f;
      if (NUMBER_OF_VOICES >= 1) { chorus_voice_effect1.delay(0, BASE_DELAY_MS + MOD_DEPTH_MS * sinf(2.0f * PI * (MOD_RATE_HZ * 0.8f) * t)); }
      if (NUMBER_OF_VOICES >= 2) { chorus_voice_effect2.delay(0, BASE_DELAY_MS + MOD_DEPTH_MS * sinf(2.0f * PI * (MOD_RATE_HZ * 1.0f) * t)); }
      if (NUMBER_OF_VOICES >= 3) { chorus_voice_effect3.delay(0, BASE_DELAY_MS + MOD_DEPTH_MS * sinf(2.0f * PI * (MOD_RATE_HZ * 1.2f) * t)); }
      if (NUMBER_OF_VOICES >= 4) { chorus_voice_effect4.delay(0, BASE_DELAY_MS + MOD_DEPTH_MS * sinf(2.0f * PI * (MOD_RATE_HZ * 1.4f) * t)); }
      }


// Distortion

    if (!DISTORTION_ON) {
      effect_mixer.gain(3, 0);  // Bitcrusher (adjust to taste)
      //bitcrusher_env.noteOff();
    } else {
      effect_mixer.gain(3, BITCRUSHER_GAIN);  // Bitcrusher (adjust to taste)
      //bitcrusher_env.noteOn();
    }   
  Serial.print("Audio Memory Usage: ");
  Serial.println(AudioMemoryUsageMax());
}

void checkCAN() {
    struct can_frame incoming;
    if (mcp2515.readMessage(&incoming) == MCP2515::ERROR_OK && incoming.can_dlc >= 5) {
        float value;
        memcpy(&value, &incoming.data[1], sizeof(float));
        uint8_t param_id = incoming.data[0];

        if (incoming.can_id >= 0x300 && incoming.can_id <= 0x3FF) {
            switch (param_id) {
                case 11: audioShield.volume(value); break;                  // Input Volume
                case 12: BPM = value; break;                                // Beats per Minute
                case 13: DIVISION_MODE = (int)value; break;                 // Delay Division
                case 14: NUMBER_OF_DELAYS = (int)value; break;              // Number of Delays
                case 15: DELAY_GAIN = value; break;                         // Delay Mix
                case 16: REVERB_TIME = value; break;
                case 17: REVERB_GAIN = value; break;
                case 18: CHORUS_GAIN = value; break;
                case 19: BASE_DELAY_MS = value; break;
                case 20: MOD_DEPTH_MS = value; break;
                case 21: MOD_RATE_HZ = value; break;
                case 22: NUMBER_OF_VOICES = (int)value; break;
                case 23: BITCRUSHER_BITS = (int)value; 
                        bitcrusher_effect.bits(BITCRUSHER_BITS); break;
                case 24: BITCRUSHER_GAIN = value; break;
                case 25: DRY_SIGNAL = value; 
                        final_mixer.gain(0, DRY_SIGNAL); 
                        final_mixer.gain(1, 1.0f - DRY_SIGNAL); 
                        break;
                case 26: final_mixer.gain(1, value); break;                // FX Gain

                // Toggles
                case 32: DELAY_ON = value > 0.5f; break;
                case 33: REVERB_ON = value > 0.5f; break;
                case 34: CHORUS_ON = value > 0.5f; break;
                case 35: DISTORTION_ON = value > 0.5f; break;

                default:
                    Serial.print("Unknown Param ID: ");
                    Serial.println(param_id);
            }
        }
    }
}
