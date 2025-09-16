hershey
=======

![Hershey Font to DXF](/images/hershey.png)

This short program is a story in two parts:

Back in the mid 1980s when I first entered college, I got a job at the University of Oregon
programming a Masscomp computer.  What was a Masscomp you say?  It was a 
[Motorola 68K based computer that ran their own version of Unix that emphasized high performance
and real time scheduling.](https://en.wikipedia.org/wiki/MASSCOMP)  For a while it was probably
the fastest computer on the University of Oregon campus, and unlike the Vax 11/750s that 
were in use in the CIS department, I mostly had it to myself.   One of the early projects I 
remember doing is writing code to [parse the Hershey Font data](https://en.wikipedia.org/wiki/Hershey_fonts)
and use them to draw vector graphics on the Wyse 35 terminals in Tek 4014 mode.  I believe I also
ran the first incarnations of my MTV raytracer on this machine.

Fastforwarding 40 years, I just got the basics of my own CNC machine up and running, a 
[Lowrider CNC V3](https://docs.v1e.com/lowrider/lowrider3/), and was trying to get some rudimentary 
software up and running.  Rather than torture myself with learning Fusion 360, and/or paying large sums
of money to generate some simple signs, I decided that for these early tests, all I needed was something
that would accept a text string and generate DXF paths.  Using [ESTLcam](https://www.estlcam.de/) which 
is a very basic but credible CAM and CNC controller that I've been using, I can convert this into gcode
which can then do simple CNC operations.

I remembered the Hershey fonts, and thought they might be useful.

So, I wrote a simple Python script that allows you to pick a particular font mapping, and then would
generate a simple DXF file for the text in the specified font. 

They aren't amazing in terms of quality, but they are free and legible.  

This was really just an hour or so of work so far, I'll probably add some more functionality soon.

It uses the ezdxf library to write DXF files.  Writing other formats would probably be pretty 
straightforward.



## Usage

```
usage: hershey.py [-h] [-f FONT] [-o OUTPUT] [-d DATA] [-v] text

Convert text to DXF using Hershey fonts.

positional arguments:
  text                  The text to convert to DXF.

options:
  -h, --help            show this help message and exit
  -f FONT, --font FONT  The Hershey font mapping file to use. (default:
                        mappings/romant.hmp)
  -o OUTPUT, --output OUTPUT
                        The name of the output DXF file. (default: sign.dxf)
  -d DATA, --data DATA  The path to the Hershey font data file. (default:
                        data/hershey_font.dat)
  -v, --verbose         Print verbose output. (default: False)
```



