#pragma once

#include <cstddef>
#include <vector>

namespace audio {

class Resampler {
public:
  std::vector<float> resample(const float* samples, std::size_t frames,
                              int sourceRate, int targetRate);
};

}
