# README

## About `runner`

This program allows you to send commands to a shell process as if they were typed by a human. `runner` takes simple configuration files as an input and uses [Pexpect](https://pexpect.readthedocs.io/en/stable/) to allow for interaction with pretty much every tool that has a command-line interface.

![demo](./img/demo.gif)

## Usage

This program will be installed as an executable called `runner` by default. `runner` takes a `.yaml` file as an input and runs commands according to the instructions in the YAML file. For more information on how to write config files, see [Writing a configuration file](#writing-a-configuration-file) or an [example](https://github.com/TrickyTroll/good-bot-runner/blob/main/tests/examples/test_conf.yaml).

```shell
runner [PATH/TO/CONFIG]
```

To try it out, you can run

```shell
runner tests/examples/test_conf.yaml
```

from the root of this repo.

## Installing

`runner` can be installed using `pip`. This means that you need a working installation of Python and Pip. See: [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).
Since this program is _not_ distributed on [pypi](https://pypi.org), you will need to download a copy of this repo first. This can by downloading the `.zip` archive or by cloning this repo.

### User install

You should download the latest release on the release [page](https://github.com/TrickyTroll/good-bot-runner/releases/tag/v1.0). From the releases page:

1. Click `Source code`.
2. Unzip the downloaded archive.
3. From a terminal, navigate to the unzipped directory.

Once you are at the root of the downloaded folder, run

```shell
pip install -U .
```

This will install a program called `runner` for you (the user running the command).

### Dev install

To get the latest unreleased copy of this program, you should clone the repository instead of downloading a release. The `main` branch is updated less frequently than the `latest` one, but the code on `main` is tested more thoroughly.

> **Note**: There is no guarantee that code outside of the `main` branch is frequently tested.

#### Cloning the repository

From your terminal:

```shell
git clone https://github.com/TrickyTroll/good-bot-runner.git
```

Then, go to the root of the cloned repo and run:

```shell
pip install -U .
```

This will install a program called `runner` for you (the user running the command).

#### Downloading the `zip` archive

On the repos [main page](https://github.com/TrickyTroll/good-bot-runner):

1. Click on `Code`.
2. Then on `Download ZIP`.

Once the archive is extracted, run

```shell
pip install -U .
```

from a terminal at the root of the folder you just downloaded. This will install a program called `runner` for you (the user running the command).

### Installing on Windows

This project is not tested regularly on Windows. For a smoother experience, I recommend using this app in a containerized Linux environment. ~~~~

## How it works

After it is done parsing the configuration, `runner` spawns a shell process and sends the first command. That is, the first element in the list associated with the key `commands`. It then waits until the shell responds to something that matches the first element in the list associated to the `expect` key.

After this first interaction with the shell process, `runner` will keep sending succeeding commands and expect something to be returned by the shell. If the expected value is not showing up, the default `timeout` is set at 30 seconds. After that, the object Python uses to represent the process will raise an error.

Once every command has been sent and the last expectation has been met, the program will close the shell process.

## Writing a configuration file

Python should interpret the YAML file as a dictionary that maps commands and expectations. One configuration file should correspond to one sequence of interactions. This means that the dictionary representation of the setup should only contain two keys.

### commands

One of the two keys is `commands`. In YAML, you should write an unindented `commands:`. Python will interpret this as the key to the following value or values.

Since you could run more than one command and you probably want those commands to be ordered, the value associated with `commands` is a list. In the configuration file, a list is represented by items with a `-` at the beginning of the line. Each item has its own line. Since this list is associated with `commands`, it can be indented to make it easier to understand.

```yaml
commands:
  - echo 'hello world'
  - ls
```

> **Note**: Even if you only want to run one command, you must write it as a list. This is due to the fact that `runner` will iterate over the items associated with `commands`, assuming that it is a list. A string is also iterable, but the result of each iteration won’t be a functional shell command (probably).

#### Using passwords

`runner` also supports the use of secrets and passwords. Passwords are necessary when recording
commands that must be run as root, for example. They can also be used to connect to a remote
machine thanks to `ssh` with a password.

Passwords are sent to the program with the help of environment variables. If you are running `runner`
directly on your machine, you can set those variables using the `export` command. This example
binds a password to the `SOME_PASSWORD` variable. This variable can then be used in
[your script](samples/with_passwords/passwords.yaml) to respond to a password prompt.

```shell
export SOME_PASSWORD=popcorn-TUB-pigskin-randy
```

Please note that this only works on UNIX-like systems. If you are using Windows, you will
get a much smoother experience with the [Docker image](https://hub.docker.com/r/trickytroll/good-bot-runner/tags?page=1&ordering=last_updated).

If you are using the Docker image, you can write a text file that contains all of your
variables on different lines.

```txt
SOME_PASSWORD=popcorn-TUB-pigskin-randy
ANOTHER_PASSWORD=odious-cloy-SQUIRE-register
```

Then, when using the `docker run` command, add the `--env-file` flag to your command with
the path towards your text file as an argument.

When writing the `.yaml` configuration file, you can tell `runner` which environment
variable to look for with the `password` keyword.

```yaml
commands:
  - ssh some-user@dev-machine
  - password: SOME_PASSWORD
expect:
  - assword
  - prompt
```

This last example will use the previously set `SOME_PASSWORD` variable to answer to the
ssh command's password prompt.

You can set as many variables as you want, but your passwords should be replaced after 
being used with this program.

> ⚠️ **Warning:** While version controlling your documentation scrips can be a good idea, always
> be careful **not** to add your `.env` files to your version control history. It is also a
> *strongly* recommended that the passwords used with `runner` are removed from your systems and
> applications afterwards.

### expect

The only other key that you should put in your configuration file is `expect`. As with the `commands` key, expect should not be indented and written like so:

```yaml
expect:
```

This time, the list will contain things to expect before sending the next command to the shell process. Items in this list can be regular expressions.

> **Note**: This is useful if you are recording a demo where you need to login somewhere. You could expect something like `assword:` before sending your credentials.  
> The `prompt` keyword can also be used to expect the next time the prompt will show up. For now, this only matches the `#` character. This is usually the root prompt.

```yaml
expect:
  - prompt
  - prompt
```
