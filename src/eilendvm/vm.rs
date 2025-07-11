use std::cell::RefCell;
use std::rc::Rc;
use crate::{assert_that, rc_cell};
use crate::eilendvm::chunk::{ChunkConstant, CodeChunk};
use crate::eilendvm::devtools::print_stack;
use crate::eilendvm::io::IO;
use crate::eilendvm::object::base_object::{EObj};
use crate::eilendvm::object::bool_object::{v_bool};
use crate::eilendvm::object::float_object::{v_float};
use crate::eilendvm::object::int_object::{v_int};
use crate::eilendvm::object::null_object::{v_null};
use crate::eilendvm::object::str_object::{v_str};
use crate::eilendvm::opcodes::OpCode;
use crate::eilendvm::value_stack::ValueStack;

pub struct VM {
    code: CodeChunk,
    ip: usize,
    value_stack: ValueStack,
    io: Box<dyn IO>
}

pub enum InstructionResult {
    Ok,
    Err(String),
}

impl VM {
    pub fn new(code: CodeChunk, io: Box<dyn IO>) -> VM {
        VM {
            code,
            ip: 0,
            value_stack: ValueStack::new(),
            io,
        }
    }
    
    pub fn get_io(&self) -> &dyn IO {
        self.io.as_ref()
    }

    pub fn run_one_instruction(&mut self) -> InstructionResult {
        let instr = &self.code.get_ops()[self.ip];
        self.ip += 1;
        //#[cfg(feature = "debug")]
        match instr {
            OpCode::Nop => InstructionResult::Ok,
            OpCode::LoadConst(const_i) => {
                assert_that!(const_i < &self.code.get_constants().len());
                match self.code.get_const(*const_i) {
                    ChunkConstant::Int(value) =>
                        self.value_stack.push(rc_cell!(v_int(*value))),
                    ChunkConstant::Float(value) =>
                        self.value_stack.push(rc_cell!(v_float(*value))),
                    ChunkConstant::Str(value) =>
                        self.value_stack.push(rc_cell!(v_str(value.clone()))),
                }
                InstructionResult::Ok
            },
            OpCode::DebugPrintStack => {
                print_stack(&self.value_stack);
                InstructionResult::Ok
            },
            OpCode::Echo => {
                let value = &self.value_stack.pop();
                self.io.print(&*value.borrow().display_str());
                self.io.print("\n");
                InstructionResult::Ok
            },
            OpCode::PushBool(value) => {
                self.value_stack.push(rc_cell!(v_bool(*value)));
                InstructionResult::Ok
            },
            OpCode::PushNull => {
                self.value_stack.push(rc_cell!(v_null()));
                InstructionResult::Ok
            }
        }
    }

    pub fn run_all(&mut self) -> InstructionResult {
        loop {
            if self.ip >= self.code.get_ops().len() {
                return InstructionResult::Ok;
            }
            let result = self.run_one_instruction();
            if let InstructionResult::Err(value) = result {
                return InstructionResult::Err(value);
            }
        }
    }

}
