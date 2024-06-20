import subprocess, os, sys
from enum import Enum
#from amdsmi import *

DEFAULT_VENDOR = "NVIDIA"
LOAD_FROM_CONFIG = True
DEBUG = True

class Fm(Enum):
    none = 0
    tf = 1
    pytorch = 2
    both = 3

def tRun(command):
    return subprocess.run(command, shell=True, capture_output=True, text=True) #output is strangly formatted, needs fixing

def check_nvidia_gpu():
    try:
        process = tRun(['nvidia-smi'])
        if process.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def get_nvidia_vram():
    try:
        process = tRun(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits'])
        if process.returncode == 0:
            vram = process.stdout.strip()
            return f"{vram/1024} GB"
        else:
            return "Could not retrieve VRAM information."
    except FileNotFoundError:
        return "nvidia-smi command not found."

def check_amd_gpu():
    try:
        process = subprocess.run(['lspci', '-nn'], capture_output=True)
        if process.returncode == 0:
            output = process.stdout.decode()
            for line in output.split('\n'):
                if 'VGA compatible controller: Advanced Micro Devices' in line:
                    return 'Radeon' in line or 'RX' in line or 'HD' in line or 'FirePro' in line
    except FileNotFoundError:
        pass
    return False

def get_amd_vram():
    try:
        lspci_result = tRun(['lspci'])
        if 'VGA compatible controller: Advanced Micro Devices' in lspci_result.stdout:
            lshw_result = tRun(['sudo', 'lshw', '-C', 'display'])
            lines = lshw_result.stdout.split('\n')
            for line in lines:
                if 'size' in line and 'MiB' in line:
                    return line.strip().split(':')[1].strip()
            return "Could not retrieve VRAM information."
        else:
            return "No AMD GPU found."
    except FileNotFoundError:
        return "lshw command not found."

class gpu:

    def __init__(self):
        self.vendor = None
        self.vram = None
        self.platform = None
        self.frameworks = Fm.both

    def get_vendor(self):
        if check_nvidia_gpu():
            self.vendor = "NVIDIA"
        if check_amd_gpu():
            self.vendor = "AMD"
        if check_nvidia_gpu() and check_amd_gpu():
            print("Multiple GPUs detected(unsuported configuration). One card by", DEFAULT_VENDOR, " is going to be used. To change that, edit the DEFAULT_VENDOR variable.")
            self.vendor = DEFAULT_VENDOR 

    def get_vram(self):
        if self.vendor == "NVIDIA":
            self.vram = get_nvidia_vram()
        if self.vendor == "AMD":
            self.vram = get_amd_vram()

    def get_framework(self):
        if self.vendor == "NVIDIA":
            self.frameworks = "cuda"
        if self.vendor == "AMD": 
            self.frameworks = "rocm"

    def get_info(self):
        self.get_vendor()
        self.get_vram()
        self.get_framework()


class SystemInfo:

    def __init__(self):
        self.cpuThreads = None
        self.ram = None
        self.gpu = gpu()
        self.tpu= None

    def get_threads(self):
        try:
            self.cores = os.cpu_count()
            return self.cores
        except Exception as e:
            return f"Error retrieving CPU cores: {str(e)}"

    def get_tpu(self):
        process = tRun(['lspci', '-nn'])
        temp = subprocess.run(['grep', '089a'], input=process.stdout, capture_output=True, text=True)
        if temp.stdout == '':
            self.tpu = 0
        else:
            self.tpu = temp.stdout.count('TPU')

    def get_ram(self):
        try:
            process = tRun(['free', '-h'])
            if process.returncode == 0:
                self.ram = process.stdout.split('\n')[1].split()[3]
                return self.ram
            else:
                return "Could not retrieve RAM information."
        except FileNotFoundError:
            return "free command not found."
       
    def get_system_info(self):
        self.get_threads()
        self.get_ram()
        self.gpu.get_info()
        self.get_tpu()

'''def overwrite():
    LOAD_FROM_CONFIG = False
    print('Enter objects to load (cpu, gpu, tpu):\n')
    for attr in input().split():
        print("Enter features to load:\n")
        features = input().split()
        for feature in features:
            getattr(system, attr).__dict__[feature] = input(f"Enter value for {feature}:\n")


if (len(sys.argv) > 1):

    if DEBUG:
        if sys.argv[1] == '-f' or '--force':
            LOAD_FROM_CONFIG = False
            overwrite()

    if LOAD_FROM_CONFIG and os.path.exists("./config.csv"):
        print('Enter objects to load (cpu, gpu, tpu):\n')
        for attr in input().split():
            print("Enter features to load:\n")
            features = input().split()
            #for feature in features:
                #getattr(system, attr).__dict__[feature] = #load from config.csv

    if LOAD_FROM_CONFIG and os.path.exists("./config.csv") == False:
        file = open("config.csv", "w")
        for val in system.__dict__:
            none_features = {attr: getattr(val, attr) is None for attr in val.__dict__}
            if none_features != {}:
                for feature in none_features:
                    print(f"{feature} missing, needs to be overwritten\n")
                    overwrite()
                    file.write(f"{val.__dict__}\n")

    if (sys.argv[1] == '-l' or '--log'):
        file = open("sys.txt", "w")

        print(tRun(['lscpu']))
        print(tRun(['free', '-h']))
        if system.gpu.vendor == "NVIDIA":
            print(tRun(['nvidia-smi']))
        #if system.gpu.vendor == "AMD":
            #print(tRun(['rocm-smi']))
        print(system.tpu.count)

        file.write(str(tRun(['lscpu'])))
        file.write(str(tRun(['free', '-h'])))
        if system.gpu.vendor == "NVIDIA":
            file.write(str(tRun(['nvidia-smi'])))
        #if system.gpu.vendor == "AMD":
            #file.write(str(tRun(['rocm-smi'])))
        file.write(str(system.tpu.count))
        file.close()

    if (sys.argv[1] == '-q' or '--query'):
        print(f"CPU Cores: {system.cpu.cores}")
        print(f"CPU Threads: {system.cpu.threads}")
        print(f"RAM: {system.ram}")
        print(f"GPU VRAM: {system.gpu.vram}")
        print(f"GPU framework: {system.gpu.frameworks}")
        print(f"TPU: CORAL TPU x{system.tpu.count}")


def GLVAK(self):
#IMPORTANT!!!!!: FOR SOME REASON REPLACING val and key with anything (tested with cVar, val) breaks the function
    val = max(self.__dict__, key=self.__dict__.get) #eg fp16
    key = self.__dict__[val] #eg 35 (@ fp16)
    return val, key
    
Tops = {"cpu": GLVAK(system.cpu.tops)[1],
        "gpu": GLVAK(system.gpu.tops)[1],
        "tpu": system.tpugroup.int8}

Prec = {"cpu": GLVAK(system.cpu.tops)[0],
        "gpu": GLVAK(system.gpu.tops)[0],
        "tpu": "int8"}

isinstances = {"cpu": system.cpu,
               "gpu": system.gpu,
               "tpu": system.tpugroup}

Values = {key : (isinstances[key].frameworks, Tops[key],Prec[key]) for key in Tops.keys()}

Rank = {k: v for k, v in sorted(Values.items(), key=lambda item: item[1][1], reverse=True)}'''




