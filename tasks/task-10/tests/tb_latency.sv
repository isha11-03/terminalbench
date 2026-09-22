module tb_latency;
    logic clk = 0, rst_n = 0, in_valid = 0, out_ready = 1;
    logic in_ready, out_valid;
    logic signed [15:0] in_a = -16'sd19, in_b = 16'sd23;
    logic signed [31:0] out_data;
    integer cycle = 0, accepted_cycle = -1, output_cycle = -1, errors = 0;

    stream_accel dut (.clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_ready(in_ready),
                      .in_a(in_a), .in_b(in_b), .out_valid(out_valid), .out_ready(out_ready),
                      .out_data(out_data));
    always #5 clk = ~clk;

    always @(posedge clk) begin
        if (!rst_n) begin
            cycle = 0;
        end else begin
            cycle = cycle + 1;
            if (in_valid && in_ready && accepted_cycle < 0)
                accepted_cycle = cycle;
            if (out_valid && output_cycle < 0)
                output_cycle = cycle;
            if (cycle > 10) begin
                if (accepted_cycle < 0 || output_cycle < 0 || output_cycle - accepted_cycle != 2)
                    errors = errors + 1;
                if ($signed(out_data) != (-19 * 23 + (-19 * 8) - (23 * 2))) errors = errors + 1;
                if (errors == 0) $display("PASS latency accepted=%0d output=%0d", accepted_cycle, output_cycle);
                else $display("FAIL latency accepted=%0d output=%0d errors=%0d", accepted_cycle, output_cycle, errors);
                $finish;
            end
        end
    end

    initial begin
        repeat (2) @(posedge clk);
        rst_n = 1'b1;
        @(negedge clk);
        in_valid = 1'b1;
        @(negedge clk);
        in_valid = 1'b0;
    end
endmodule
