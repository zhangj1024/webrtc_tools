# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from core import perf_benchmark

from measurements import memory
import page_sets
from telemetry import benchmark


@benchmark.Enabled('android')
class MemoryMobile(perf_benchmark.PerfBenchmark):
  test = memory.Memory
  page_set = page_sets.MobileMemoryPageSet

  @classmethod
  def Name(cls):
    return 'memory.mobile_memory'


@benchmark.Disabled('yosemite')  # crbug.com/517806
class MemoryTop7Stress(perf_benchmark.PerfBenchmark):
  """Use (recorded) real world web sites and measure memory consumption."""
  test = memory.Memory
  page_set = page_sets.Top7StressPageSet

  @classmethod
  def Name(cls):
    return 'memory.top_7_stress'


class MemoryLongRunningIdleGmail(perf_benchmark.PerfBenchmark):
  """Use (recorded) real world web sites and measure memory consumption
  of long running idle Gmail page """
  test = memory.Memory
  page_set = page_sets.LongRunningIdleGmailPageSet

  @classmethod
  def Name(cls):
    return 'memory.long_running_idle_gmail'


class MemoryLongRunningIdleGmailBackground(perf_benchmark.PerfBenchmark):
  """Use (recorded) real world web sites and measure memory consumption
  of long running idle Gmail page in background tab"""
  test = memory.Memory
  page_set = page_sets.LongRunningIdleGmailBackgroundPageSet

  @classmethod
  def Name(cls):
    return 'memory.long_running_idle_gmail_background'
