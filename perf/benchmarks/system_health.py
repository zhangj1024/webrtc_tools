# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import os
import re

from core import perf_benchmark
from telemetry import benchmark
from telemetry.timeline import chrome_trace_category_filter
from telemetry.web_perf import timeline_based_measurement
import page_sets


# See tr.v.Numeric.getSummarizedScalarNumericsWithNames()
# https://github.com/catapult-project/catapult/blob/master/tracing/tracing/value/numeric.html#L323
_IGNORED_STATS_RE = re.compile(r'_(std|count|max|min|sum|pct_\d{4}(_\d+)?)$')


class _CommonSystemHealthBenchmark(perf_benchmark.PerfBenchmark):
  """Chrome Common System Health Benchmark.

  This test suite contains system health benchmarks that can be collected
  together due to the low overhead of the tracing agents required. If a
  benchmark does have significant overhead, it should either:

    1) Be rearchitected such that it doesn't. This is the most preferred option.
    2) Be run in a separate test suite (e.g. memory).

  https://goo.gl/Jek2NL.
  """

  def CreateTimelineBasedMeasurementOptions(self):
    options = timeline_based_measurement.Options(
        chrome_trace_category_filter.ChromeTraceCategoryFilter())
    options.config.chrome_trace_config.category_filter.AddFilterString('rail')
    # TODO(charliea): Reenable BattOr tracing on the main perf waterfall once
    # the BattOrs stop crashing as their SD cards fill up.
    # crbug.com/652384
    options.config.enable_battor_trace = (
        os.environ.get('BUILDBOT_MASTERNAME') == 'chromium.perf.fyi')
    options.config.enable_chrome_trace = True
    options.SetTimelineBasedMetrics(['clockSyncLatencyMetric', 'powerMetric'])
    return options

  def CreateStorySet(self, options):
    return page_sets.SystemHealthStorySet(platform=self.PLATFORM)

  @classmethod
  def ShouldTearDownStateAfterEachStoryRun(cls):
    return True

  @classmethod
  def Name(cls):
    return 'system_health.common_%s' % cls.PLATFORM


class DesktopCommonSystemHealth(_CommonSystemHealthBenchmark):
  """Desktop Chrome Energy System Health Benchmark."""
  PLATFORM = 'desktop'

  @classmethod
  def ShouldDisable(cls, possible_browser):
    # http://crbug.com/624355 (reference builds).
    return (possible_browser.platform.GetDeviceTypeName() != 'Desktop' or
            possible_browser.browser_type == 'reference')


class MobileCommonSystemHealth(_CommonSystemHealthBenchmark):
  """Mobile Chrome Energy System Health Benchmark."""
  PLATFORM = 'mobile'

  @classmethod
  def ShouldDisable(cls, possible_browser):
    # http://crbug.com/612144
    if (possible_browser.browser_type == 'reference' and
        possible_browser.platform.GetDeviceTypeName() == 'Nexus 5X'):
      return True

    return possible_browser.platform.GetDeviceTypeName() == 'Desktop'


class _MemorySystemHealthBenchmark(perf_benchmark.PerfBenchmark):
  """Chrome Memory System Health Benchmark.

  This test suite is run separately from the common one due to the high overhead
  of memory tracing.

  https://goo.gl/Jek2NL.
  """
  options = {'pageset_repeat': 3}

  def SetExtraBrowserOptions(self, options):
    options.AppendExtraBrowserArgs([
        # TODO(perezju): Temporary workaround to disable periodic memory dumps.
        # See: http://crbug.com/513692
        '--enable-memory-benchmarking',
    ])

  def CreateTimelineBasedMeasurementOptions(self):
    options = timeline_based_measurement.Options(
        chrome_trace_category_filter.ChromeTraceCategoryFilter(
            '-*,disabled-by-default-memory-infra'))
    options.config.enable_android_graphics_memtrack = True
    options.SetTimelineBasedMetrics(['memoryMetric'])
    return options

  def CreateStorySet(self, options):
    return page_sets.SystemHealthStorySet(platform=self.PLATFORM,
                                          take_memory_measurement=True)

  @classmethod
  def ShouldTearDownStateAfterEachStoryRun(cls):
    return True

  @classmethod
  def Name(cls):
    return 'system_health.memory_%s' % cls.PLATFORM

  @classmethod
  def ValueCanBeAddedPredicate(cls, value, is_first_result):
    # TODO(crbug.com/610962): Remove this stopgap when the perf dashboard
    # is able to cope with the data load generated by TBMv2 metrics.
    return not _IGNORED_STATS_RE.search(value.name)


class DesktopMemorySystemHealth(_MemorySystemHealthBenchmark):
  """Desktop Chrome Memory System Health Benchmark."""
  PLATFORM = 'desktop'

  @classmethod
  def ShouldDisable(cls, possible_browser):
    # http://crbug.com/624355 (reference builds).
    return (possible_browser.platform.GetDeviceTypeName() != 'Desktop' or
            possible_browser.browser_type == 'reference')


class MobileMemorySystemHealth(_MemorySystemHealthBenchmark):
  """Mobile Chrome Memory System Health Benchmark."""
  PLATFORM = 'mobile'

  @classmethod
  def ShouldDisable(cls, possible_browser):
    # http://crbug.com/612144
    if (possible_browser.browser_type == 'reference' and
        possible_browser.platform.GetDeviceTypeName() == 'Nexus 5X'):
      return True

    return possible_browser.platform.GetDeviceTypeName() == 'Desktop'


@benchmark.Enabled('android-webview')
class WebviewStartupSystemHealthBenchmark(perf_benchmark.PerfBenchmark):
  """Webview startup time benchmark

  Benchmark that measures how long WebView takes to start up
  and load a blank page. Since thie metric only requires the trace
  markers recorded in atrace, Chrome tracing is not enabled for this
  benchmark.
  """
  options = {'pageset_repeat': 20}

  def CreateStorySet(self, options):
    return page_sets.SystemHealthStorySet(platform='mobile', case='blank')

  def CreateTimelineBasedMeasurementOptions(self):
    options = timeline_based_measurement.Options()
    options.SetTimelineBasedMetrics(['webviewStartupMetric'])
    options.config.enable_atrace_trace = True
    options.config.enable_chrome_trace = False
    options.config.atrace_config.app_name = 'org.chromium.webview_shell'
    return options

  @classmethod
  def ShouldTearDownStateAfterEachStoryRun(cls):
    return True

  @classmethod
  def Name(cls):
    return 'system_health.webview_startup'


@benchmark.Enabled('android-webview')
class WebviewMultiprocessStartupSystemHealthBenchmark(
    WebviewStartupSystemHealthBenchmark):
  """Webview multiprocess startup time benchmark

  Benchmark that measures how long WebView takes to start up
  and load a blank page with multiprocess enabled.
  """

  def SetExtraBrowserOptions(self, options):
    options.AppendExtraBrowserArgs(
        ['--webview-sandboxed-renderer'])

  @classmethod
  def Name(cls):
    return 'system_health.webview_startup_multiprocess'
