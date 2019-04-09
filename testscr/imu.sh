#!/bin/bash

minimu9-ahrs --mode raw | awk '{print $1 "\t" $2 "\t" $3}'
