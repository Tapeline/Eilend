use crate::eilendvm::object::base_object::EObjRef;
use std::cell::Ref;
use std::cell::RefCell;
use std::rc::Rc;
use std::any::Any;
use crate::eilendvm::object::base_object::{EObj, EObjTyp};
use crate::eilendvm::object::table::Table;
use crate::{eobj_common_converters, eobj_common_impl};

pub struct EStr {
    table: Table,
    value: String
}

impl EObj for EStr {
    eobj_common_impl!(EObjTyp::STR);

    fn display_str(&self) -> String {
        self.value.clone()
    }
}

impl EStr {
    pub fn get_value(&self) -> &String { &self.value }
}


eobj_common_converters!(EStr, str, EObjTyp::STR, String);
