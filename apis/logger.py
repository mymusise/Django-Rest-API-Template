LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(request_id)s] [%(filename)s:%(lineno)d] %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
        },
        'apis_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
            'filename': 'logs/knowledge.log',
        },
        'exception_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
            'filename': 'logs/exception.log',
        },
        'aliyun_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
            'filename': 'logs/aliyun.log',
        }
    },
    'loggers': {
        '': {
            'handlers': ['apis_handler'],
            'level': 'INFO',
            'propagate': False,
        },
        'apis': {
            'handlers': ['apis_handler', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'aliyun': {
            'handlers': ['aliyun_handler', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'exception': {
            'handlers': ['exception_handler', 'console'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}
