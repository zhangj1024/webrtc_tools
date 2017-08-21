# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from core import perf_benchmark
import page_sets

from telemetry import benchmark
from telemetry import story
from telemetry.timeline import chrome_trace_category_filter
from telemetry.web_perf import timeline_based_measurement
from telemetry.web_perf.metrics import startup


class _StartupPerfBenchmark(perf_benchmark.PerfBenchmark):
  """Measures time to start Chrome."""

  def SetExtraBrowserOptions(self, options):
    options.AppendExtraBrowserArgs([
        '--enable-stats-collection-bindings'
    ])

  def CreateCoreTimelineBasedMeasurementOptions(self):
    startup_category_filter = (
        chrome_trace_category_filter.ChromeTraceCategoryFilter(
            filter_string='startup,blink.user_timing'))
    options = timeline_based_measurement.Options(
        overhead_level=startup_category_filter)
    options.SetLegacyTimelineBasedMetrics(
        [startup.StartupTimelineMetric()])
    return options


@benchmark.Owner(emails=['pasko@chromium.org'])
class StartWithUrlColdTBM(_StartupPerfBenchmark):
  """Measures time to start Chrome cold with startup URLs."""

  page_set = page_sets.StartupPagesPageSet
  options = {'pageset_repeat': 5}

  def SetExtraBrowserOptions(self, options):
    options.clear_sytem_cache_for_browser_and_profile_on_start = True
    super(StartWithUrlColdTBM, self).SetExtraBrowserOptions(options)

  @classmethod
  def ShouldDisable(cls, possible_browser):  # http://crbug.com/667470
    return (possible_browser.platform.GetDeviceTypeName() in
            ['Nexus 7v2', 'Nexus 9'])

  @classmethod
  def Name(cls):
    return 'start_with_url.cold.startup_pages'

  # TODO(rnephew): Test if kapook.com fails on both or just one of the configs.
  def GetExpectations(self):
    class StoryExpectations(story.expectations.StoryExpectations):
      def SetExpectations(self):
        self.PermanentlyDisableBenchmark(
            [story.expectations.ALL_DESKTOP], 'Mobile Benchmark')
        self.PermanentlyDisableBenchmark(
            [story.expectations.ANDROID_WEBVIEW], 'Requires tabs')
        self.DisableStory(
            'http://kapook.com', [story.expectations.ALL], 'crbug.com/667470')
    return StoryExpectations()


@benchmark.Owner(emails=['pasko@chromium.org'])
class StartWithUrlWarmTBM(_StartupPerfBenchmark):
  """Measures stimetime to start Chrome warm with startup URLs."""

  page_set = page_sets.StartupPagesPageSet
  options = {'pageset_repeat': 11}

  @classmethod
  def Name(cls):
    return 'start_with_url.warm.startup_pages'

  @classmethod
  def ValueCanBeAddedPredicate(cls, value, is_first_result):
    del value  # unused
    # Ignores first results because the first invocation is actualy cold since
    # we are loading the profile for the first time.
    return not is_first_result

  # TODO(rnephew): Test if kapook.com fails on both or just one of the configs.
  def GetExpectations(self):
    class StoryExpectations(story.expectations.StoryExpectations):
      def SetExpectations(self):
        self.PermanentlyDisableBenchmark(
            [story.expectations.ALL_DESKTOP], 'Mobile Benchmark')
        self.PermanentlyDisableBenchmark(
            [story.expectations.ANDROID_WEBVIEW], 'Requires tabs')
        self.DisableStory(
            'http://kapook.com', [story.expectations.ALL], 'crbug.com/667470')
    return StoryExpectations()

