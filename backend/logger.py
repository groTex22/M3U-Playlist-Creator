from queue import Queue

log_queue = Queue()

def log(message):
    """Отправка сообщения в очередь логов"""
    log_queue.put(message)