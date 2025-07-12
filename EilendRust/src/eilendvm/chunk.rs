use std::collections::HashMap;
use crate::eilendvm::opcodes::OpCode;

pub enum ChunkConstant {
    Int(i64),
    Float(f64),
    Str(String),
}

pub struct CodeChunk {
    code: Vec<OpCode>,
    constants: Vec<ChunkConstant>,
    lineno: HashMap<usize, usize>,
}

impl CodeChunk {
    pub fn new() -> CodeChunk {
        CodeChunk {
            code: Vec::new(),
            constants: Vec::new(),
            lineno: HashMap::new(),
        }
    }

    pub fn add_op(&mut self, opcode: OpCode, lineno: usize) -> usize {
        self.code.push(opcode);
        self.lineno.insert(self.code.len() as usize - 1, lineno);
        self.code.len() - 1
    }

    pub fn add_op_no_ln(&mut self, opcode: OpCode) {
        self.code.push(opcode);
    }

    pub fn get_ops(&self) -> &Vec<OpCode> {
        &self.code
    }

    pub fn get_lineno(&self, pos: usize) -> Option<&usize> {
        self.lineno.get(&pos)
    }

    pub fn get_const(&self, index: usize) -> &ChunkConstant {
        &self.constants[index]
    }

    pub fn get_constants(&self) -> &Vec<ChunkConstant> {
        &self.constants
    }

    pub fn add_const(&mut self, constant: ChunkConstant) {
        self.constants.push(constant);
    }
}
