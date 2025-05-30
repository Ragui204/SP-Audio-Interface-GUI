#include "Bitcrusher.h"

void Bitcrusher::update(void) {
  audio_block_t *block = receiveWritable();
  if (!block) return;

  const int16_t silenceThreshold = 10;

  for (int i = 0; i < AUDIO_BLOCK_SAMPLES; i++) {
    if (sampleCounter == 0) {
      int16_t input = block->data[i];
      if (abs(input) < silenceThreshold) {
        lastSample = 0;
      } else {
        int shift = 16 - crushBits;
        lastSample = (input >> shift) << shift;
      }
    }

    block->data[i] = lastSample;

    sampleCounter++;
    if (sampleCounter >= sampleStep) {
      sampleCounter = 0;
    }
  }

  transmit(block);
  release(block);
}
