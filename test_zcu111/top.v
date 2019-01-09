/* Machine-generated using Migen */
module top(
	output user_led,
	input clk125_p,
	input clk125_n
);

reg [25:0] counter = 26'd0;
wire sys_clk;
wire sys_rst;
wire por_clk;
wire clk_se;
reg int_rst = 1'd1;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign user_led = counter[25];
assign sys_clk = clk_se;
assign por_clk = clk_se;
assign sys_rst = int_rst;

always @(posedge por_clk) begin
	int_rst <= 1'd0;
end

always @(posedge sys_clk) begin
	counter <= (counter + 1'd1);
	if (sys_rst) begin
		counter <= 26'd0;
	end
end

IBUFDS IBUFDS(
	.I(clk125_p),
	.IB(clk125_n),
	.O(clk_se)
);

endmodule
