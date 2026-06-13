#pragma once

#include <cstddef>

namespace audio {

class Normalizer {
public:
  void normalizePeak(float* samples, std::size_t frames, double targetPeak);
  void normalizeRms(float* samples, std::size_t frames, double targetRms);
};

}
