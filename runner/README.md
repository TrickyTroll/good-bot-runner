# Developer `README`

This `README` contains useful information if you want to work
on `runner`. For more general documentation, see the project's
[main](../README.md) `README`.

## Dependencies

To develop `runner` the [Poetry](https://python-poetry.org) dependency
manager was used. To install Poetry, see their
[installation](https://python-poetry.org/docs/#installation) instructions.

When running `pip install .` in this project's root
directory, every dependency mentioned in the `pyproject.toml` file
will be installed. **This does not include development dependencies.**

To install the latter, you will need to run the following command:

```shell
poetry install .
```

## Testing

[Some tests](./tests) are written under the `/tests` directory.
Once you have installed every required [dependency](#dependencies),
you can simply run the following command from this project's root
directory.

```shell
pytest .
```

Testing is also done automatically in the project's `main` branch
using Github actions.

### Writing tests

`runner` is tested using the `unittest` Python module. If you
are not familiar with `unittest`, please refer to the
[documentation](https://docs.python.org/3/library/unittest.html).

Feel free to use `pytest` if you prefer. Future tests will probably
be written using `pytest`.

`pytest` will run every function with a name that starts with
`test_`. It is important to name your tests properly or else
they won’t be executed.

## Typing

Most of `runner`'s code is typed. Type checking is done automatically
on every merge with the `main` branch. This also works with pull
requests.

The type checking is done using `mypy`. If you have installed every
dev dependencies, you should be able to test the program by running:

```shell
mypy runner
```

from the programs root directory.

## Modules

### `classmodule.py`

[`classmodule.py`](classmodule.py) contains the main `Commands`
class. This class is used to create `Commands` object that can
run commands on a `bash` prompt.

While the humanlike typing is done in the
[`human_typing`](#human_typingpy) module, process spawning and
interaction are done in this module.

**This is where to start if you want to change the way `runner`**
**spawns processes and interacts with them.**

`runner` uses the Pexpect Python module to spawn processes and
interact with them. The child object that is used in many functions
is an object of type `pty_spawn.spawn` that has many methods to
allow for interaction with a process. For more information in Pexpect,
please refer to their [documentation](https://pexpect.readthedocs.io/en/stable/).

The `classmodule` also takes care of the **password handling**.
Functions that retrieve passwords from environment variables are
defined in the `Commands` object.

#### `Commands` object methods

* `fake_typing()`: Uses the `type_sentence` method from `human_typing` to
  "type" a string of text to a child process.
* `fake_typing_secret()`: Similar to `fake_typing` but turns of echoing
  and stops printing the results to `stdout`. This makes sure that passwords
  are not recorded.
* `is_password()`: Checks if the next thing to send to the process is a
  password.
* `get_secret()`: Gets a password from an environment variable mentioned
  in the user's configuration file.
* `run()`: Uses every other methods to start the `bash` process and
  interact with it until every command defined by the used has been
  sent.

### `funcmodule.py`

The [funcmodule](funcmodule.py) contains every function used by
the command line interface to parse instruction files.

It is the file to modify if you want to improve the parser or
interact with the user before anything else runs.

### `human_typing.py`

The [human_typing](human_typing.py) module contains every function
that affects how the program types. If you want to make `runner`'s
typing even more human-like, this is where you should get started.

To try to make the used believe that someone is actually typing
on the command line, `runner` randomly introduces typos and delays.
The chances of making typos and the time between keystrokes is
based on different [papers](#references) on the subject.

The `type_sentence()` uses `type_letters()` to type a sentence in 
the most natural way possible. It splits the sentence and sends 
each keypress to the `type_letters()` function.

`type_letters()` takes care of introducing the required typos and
delays. It uses every other functions in the module.

![Functions sequence diagram](../samples/img/sequence-diagram.png)

#### Typos

Functions used to generate typos are

* `is_typo()`: Determine whether or not there will be a typo based
  on percentage chances.
* `pick_typo()`: Picks a plausible typo (keys near the next one to
  press).
* `type_typo()`: Sends the typo to the child process and corrects it
  by sending a `\b` character and typing the correct character.

Chances of generating typos are defined in the `is_typo()` function,
while the plausible typos are defined with the `PLAUSIBLE_TYPO`
variable.

#### Delays

`runner` uses two different types of delays. There are delays
between *each* characters and delays between *some* words.

Functions used to compute delays are the following:

* `is_pause()`: To determine if there should be a pause between
  two words.
* `pause_time()`: Returns how long the pause between two words
  shoud be.
* `get_delay()`: Returns the delay between two keypresses.

##### Delays between characters

Typing speed is determined by how much time is spent between
each character typed. The delay is longer when we have to press
two consecutive keys using the same finger [1]. Studies have also
found which key combination is most likely to be typed by one or
two hands [3].

Using this information, a delay is computed before each keypress
by the `get_delay()` function.

##### Delays between words

People sometimes take pauses while typing. To mimic this behaviour,
`runner` has a 20 to 30% chances of taking a .5 to 1 second pauses
between words.

> **Note:** These numbers are not based on any research. They were
> just picked based on what felt more natural during trials.

Pauses are introduced in the `type_letters()` function by checking
if the next character is a space.

```python
if next == " ":
    # If the next char to type is a space, compute chances of taking
    # a pause.
    if is_pause():
        time.sleep(pause_time())
```

## References

[1] A. M. Feit, D. Weir, and A. Oulasvirta, “How We Type: Movement Strategies and Performance in Everyday Typing,” in Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems, San Jose California USA, May 2016, pp. 4262–4273. doi: 10.1145/2858036.2858233.

[2] R. Banerjee, S. Feng, J. S. Kang, and Y. Choi, “Keystroke Patterns as Prosody in Digital Writings: A Case Study with Deceptive Reviews and Essays,” in Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP), Doha, Qatar, 2014, pp. 1469–1473. doi: 10.3115/v1/D14-1155.

[3] V. Dhakal, A. M. Feit, P. O. Kristensson, and A. Oulasvirta, “Observations on Typing from 136 Million Keystrokes,” in Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems, Montreal QC Canada, Apr. 2018, pp. 1–12. doi: 10.1145/3173574.3174220.
