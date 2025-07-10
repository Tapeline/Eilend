pub enum OpCode {
    Nop,

    // Data loading
    LoadConst(usize),
    PushBool(bool),
    PushNull,

    // Basics
    Echo,

    // Debug
    DebugPrintStack,
}
