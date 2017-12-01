#!/usr/bin/env python

# echo line | logstashtester logstash.conf --type=apache

import os
import subprocess


def customize_config(config, input_type):
    # type: (str, str) -> str
    """
    This function:
    * Strips the input and output sections from a logstash config file
    * Adds a "type" statement if input_type is non-empty
    * Configures input from stdin
    * Sets output to JSON format
    """
    # FIXME: Actually customize the config
    return config


def run_logstash(config, input_type=None):
    # type: (str, str) -> None
    logstash_cmd = [
        "logstash",
        "-e", customize_config(config, input_type),
    ]

    docker_cmd = ['docker', 'run']
    if os.isatty(0):
        print("Reading logs from stdin, press CTRL-D to finish")
        print("")
        print("Logstash starting...")
        docker_cmd.append('-it')
    docker_cmd.append('logstash:2.4.1-alpine')

    env = os.environ.copy()
    # From: http://stackoverflow.com/a/2325109/473672
    env['LS_JAVA_OPTS'] = "-Djava.security.egd=file:/dev/./urandom"

    subprocess.call(
        docker_cmd + logstash_cmd,
        env=env,

        # Just pass our stdin to Logstash's stdin
        stdin=None
    )


if __name__ == "__main__":
    run_logstash("")
