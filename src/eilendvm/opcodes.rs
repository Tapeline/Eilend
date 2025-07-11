pub enum OpCode {
    Nop,

    // Data construction
    LoadConst(usize),
    PushBool(bool),
    PushNull,

    // Variables
    StoreGlobal(usize),
    LoadGlobal(usize),

    // Basics
    Echo,

    // Debug
    DebugPrintStack,
}
