use crate::eilendvm::object::base_object::{EObj, EObjRef};
use std::any::Any;
use std::cell::RefCell;
use std::rc::Rc;
use crate::eilendvm::object::base_object::EObjTyp;
use crate::eilendvm::object::table::Table;
use crate::eobj_common_impl;

pub struct ENull {
    table: Table,
}

impl EObj for ENull {
    eobj_common_impl!(EObjTyp::NULL);
}

pub fn v_null() -> ENull {
    ENull { table: Table::new() }
}

pub fn v_null_ref() -> EObjRef {
    Rc::new(RefCell::new(v_null()))
}
