# `runner` samples

This directory contains configuration samples. These samples can be
used to lean possible ways `runner` can be used.

## Test configuration

[This](./basic/test_conf.yaml) sample show how to tell the program to type basic
shell commands and expect the prompt.

![A small example of what runner can do](./img/basic_demo.gif)

## With passwords

[With passwords](with_passwords/passwords.yaml) shows how to configure
`runner` to use passwords. `runner` uses the password to connect to a
remote container.

This example also provides an [example](with_passwords/.env) of an
environment file.

![The program answers to password prompts](img/with-password.gif)

## Typos example

The [typos example](./typos/typos.yaml) just makes the program type a lot
of characters to increase the chances of making a typo.

![The program can make typos just like a real person](img/typos_demo.gif)
