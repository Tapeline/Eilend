use crate::eilendvm::chunk::{ChunkConstant, CodeChunk};
use crate::eilendvm::opcodes::OpCode;
use crate::eilendvm::devtools;
use crate::eilendvm::vm::VM;

mod eilendvm;

fn main() {
    let mut chunk = CodeChunk::new();
    chunk.add_const(ChunkConstant::Str("Test".to_owned()));
    chunk.add_const(ChunkConstant::Float(1.2));
    chunk.add_const(ChunkConstant::Int(3));
    chunk.add_op(OpCode::LoadConst(0), 1);
    chunk.add_op_no_ln(OpCode::LoadConst(1));
    chunk.add_op_no_ln(OpCode::LoadConst(2));
    chunk.add_op_no_ln(OpCode::DebugPrintStack);
    devtools::print_chunk(&chunk);
    let mut vm = VM::new(chunk);
    vm.run_all();
}
