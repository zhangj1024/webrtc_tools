# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import re

from benchmarks import v8_helper
from core import perf_benchmark
from telemetry import benchmark
from telemetry.timeline import chrome_trace_config
from telemetry.timeline import chrome_trace_category_filter
from telemetry.web_perf import timeline_based_measurement
import page_sets


# See tr.v.Numeric.getSummarizedScalarNumericsWithNames()
# https://github.com/catapult-project/catapult/blob/master/tracing/tracing/value/numeric.html#L323
_IGNORED_MEMORY_STATS_RE = re.compile(r'_(std|count|min|sum|pct_\d{4}(_\d+)?)$')

# Track only the high-level GC stats to reduce the data load on dashboard.
_IGNORED_V8_STATS_RE = re.compile(
    r'_(idle_deadline_overrun|percentage_idle|outside_idle)')
_V8_GC_HIGH_LEVEL_STATS_RE = re.compile(r'^v8-gc-('
    r'full-mark-compactor_|'
    r'incremental-finalize_|'
    r'incremental-step_|'
    r'latency-mark-compactor_|'
    r'memory-mark-compactor_|'
    r'scavenger_|'
    r'total_)')


class _V8BrowsingBenchmark(perf_benchmark.PerfBenchmark):
  """Base class for V8 browsing benchmarks.
  This benchmark measures memory usage with periodic memory dumps and v8 times.
  See browsing_stories._BrowsingStory for workload description.
  """

  def CreateTimelineBasedMeasurementOptions(self):
    categories = [
      # Disable all categories by default.
      '-*',
      # Memory categories.
      'disabled-by-default-memory-infra',
      # EQT categories.
      'blink.user_timing',
      'loading',
      'navigation',
      'toplevel',
      # V8 categories.
      'blink.console',
      'disabled-by-default-v8.gc',
      'renderer.scheduler',
      'v8',
      'webkit.console',
      # TODO(crbug.com/616441, primiano): Remove this temporary workaround,
      # which enables memory-infra V8 code stats in V8 code size benchmarks
      # only (to not slow down detailed memory dumps in other benchmarks).
      'disabled-by-default-memory-infra.v8.code_stats',
    ]
    options = timeline_based_measurement.Options(
        chrome_trace_category_filter.ChromeTraceCategoryFilter(
            ','.join(categories)))
    options.config.enable_android_graphics_memtrack = True
    # Trigger periodic light memory dumps every 1000 ms.
    memory_dump_config = chrome_trace_config.MemoryDumpConfig()
    memory_dump_config.AddTrigger('light', 1000)
    options.config.chrome_trace_config.SetMemoryDumpConfig(memory_dump_config)
    options.SetTimelineBasedMetrics([
      'expectedQueueingTimeMetric', 'v8AndMemoryMetrics'])
    return options

  def CreateStorySet(self, options):
    return page_sets.SystemHealthStorySet(platform=self.PLATFORM, case='browse')

  @classmethod
  def ValueCanBeAddedPredicate(cls, value, is_first_result):
    # TODO(crbug.com/610962): Remove this stopgap when the perf dashboard
    # is able to cope with the data load generated by TBMv2 metrics.
    if 'memory:chrome' in value.name:
      return ('renderer_processes' in value.name and
              not _IGNORED_MEMORY_STATS_RE.search(value.name))
    if 'v8-gc' in value.name:
      return (_V8_GC_HIGH_LEVEL_STATS_RE.search(value.name) and
              not _IGNORED_V8_STATS_RE.search(value.name))
    # Allow all other metrics.
    return True

  @classmethod
  def ShouldTearDownStateAfterEachStoryRun(cls):
    return True


class _V8RuntimeStatsBrowsingBenchmark(perf_benchmark.PerfBenchmark):
  """Base class for V8 browsing benchmarks that measure RuntimeStats.
  RuntimeStats measure the time spent by v8 in different phases like
  compile, JS execute, runtime etc.,
  See browsing_stories._BrowsingStory for workload description.
  """

  def CreateTimelineBasedMeasurementOptions(self):
    categories = [
      # Disable all categories by default.
      '-*',
      # Memory categories.
      'disabled-by-default-memory-infra',
      # UE categories requred by runtimeStatsTotalMetric to bucket
      # runtimeStats by UE.
      'rail',
      # EQT categories.
      'blink.user_timing',
      'loading',
      'navigation',
      'toplevel',
      # V8 categories.
      'blink.console',
      'disabled-by-default-v8.gc',
      'renderer.scheduler',
      'v8',
      'webkit.console',
      'disabled-by-default-v8.runtime_stats',
    ]
    options = timeline_based_measurement.Options(
        chrome_trace_category_filter.ChromeTraceCategoryFilter(
            ','.join(categories)))
    options.config.enable_android_graphics_memtrack = True
    # Trigger periodic light memory dumps every 1000 ms.
    memory_dump_config = chrome_trace_config.MemoryDumpConfig()
    memory_dump_config.AddTrigger('light', 1000)
    options.config.chrome_trace_config.SetMemoryDumpConfig(memory_dump_config)

    options.SetTimelineBasedMetrics([
      'expectedQueueingTimeMetric', 'runtimeStatsTotalMetric', 'gcMetric'])
    return options

  def CreateStorySet(self, options):
    return page_sets.SystemHealthStorySet(platform=self.PLATFORM, case='browse')

  @classmethod
  def ShouldTearDownStateAfterEachStoryRun(cls):
    return True


class _V8DesktopBrowsingBenchmark(_V8BrowsingBenchmark):

  @classmethod
  def ShouldDisable(cls, possible_browser):
    # http://crbug.com/628736
    if (possible_browser.platform.GetOSName() == 'mac' and
        possible_browser.browser_type == 'reference'):
      return True

    return possible_browser.platform.GetDeviceTypeName() != 'Desktop'


class _V8MobileBrowsingBenchmark(_V8BrowsingBenchmark):

  @classmethod
  def ShouldDisable(cls, possible_browser):
    return possible_browser.platform.GetDeviceTypeName() == 'Desktop'


@benchmark.Owner(emails=['ulan@chromium.org'])
class V8DesktopBrowsingBenchmark(_V8DesktopBrowsingBenchmark):
  PLATFORM = 'desktop'

  @classmethod
  def Name(cls):
    return 'v8.browsing_desktop'


@benchmark.Owner(emails=['ulan@chromium.org'])
@benchmark.Disabled('reference')  # http://crbug.com/628631
class V8MobileBrowsingBenchmark(_V8MobileBrowsingBenchmark):
  PLATFORM = 'mobile'

  @classmethod
  def Name(cls):
    return 'v8.browsing_mobile'


@benchmark.Disabled('reference')  # http://crbug.com/700390
@benchmark.Disabled('all')
@benchmark.Owner(emails=['mvstaton@chromium.org'])
class V8DesktopTurboBrowsingBenchmark(_V8DesktopBrowsingBenchmark):
  PLATFORM = 'desktop'

  def SetExtraBrowserOptions(self, options):
    super(V8DesktopTurboBrowsingBenchmark, self).SetExtraBrowserOptions(
        options)
    v8_helper.EnableTurbo(options)

  @classmethod
  def Name(cls):
    return 'v8.browsing_desktop_turbo'



@benchmark.Disabled('reference')  # http://crbug.com/628631
@benchmark.Disabled('all')
@benchmark.Owner(emails=['mvstaton@chromium.org'])
class V8MobileTurboBrowsingBenchmark(_V8MobileBrowsingBenchmark):
  PLATFORM = 'mobile'

  def SetExtraBrowserOptions(self, options):
    super(V8MobileTurboBrowsingBenchmark, self).SetExtraBrowserOptions(
        options)
    v8_helper.EnableTurbo(options)

  @classmethod
  def Name(cls):
    return 'v8.browsing_mobile_turbo'


@benchmark.Disabled('reference')  # http://crbug.com/700390
@benchmark.Owner(emails=['hablich@chromium.org'])
class V8DesktopClassicBrowsingBenchmark(_V8DesktopBrowsingBenchmark):
  PLATFORM = 'desktop'

  def SetExtraBrowserOptions(self, options):
    super(V8DesktopClassicBrowsingBenchmark, self).SetExtraBrowserOptions(
        options)
    v8_helper.EnableClassic(options)

  @classmethod
  def Name(cls):
    return 'v8.browsing_desktop_classic'


@benchmark.Disabled('reference')  # http://crbug.com/628631
@benchmark.Owner(emails=['hablich@chromium.org'])
class V8MobileClassicBrowsingBenchmark(_V8MobileBrowsingBenchmark):
  PLATFORM = 'mobile'

  def SetExtraBrowserOptions(self, options):
    super(V8MobileClassicBrowsingBenchmark, self).SetExtraBrowserOptions(
        options)
    v8_helper.EnableClassic(options)

  @classmethod
  def Name(cls):
    return 'v8.browsing_mobile_classic'


@benchmark.Owner(emails=['mythria@chromium.org'])
@benchmark.Disabled('win')  # http://crbug.com/704197
class V8RuntimeStatsDesktopBrowsingBenchmark(
    _V8RuntimeStatsBrowsingBenchmark):
  PLATFORM = 'desktop'

  @classmethod
  def ShouldDisable(cls, possible_browser):
    return possible_browser.platform.GetDeviceTypeName() != 'Desktop'

  @classmethod
  def Name(cls):
    return 'v8.runtimestats.browsing_desktop'


@benchmark.Disabled('reference')  # http://crbug.com/700390
@benchmark.Disabled('all')
@benchmark.Owner(emails=['mythria@chromium.org'])
class V8RuntimeStatsDesktopTurboBrowsingBenchmark(
    _V8RuntimeStatsBrowsingBenchmark):
  PLATFORM = 'desktop'

  def SetExtraBrowserOptions(self, options):
    super(V8RuntimeStatsDesktopTurboBrowsingBenchmark,
        self).SetExtraBrowserOptions(options)
    v8_helper.EnableTurbo(options)

  @classmethod
  def ShouldDisable(cls, possible_browser):
    return possible_browser.platform.GetDeviceTypeName() != 'Desktop'

  @classmethod
  def Name(cls):
    return 'v8.runtimestats.browsing_desktop_turbo'


@benchmark.Disabled('reference',  # http://crbug.com/700390
                    'win')        # http://crbug.com/704197
@benchmark.Owner(emails=['hablich@chromium.org'])
class V8RuntimeStatsDesktopClassicBrowsingBenchmark(
    _V8RuntimeStatsBrowsingBenchmark):
  PLATFORM = 'desktop'

  def SetExtraBrowserOptions(self, options):
    super(V8RuntimeStatsDesktopClassicBrowsingBenchmark,
        self).SetExtraBrowserOptions(options)
    v8_helper.EnableClassic(options)

  @classmethod
  def ShouldDisable(cls, possible_browser):
    return possible_browser.platform.GetDeviceTypeName() != 'Desktop'

  @classmethod
  def Name(cls):
    return 'v8.runtimestats.browsing_desktop_classic'



@benchmark.Disabled('reference')  # http://crbug.com/694658
@benchmark.Owner(emails=['mythria@chromium.org'])
class V8RuntimeStatsMobileBrowsingBenchmark(
    _V8RuntimeStatsBrowsingBenchmark):
  PLATFORM = 'mobile'

  @classmethod
  def ShouldDisable(cls, possible_browser):
    return possible_browser.platform.GetDeviceTypeName() == 'Desktop'

  @classmethod
  def Name(cls):
    return 'v8.runtimestats.browsing_mobile'


@benchmark.Disabled('reference')  # http://crbug.com/694658
@benchmark.Disabled('all')
@benchmark.Owner(emails=['mythria@chromium.org'])
class V8RuntimeStatsMobileTurboBrowsingBenchmark(
    _V8RuntimeStatsBrowsingBenchmark):
  PLATFORM = 'mobile'

  def SetExtraBrowserOptions(self, options):
    super(V8RuntimeStatsMobileTurboBrowsingBenchmark,
        self).SetExtraBrowserOptions(options)
    v8_helper.EnableTurbo(options)

  @classmethod
  def ShouldDisable(cls, possible_browser):
    return possible_browser.platform.GetDeviceTypeName() == 'Desktop'

  @classmethod
  def Name(cls):
    return 'v8.runtimestats.browsing_mobile_turbo'


@benchmark.Disabled('reference')  # http://crbug.com/694658
@benchmark.Owner(emails=['hablich@chromium.org'])
class V8RuntimeStatsMobileClassicBrowsingBenchmark(
    _V8RuntimeStatsBrowsingBenchmark):
  PLATFORM = 'mobile'

  def SetExtraBrowserOptions(self, options):
    super(V8RuntimeStatsMobileClassicBrowsingBenchmark,
        self).SetExtraBrowserOptions(options)
    v8_helper.EnableClassic(options)

  @classmethod
  def ShouldDisable(cls, possible_browser):
    return possible_browser.platform.GetDeviceTypeName() == 'Desktop'

  @classmethod
  def Name(cls):
    return 'v8.runtimestats.browsing_mobile_classic'
