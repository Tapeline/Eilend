const opcodes = @import("opcodes.zig");
const std = @import("std");

pub fn print_instruction(op: *opcodes.OpCode) void {
    switch (op.*) {
        opcodes.OpCodeTag.NOP =>
            std.debug.print("NOP", .{}),
        opcodes.OpCodeTag.LOAD_CONST => |index| {
            std.debug.print("LOAD_CONST\t{}", .{index});
        },
    }
}
