import cv2
from PIL import Image
import numpy as np

def convert_video(input_file, output_file, target_resolution, target_frame_rate):
    # Read input video
    cap = cv2.VideoCapture(input_file)
    # Get input video resolution and frame rate
    input_resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    input_frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    # Calculate scaling factor for target resolution
    scale_width = target_resolution[0] / input_resolution[0]
    scale_height = target_resolution[1] / input_resolution[1]
    scale = min(scale_width, scale_height)
    # Calculate new dimensions
    new_width = int(input_resolution[0] * scale)
    new_height = int(input_resolution[1] * scale)
    # Define output codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, target_frame_rate, (new_width, new_height))
    # Process frames and write to output file
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            # Resize frame to target resolution
            resized_frame = cv2.resize(frame, (new_width, new_height), interpolation = cv2.INTER_AREA)
            # Write resized frame to output file
            out.write(resized_frame)
        else:
            break
    # Release VideoCapture and VideoWriter objects
    cap.release()
    out.release()

def generate_hex_file(input_file):
    # Open input file and read all frames as images
    cap = cv2.VideoCapture(input_file)
    frames = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frames.append(frame)
        else:
            break
    # Release VideoCapture object
    cap.release()
    # Scale the resolution of each frame to 80x60
    scaled_frames = []
    for frame in frames:
        scaled_frame = cv2.resize(frame, (80, 60), interpolation = cv2.INTER_AREA)
        scaled_frames.append(scaled_frame)
    # Convert each frame to 12-bit color depth
    converted_frames = []
    for frame in scaled_frames:
        converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        converted_frames.append(converted_frame)
    # Iterate over each frame and convert each pixel to hex
    hex_frames = []
    for frame in converted_frames:
        hex_frame = []
        for row in frame:
            hex_row = []
            for pixel in row:
                # print(pixel)
                # The pixel is a list of 3 values, each between 0 and 255. Convert to a 12-bit value of RRRRGGGGBBBB
                # Scale each value to 4 bits
                r = int(pixel[0] / 16)
                g = int(pixel[1] / 16)
                b = int(pixel[2] / 16)
                # convert r, g, b to binary
                r = bin(r)[2:]
                # pad r, g, b to 4 bits
                r = r.zfill(4)
                g = bin(g)[2:]
                g = g.zfill(4)
                b = bin(b)[2:]
                b = b.zfill(4)
                # append r, g, b to a single string
                rgb = r + g + b
                # convert rgb to hex
                # hex_pixel = hex(int(rgb, 2))[2:]
                # append hex_pixel to hex_row
                hex_row.append(rgb)

            # Add the row to the frame
            hex_frame.append(hex_row)
        # Add the frame to the list of frames
        hex_frames.append(hex_frame)
    # Write the hex frames to a file
    with open('output.bin', 'w') as f:
        for frame in hex_frames:
            for row in frame:
                for pixel in row:
                    f.write(pixel + ' ')
                f.write('\n')
            f.write('\n')

# function to render back a bin file to a image
def degenerate_hex_file(input_file, width, height):
    #Open the file
    with open(input_file, 'r') as f:
        # Read all strings in, separated by whitespace
        strings = f.read().split()
        # Strings are binary values: 0-3 are R, 4-7 are G, 8-11 are B
        # Convert each string to a tuple of 3 values
        pixels = []
        for string in strings:
            # Convert string to integer
            integer = int(string, 2)
            # Convert integer to RGB
            r = integer & 0b111100000000
            r = r >> 8
            g = integer & 0b000011110000
            g = g >> 4
            b = integer & 0b000000001111
            # Convert RGB to 8-bit values
            r = r * 16
            g = g * 16
            b = b * 16
            # Append RGB to pixels
            pixels.append((r, g, b))
        # cut off the extra pixels
        pixels = pixels[:width * height]
        # Convert pixels to image
        image = Image.new('RGB', (width, height))
        image.putdata(pixels)
        # Save image
        image.save('output.png')

    pass
if __name__ == '__main__':
    # Example usage
    input_file = 'maxresdefault.jpg'
    output_file = 'output.mp4'
    target_resolution = (80, 60)
    target_frame_rate = 60

    # Convert video to target resolution
    convert_video(input_file, output_file, target_resolution, target_frame_rate)

    # Generate hex file from output video
    generate_hex_file(output_file)
    # Degenerate hex file to video
    degenerate_hex_file('output.bin', 80,60)
