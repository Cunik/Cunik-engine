# Cunik
***(The project is under development.)***

[![Build Status](https://travis-ci.org/Cunik/Cunik-engine.svg?branch=master)](https://travis-ci.org/Cunik/Cunik-engine)

Cunik is a solution for easily building, packaging, delivering, fetching, deploying and managing unikernel images over different unikernel implementations like Rumprun, OSv, MirageOS and IncludeOS, which enables people launching unikernel applications by several command lines.

## Why does Cunik exist?

Containers are a good isolation mechanism, but not good enough. 

### Safety

As for containers, once a application has any security problem, it will affect all the applications which run on the same operating system. Luckily, unikernel can solve the problem better.

### Efficiency

The success of docker increases the availability of system resources greatly. However, because docker gnerally runs on a streamline Linux kernel system, it's speed is limited by the Linux kernel. Otherwise, unikernel can meet the needs of customized cores and it  can reduce performance overhead.

Unikernel is a good candidate for improving efficiency and safety. However, it is hard to build and manage, since there is so many different implementations and each of them uses different tool chains in building and deploying.

So we present Cunik, which aims at enabling you get Unikernel images and deploy them in several commands, and easy to configure just like writing Dockerfiles.

## What can you do with it?

By using Cunik, you can:

- get better isolation and higher performance than using container techs;
- easily build and manage unikernel applications than directly play with unikernel implementations like Rumprun, ClickOS.

## Getting started

These instructions will get you running Cunik Engine and a Cunik-nginx on your machine.

First of all, let's get the source code:

```shell
git clone https://github.com/Cunik/Cunik-engine.git
```

Then install all the dependencies:

```shell
pip3 install -r requirements.txt
```

A Cunik engine is a deamon that listens on the host and waits for requests from clients. Now, let's launch the Cunik engine.

Copy `config.py.sample` to `config.py`, and make sure it's right.

Run the deamon:

```shell
python3 engine.py runserver
```

Test the API by sending request manually.

## Contributing

(none)

## Links

(none)

## Licensing

The code in this project is licensed under MIT license.