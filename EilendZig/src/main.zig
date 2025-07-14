const std = @import("std");
const opcodes = @import("opcodes.zig");
const devtools = @import("devtools.zig");

pub fn main() !void {
    var op = opcodes.OpCode{ .LOAD_CONST = 42 };
    devtools.print_instruction(&op);
}

test "simple test" {
    var list = std.ArrayList(i32).init(std.testing.allocator);
    defer list.deinit(); // try commenting this out and see if zig detects the memory leak!
    try list.append(42);
    try std.testing.expectEqual(@as(i32, 42), list.pop());
}
