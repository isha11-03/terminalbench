module stream_accel #(
    parameter integer WIDTH = 16
) (
    input  logic clk,
    input  logic rst_n,
    input  logic in_valid,
    output logic in_ready,
    input  logic signed [WIDTH-1:0] in_a,
    input  logic signed [WIDTH-1:0] in_b,
    output logic out_valid,
    input  logic out_ready,
    output logic signed [(2*WIDTH)-1:0] out_data
);
    localparam integer OUT_WIDTH = 2 * WIDTH;
    logic stage1_valid, stage2_valid;
    logic signed [OUT_WIDTH-1:0] stage1_data, stage2_data;

    assign in_ready = !stage1_valid;
    assign out_valid = stage2_valid;
    assign out_data = stage2_data;

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            stage1_valid <= 1'b0;
            stage2_valid <= 1'b0;
            stage1_data <= '0;
            stage2_data <= '0;
        end else begin
            // Baseline defects: this is not an elastic transfer and stalls overwrite output.
            if (stage2_valid || out_ready) begin
                stage2_valid <= stage1_valid;
                stage2_data <= stage1_data;
            end
            if (in_ready) begin
                stage1_valid <= in_valid;
                stage1_data <= in_a * in_b + (in_a <<< 3) - (in_b <<< 1);
            end
        end
    end
endmodule
