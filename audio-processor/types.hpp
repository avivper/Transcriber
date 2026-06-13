#pragma once

namespace audio {

struct Segment {
  double start;
  double end;
};

struct ProcessOptions {
  bool highPass = true;
  double highPassHz = 80.0;
  bool normalize = true;
  double targetPeak = 0.97;
  int peakBuckets = 480;
  double vadFrameMs = 30.0;
  double vadEnergyThresh = 0.01;
  double vadMinSilenceMs = 400.0;
  double vadMinSpeechMs = 250.0;
};

}
