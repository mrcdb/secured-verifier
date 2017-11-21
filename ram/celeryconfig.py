from datetime import timedelta
import config as cfg

#CELERYBEAT_SCHEDULE = {
#    'add-every-15-seconds': {
#        'task': 'tasks.pollhostsCheckCert',
#        'schedule': timedelta(seconds=15),
#        'args': (cfg.OAT_VERIFIER, cfg.OAT_NODE, cfg.OAT_LEVEL),
#    },
#}

CELERYBEAT_SCHEDULE = {
    'add-every-15-seconds': {
        'task': 'tasks.pollhostsCheckCont',
        'schedule': timedelta(seconds=15),
        'args': (cfg.OAT_VERIFIER, cfg.OAT_NODE, cfg.OAT_LEVEL, cfg.OAT_CONT_LIST),
    },
}
