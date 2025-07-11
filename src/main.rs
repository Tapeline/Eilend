use crate::eilendvm::chunk::{ChunkConstant, CodeChunk};
use crate::eilendvm::opcodes::OpCode;
use crate::eilendvm::devtools;
use crate::eilendvm::devtools::{print_chunk, print_constant};
use crate::eilendvm::io::{StdIO, StrIO};
use crate::eilendvm::vm::VM;

pub mod eilendvm;
mod tests;

fn main() {
    let mut chunk = CodeChunk::new();
    chunk.add_const(ChunkConstant::Str("Test".to_owned()));
    chunk.add_const(ChunkConstant::Float(1.2));
    chunk.add_const(ChunkConstant::Int(3));
    chunk.add_const(ChunkConstant::Str("a".to_owned()));
    chunk.add_const(ChunkConstant::Str("b".to_owned()));
    chunk.add_const(ChunkConstant::Str("c".to_owned()));
    chunk.add_op_no_ln(OpCode::LoadConst(0));
    chunk.add_op_no_ln(OpCode::StoreGlobal(3));
    chunk.add_op_no_ln(OpCode::PushBool(true));
    chunk.add_op_no_ln(OpCode::JumpIfTrue(5));
    chunk.add_op_no_ln(OpCode::LoadConst(1));
    chunk.add_op_no_ln(OpCode::StoreGlobal(4));
    chunk.add_op_no_ln(OpCode::LoadConst(2));
    chunk.add_op_no_ln(OpCode::StoreGlobal(5));
    chunk.add_op_no_ln(OpCode::LoadGlobal(3));
    chunk.add_op_no_ln(OpCode::Echo);
    chunk.add_op_no_ln(OpCode::LoadGlobal(4));
    chunk.add_op_no_ln(OpCode::Echo);
    chunk.add_op_no_ln(OpCode::LoadGlobal(5));
    chunk.add_op_no_ln(OpCode::Echo);
    print_chunk(&chunk);
    let mut vm = VM::new(chunk, Box::new(StdIO{}));
    vm.run_all();
}
