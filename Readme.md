# CPE 133 Final Project: Shit Video Player

This project is a composition of a Video Processor, written in a high-level language, and a Verilog module that renders the generated data on the VGA port. 

## Video Processor:

This part, written in Python, takes an MP4 and creates a HEX data table at the appropriate resolution and framerate, with the appropriate data for color in the specification according to the provided VGA driver. 

## Memory file: 

The output memory file must be interacted with by the Basys 3 board in Verilog somehow

## Video Player:

The easy part: Read cells from the Memory File and pass them into the VGA driver

## VGA driver:

Provided by the professor, allows us to use the BASYS 3 VGA connector without ripping our heads out.
