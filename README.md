# Cunik
***(The project is under development.)***

[![Build Status](https://travis-ci.org/Cunik/Cunik-engine.svg?branch=master)](https://travis-ci.org/Cunik/Cunik-engine)

Cunik is a solution for easily building, packaging, delivering, fetching, deploying and managing unikernel images over different unikernel implementations like Rumprun, OSv, MirageOS and IncludeOS, which enables people launching unikernel applications by several command lines.

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

### Get Source Code

```shell
git clone https://github.com/Cunik/Cunik-engine.git
```

### Install System Package Dependencies

On Debian, install the following using apt:

* libvirt-daemon-system
* libvirt-dev

### Install Python Package Dependencies

```shell
pip3 install -r requirements.txt
```

### Create Cunik-Root Manually

Cunik intends to load its images and other information from a single folder(`/var/cunik`). For now, you need to create it manually. Get [this](https://www.dropbox.com/s/fgrs238vfp111pn/Cunik-root.tar.gz?dl=0), decompress it, and copy or link to `/var/cunik`.

### Start Cunik-engine

A Cunik Engine is a daemon that listens on the host and waits for requests from clients. Now, let's launch the Cunik Engine.

Run the daemon:

```shell
python3 engine.py runserver
```

Actually, we need to be `root` to configure network and manage vm. So run the command line above as `root` or use `sudo`, and use what ever techniques to prevent unexpected damage.

### Start a Cunik and Test It

Use [Cunik-cli](https://github.com/Cunik/Cunik-cli) to start a Cunik. Example:

```
cunik-cli create nginx 10.0.125.3
```

**Don't** change **`10.0.125`** since it is hard-coded for now.

Then `curl 10.0.125.3` to see if it works.

Following are the images that you can give it a try:

* nginx

  Runmrun implementation of nginx.

* redis-server

  Rumprun implementation of redis. Test it with `redis-cli -h <address>`.

* redis-server-osv

  OSv implementation of reids. Unable to access for now(we are sure it's online(`nmap`-ed it)). We'd be glad if you can help us fix it.

## Contributing

(none)

## Links

(none)

## Licensing

The code in this project is licensed under MIT license.
