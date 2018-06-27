# Cunik
***(The project is under development.)***

[![Build Status](https://travis-ci.org/Cunik/Cunik-engine.svg?branch=master)](https://travis-ci.org/Cunik/Cunik-engine)

Cunik is a solution for easily building, packaging, delivering, fetching, deploying and managing unikernel images over different unikernel implementations like Rumprun, OSv, MirageOS, and IncludeOS, which enables people launching unikernel applications by several command lines.

## Why does Cunik exist?

Containers are a good isolation mechanism, but not good enough. 

### Safety

As for containers, once an application has any security problems, it will affect all the applications which are running on the same operating system. Luckily, unikernel can solve the problem better.

### Efficiency

The success of Docker increases the availability of system resources greatly. However, since Docker generally runs on a streamlined Linux kernel system, its speed is limited by the Linux kernel. Otherwise, unikernel can meet the needs of customized cores and it can reduce performance overhead.

Unikernel is a good candidate for improving efficiency and safety. However, it is hard to build and manage, since there are so many different implementations and each of them uses different toolchains when building and deploying.

So we present Cunik, which aims at enabling you to get Unikernel images and deploy them in several commands, and it is easy to configure just like writing Dockerfiles.

## What can you do with it?

By using Cunik, you can:

- get better isolation and higher performance than using container techs;
- easily build and manage unikernel applications than directly playing with unikernel implementations like Rumprun and ClickOS.

## Getting started

These instructions will get you running Cunik Engine and a Cunik-nginx on your machine.

First, let's get the source code:

```shell
git clone https://github.com/Cunik/Cunik-engine.git
```

Then install all the dependencies:

```shell
pip3 install -r requirements.txt
```

A Cunik Engine is a daemon that listens on the host and waits for requests from clients. Now, let's launch the Cunik Engine.

Copy `config.py.sample` to `config.py`, and make sure it's correct.

Run the deamon:

```shell
python3 engine.py runserver
```

Test the API by sending requests manually.

## Contributing

(none)

## Links

(none)

## Licensing

The code in this project is licensed under MIT license.
