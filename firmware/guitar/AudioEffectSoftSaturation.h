#ifndef effect_softsaturation_h_
#define effect_softsaturation_h_

#include <Arduino.h>
#include <AudioStream.h>
#include <math.h>

class AudioEffectSoftSaturation : public AudioStream {
public:
  AudioEffectSoftSaturation() : AudioStream(1, inputQueueArray) {
    drive = 1.0f;
    mix = 1.0f;
  }

  void setDrive(float d) {
    if (d < 0.1f) d = 0.1f;
    if (d > 10.0f) d = 10.0f;
    drive = d;
  }

  void setMix(float m) {
    if (m < 0.0f) m = 0.0f;
    if (m > 1.0f) m = 1.0f;
    mix = m;
  }

  virtual void update(void);

private:
  audio_block_t *inputQueueArray[1];
  float drive;
  float mix;
};

void AudioEffectSoftSaturation::update(void) {
  audio_block_t *block;
  block = receiveWritable(0);
  if (!block) return;

  for (int i = 0; i < AUDIO_BLOCK_SAMPLES; i++) {
    float x = block->data[i] / 32768.0f;
    float y = tanh(x * drive);
    float mixed = (mix * y + (1.0f - mix) * x);
    block->data[i] = (int16_t)(mixed * 32767.0f);
  }

  transmit(block);
  release(block);
}

#endif
