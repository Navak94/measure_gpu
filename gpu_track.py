import os.path
import xlwt
import subprocess as sp
import os
from threading import Thread , Timer
import sched, time

def get_gpu_memory_used():
    
    COMMAND = "nvidia-smi --query-gpu=memory.used --format=csv"
    memory_use_values = body(COMMAND)
    return memory_use_values

def get_gpu_memory_total():
    
    COMMAND = "nvidia-smi --query-gpu=memory.total --format=csv"
    memory_free_values = body(COMMAND)
    return memory_free_values

def get_gpu_temperature():
    
    COMMAND = "nvidia-smi --query-gpu=temperature.gpu --format=csv"
    gpu_temp = body(COMMAND)
    return gpu_temp

def get_utilization_gpu_nvidia():
    
    COMMAND = "nvidia-smi --query-gpu=utilization.gpu --format=csv"
    gpu_utilization_nvidia = body(COMMAND)
    return gpu_utilization_nvidia

def get_utilization_memory_nvidia():
    
    COMMAND = "nvidia-smi --query-gpu=utilization.memory --format=csv"
    gpu_utilization_nvidia = body(COMMAND)
    return gpu_utilization_nvidia
    
def get_timestamp_from_nvidia():
    
    COMMAND = "nvidia-smi --query-gpu=timestamp --format=csv"
    timestamp = body(COMMAND)
    return timestamp
    

def body(COMMAND):
    output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
    ACCEPTABLE_AVAILABLE_MEMORY = 1024

    try:
        memory_info = output_to_list(sp.check_output(COMMAND.split(),stderr=sp.STDOUT))[1:]
    except sp.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

    if "timestamp" in COMMAND:
       info = str(memory_info)
       info = info.replace("r","").replace("[","").replace("]","").replace("'","").replace("\\","")

    else:
        info = [int(x.split()[0]) for i, x in enumerate(memory_info)]
        info = str(info)
        info = info.replace("[","").replace("]","")
        info = float(info)
        
    return info


def print_gpu_memory_every_5secs():

    #prints itself every 5 seconds
    Timer(5.0, print_gpu_memory_every_5secs).start()
    memory_used = get_gpu_memory_used()
    memory_total = get_gpu_memory_total()

    #values to be written to the csv file
    gpu_temperature = get_gpu_temperature()
    utilization_gpu_nvidia = get_utilization_gpu_nvidia()
    utilization_memory_nvidia = get_utilization_memory_nvidia()
    calculated_utilization = (memory_used/memory_total)*100
    timestamp_from_nvidia = get_timestamp_from_nvidia()
    

    try:
        if os.path.isfile("Output.csv"):
            text_file = open("Output.csv", "a")
            text_file.write(str(gpu_temperature)+","+ str(utilization_gpu_nvidia)+","+ str(utilization_memory_nvidia)+","+ str(calculated_utilization)+ ","+ timestamp_from_nvidia + "\n")
            text_file.close()
        if os.path.isfile("Output.csv")== False:
            text_file = open("Output.csv", "a")
            text_file.write("GPU temperature , Nvidia's measured GPU utilization, Nvidia's Measured memory utilization, my calculated utilization, timestamp\n")
            text_file.close()
    except AttributeError:
        pass
print_gpu_memory_every_5secs()

