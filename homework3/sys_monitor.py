"""
psutil: library for retrieving information on running processes
and system utilization (CPU, memory, disks, network)
"""
import json
import datetime
import time
import psutil
import yaml


class Monitor(object):
    """
    Monitor your system/server state via psutil library.

    :param cpu_interval: int, CPU delay in minutes for calculation
    of io differences
    :param output_format: json | None, format of output data
    :current_number: int, Current counter for SNAPSHOT
    """
    current_number = 0

    def __init__(self, cpu_interval, output_format=None):

        self.cpu_interval = cpu_interval
        self.output_format = output_format

        self.cpu_load = psutil.cpu_percent(interval=self.cpu_interval * 1,
                                           percpu=False)

        self.vrt_mem = psutil.virtual_memory()
        self.swp_mem = psutil.swap_memory()
        self.disk_io = psutil.disk_io_counters()
        self.net_io = psutil.net_io_counters()

    @classmethod
    def increment_number(cls):
        """
        :return: incremented number
        """
        cls.current_number += 1
        return Monitor.current_number

    def get_system_info(self):
        """
        Get system utilization information (CPU, memory, disks, network)
        in appropriate text format

        :time.sleep(1): Delay to get io difference between states of disk
        before and after calculation
        :return: formed data in json or in plain text format
        """
        total_mem = self.vrt_mem.total + self.swp_mem.total
        mem_percent = round((float(self.vrt_mem.used) / total_mem * 100), 1)
        time.sleep(1)
        disk_after = psutil.disk_io_counters()
        disk_r = (disk_after[2] - self.disk_io[2]) >> 10   # convert to Kb
        disk_w = (disk_after[3] - self.disk_io[3]) >> 10
        net_s = self.net_io.bytes_sent >> 10
        net_r = self.net_io.bytes_recv >> 10

        disk_io = '{0}/{1}'.format(disk_r, disk_w)
        net_io = '{0}/{1}'.format(net_s, net_r)

        if self.output_format == 'json':
            data = dict()
            data['cpu_load'] = self.cpu_load
            data['mem_load'] = mem_percent
            data['mem_vrt'] = self.vrt_mem.percent
            data['disk_io'] = disk_io
            data['net_io'] = net_io
            return json.dumps(data)
        else:
            return ('CPU load                 : {0}%\n'
                    'Memory usage             : {1}%\n'
                    'Virtual memory usage     : {2}%\n'
                    'IO disk info read/write  : {3}Kb\n'
                    'IO net info sent/receive : {4}Kb\n'
                    .format(self.cpu_load,
                            mem_percent,
                            self.vrt_mem.percent,
                            disk_io,
                            net_io))


if __name__ == '__main__':

    # Open yaml config file and get essential parameters
    with open("config.yml", 'r') as config:
        file_data = yaml.load(config)

    interval = file_data['common']['interval']
    text_format = file_data['common']['output']

    # Launch script
    while True:

        # Create a new instance in order to collect a new system data
        sys_data = Monitor(interval, text_format)

        # Set up date header in appropriate format
        time_format = datetime.datetime.fromtimestamp(
            time.time()).strftime('%d.%m.%Y %H:%M:%S')

        # Open file for new writing/appending
        logging = open("snapshot_log.txt", "a+")
        logging.write("\nSNAPSHOT {0}: {1}\n{2}\n".format(
            sys_data.increment_number(),
            time_format,
            sys_data.get_system_info()))

        # Close file after completion
        logging.close()
