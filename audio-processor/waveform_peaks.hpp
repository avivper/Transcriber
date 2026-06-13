#pragma once

#include <cstddef>
#include <vector>

namespace audio {

class WaveformPeaks {
public:
  void build(const float* samples, std::size_t frames, int buckets);
  const std::vector<float>& values() const;

private:
  std::vector<float> values_;
};

}
