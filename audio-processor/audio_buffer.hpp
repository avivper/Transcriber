#pragma once

#include <cstddef>
#include <vector>

namespace audio {

class AudioBuffer {
public:
  AudioBuffer();
  AudioBuffer(int sampleRate, std::size_t frames);

  float* data();
  const float* data() const;
  std::size_t frames() const;
  int sampleRate() const;

  void resize(std::size_t frames);
  void setSampleRate(int sampleRate);
  void assign(const float* samples, std::size_t frames, int sampleRate);

private:
  std::vector<float> samples_;
  int sampleRate_;
};

}
