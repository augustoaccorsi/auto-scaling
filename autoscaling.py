from subprocess import Popen, PIPE
import json
from typing import Any


class AutoScaling:

    auto_scaling_info = {}
    instances = []

    def json_converter(self, output):
        return json.loads(output)

    def describe(self, autoscalinggroup, region):
        p = Popen(['bat-files\describe-auto-scaling-group.bat', autoscalinggroup, region], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output = p.communicate()[0]

        result = output.decode('utf-8').split("--region sa-east-1")
        self.auto_scaling_info = self.json_converter(result[1])

    def get_instances(self):
        print(self.auto_scaling_info)

if __name__ == '__main__':
    autoscaling = AutoScaling()
    autoscaling.describe("web-app-asg", "sa-east-1")
    autoscaling.get_instances()