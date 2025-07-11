use std::collections::vec_deque::Iter;
use std::collections::VecDeque;
use crate::eilendvm::object::base_object::EObjRef;

pub struct ValueStack {
    stack: VecDeque<EObjRef>,
}

impl ValueStack {
    pub fn new() -> ValueStack {
        ValueStack { stack: VecDeque::new() }
    }

    pub fn push(&mut self, value: EObjRef) {
        self.stack.push_back(value);
    }

    pub fn pop(&mut self) -> EObjRef {
        self.stack.pop_back().unwrap()
    }

    pub fn len(&self) -> usize {
        self.stack.len()
    }
    
    pub fn iter(&self) -> Iter<'_, EObjRef> {
        self.stack.iter()
    }
}
