pub enum OpCode {
    Nop,

    // Data construction
    LoadConst(usize),
    PushBool(bool),
    PushNull,

    // Variables
    StoreGlobal(usize),
    LoadGlobal(usize),

    // Control flow
    JumpIfTrue(usize),
    JumpIfFalse(usize),
    Jump(usize),
    Call(usize),

    // Basics
    Echo,

    // Debug
    DebugPrintStack,
}
