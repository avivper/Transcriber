#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

#include "types.hpp"
#include "audio_buffer.hpp"
#include "biquad_filter.hpp"
#include "normalizer.hpp"
#include "waveform_peaks.hpp"
#include "voice_activity_detector.hpp"

namespace audio {

class AudioProcessor {
public:
  AudioProcessor();

  void setOptions(const ProcessOptions& options);

  void load(std::uintptr_t samplesPtr, std::size_t frames, int sampleRate);

  void process();

  std::uintptr_t outputPtr() const;
  std::size_t outputFrames() const;
  int outputSampleRate() const;

  std::uintptr_t peaksPtr() const;
  std::size_t peaksCount() const;

  std::size_t segmentCount() const;
  Segment segmentAt(std::size_t index) const;

private:
  ProcessOptions options_;
  AudioBuffer buffer_;
  BiquadFilter highPass_;
  Normalizer normalizer_;
  WaveformPeaks peaks_;
  VoiceActivityDetector vad_;
  std::vector<Segment> segments_;
};

}
