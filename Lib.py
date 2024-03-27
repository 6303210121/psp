
# ospf_lib.py

class OSPFConfig:
    def __init__(self, device):
        self.device = device

    def configure_ospf(self, process_id, network, area):
        config_commands = [
            f"router ospf {process_id}",
            f"network {network} area {area}",
            "end"
        ]
        self.device.execute(config_commands)


class OSPFMonitor:
    def __init__(self, device):
        self.device = device

    def get_ospf_neighbors(self):
        output = self.device.parse("show ip ospf neighbor")
        return output
