import logging

log_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

#File to log to
logFile = 'logs/app.log'

#Setup File handler
file_handler = logging.FileHandler(logFile, mode='w', encoding="utf-8")
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

#Setup Stream Handler (i.e. console)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.INFO)

#Get our logger
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

#Add both Handlers
app_log.addHandler(file_handler)
app_log.addHandler(stream_handler)