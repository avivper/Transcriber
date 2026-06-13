#pragma once

#include <cstddef>

namespace audio {

class BiquadFilter {
public:
  BiquadFilter();

  void setHighPass(double cutoffHz, double sampleRate, double q = 0.707);
  void process(float* samples, std::size_t frames);
  void reset();

private:
  double b0_;
  double b1_;
  double b2_;
  double a1_;
  double a2_;
  double z1_;
  double z2_;
};

}
