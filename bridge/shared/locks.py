import threading

lcd_lock = threading.Lock()
dht_lock = threading.Lock()
matrix_lock = threading.Lock()
