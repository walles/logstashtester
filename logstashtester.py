#!/usr/bin/env python

"""
EXAMPLE: logstashtester logstash.conf --type=apache

--type is optional

Log lines will be read from stdin.
"""

import os
import sys
import subprocess


def braces_delta(line):
    # type: (str) -> int
    line = line.strip()
    if line.startswith('#'):
        # Comment line, never mind
        return 0

    delta = 0
    for char in line:
        if char == '{':
            delta += 1
        if char == '}':
            delta -= 1

    return delta


def strip_config(config):
    # type: (str) -> str
    """
    Removes any input or output sections from a logstash config file.
    """
    braces_opened = 0
    is_stripping = False
    stripped = ""
    for line in config.splitlines(True):
        if line.strip().startswith("input"):
            # Strip out the input section
            assert not is_stripping
            assert braces_opened == 0
            is_stripping = True

        if line.strip().startswith("output"):
            # Strip out the output section
            assert not is_stripping
            assert braces_opened == 0
            is_stripping = True

        braces_opened += braces_delta(line)
        if is_stripping and braces_opened == 0:
            # Got to the end of the section we're stripping out
            is_stripping = False

            # Skip closing brace of the section we're stripping
            continue

        if is_stripping:
            # Skip this line since we're stripping
            continue

        stripped += line

    return stripped


def customize_config(config, input_type):
    # type: (str, str) -> str
    """
    This function:
    * Strips the input and output sections from a logstash config file
    * Adds a "type" statement if input_type is non-empty
    * Configures input from stdin
    * Sets output to JSON format
    """
    customized_config = strip_config(config)

    type_line = ""
    if input_type:
        type_line = 'type => "{}"'.format(input_type)
    customized_config += """

    input {
      stdin {
        codec => line
        %s
      }
    }

    output {
      stdout {
        codec => rubydebug
      }
    }
    """ % (type_line,)

    return customized_config


def run_logstash(config, input_type=None):
    # type: (str, str) -> None
    logstash_cmd = [
        "logstash",
        "-e", customize_config(config, input_type),
    ]

    docker_cmd = ['docker', 'run', '--rm']
    if os.isatty(0):
        print("Reading logs from stdin, press CTRL-D to finish")
        print("")
        print("Logstash starting...")
        docker_cmd.append('-t')
    else:
        docker_cmd.append('--sig-proxy=true')
    docker_cmd.append('-i')
    docker_cmd.append('logstash:5-alpine')

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
    args = sys.argv[:]
    args.pop(0)  # Remove script name from args
    if not 1 <= len(args) <= 2:
        sys.stderr.write(__doc__)
        exit(1)

    if args[0] in ['-h', '--help']:
        print(__doc__)
        exit(0)

    logstash_conf_name = args.pop(0)
    input_type = None
    if args:
        type_arg = args.pop(0)
        if not type_arg.startswith('--type='):
            sys.stderr.write("ERROR: Unknown argument <" + type_arg + ">\n")
            sys.stderr.write(__doc__)
            sys.stderr.write("\n")
            exit(1)
        input_type = type_arg[len('--type='):]

    with open(logstash_conf_name, 'r') as logstash_conf:
        run_logstash(logstash_conf.read(), input_type)
