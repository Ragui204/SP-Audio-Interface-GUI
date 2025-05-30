#ifndef Bitcrusher_h_
#define Bitcrusher_h_

#include <Arduino.h>
#include <AudioStream.h>

class Bitcrusher : public AudioStream {
public:
  Bitcrusher(void) : AudioStream(1, inputQueueArray) {}

  void bits(uint8_t b) {
    if (b > 16) b = 16;
    else if (b == 0) b = 1;
    crushBits = b;
  }

  void sampleRate(float hz) {
    int n = (AUDIO_SAMPLE_RATE_EXACT / hz) + 0.5f;
    if (n < 1) n = 1;
    else if (n > 64) n = 64;
    sampleStep = n;
  }

  virtual void update(void);

private:
  uint8_t crushBits = 16;
  uint8_t sampleStep = 1;
  audio_block_t *inputQueueArray[1];
  int16_t lastSample = 0;
  uint8_t sampleCounter = 0;
};

#endif
