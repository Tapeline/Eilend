pub const OpCodeTag = enum {
    NOP,
    LOAD_CONST
};

pub const OpCode = union(OpCodeTag) {
    NOP: void,
    LOAD_CONST: (usize),
};
