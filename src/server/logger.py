import logging.config


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
        'xigua': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s %(message)s'
        }
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
            'filename': '../logs/running.log',
        },
        'django_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['request_id'],
            'filename': '../logs/django.log',
        },
        'request_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
            'filename': '../logs/request.log',
        },
        'xigua_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'xigua',
            'filename': '../logs/xigua.log',
        },
        'pay_cb_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': '../logs/pay_cb.log',
        },
        'exception_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
            'filename': '../logs/exception.log',
        }
    },
    'loggers': {
        '': {
            'handlers': ['apis_handler', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['django_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apis': {
            'handlers': ['apis_handler', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'request': {
            'handlers': ['request_handler', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'xigua': {
            'handlers': ['xigua_handler', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'pay_cb': {
            'handlers': ['apis_handler', 'pay_cb_handler', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'exception': {
            'handlers': ['exception_handler', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('apis')
request_logger = logging.getLogger('request')
exception_logger = logging.getLogger('exception')
