# good-bot

Automating the recording of documentation videos using Video Puppet and Python!

This cool application allows you to create terminal recordings using only a markdown file and 
a simple syntax.

## Usage

1. Clone this repository.

2. Write a markdown file that uses the syntax described below. You can see an example under 
the example folder.

3. Change your current working directory to this repo.

4. Build your container using ```docker build [--tag something you want] .```.

5. Change your current working directory to the one that contains your instruction file.

6. Run your container using ```docker run -it [--name something you want] -v $(PWD):/toto [the tag you chose] your_script.md ```.

**The ```-it``` is important, since you will need a TTY to run the commands!!!**

```your_script.md``` is the name of the instructions file you want to use.

7. Let the container do his thing. When it's done, a new folder called ```your_video``` should have been created
inside of your current working directory.

8. Send the content of the your_video folder to Video Puppet!

## How it works

To explain how good-bot works, let's first examine what it does.

![Where is x function running](https://docs.google.com/drawings/d/e/2PACX-1vSP3jd_BWWXzxL_WmsfMpxDAS5xrd2vLejp3PUAgnjejE_O5PDRzVk0lH8OzlZXcUZ6qVl_cfTcjxso/pub?w=960&h=720)

### The build

When the user builds a container using the Dockerfile, a container image is created. This 
image is based on Ubuntu and contains the directory in which the ```docker build``` command 
was executed. This is why you must build your container inside the main repository of this 
app.

The good-bot directory will be copied inside the container under the folder ```/home/all/```

The build will also create two other directories:

* ```/tutorial```: This is just a clean directory. It is where the commands specified in the 
instruction file are going to be executed.

* ```/usr/local/go/bin```: This is where ```ttyrec2gif``` can be called from.

### Running the container

####  Analyzing the docker run command


#### What happends after you press enter

Every time the container is run, it also uses python to run the script called 
```so_it_begins.py```. ```so_it_begins.py``` only takes one argument: the path towards the 
instructions file you wrote.

This script also imports functions from ```app/functions.py``` that do a 
few things:

1. ```instruction_finder```: This function reads the file called ```your_script.md``` under 
The ```script``` directory. It looks under each ```hr``` if there is the string 
```(instructions:```. If the string is not present, it reads the next line, assuming that it 
is the file's header. In the case that the string  is there, instruction_finder creates 
a dictionary using the next 3 lines. The dictionary's format is 
```{"command": , "media_format": , "file_name"}```. The next 3 lines shoud then contain 
The command to run, the media format (only gifs are supported for now), and the file name, 
respectively. Further details on the syntax can be found below. The dictionary is 
appended to a list, which is returned when the function has read the whole file.

2. ```script_maker```: This function creates a bash script for each instruction made by 
```instruction_finder```. The bash script imports ```demo-magic.sh``` and is made to follow 
[Demo-Magic's](https://github.com/paxtonhare/demo-magic) syntax. Demo-Magic is a bash script 
that automates typing of functions. This is useful because the commands will be typed 
and recorded inside the container without needing any input other that the initial 
markdown file from the user. The shell scripts are saved in a new folder called ```shell_scripts```.

3. ```instruction_executer```: Iters over every file inside of ```shell_scripts``` and 
runs the scripts while recoding using [Asciinema](https://asciinema.org/). Asciinema 
creates json files that will allow you to replay what happened on your terminal while Asciinema 
was recoding. These files can later be converted into gifs.

4. ```new_script```: Finally, a new video script is created. This video plan respects 
[Video Puppet's](https://www.videopuppet.com/docs/format/) Markdown format. 
Whenever ```new_script``` is called, a new markdown file
is created by reading through the old one and removing the ```instructions``` mentions, 
replacing them with a line similar to: ```![freeze](somefile.gif)```.

The previous 4 steps ran inside the Ubuntu docker container. This allows you to run 
commands that install stuff that you already have locally an still go through the 
installation steps. It also allows you install whatever you want without having to remove it 
from your computer afterwards!

The only problem is that the new script and all the recordings are still inside the 
container!!! Luckily, the python script ```is_this_how_it_ends.py``` is made to fetch them 
for you. Here is what it does:

1. It asks the user for the container's name (or id if you're that kind of person).

2. ```is_this_how_it_ends.py``` then pulls [Asciicast2gif's](https://github.com/asciinema/asciicast2gif)
Docker image. Asciicast2gif is the tool used to convert your recordings.

3. Using ```docker cp```, the script copies the folder that contains the recordings and the 
new video script. It also converts the asciicasts into gifs and bundles everything in a cool 
directory called ```your_video```. This folder is what you can send to Video Puppet to 
create a video!


## Syntax

Here is an example of the very pointillous syntax that you ~~sould~~ must use:

```
---
size: 1080p
---
(instructions:
	[command]
	[media_format]
	[file_name]
)

```



## What could be improved?

* The pathing is pretty bad. Should be done using pathlib instead of os.

* Giving users more options, like the colours of their terminal and the speed at which the 
typing is done.

* Making the value associated with "command" a list, allowing for multiple commands to be
recorded at the same time.

* A main script that builds the container, runs it, and transfers the data.

* Allowing more than just the gif format (stills and code formatted text cells could be 
useful.

* It's overall very syntax dependent, which is annoying.
