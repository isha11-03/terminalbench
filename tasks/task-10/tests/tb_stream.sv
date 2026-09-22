module tb_stream;
    localparam integer N = 24;
    logic clk = 0, rst_n = 0, in_valid = 0, out_ready = 0;
    logic in_ready, out_valid;
    logic signed [15:0] in_a, in_b;
    logic signed [31:0] out_data;
    integer a_vec [0:N-1];
    integer b_vec [0:N-1];
    integer expected [0:255];
    integer sent = 0, received = 0, rd = 0, cycle = 0, errors = 0;
    integer i, exp_value;

    stream_accel dut (.clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_ready(in_ready),
                      .in_a(in_a), .in_b(in_b), .out_valid(out_valid), .out_ready(out_ready),
                      .out_data(out_data));
    always #5 clk = ~clk;

    always @(*) begin
        out_ready = rst_n && ((cycle % 7) != 2) && ((cycle % 11) != 5);
    end

    always @(negedge clk) begin
        if (!rst_n) begin
            in_valid <= 1'b0;
            in_a <= 0;
            in_b <= 0;
        end else if (sent < N) begin
            in_valid <= 1'b1;
            in_a <= a_vec[sent];
            in_b <= b_vec[sent];
        end else begin
            in_valid <= 1'b0;
        end
    end

    always @(posedge clk) begin
        if (!rst_n) begin
            // Reset is checked after the reset edge by the latency bench.
        end else begin
            cycle = cycle + 1;
            if (in_valid && in_ready) begin
                exp_value = a_vec[sent] * b_vec[sent] + (a_vec[sent] <<< 3) - (b_vec[sent] <<< 1);
                expected[sent] = exp_value;
                sent = sent + 1;
            end
            if (out_valid && out_ready) begin
                if ($signed(out_data) !== expected[rd]) begin
                    $display("MISMATCH index=%0d got=%0d expected=%0d", rd, $signed(out_data), expected[rd]);
                    errors = errors + 1;
                end
                rd = rd + 1;
                received = received + 1;
            end
            if (cycle > 500) begin
                $display("TIMEOUT sent=%0d received=%0d", sent, received);
                $finish;
            end
        end
    end

    initial begin
        a_vec[0]=16'sh0003; b_vec[0]=16'sh0007;
        a_vec[1]=-16'sd12; b_vec[1]=16'sd9;
        a_vec[2]=16'sh7fff; b_vec[2]=-16'sd2;
        a_vec[3]=-32768; b_vec[3]=1;
        a_vec[4]=-16'sd231; b_vec[4]=-16'sd17;
        a_vec[5]=0; b_vec[5]=-32768;
        a_vec[6]=16'sd32767; b_vec[6]=16'sd32767;
        a_vec[7]=-32768; b_vec[7]=-32768;
        for (i=8; i<N; i=i+1) begin
            a_vec[i] = (i * 7919) % 65536 - 32768;
            b_vec[i] = (i * 3571 + 19) % 65536 - 32768;
        end
        repeat (3) @(posedge clk);
        rst_n = 1'b1;
        wait (received == N);
        repeat (2) @(posedge clk);
        if (sent != N || received != N || errors != 0)
            $display("FAIL sent=%0d received=%0d errors=%0d", sent, received, errors);
        else
            $display("PASS stream sent=%0d received=%0d", sent, received);
        $finish;
    end
endmodule
