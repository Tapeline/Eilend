pub enum OpCode {
    Nop,
    LoadConst(usize),
    DebugPrintStack,
    Echo
}