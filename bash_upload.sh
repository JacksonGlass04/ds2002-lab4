#!/bin/bash

aws s3 cp $1 s3://$2/

aws s3 presign --expires-in $3 s3://$2/$1
