from celery import Celery
import oat

app = Celery('tasks', broker='amqp://guest@localhost//')
app.config_from_object('celeryconfig')

@app.task
def pollhostsCheckCert(verifier, node, level):
    return oat.issuePollAttestationCheckCert(verifier, node, level)

@app.task
def pollhostsCheckCont(verifier, node, level, cont_list):
    return oat.issuePollAttestationContCheck(verifier, node, level, cont_list)
