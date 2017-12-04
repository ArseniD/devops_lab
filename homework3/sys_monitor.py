import datetime
import time
import psutil
import yaml
import json


class sysMonitor:
    def __init__(self):
        """
        :current_number: int, Current counter for SNAPSHOT
        """
        self.current_number = 0

        self.cpu_nums = psutil.cpu_count()
        self.vrt_mem = psutil.virtual_memory()
        self.swp_mem = psutil.swap_memory()
        self.disk_io = psutil.disk_io_counters()
        self.net_io = psutil.net_io_counters()

        self.total_mem = self.vrt_mem.total + self.swp_mem.total
        self.used_mem = self.vrt_mem.used
        self.used_vrt_mem = self.vrt_mem.percent

    def increment_number(self):
        """

        :return: incremented number
        """
        self.current_number += 1
        return self.current_number

    def get_system_info(self, cpu_interval, output_format=None):
        """
        :param cpu_interval: int, CPU delay in minutes for calculation
        of io differences
        :param output_format: json | None, format of output data
        :return: formed data in json or in plain text format
        """
        disk_before = psutil.disk_io_counters()
        cpu_percent = psutil.cpu_percent(interval=cpu_interval * 60,
                                         percpu=False)
        mem_percent = round((float(self.used_mem) / self.total_mem * 100), 1)
        vrt_mem_percent = self.used_vrt_mem

        disk_after = psutil.disk_io_counters()
        disk_r = (disk_after.read_bytes -
                  disk_before.read_bytes) >> 10  # convert to Kb
        disk_w = (disk_after.write_bytes -
                  disk_before.write_bytes) >> 10  # convert to Kb
        disk_io = '{0}/{1}'.format(disk_r, disk_w)

        net_s = self.net_io.bytes_sent >> 10  # convert to Kb
        net_r = self.net_io.bytes_recv >> 10  # convert to Kb
        net_io = '{0}/{1}'.format(net_s, net_r)

        if output_format == 'json':
            data = {}
            data['cpu_load'] = cpu_percent
            data['mem_load'] = mem_percent
            data['mem_vrt'] = vrt_mem_percent
            data['disk_io'] = disk_io
            data['net_io'] = net_io
            return json.dumps(data)
        else:
            return ('CPU load                 : {0}%\n'
                    'Memory usage             : {1}%\n'
                    'Virtual memory usage     : {2}%\n'
                    'IO disk info read/write  : {3}Kb\n'
                    'IO net info sent/receive : {4}Kb\n'
                    .format(cpu_percent,
                            mem_percent,
                            vrt_mem_percent,
                            disk_io,
                            net_io))


if __name__ == '__main__':

    # Open yaml config file and get essential parameters
    with open("config.yml", 'r') as config:
        data = yaml.load(config)

    interval = data['common']['interval']
    output_format = data['common']['output']

    while (True):

        # Create a new instance in order to collect a new system data
        sys_data = sysMonitor()

        # Set up date header in appropriate format
        time_format = datetime.datetime.fromtimestamp(
            time.time()).strftime('%d.%m.%Y,%H:%M:%S')

        # Open file for new writing/appending
        logging = open("snapshot_log.txt", "a+")
        logging.write("\nSNAPSHOT {0}:"
                      " {1}\n"
                      "{2}\n".format(sys_data.increment_number(),
                                     time_format,
                                     sys_data.get_system_info(
                                     interval, output_format)))
        # Close file after completion
        logging.close()
