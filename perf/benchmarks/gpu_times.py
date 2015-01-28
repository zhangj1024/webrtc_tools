# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
from metrics import gpu_timeline
import page_sets
from telemetry import benchmark
from telemetry.core.platform import tracing_category_filter
from telemetry.web_perf import timeline_based_measurement

TOPLEVEL_GL_CATEGORY = 'gpu_toplevel'
TOPLEVEL_CATEGORIES = ['disabled-by-default-gpu.device',
                       'disabled-by-default-gpu.service']


def _GetGPUTimelineMetric(_):
      return [gpu_timeline.GPUTimelineMetric()]


class _GPUTimes(benchmark.Benchmark):
  def CreateTimelineBasedMeasurementOptions(self):
    cat_string = ','.join(TOPLEVEL_CATEGORIES)
    cat_filter = tracing_category_filter.TracingCategoryFilter(cat_string)

    return timeline_based_measurement.Options(
        overhead_level=cat_filter,
        get_metrics_from_flags_callback=_GetGPUTimelineMetric)


@benchmark.Enabled('android')
class GPUTimesKeyMobileSites(_GPUTimes):
  """Measures GPU timeline metric on key mobile sites."""
  page_set = page_sets.KeyMobileSitesSmoothPageSet


class GPUTimesTop25Sites(_GPUTimes):
  """Measures GPU timeline metric for the top 25 sites."""
  page_set = page_sets.Top25SmoothPageSet
