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


def __tmp1(count, data, __tmp6: <FILL>):
  if isinstance(data, list):
    for node in data:
      count = __tmp1(count, node, __tmp6)
  else:
    if "completed" in data:
      count += 1 if data["completed"] == __tmp6 else 0
    for node in data:
      if isinstance(data[node], list) or isinstance(data[node], dict):
        count = __tmp1(count, data[node], __tmp6)
  return count


def _get_tasks(tasks, data):
  if isinstance(data, list):
    for node in data:
      _get_tasks(tasks, node)
  else:
    if "dateAdded" in data and "completionDate" in data:
      if data["dateAdded"]:
        tasks.append((data["dateAdded"], data["completionDate"], data["name"]))
    for node in data:
      if isinstance(data[node], list) or isinstance(data[node], dict):
        _get_tasks(tasks, data[node])
  return tasks


def __tmp2(task):
  started, completed, name = task
  if started:
    started = datetime.datetime.utcfromtimestamp(started / 1000)
  if completed:
    completed = datetime.datetime.utcfromtimestamp(completed / 1000)
  return started, completed, name


def __tmp7(data):
  tasks = _get_tasks([], data)
  tasks = [__tmp2(x) for x in sorted(tasks, key=lambda x: x[0])]
  return tasks


def __tmp0(tasks, date, completed: bool):
  count = 0
  for task in tasks:
    # count complete and incomplete tasks:
    if completed and task[1] and task[1].date() <= date:
      count += 1
    elif not completed and task[0] and task[0].date() <= date:
      count += 1
  return count


def process_json(infile, __tmp4):
  me.mkdir(os.path.dirname(__tmp4))

  app.Log(2, f"Parsing {infile.name}")
  data = json.load(infile)

  completed = __tmp1(0, data, __tmp6=True)
  incomplete = __tmp1(1, data, __tmp6=False)

  tasks = __tmp7(data)
  start = tasks[0][0].date()
  today = datetime.date.today()

  with open(__tmp4, "w") as outfile:
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
      incomplete = __tmp0(tasks, date, completed=False)
      __tmp6 = __tmp0(tasks, date, completed=True)
      delta_added = incomplete - last_incomplete
      delta_completed = __tmp6 - last_complete
      delta = delta_added - delta_completed
      writer.writerow(
        [date, incomplete, __tmp6, delta_added, delta_completed, delta]
      )
      last_incomplete = incomplete
      last_complete = __tmp6

    nrows = len(tasks)
    app.Log(1, f'Exported {nrows} records to "{outfile.name}"')


def generate_json(__tmp3, __tmp4):
  app.Log(2, f"Exporting OmniFocus database to JSON")
  subprocess.check_output([__tmp3, "-o", __tmp4])
  return __tmp4


def __tmp5(__tmp3, __tmp4):
  with TemporaryDirectory(prefix="me.csv-") as tmpdir:
    pwd = os.getcwd()
    os.chdir(tmpdir)
    jsonpath = generate_json(__tmp3, "omnifocus.json")
    with open(jsonpath) as infile:
      process_json(infile, f"{__tmp4}/Tasks.csv")
    os.chdir(pwd)
