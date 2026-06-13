#pragma once

#include <cstddef>
#include <vector>

#include "types.hpp"

namespace audio {

class VoiceActivityDetector {
public:
  std::vector<Segment> detect(const float* samples, std::size_t frames,
                              int sampleRate, const ProcessOptions& options);
};

}
