use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;
use crate::eilendvm::chunk::CodeChunk;
use crate::eilendvm::object::func_object::{EFunc, FuncData};
use crate::eilendvm::object::table::Table;
use crate::eilendvm::opcodes::OpCode::Call;

pub struct CallFrame {
    pub function: Rc<RefCell<EFunc>>,
    pub ip: usize,
    pub locals: Table
}

impl CallFrame {
    pub fn get_current_line(&self) -> usize {
        let func = self.function.borrow();
        if let Some(lineno) = func.get_value().code.get_lineno(self.ip - 1) {
            *lineno
        } else {
            0
        }
    }

    pub fn get_name(&self) -> String {
        let func = self.function.borrow();
        func.get_value().name.clone()
    }
}

pub struct CallStack {
    pub frames: VecDeque<CallFrame>,
}

impl CallStack {
    pub fn new() -> CallStack {
        CallStack {
            frames: VecDeque::new(),
        }
    }

    pub fn push(&mut self, frame: CallFrame) {
        self.frames.push_back(frame);
    }

    pub fn frame(&mut self) -> &mut CallFrame {
        self.frames.front_mut().unwrap()
    }

    pub fn new_frame(&mut self, function: Rc<RefCell<EFunc>>) -> &mut CallFrame {
        self.push(CallFrame{
            function: function,
            ip: 0,
            locals: Table::new()
        });
        self.frame()
    }
}


