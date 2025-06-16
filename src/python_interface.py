import ctypes
import numpy as np
import os

class TsotchkeInterface:
    def __init__(self):
        self.lib = None
        self.system_ptr = None
        self.is_native = False
        self.frame_count = 0
        
        # Try to load native library
        if os.path.exists('./libtsotchke_native.so'):
            try:
                self.lib = ctypes.CDLL('./libtsotchke_native.so')
                self.lib.tsotchke_create.argtypes = [ctypes.c_int, ctypes.c_float]
                self.lib.tsotchke_create.restype = ctypes.c_void_p
                self.lib.tsotchke_destroy.argtypes = [ctypes.c_void_p]
                self.lib.tsotchke_get_collision_risk.argtypes = [ctypes.c_void_p]
                self.lib.tsotchke_get_collision_risk.restype = ctypes.c_float
                self.is_native = True
                print("🚀 Native C library loaded!")
            except:
                print("📊 Using Python fallback")
        else:
            print("📊 Native library not found, using Python mode")
    
    def initialize(self, grid_size=128, coupling=0.15):
        if self.lib:
            self.system_ptr = self.lib.tsotchke_create(grid_size, coupling)
            return self.system_ptr is not None
        else:
            self.grid_size = grid_size
            self.coupling = coupling
            self.frame_count = 0
            print(f"✅ Python mode: {grid_size}x{grid_size}")
            return True
    
    def get_collision_risk(self):
        if self.lib and self.system_ptr:
            return self.lib.tsotchke_get_collision_risk(self.system_ptr)
        else:
            self.frame_count += 1
            risk = 0.3 + 0.4 * np.sin(self.frame_count * 0.1)
            return abs(risk)
    
    def cleanup(self):
        if self.lib and self.system_ptr:
            self.lib.tsotchke_destroy(self.system_ptr)
        else:
            print(f"💾 Python cleanup after {self.frame_count} frames")
