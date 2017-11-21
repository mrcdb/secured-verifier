#!/bin/bash

> container-ids.txt
celery -A tasks worker --beat 
