use crate::eilendvm::object::base_object::EObjRef;
use std::cell::Ref;
use std::cell::RefCell;
use std::rc::Rc;
use std::any::Any;
use crate::eilendvm::object::base_object::{EObj, EObjTyp};
use crate::eilendvm::object::table::Table;
use crate::{eobj_common_converters, eobj_common_impl};

pub struct EBool {
    table: Table,
    value: bool
}

impl EObj for EBool {
    eobj_common_impl!(EObjTyp::BOOL);

    fn display_str(&self) -> String {
        self.value.to_string()
    }

    fn is_truthy(&self) -> bool { self.value }
    fn is_falsy(&self) -> bool { !self.value }
}

impl EBool {
    pub fn get_value(&self) -> bool { self.value }
}

eobj_common_converters!(EBool, bool, EObjTyp::BOOL, bool);
