import psutil
import platform
import functools


@functools.lru_cache(maxsize=1)
def get_system_info():
    """Fetches combined system information (Cached for ultra-fast repeated access)."""
    uname = platform.uname()
    return {
        "System": uname.system,
        "Node Name": uname.node,
        "Release": uname.release,
        "Version": uname.version,
        "Machine": uname.machine,
        "Processor": uname.processor,
    }

def get_cpu_info():
    """Fetches CPU usage percentage quickly without blocking heavily."""
    return psutil.cpu_percent(interval=0.5)

def get_memory_info():
    try:
        svmem = psutil.virtual_memory()
        return {
            "Total": f"{svmem.total / (1024**3):.2f} GB",
            "Available": f"{svmem.available / (1024**3):.2f} GB",
            "Used": f"{svmem.used / (1024**3):.2f} GB",
            "Percentage": svmem.percent
        }
    except Exception:
        return {"Total": "0 GB", "Used": "0 GB", "Percentage": 0}

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = []
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            free_gb = partition_usage.free / (1024**3)
            disk_info.append({
                "Device": partition.device,
                "Total": f"{partition_usage.total / (1024**3):.2f} GB",
                "Used": f"{partition_usage.used / (1024**3):.2f} GB",
                "Free_GB": free_gb,
                "Free_Formatted": f"{free_gb:.2f} GB",
                "Percentage": partition_usage.percent
            })
        except Exception:
            # Ignore drives that aren't ready (like empty CD drives) safely
            continue
    return disk_info
