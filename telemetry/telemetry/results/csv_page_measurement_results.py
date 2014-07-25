# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import csv

from telemetry.results import page_measurement_results
from telemetry.value import merge_values


class CsvPageMeasurementResults(
    page_measurement_results.PageMeasurementResults):
  def __init__(self, output_stream):
    super(CsvPageMeasurementResults, self).__init__(output_stream)
    self._results_writer = csv.writer(self._output_stream)
    self._representative_value_names = None

  def PrintSummary(self):
    try:
      values = merge_values.MergeLikeValuesFromSamePage(
          self.all_page_specific_values)
      self._OutputHeader(values)
      value_groups_by_page = merge_values.GroupStably(
          values, lambda value: value.page.url)
      for values_for_page in value_groups_by_page:
        self._OutputValuesForPage(values_for_page[0].page, values_for_page)
    finally:
      super(CsvPageMeasurementResults, self).PrintSummary()

  def _OutputHeader(self, values):
    """Output the header rows.

    This will retrieve the header string from the given values. As a
    results, you would typically pass it all of the recorded values at
    the end of the entire telemetry run. In cases where each page
    produces the same set of value names, you may call this method
    with that set of values.

    Args:
      values: A set of values from which to extract the header string,
          which is the value name and the units.
    """
    representative_values = {}
    for value in values:
      if value.name not in representative_values:
        representative_values[value.name] = value
    self._representative_value_names = list(
        representative_values.keys())
    self._representative_value_names.sort()

    row = ['page_name']
    for value_name in self._representative_value_names:
      units = representative_values[value_name].units
      row.append('%s (%s)' % (value_name, units))
    self._results_writer.writerow(row)
    self._output_stream.flush()

  def _OutputValuesForPage(self, page, page_values):
    row = [page.display_name]
    values_by_value_name = {}
    for value in page_values:
      values_by_value_name[value.name] = value

    for value_name in self._representative_value_names:
      value = values_by_value_name.get(value_name, None)
      if value and value.GetRepresentativeNumber():
        row.append('%s' % value.GetRepresentativeNumber())
      else:
        row.append('-')
    self._results_writer.writerow(row)
    self._output_stream.flush()
