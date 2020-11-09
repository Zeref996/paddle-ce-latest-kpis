# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
sys.path.insert(0, os.environ['ceroot'])

from kpi import CostKpi, DurationKpi, AccKpi

dynamic_train_reward_kpi = AccKpi('Average_reward', 0.002, 0, actived=True)
dynamic_train_loss_kpi = CostKpi('loss_probs', 0.002, 0, actived=True)
dynamic_train_elapse_kpi = DurationKpi(
    'Elapse', 0.002, 0, actived=True, unit_repr="ms")

tracking_kpis = [
    dynamic_train_reward_kpi, dynamic_train_loss_kpi, dynamic_train_elapse_kpi
]


def parse_log(log: str):
    """[summary]
    Args:
        log (str): log read from sys std input
    Returns:
        dynamic_logs[-1] (dict): parsed log info
    """
    dynamic_Elapse = []
    dy2staic_Elapse = []
    for line in log.split('\n'):
        Log = {}
        fs = line.strip().split(',\t')
        if "ToStatic = False" in fs:
            dynamic_Average_reward = float(fs[3].split('=')[-1])
            dynamic_loss_probs = float(fs[4].split('=')[-1])
            dynamic_Elapse.append(float(fs[5].split('=')[-1]))
        elif "ToStatic = True" in fs:
            dy2static_Average_reward = float(fs[3].split('=')[-1])
            dy2static_loss_probs = float(fs[4].split('=')[-1])
            dy2staic_Elapse.append(float(fs[5].split('=')[-1]))
        else:
            pass
    Log['dynamic_Average_reward'] = dynamic_Average_reward
    Log['dynamic_loss_probs'] = dynamic_loss_probs
    Log['dynamic_Elapse'] = sum(dynamic_Elapse) / len(dynamic_Elapse)

    Log['dy2static_Average_reward'] = dy2static_Average_reward
    Log['dy2static_loss_probs'] = dy2static_loss_probs
    Log['dy2staic_Elapse'] = sum(dy2staic_Elapse) / len(dy2staic_Elapse)
    return Log


def log_to_ce(log: str):
    """[summary]
    Args:
        log (str): log read from sys std input
    """
    dict_log = parse_log(log)

    kpi_tracker = {}
    for kpi in tracking_kpis:
        kpi_tracker[kpi.name] = kpi

    for key in dict_log:
        kpi_tracker[key].add_record(dict_log[key])
        kpi_tracker[key].persist()


if __name__ == '__main__':
    log = sys.stdin.read()
    print("*****")
    log_to_ce(log)
    print("*****")
