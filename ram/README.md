## Description  ###############################################################
The scripts in this directory are used for send periodic attestation requests to the OpenAttestation framework and to host a new web service for users and machines to read the attestation results.

It is recommanded to create a non-priliveged user to execute the scripts, since it is unwise to start a infinite periodic task with the `root` account. In following case, a temperal user `cassandra` is created and used to run the following scripts.

It is also recommanded to copy the `ram` directory into the `HOME` directory of the un-privileged user.

## Dependencies ###############################################################

On Debian based systems

    root@verifier# apt-get install mysql-connector-python rabbitmq-server python-pip
    root@verifier# pip install tornado Celery urllib3 requests

On RedHat based systems

    root@verifier# yum install mysql-connector-python rabbitmq-server python-pip
    root@verifier# pip install tornado Celery urllib3 requests

## Configure web server #######################################################
The web server is hosted using [Tornado](http://www.tornadoweb.org/en/stable/), a Python web framework. It will access to the database used by the OpenAttestation framework, and read the last attestation results when user asks about it using a browser or a POST request.

Configuration file for the web server is config.py, need to change `BASE_DIR` to the location of `ram` directory.

If the database used by OpenAttestation does not have user `verifier` with password `secured`, need to create the user in the database and allow him to access the `oat_db` database.

Then to start the web server with following command in the `ram` directory:
```bash
cassandra@verifier:$ python webapp.py --run-webapp &
```

## Configure periodic attestation task ########################################
Periodic attestation task is sent using [Celery](http://www.celeryproject.org/), an asynchronous task queue/job queue based on distributed message passing, which also support scheduling.

In this setting, [rabbitmq](http://www.rabbitmq.com/) is used as it is the default broker used by Celery.

Once `rabbitmq-server` is installed, configure it as following:

```bash
root@verifier:# rabbitmqctl add_user cassandra secured
root@verifier:# rabbitmqctl add_vhost cassandravhost
root@verifier:# rabbitmqctl set_permissions -p cassandravhost cassandra ".*" ".*" ".*"
root@verifier:# rabbitmq-server -detached
```

If you start the `rabbitmq-server`, your rabbit node should now be rabbit@myhost, as verified by _rabbitmqctl_:

```bash
root@verifier:# rabbitmqctl status
```
If you need to stop the rabbitmq server, just run:
```bash
root@verifier:# rabbitmqctl stop
```

After rabbitmq server is running, you can configure Celery in `config.py`, and `celeryconfig.py`.

In `celeryconfig.py`, you can change the periodic attestation frequency. In `config.py`, you can change the OpenAttestation related parameters, especially `OAT_NODE`, `OAT_VERIFIER` and `OAT_LEVEL`. Also, the new certificate generated by OpenAttestation (i.e. certfile.cer) needs to be copied from the `OpenAttestation/CommandTool` into `data` directory to replace the old one.

Then run the following command in the `ram` directory to start the periodic attestation process.
```bash
cassandra@verifier$ celery -A tasks worker --loglevel=info --beat &
```
In order for OpenAttestation to know the certificate used by strongswan in the NED to authenticate itself, when the NED is registering to the verifier, it also needs to input the digest of the file containing his certificate (i.e. [`peerCert.der`](https://gitlab.secured-fp7.eu/secured/ned/tree/strongswan/strongswan) step 6 in NED repository) along with it, see [step 7](https://gitlab.secured-fp7.eu/secured/verifier/blob/devel/README.md) in verifier repository.

When NED revokes its certificate, it needs to be re-registered again, with the digest of the certificate, with the _update_cert.sh_ script in `OpenAttestation/CommandTool` directory.


## Example ####################################################################
Open  `http://verifier:8899/user/status?CN=ned2&LEVEL=4&DGST=8b71648e9c52a24cfe259305c611483ea56ca4dc` with a browser to see the attestation result.

* CN is the common name of the NED
* LEVEL is the trust level of the requirement
* DGST is the digest of the strongSwan certificate used by the NED

Or send POST requests to `http://verifier:8899/mach/status`
```bash
$ PDATA='{"hosts":["ned"],"analysisType":"load-time+check-cert,l_req=l4_ima_all_ok|>=,cert_digest=efae492da504edea2c2358dea1fb1e6770780b6e"}'
$ curl -XPOST -H "Content-Type:application/json" -d "$PDATA" http://verifier:8899/mach/status

```

Responses will be a JSON message structured as follow

    {
        "status": "success",
        "n_results": 1,
        "results":[
            {
                "trust_lvl": "trusted",
                "host_name": "ned"
            },
        ]
    }

## License ####################################################################

    The MIT License (MIT)

    Copyright (c) 2015 Paolo Smiraglia <paolo.smiraglia@polito.it>
                       Tao Su <tao.su@polito.it>
                       TORSEC Group (http://security.polito.it)
                       Politecnico di Torino

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.