# Copyright 2018-2020 Chris Cummins <chrisc.101@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import csv
import datetime
import json
import os
import subprocess
from tempfile import TemporaryDirectory

from datasets.me_db import utils as me


def __tmp1(count, data, __tmp9: bool):
  if isinstance(data, list):
    for node in data:
      count = __tmp1(count, node, __tmp9)
  else:
    if "completed" in data:
      count += 1 if data["completed"] == __tmp9 else 0
    for node in data:
      if isinstance(data[node], list) or isinstance(data[node], dict):
        count = __tmp1(count, data[node], __tmp9)
  return count


def __tmp5(__tmp10, data):
  if isinstance(data, list):
    for node in data:
      __tmp5(__tmp10, node)
  else:
    if "dateAdded" in data and "completionDate" in data:
      if data["dateAdded"]:
        __tmp10.append((data["dateAdded"], data["completionDate"], data["name"]))
    for node in data:
      if isinstance(data[node], list) or isinstance(data[node], dict):
        __tmp5(__tmp10, data[node])
  return __tmp10


def __tmp0(__tmp4):
  started, completed, name = __tmp4
  if started:
    started = datetime.datetime.utcfromtimestamp(started / 1000)
  if completed:
    completed = datetime.datetime.utcfromtimestamp(completed / 1000)
  return started, completed, name


def __tmp11(data):
  __tmp10 = __tmp5([], data)
  __tmp10 = [__tmp0(x) for x in sorted(__tmp10, key=lambda x: x[0])]
  return __tmp10


def task_count(__tmp10, date, completed: <FILL>):
  count = 0
  for __tmp4 in __tmp10:
    # count complete and incomplete tasks:
    if completed and __tmp4[1] and __tmp4[1].date() <= date:
      count += 1
    elif not completed and __tmp4[0] and __tmp4[0].date() <= date:
      count += 1
  return count


def process_json(__tmp8, __tmp6):
  me.mkdir(os.path.dirname(__tmp6))

  app.Log(2, f"Parsing {__tmp8.name}")
  data = json.load(__tmp8)

  completed = __tmp1(0, data, __tmp9=True)
  incomplete = __tmp1(1, data, __tmp9=False)

  __tmp10 = __tmp11(data)
  start = __tmp10[0][0].date()
  today = datetime.date.today()

  with open(__tmp6, "w") as outfile:
    writer = csv.writer(outfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)

    # Write header
    writer.writerow(
      [
        "Date",
        "Incomplete Tasks",
        "Complete Tasks",
        "Tasks Added",
        "Tasks Completed",
        "Tasks Delta",
      ]
    )

    last_incomplete, last_complete = 0, 0

    for date in me.daterange(start, today):
      incomplete = task_count(__tmp10, date, completed=False)
      __tmp9 = task_count(__tmp10, date, completed=True)
      delta_added = incomplete - last_incomplete
      delta_completed = __tmp9 - last_complete
      delta = delta_added - delta_completed
      writer.writerow(
        [date, incomplete, __tmp9, delta_added, delta_completed, delta]
      )
      last_incomplete = incomplete
      last_complete = __tmp9

    nrows = len(__tmp10)
    app.Log(1, f'Exported {nrows} records to "{outfile.name}"')


def __tmp3(__tmp2, __tmp6):
  app.Log(2, f"Exporting OmniFocus database to JSON")
  subprocess.check_output([__tmp2, "-o", __tmp6])
  return __tmp6


def __tmp7(__tmp2, __tmp6):
  with TemporaryDirectory(prefix="me.csv-") as tmpdir:
    pwd = os.getcwd()
    os.chdir(tmpdir)
    jsonpath = __tmp3(__tmp2, "omnifocus.json")
    with open(jsonpath) as __tmp8:
      process_json(__tmp8, f"{__tmp6}/Tasks.csv")
    os.chdir(pwd)
