use crate::{pop_stack, vm_panic};
use std::cell::RefCell;
use std::rc::Rc;
use crate::{assert_that, rc_cell};
use crate::eilendvm::call_stack::{CallFrame, CallStack};
use crate::eilendvm::chunk::{ChunkConstant, CodeChunk};
use crate::eilendvm::devtools::print_stack;
use crate::eilendvm::io::IO;
use crate::eilendvm::object::base_object::{EObj, EObjRef};
use crate::eilendvm::object::bool_object::{v_bool};
use crate::eilendvm::object::float_object::{v_float};
use crate::eilendvm::object::func_object::{as_efunc, is_efunc, EFunc};
use crate::eilendvm::object::int_object::{v_int};
use crate::eilendvm::object::null_object::{v_null};
use crate::eilendvm::object::str_object::{v_str};
use crate::eilendvm::object::table::Table;
use crate::eilendvm::opcodes::OpCode;
use crate::eilendvm::value_stack::ValueStack;

pub struct VM {
    code: CodeChunk,
    ip: usize,
    value_stack: ValueStack,
    io: Box<dyn IO>,
    globals: Table,
    call_stack: CallStack
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
            globals: Table::new(),
            call_stack: CallStack::new()
        }
    }
    
    pub fn get_io(&self) -> &dyn IO {
        self.io.as_ref()
    }



    pub fn run_one_instruction(&mut self) {
        let mut frame = self.call_stack.frame();
        let mut frame_func = frame.function.borrow_mut();
        let frame_data = frame_func.get_value_mut();
        let code = &frame_data.code;
        let instr = &code.get_ops()[frame.ip];
        frame.ip += 1;
        match instr {
            OpCode::Nop => {},

            OpCode::LoadConst(const_i) => {
                assert_that!(frame, const_i < &code.get_constants().len());
                match code.get_const(*const_i) {
                    ChunkConstant::Int(value) =>
                        self.value_stack.push(rc_cell!(v_int(*value))),
                    ChunkConstant::Float(value) =>
                        self.value_stack.push(rc_cell!(v_float(*value))),
                    ChunkConstant::Str(value) =>
                        self.value_stack.push(rc_cell!(v_str(value.clone()))),
                }
            },

            OpCode::DebugPrintStack => {
                print_stack(&self.value_stack);
            },

            OpCode::Echo => {
                let value = pop_stack!(self, frame);
                self.io.print(&*value.borrow().display_str());
                self.io.print("\n");
            },

            OpCode::PushBool(value) => {
                self.value_stack.push(rc_cell!(v_bool(*value)));
            },

            OpCode::PushNull => {
                self.value_stack.push(rc_cell!(v_null()));
            },

            OpCode::StoreGlobal(index) => {
                let value = pop_stack!(self, frame);
                assert_that!(frame, index < &code.get_constants().len());
                if let ChunkConstant::Str(name) = code.get_const(*index) {
                     self.globals.put(name.to_string(), value);
                } else {
                    vm_panic!(frame, "Global name is not a string");
                }
            },

            OpCode::LoadGlobal(index) => {
                assert_that!(frame, index < &code.get_constants().len());
                if let ChunkConstant::Str(name) = code.get_const(*index) {
                    if let Some(value) = self.globals.get(name) {
                        self.value_stack.push(value.clone());
                    } else {
                        // TODO make it return an error instead
                        vm_panic!(frame, "Global not found");
                    }
                } else {
                    vm_panic!(frame, "Global name is not a string");
                }
            },

            OpCode::Jump(amount) => {
                if frame.ip + amount >= code.get_ops().len() {
                    vm_panic!(frame, "Jump out of bounds");
                }
                frame.ip += amount - 1;
            },

            OpCode::JumpIfFalse(amount) => {
                let value = &pop_stack!(self, frame);
                if frame.ip + amount >= code.get_ops().len() {
                    vm_panic!(frame, "Jump out of bounds");
                }
                if value.borrow().is_falsy() {
                    frame.ip += amount - 1;
                }
            },

            OpCode::JumpIfTrue(amount) => {
                let value = &pop_stack!(self, frame);
                if frame.ip + amount >= code.get_ops().len() {
                    vm_panic!(frame, "Jump out of bounds");
                }
                if value.borrow().is_truthy() {
                    frame.ip += amount - 1;
                }
            }

            OpCode::Call(arg_count) => {
                if (frame.ip + arg_count) >= code.get_ops().len() {
                    vm_panic!(frame, "Call out of bounds");
                }
                let func = pop_stack!(self, frame);
                if !is_efunc(&func) {
                    // TODO
                    vm_panic!(frame, "Can call only functions");
                }
                let func = as_efunc(&func).as_any().downcast_ref::<EFunc>().unwrap();
                let new_frame = self.call_stack.new_frame(
                    Rc::new(RefCell::new(func))
                );
            }
        }
    }

    pub fn run_all(&mut self) -> InstructionResult {
        loop {
            if self.ip >= self.code.get_ops().len() {
                return InstructionResult::Ok;
            }
            let result = self.run_one_instruction();
            //if let InstructionResult::Err(value) = result {
            //    return InstructionResult::Err(value);
            //}
        }
    }

}
