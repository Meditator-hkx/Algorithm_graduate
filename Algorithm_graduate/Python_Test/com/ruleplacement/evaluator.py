'''
Mainly for performace analysis
link_usage_avg, link_usage_most, swicth_usage_avg, switch_usage_most under different flow numbers with a given topo
'''

class Evaluator:

    def __init__(self, topo):
        self.network = topo
   #     self.avg_link_usage, self.avg_switch_usage = self.computeAvgUsage(self.network)
        self.max_link_usage, self.max_switch_usage, self.all_usage = self.computeMaxUsage(self.network)

    def computeAvgUsage(self, topo):

        return None



    def computeMaxUsage(self, topo):

        LinkUsageSet = [];SwitchUsageSet = []
        for link in topo.LinkSet:
            temp_usage = link.link_used / link.MAX_CAPACITY
            LinkUsageSet.append(temp_usage)
        MaxLinkUsage = max(LinkUsageSet)

        for switch in topo.SwitchSet:
            temp_usage = float(switch.rule_num) / switch.MAX_MEM_SIZE
            SwitchUsageSet.append(temp_usage)
        MaxSwitchUsage = max(SwitchUsageSet)

        return MaxLinkUsage, MaxSwitchUsage, [LinkUsageSet, SwitchUsageSet]