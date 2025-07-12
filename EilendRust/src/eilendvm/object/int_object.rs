use crate::eilendvm::object::base_object::EObjRef;
use std::cell::Ref;
use std::cell::RefCell;
use std::rc::Rc;
use std::any::Any;
use crate::eilendvm::object::base_object::{EObj, EObjTyp};
use crate::eilendvm::object::table::Table;
use crate::{eobj_common_converters, eobj_common_impl};

pub struct EInt {
    table: Table,
    value: i64
}

impl EObj for EInt {
    eobj_common_impl!(EObjTyp::INT);

    fn display_str(&self) -> String {
        self.value.to_string()
    }
    
    fn is_truthy(&self) -> bool { self.value != 0 }
    fn is_falsy(&self) -> bool { self.value == 0 }
}

impl EInt {
    pub fn get_value(&self) -> i64 { self.value }
}

eobj_common_converters!(EInt, int, EObjTyp::INT, i64);
