// AGNI Health — I2S Bowel Sound Recorder
// XIAO nRF52840 Sense + INMP441 MEMS Microphone
// Sampling: 16 kHz, 16-bit, mono
// 
// Hardware:
//   INMP441 VDD  → XIAO 3.3V
//   INMP441 GND  → XIAO GND
//   INMP441 L/R  → XIAO GND (left channel)
//   INMP441 DOUT → XIAO P0_03 (D3)
//   INMP441 BCLK → XIAO P0_02 (D2)
//   INMP441 WS   → XIAO P0_28 (D4)
//
// Output: Binary stream of 512 int16 samples over Serial
// Protocol: Starts with "AGNI_RECORDING:16000Hz" marker

#include <I2S.h>

const int sampleRate = 16000;
const int samplesPerPacket = 512;  // 32ms @ 16kHz
I2S i2s(INPUT);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!i2s.begin(I2S_PHILIPS_MODE, sampleRate, 16)) {
    Serial.println("I2S_FAIL");
    while (1);
  }

  // Signal start
  Serial.println("AGNI_RECORDING:16000Hz");
}

void loop() {
  int samples[samplesPerPacket];
  int idx = 0;

  while (idx < samplesPerPacket) {
    int sample = i2s.read();
    // Filter out invalid reads (0 and -1 are I2S idle values)
    if (sample != 0 && sample != -1) {
      samples[idx++] = sample;
    }
  }

  // Send as binary — 512 int16 values (1024 bytes)
  Serial.write((uint8_t*)samples, samplesPerPacket * sizeof(int));
}
