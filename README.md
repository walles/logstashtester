# Logstashtester

Tests [logstash](https://www.elastic.co/products/logstash) configurations with example
input.

Prints on stdout what logstash would have sent to Elasticsearch for
the given config file and input.

Syntax: `logstashtester logstash.conf [--type=<type>]`.

Logstash config is read from `logstash.conf`, and log lines from `STDIN`.

If your config file depends on the input type, you can specify the type of your
log lines using the `--type` option.

## Requirements
To run the Logstashtester you first need to have
[Docker](https://store.docker.com/search?type=edition&offering=community)
running on your system.

# TODO
* Hint user if `docker` is not available

## DONE
* Add command line parsing
* Actually use the user specified logstash config file
* Customize user logstash file for testing before executing it
