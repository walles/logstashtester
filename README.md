# Logstashtester

Tests [logstash](www.elastic.co/products/logstash) configurations with example
input.

Syntax: `logstashtester logstash.conf [--type=<type>]`.

Logstash config is read from `logstash.conf`, and log lines from `STDIN`.

If your config file depends on the input type, you can specify the type of your
log lines using the `--type` option.

## Requirements
To run the Logstashtester you first need to have
[Docker](https://store.docker.com/search?type=edition&offering=community)
running on your system.

# TODO
* Add command line parsing
* Actually use the user specified logstash config file
* Hint user if `docker` is not available
