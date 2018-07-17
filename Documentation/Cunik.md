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

