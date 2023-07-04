`timescale 1ns / 1ps

module image_renderer(
    input CLK,
    output [2:0] vgaRed,
    output [2:0] vgaGreen,
    output [1:0] vgaBlue,
    output HS,
    output VS);

    localparam WIDTH = 640;
    localparam HEIGHT = 480;
    localparam DATA_WIDTH = 24;
    localparam MEM_DEPTH = WIDTH * HEIGHT;
    localparam MEM_ADDR_WIDTH = $clog2(MEM_DEPTH);
    
    logic [DATA_WIDTH-1:0] framebuffer [0:MEM_DEPTH-1];
    logic [MEM_ADDR_WIDTH-1:0] address = 0;
    logic [DATA_WIDTH-1:0] pixel_data;
    integer hex_file;
    
    // Open and read the hex file
    initial begin
        hex_file = $fopen("image.hex", "r");
        if (hex_file == 0) begin
            $display("Error: could not open hex file");
            $finish;
        end
        
        for (int i = 0; i < MEM_DEPTH; i++) begin
            if ($feof(hex_file)) begin
                $display("Error: hex file is too short");
                $finish;
            end
            $fscanf(hex_file, "%h", pixel_data);
            framebuffer[i] = pixel_data;
        end
        
        $fclose(hex_file);
    end
    
    // VGA output
    vga_driver vga_out(
        .CLK(CLK),
        .RED(framebuffer[address][23:16]),
        .GREEN(framebuffer[address][15:8]),
        .BLUE(framebuffer[address][7:0]),
        .ROW(address / WIDTH),
        .COLUMN(address % WIDTH),
        .ROUT(vgaRed),
        .GOUT(vgaGreen),
        .BOUT(vgaBlue),
        .HSYNC(HS),
        .VSYNC(VS)
    );
    
    // Advance to the next pixel on the rising edge of CLK
    always_ff @(posedge CLK) begin
        if (address == MEM_DEPTH-1) begin
            address <= 0;
        end else begin
            address <= address + 1;
        end
    end
    
endmodule
