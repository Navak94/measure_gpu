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
    


def body(COMMAND):
    output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
    ACCEPTABLE_AVAILABLE_MEMORY = 1024
    try:
        memory_info = output_to_list(sp.check_output(COMMAND.split(),stderr=sp.STDOUT))[1:]
    except sp.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    info = [int(x.split()[0]) for i, x in enumerate(memory_info)]
    info = str(info)
    info = info.replace("[","").replace("]","")
    info = float(info)
    return info


def print_gpu_memory_every_5secs():
        #This function calls itself every 5 secs and print the gpu_memory.
    Timer(5.0, print_gpu_memory_every_5secs).start()
    memory_used = get_gpu_memory_used()
    memory_total = get_gpu_memory_total()
    gpu_temperature = get_gpu_temperature()
    utilization_gpu_nvidia = get_utilization_gpu_nvidia()
    utilization_memory_nvidia = get_utilization_memory_nvidia()
    calculated_utilization = (memory_used/memory_total)*100
    
    print(calculated_utilization)

print_gpu_memory_every_5secs()

