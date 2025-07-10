use std::any::Any;
use crate::eilendvm::object::base_object::{EObj, EObjDyn, EObjTyp};
use crate::eilendvm::object::str_object::EStr;
use crate::eilendvm::object::table::Table;
use crate::{eobj_common_converters, eobj_common_impl};
use crate::eilendvm::object::float_object::EFloat;

pub struct EInt {
    table: Table,
    value: i64
}

impl EObj for EInt {
    eobj_common_impl!(EObjTyp::INT);

    fn display_str(&self) -> String {
        self.value.to_string()
    }
}

impl EInt {
    pub fn get_value(&self) -> i64 { self.value }
}

eobj_common_converters!(EInt, int, EObjTyp::INT, i64);
