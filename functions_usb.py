# main.py
import psutil
import os
import time

def get_usb_drives():
    """Retourne une liste des chemins des clés USB détectées."""
    usb_drives = []
    partitions = psutil.disk_partitions()
    for p in partitions:

        if os.name == 'nt' and len(p.mountpoint) == 3 and p.mountpoint[1:] == ':\\' and p.mountpoint[0].isalpha() and p.fstype not in ('CDFS', 'UDF'):

            if p.mountpoint.upper() != 'C:\\':
                try:
                    _ = os.listdir(p.mountpoint)
                    usb_drives.append(p.mountpoint)
                except OSError:
                    pass
        elif os.name != 'nt':
            if 'removable' in p.opts or 'usb' in p.device.lower():
                 try:
                    _ = os.listdir(p.mountpoint)
                    usb_drives.append(p.mountpoint)
                 except OSError:
                    pass
    return usb_drives

def wait_for_usb_drive(timeout):
    """Attend la détection d'une clé USB pendant un certain temps."""
    print(f"Attente d'une clé USB pendant {timeout} secondes...")
    start_time = time.time()
    initial_drives = set(get_usb_drives())
    
    while (time.time() - start_time) < timeout:
        current_drives = set(get_usb_drives())
        new_drives = list(current_drives - initial_drives)
        
        if new_drives:
            return new_drives[0] 
        time.sleep(1)
    return None

def wait_for_usb_disconnection(usb_path: str, timeout=60):
    """
    Attend que la clé USB spécifiée soit déconnectée.
    """
    print(f"En attente de la déconnexion de '{usb_path}'...")
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        current_drives = get_usb_drives()
        if usb_path not in current_drives:
            return True
        time.sleep(1)
    print(f"La clé USB '{usb_path}' n'a pas été déconnectée après {timeout} secondes.")
    return False